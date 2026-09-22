"""Separate demos replay physical requests on a retained machine."""

import unittest

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.operating_demonstrations import DEMONSTRATIONS, replay


class OperatingDemonstrationDefinitionTest(unittest.TestCase):
    def test_small_set_uses_only_independent_physical_inputs(self):
        self.assertEqual(set(DEMONSTRATIONS), {
            'addition', 'carry', 'overflow', 'subtraction', 'shift', 'clearing'})
        for name, steps in DEMONSTRATIONS.items():
            self.assertTrue(steps, name)
            for step in steps:
                self.assertIn(step.input, {'digit_1', 'digit_2', 'crank_rotation',
                    'crank_elevation', 'carriage_elevation', 'carriage_rotation',
                    'clearing_rotation'})
                self.assertGreater(step.duration, 0)
                self.assertIn(step.kind, ('by', 'to'))


class OperatingDemonstrationReplayTest(unittest.TestCase):
    model = OperatingCurta

    def test_all_demonstrations_replay_exactly_from_the_initial_snapshot(self):
        for name in DEMONSTRATIONS:
            with self.subTest(name=name):
                sim = Sim(self.model(), dt=.1)
                initial = sim.snapshot()
                first = replay(sim, name, initial)
                expected = sim.snapshot()
                second = replay(sim, name, initial)
                self.assertEqual(sim.snapshot(), expected)
                self.assertEqual(first, second)
