"""Run the unchanged fifteen-station capture assertions on frame mates."""

from simulation.carry_mate_capture import CarryMateCaptureBench
from simulation.test_carry_bank_capture import CarryBankCaptureTest as _CaptureContract


class CarryMateCaptureTest(_CaptureContract):
    node = CarryMateCaptureBench
