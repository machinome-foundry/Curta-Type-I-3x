"""Rerun original all-station spring/detent contracts on the shoulder trial."""

from simulation import test_carry_bank_capture as capture
from simulation.counter_guide_trial import CounterShoulderTrial


class CounterShoulderCaptureTest(capture.CarryBankCaptureTest):
    node = CounterShoulderTrial
