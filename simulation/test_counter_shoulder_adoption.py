"""Production-facing shoulder shape gate, red before the isolated fit lands."""

import unittest
from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.counter_guide_shoulder import ShoulderClearedTurnsSlider
from simulation import test_counter_shoulder_operating_trial as trial_tests


class OperatingCounterShoulderTest(unittest.TestCase):
    def test_every_production_counter_uses_the_verified_shoulder(self):
        sim = Sim(OperatingCurta(), dt=.1)
        self.assertEqual(len(sim.state), 216)
        expected = ShoulderClearedTurnsSlider().shape()
        carries = sim.node.carry_mechanism.turns_carries
        for index in range(1, 6):
            lever = getattr(carries, f'turns_tens_lever_assembly_{index}')
            actual = lever.tens_slider_for_turns_counter.shape()
            with self.subTest(station=index):
                self.assertTrue(actual.isValid())
                self.assertEqual(len(actual.Solids()), 1)
                self.assertEqual(actual.cut(expected).Volume(), 0)
                self.assertEqual(expected.cut(actual).Volume(), 0)


class OperatingCounterShoulderStateTest(trial_tests.CounterShoulderOperatingIdentityTest):
    model = OperatingCurta
