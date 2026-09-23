"""Requests meet physical stops without preparing another control's position."""

import unittest
from machinome.simulation import Sim
from simulation.running import OperatingCurta, register_reading

LIFT = 'carriage.registers.lift'
RING = 'carriage.registers.clearing_ring.turn'
PIN = 'carriage.registers.carrier.upper_carriage_body_1.clearing_pin.slide'
SHIFT = 'carriage.registers.turn'


class RunningCarriageIndexTest(unittest.TestCase):
    model = OperatingCurta

    def test_every_working_slot_stops_in_both_directions_and_retains_the_stop(self):
        sim = Sim(self.model(), dt=.1)
        for slot in range(0, 101, 20):
            for direction in (-1, 1):
                if not 0 <= slot + direction * 10 <= 100:
                    continue
                sim.move('carriage_elevation', to=6)
                sim.move('carriage_rotation', to=slot)
                sim.move('carriage_elevation', to=0)
                command = sim.move('carriage_rotation', to=slot + direction * 10, duration=.1)
                sim.run(.1)
                self.assertEqual(command.status, 'blocked')
                self.assertAlmostEqual(sim.state[SHIFT], slot + direction * .18, places=6)
                self.assertEqual(sim.state[LIFT], 0)
                stopped = sim.state[SHIFT]
                sim.move('carriage_rotation', to=slot + direction * 10, duration=.1)
                sim.run(.1)
                self.assertEqual(sim.state[SHIFT], stopped)

    def test_clearing_and_indexing_stops_both_need_their_own_release(self):
        sim = Sim(self.model(), dt=.1)
        sim.move('carriage_elevation', to=6)
        sim.move('carriage_rotation', to=.5)
        sim.move('clearing_rotation', to=90)
        sim.move('carriage_elevation', to=0)
        self.assertAlmostEqual(sim.state[LIFT], 5.5385, places=5)
        sim.move('carriage_rotation', to=0)
        self.assertAlmostEqual(sim.state[LIFT], 5.5385, places=5)
        sim.move('carriage_elevation', to=0)
        self.assertAlmostEqual(sim.state[LIFT], 4.810085, places=5)
        sim.move('clearing_rotation', to=0)
        self.assertAlmostEqual(sim.state[LIFT], 4.810085, places=5)
        sim.move('carriage_elevation', to=0)
        self.assertEqual(sim.state[LIFT], 0)

    def test_seated_shift_stops_at_the_indexing_key_without_lifting(self):
        sim = Sim(self.model(), dt=.1)
        command = sim.move('carriage_rotation', to=10, duration=.2)
        sim.run(.2)
        self.assertEqual(command.status, 'blocked')
        self.assertGreater(sim.state[SHIFT], 0)
        self.assertLess(sim.state[SHIFT], 1)
        self.assertEqual(sim.state[LIFT], 0)
        stopped = sim.state[SHIFT]
        for _ in range(3):
            sim.move('carriage_rotation', to=10, duration=.2)
            sim.run(.2)
            self.assertAlmostEqual(sim.state[SHIFT], stopped)

    def test_between_position_seating_stops_without_completing_the_shift(self):
        sim = Sim(self.model(), dt=.1)
        sim.move('carriage_elevation', to=6)
        sim.move('carriage_rotation', to=10)
        command = sim.move('carriage_elevation', to=0, duration=.2)
        sim.run(.2)
        self.assertEqual(command.status, 'blocked')
        self.assertGreater(sim.state[LIFT], 5.8)
        self.assertAlmostEqual(sim.state[SHIFT], 10)
        held = sim.state[LIFT]
        sim.move('carriage_rotation', to=20)
        self.assertAlmostEqual(sim.state[LIFT], held)
        sim.move('carriage_elevation', to=0)
        self.assertAlmostEqual(sim.state[LIFT], 0)
        self.assertAlmostEqual(sim.state[SHIFT], 20)

    def test_partial_lift_does_not_clear_the_keys_and_full_lift_does(self):
        sim = Sim(self.model(), dt=.1)
        sim.move('carriage_elevation', to=3)
        sim.move('carriage_rotation', to=10, duration=.2)
        sim.run(.2)
        self.assertLess(sim.state[SHIFT], 1)
        self.assertAlmostEqual(sim.state[LIFT], 3)
        held = sim.state[SHIFT]
        saved = sim.snapshot()

        def resume():
            sim.move('carriage_elevation', to=6)
            self.assertAlmostEqual(sim.state[SHIFT], held)
            sim.move('carriage_rotation', to=20)
            self.assertAlmostEqual(sim.state[SHIFT], 20)
            sim.move('carriage_elevation', to=0)
            self.assertAlmostEqual(sim.state[LIFT], 0)

        resume()
        expected = sim.snapshot()
        sim.restore(saved)
        resume()
        self.assertEqual(sim.snapshot(), expected)


class RunningClearingInterlockTest(unittest.TestCase):
    model = OperatingCurta

    def test_each_ring_rest_blocks_both_directions_without_auto_lift(self):
        sim = Sim(self.model(), dt=.1)
        for rest in (0, 230, 360):
            for direction in (-1, 1):
                sim.move('carriage_elevation', to=6)
                sim.move('clearing_rotation', to=rest)
                sim.move('carriage_elevation', to=0)
                command = sim.move('clearing_rotation', to=rest + direction * 90, duration=.2)
                sim.run(.2)
                self.assertEqual(command.status, 'blocked',
                                 (rest, direction, sim.state[RING], sim.state[PIN], sim.state[LIFT]))
                admitted = (-sim.state[RING] - rest) * direction
                self.assertGreater(admitted, 0)
                self.assertLess(admitted, 5)
                self.assertEqual(sim.state[LIFT], 0)
                self.assertLessEqual(sim.state[PIN], 3.090001)

    def test_partial_clearing_blocks_seating_without_finishing_the_sweep(self):
        sim = Sim(self.model(), dt=.1)
        sim.move('carriage_elevation', to=6)
        sim.move('clearing_rotation', to=90)
        command = sim.move('carriage_elevation', to=0, duration=.2)
        sim.run(.2)
        self.assertEqual(command.status, 'blocked')
        self.assertGreater(sim.state[LIFT], 4.7)
        self.assertLess(sim.state[LIFT], 4.9)
        self.assertAlmostEqual(sim.state[RING], -90)
        held = sim.state[LIFT]
        for _ in range(3):
            sim.move('carriage_elevation', to=0, duration=.2)
            sim.run(.2)
            self.assertAlmostEqual(sim.state[LIFT], held)
        # Returning the ring frees seating; it does not perform seating.
        sim.move('clearing_rotation', to=0)
        self.assertAlmostEqual(sim.state[LIFT], held)
        sim.move('carriage_elevation', to=0)
        self.assertAlmostEqual(sim.state[LIFT], 0)

    def test_seated_ring_request_uses_real_play_without_lifting_the_carriage(self):
        sim = Sim(self.model(), dt=.1)
        command = sim.move('clearing_rotation', to=90, duration=.2)
        sim.run(.2)
        self.assertEqual(command.status, 'blocked')
        self.assertGreater(-sim.state[RING], 0)
        self.assertLess(-sim.state[RING], 5)
        self.assertLessEqual(sim.state[PIN], 3.090001)
        self.assertEqual(sim.state[LIFT], 0)
        held = sim.state[RING]
        for _ in range(3):
            sim.move('clearing_rotation', to=90, duration=.2)
            sim.run(.2)
            self.assertAlmostEqual(sim.state[RING], held)
        self.assertEqual(register_reading(sim), 0)
        self.assertEqual(register_reading(sim, True), 0)

    def test_partial_lift_opens_only_its_actual_clearance_and_replays(self):
        sim = Sim(self.model(), dt=.1)
        sim.move('carriage_elevation', to=2)
        sim.move('clearing_rotation', to=90, duration=.2)
        sim.run(.2)
        self.assertGreater(-sim.state[RING], 5)
        self.assertLess(-sim.state[RING], 6)
        self.assertAlmostEqual(sim.state[LIFT], 2)
        stopped = sim.snapshot()
        angle = sim.state[RING]

        def resume():
            sim.move('carriage_elevation', to=6)
            self.assertAlmostEqual(sim.state[RING], angle)
            sim.move('clearing_rotation', to=90)
            self.assertAlmostEqual(sim.state[RING], -90)

        resume()
        expected = sim.snapshot()
        sim.restore(stopped)
        resume()
        self.assertEqual(sim.snapshot(), expected)
