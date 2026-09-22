"""Exercise unchanged arithmetic contracts against the isolated tens trial."""

from unittest.mock import patch
from simulation import test_running as running_tests
from simulation.counter_tens_operating_trial import CounterTensOperatingTrial


class CounterTensArithmeticTrialTest(running_tests.RunningCurtaTest):
    def setUp(self):
        super().setUp()
        # The inherited tests issue only public controls. Swap their factory,
        # not their expected readings, starting state, timestep or operation.
        factory = patch.object(running_tests, 'OperatingCurta', CounterTensOperatingTrial)
        factory.start()
        self.addCleanup(factory.stop)
