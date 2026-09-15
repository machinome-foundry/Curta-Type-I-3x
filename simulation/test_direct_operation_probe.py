"""Reduced prerequisites, before the complete machine relies on them."""

import unittest

from solid_node.simulation import Sim
from simulation.tools.direct_operation_probe import clearing_fixture
from simulation.tools.shifted_carry_probe import fixed_fixture


class RetainedClearingPrerequisiteTest(unittest.TestCase):
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
