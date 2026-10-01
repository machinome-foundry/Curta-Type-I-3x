"""Unchanged production arithmetic scenarios on the unadopted counter bank."""

from unittest.mock import patch

from simulation import test_mechanistic as running_tests
from simulation.counter_bank_operating_trial import CounterBankOperatingTrial


class CounterBankArithmeticTrialTest(running_tests.MechanisticCurtaTest):
    def setUp(self):
        super().setUp()
        self.factory_patch = patch.object(running_tests, 'MechanisticCurta', CounterBankOperatingTrial)
        self.factory_patch.start()
        self.addCleanup(self.factory_patch.stop)
