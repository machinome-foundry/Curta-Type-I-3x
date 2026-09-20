"""Endpoint meaning and unseated engagement are independent of a mode flag."""

import unittest
from simulation.reverser_modes import counter_count, overlaps


class ReverserModeTest(unittest.TestCase):
    def test_all_four_working_combinations(self):
        for knob, subtract, expected in (
                (3.9075, 0, (1, 0, 0, 0, 0, 0)),
                (-4.9425, 0, (9, 9, 9, 9, 9, 9)),
                (3.9075, 1, (9, 9, 9, 9, 9, 9)),
                (-4.9425, 1, (1, 0, 0, 0, 0, 0))):
            self.assertEqual(tuple(counter_count(i, knob+.0925, 9*subtract)
                                   for i in range(6)), expected)

    def test_unseated_height_can_drive_higher_channels_with_single_teeth(self):
        self.assertEqual(tuple(counter_count(i, -3+.0925, 0) for i in range(6)),
                         (1, 1, 1, 1, 1, 1))

    def test_touching_band_faces_are_not_positive_axial_engagement(self):
        self.assertFalse(overlaps(0, 1.5))
        self.assertFalse(overlaps(1.5, 0))
        self.assertTrue(overlaps(0, 1.49))
