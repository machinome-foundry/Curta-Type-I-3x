"""Reuse the unchanged seventeen-ball capture check without the sweep suite."""

from machinome.test import TestCase
from simulation.detent_mate_capture import DetentMateCaptureBench
from simulation.test_dial_detent_bank import DialDetentBankTest


class DetentMateCaptureTest(TestCase):
    node = DetentMateCaptureBench

    def test_each_ball_is_captured_by_its_own_dial_and_finger(self):
        DialDetentBankTest.test_each_ball_is_captured_by_its_own_dial_and_finger(self)
