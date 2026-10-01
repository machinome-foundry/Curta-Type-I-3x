"""The accepted tens restraint must operate in the manifest's default root."""

from simulation import test_higher_operating_trial as trial_tests
from simulation.mechanistic import MechanisticCurta


class OperatingHigherLockoutTest(trial_tests.HigherOperatingTrialTest):
    model = MechanisticCurta
