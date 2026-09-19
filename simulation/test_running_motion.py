"""Physical requests must move the installed parts by their measured travel.

These checks use a retained run, not the old calculator's pose inputs. They
prove displacement, not clearance or mechanical interlock acceptance.
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
