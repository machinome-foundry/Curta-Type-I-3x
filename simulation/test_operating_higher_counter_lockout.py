"""Every higher counter needs its own actual-root withdrawal restraint.

These production tests remain red until independent parts/contact/arithmetic
and replay gates justify adoption. They retain the same physical input order
as the tens case, shifted by each source station's measured 20-degree phase.
"""

from simulation import test_operating_counter_tens_lockout as counter_tests


class OperatingCounterHundredsLockoutTest(counter_tests.OperatingCounterTensLockoutTest):
    station = 3


class OperatingCounterFourthLockoutTest(counter_tests.OperatingCounterTensLockoutTest):
    station = 4


class OperatingCounterFifthLockoutTest(counter_tests.OperatingCounterTensLockoutTest):
    station = 5


class OperatingCounterSixthLockoutTest(counter_tests.OperatingCounterTensLockoutTest):
    station = 6
