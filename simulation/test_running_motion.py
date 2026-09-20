"""Physical requests must move the installed parts by their measured travel.

These checks use a retained run, not the old calculator's pose inputs. They
prove displacement and the specifically named carriage/frame stop contacts,
not whole-machine clearance or complete mechanical interlock acceptance.
"""

import numpy as np
from math import cos, sin, radians
from machinome.simulation import Sim
from machinome.test import TestCase
from simulation.running_motion import RunningMotionBench


def rotation(degrees):
    angle = radians(degrees)
    return np.array(((cos(angle), -sin(angle), 0),
                     (sin(angle), cos(angle), 0), (0, 0, 1)))


class RunningMotionTest(TestCase):
    node = RunningMotionBench

    def test_admitted_carriage_and_clearing_stops_match_installed_world_contacts(self):
        sim = Sim(self.node, dt=.1, meshes=True)
        carrier = self.node.carriage.registers.carrier.upper_carriage_body_1
        body, pin = carrier.counter_body, carrier.clearing_pin
        frame = self.node.frame.upper_frame.main_body
        try:
            command = sim.move('carriage_rotation', to=10)
            self.assertEqual(command.status, 'blocked')
            self.assertAlmostEqual(sim.state['carriage.registers.turn'], .18)
            self.assertNotIntersecting(body, frame)
            self.assertBlockedBeyond(body, .02, against=frame,
                                     axis=(0, 0, -1), directions='forward')
            sim.move('carriage_elevation', to=6)
            sim.move('carriage_rotation', to=10)
            command = sim.move('carriage_elevation', to=0)
            self.assertEqual(command.status, 'blocked')
            self.assertAlmostEqual(sim.state['carriage.registers.lift'], 6)
            self.assertFreeWithin(body, .01, against=frame, along=(0, 0, 1))
            self.assertBlockedBeyond(body, .1, against=frame,
                                     along=(0, 0, 1), directions='forward')
            sim.move('carriage_rotation', to=20)
            sim.move('clearing_rotation', to=90)
            command = sim.move('carriage_elevation', to=0)
            self.assertEqual(command.status, 'blocked')
            self.assertAlmostEqual(sim.state['carriage.registers.lift'], 4.810085)
            self.assertFreeWithin(pin, .01, against=frame, along=(0, 0, 1))
            self.assertBlockedBeyond(pin, .1, against=frame,
                                     along=(0, 0, -1), directions='forward')
        finally:
            sim.reset()

    def test_all_markers_move_independently_and_upper_bank_follows_its_track(self):
        from simulation.running import register_reading

        sim = Sim(self.node, dt=.1, meshes=True)
        markers = [getattr(self.node.enclosure.decimal_markers if index < 6 else
                           self.node.carriage.registers.clearing_ring.decimal_markers,
                           f'decimal_marker_{index}') for index in range(1, 11)]
        pieces = [(marker.position_marker, marker.p_3mm_ball,
                   marker.decimal_marker_spring) for marker in markers]
        before = [[piece.mesh.vertices.copy() for piece in group] for group in pieces]
        try:
            # Move in physical order so each preceding marker opens space.
            # Every request is to a distinct public input, never a bank setter.
            for selected in range(1, 11):
                sim.move(f'marker_{selected}_rotation', by=20)
                for index, (marker, group, original) in enumerate(
                        zip(markers, pieces, before), 1):
                    angle = 20 if index <= selected else 0
                    bank = ('enclosure.decimal_markers' if index < 6 else
                            'carriage.registers.clearing_ring.decimal_markers')
                    self.assertAlmostEqual(sim.state[f'{bank}.decimal_marker_{index}.turn'], angle)
                    self.assertAlmostEqual(marker.turn.value, angle)
                    # Both installed tracks now share the native main-shaft axis;
                    # the lower marker joints keep their source-local datum.
                    center = np.asarray((0, 0, 0))
                    for piece, points in zip(group, original):
                        expected = (points - center) @ rotation(angle).T + center
                        np.testing.assert_allclose(piece.mesh.vertices, expected,
                                                   rtol=0, atol=.00001)
            moved = [[piece.mesh.vertices.copy() for piece in group] for group in pieces]
            sim.move('carriage_elevation', to=6)
            sim.move('carriage_rotation', to=20)
            sim.move('clearing_rotation', to=90)
            for index, (group, original) in enumerate(zip(pieces, moved), 1):
                for piece, points in zip(group, original):
                    expected = points if index < 6 else points @ rotation(-70).T + (0, 0, 6)
                    np.testing.assert_allclose(piece.mesh.vertices, expected,
                                               rtol=0, atol=.00001)
            self.assertEqual(register_reading(sim), 0)
            self.assertEqual(register_reading(sim, True), 0)
            self.assertTrue(all(sim.state[f'digit_{i}'] == 0 for i in range(1, 9)))
        finally:
            sim.reset()

    def test_carriage_spring_endpoints_follow_seats_during_lift_and_shift(self):
        sim = Sim(self.node, dt=.1, meshes=True)
        positioning = self.node.carriage.positioning
        lower = positioning.thrust_ring
        upper = positioning.carriage_spring_sleeve
        spring = positioning.carriage_spring.wire
        caps = spring.mesh.vertices[-2:].copy()
        lower_before = lower.mesh.vertices.copy()
        upper_before = upper.mesh.vertices.copy()
        try:
            for lift in (1.5, 3, 4.5, 6):
                sim.move('carriage_elevation', to=lift)
                np.testing.assert_allclose(lower.mesh.vertices, lower_before + (0, 0, lift),
                                           rtol=0, atol=.00001)
                np.testing.assert_allclose(spring.mesh.vertices[-2], caps[0] + (0, 0, lift),
                                           rtol=0, atol=.00001)
                np.testing.assert_allclose(spring.mesh.vertices[-1], caps[1],
                                           rtol=0, atol=.00001)
                np.testing.assert_array_equal(upper.mesh.vertices, upper_before)
            lifted = spring.mesh.vertices.copy()
            sim.move('carriage_rotation', to=20)
            np.testing.assert_array_equal(spring.mesh.vertices, lifted)
        finally:
            sim.reset()

    def test_clearing_follower_and_spring_follow_retained_ring_motion(self):
        sim = Sim(self.node, dt=.1, meshes=True)
        carriage = self.node.carriage.registers
        carrier = carriage.carrier.upper_carriage_body_1
        pin, sleeve = carrier.clearing_pin, carrier.clearing_stop_pin_sleeve
        spring = carrier.clearing_pin_spring.wire
        cover = carriage.clearing_ring.clearing_cover
        try:
            sim.move('carriage_elevation', to=6)
            caps = spring.mesh.vertices[-2:].copy()
            pin_before = pin.mesh.centroid.copy()
            sleeve_before = sleeve.mesh.vertices.copy()
            heights = []
            for angle in (0, 5, 90, 230, 240, 360, 0):
                sim.move('clearing_rotation', to=angle)
                travel = pin.mesh.centroid - pin_before
                heights.append(float(travel[2]))
                np.testing.assert_allclose(spring.mesh.vertices[-2], caps[0] + travel,
                                           rtol=0, atol=.00001)
                np.testing.assert_allclose(spring.mesh.vertices[-1], caps[1],
                                           rtol=0, atol=.00001)
                np.testing.assert_array_equal(sleeve.mesh.vertices, sleeve_before)
                self.assertNotIntersecting(pin, cover)
                self.assertNotIntersecting(spring, pin)
                self.assertNotIntersecting(spring, sleeve)
            self.assertGreater(max(heights) - min(heights), 4)
        finally:
            sim.reset()

    def test_subtraction_lifts_the_crank_and_drum_nine_mm(self):
        sim = Sim(self.node, dt=.1, meshes=True)
        crank = self.node.main_drive.crank.crank_handle_1.main_crank
        drum = self.node.main_drive.stepped_drum.main_axle_step_drum_1.main_axle_step_drum_top_1
        bell = self.node.carry_mechanism.tens_bell.tens_bell_1
        before = [part.mesh.vertices.copy() for part in (crank, drum, bell)]
        try:
            sim.move('crank_elevation', to=9)
            for part, points in zip((crank, drum), before):
                np.testing.assert_allclose(part.mesh.vertices, points + (0, 0, 9),
                                           rtol=0, atol=.00001)
            np.testing.assert_array_equal(bell.mesh.vertices, before[2])
        finally:
            sim.reset()

    def test_lift_and_shift_move_the_carriage_but_not_the_transmission(self):
        sim = Sim(self.node, dt=.1, meshes=True)
        dial = self.node.carriage.registers.result_register.p_10203_1.results_dial_type_1
        shaft = self.node.transmission.result.ones.p_10208_1.transmission_gear_tip
        before, fixed = dial.mesh.vertices.copy(), shaft.mesh.vertices.copy()
        dial_key = 'carriage.registers.result_register.p_10203_1.turn'
        initial_dial = sim.state[dial_key]
        try:
            sim.move('carriage_elevation', to=6)
            np.testing.assert_allclose(dial.mesh.vertices, before + (0, 0, 6),
                                       rtol=0, atol=.00001)
            sim.move('carriage_rotation', to=20)
            self.assertAlmostEqual(sim.state['carriage.registers.turn'], 20)
            self.assertAlmostEqual(sim.state[dial_key], initial_dial)
            self.assertAlmostEqual(self.node.carriage.registers.result_register.p_10203_1.turn.value,
                                   initial_dial)
            expected = before @ rotation(20).T + (0, 0, 6)
            np.testing.assert_allclose(dial.mesh.vertices, expected, rtol=0, atol=.00001)
            np.testing.assert_array_equal(shaft.mesh.vertices, fixed)
        finally:
            sim.reset()

    def test_clearing_plate_follows_the_ring_clockwise(self):
        sim = Sim(self.node, dt=.1, meshes=True)
        plate = self.node.carriage.registers.clearing_ring.clearing_cover
        before = plate.mesh.vertices.copy()
        try:
            sim.move('carriage_elevation', to=6)
            command = sim.move('clearing_rotation', by=90)
            self.assertEqual(command.status, 'completed')
            self.assertAlmostEqual(sim.state['carriage.registers.clearing_ring.turn'], -90)
            self.assertAlmostEqual(self.node.carriage.registers.clearing_ring.turn.value, -90)
            expected = before @ rotation(-90).T + (0, 0, 6)
            np.testing.assert_allclose(plate.mesh.vertices, expected, rtol=0, atol=.00001)
        finally:
            sim.reset()
