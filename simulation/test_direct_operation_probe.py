"""Reduced prerequisites, before the complete machine relies on them."""

import unittest

from machinome.simulation import Sim
from simulation.tools.direct_operation_probe import clearing_fixture
from simulation.tools.shifted_carry_probe import ShiftedCarry, fixed_fixture


class RetainedClearingPrerequisiteTest(unittest.TestCase):
    def test_live_associations_match_fixed_twins_at_multiple_tick_sizes(self):
        for position in (0, 1):
            for ticks in (1, 12, 240):
                with self.subTest(position=position, ticks=ticks):
                    live = Sim(ShiftedCarry(), dt=1 / ticks,
                               state={'shift': position})
                    fixed = Sim(fixed_fixture(position), dt=1 / ticks)
                    for sim in (live, fixed):
                        command = sim.move('crank', by=2, duration=1)
                        sim.run(1)
                        self.assertEqual(command.status, 'completed')
                    for key in ('lower.turn', 'higher.turn', 'carry.travel'):
                        self.assertAlmostEqual(live.state[key], fixed.state[key], places=8)

    def test_live_shift_holds_real_coordinates_and_snapshot_replays(self):
        sim = Sim(ShiftedCarry(), dt=.02)
        sim.move('crank', by=.75, duration=.2)
        sim.run(.2)
        held = {key: sim.state[key] for key in
                ('lower.turn', 'higher.turn', 'carry.travel')}
        saved = sim.snapshot()
        for _ in range(2):
            sim.move('shift', to=1, duration=.2)
            sim.run(.2)
            for key, value in held.items():
                self.assertEqual(sim.state[key], value)
            sim.move('crank', by=2, duration=.2)
            sim.run(.2)
            sim.move('shift', to=0)
            after = sim.snapshot()
            if _ == 0:
                expected = after
                sim.restore(saved)
            else:
                self.assertEqual(after, expected)

    def test_each_fixed_carry_association_constructs_and_admits_crank_travel(self):
        for position in (0, 1):
            with self.subTest(position=position):
                sim = Sim(fixed_fixture(position), dt=.02)
                command = sim.move('crank', by=2)
                self.assertTrue(sim.running)
                self.assertEqual(command.status, 'completed')
                self.assertEqual(command.admitted, 2)
                self.assertEqual(sim.state['lower.turn'], 2 if position == 0 else 0)
                self.assertEqual(sim.state['carry.travel'], 1)

    def test_both_directions_repeated_clear_and_snapshot_resume(self):
        for direction in (-1, 1):
            for digit in range(10):
                with self.subTest(direction=direction, digit=digit):
                    sim = Sim(clearing_fixture(digit * 36), dt=.02, record=8)
                    sim.move('rack', by=direction * 12)
                    saved = sim.snapshot()
                    command = sim.move('rack', by=direction * 720)
                    self.assertEqual(command.status, 'completed')
                    expected = (0 if digit == 0 else .5 if direction < 0 else 359.5)
                    self.assertAlmostEqual(sim.state['wheel.rotation'], expected, places=7)
                    first = sim.snapshot()
                    first_angle = sim.state['wheel.rotation']
                    sim.move('rack', by=direction * 720)
                    self.assertEqual(sim.state['wheel.rotation'], first_angle)
                    sim.restore(saved)
                    sim.move('rack', by=direction * 720)
                    self.assertEqual(sim.snapshot(), first)
