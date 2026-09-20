"""Working modes retain their meanings; partial settings follow source bands."""

import unittest
from simulation.result_modes import result_count


class ResultModeTest(unittest.TestCase):
    def test_every_working_digit_in_both_crank_modes(self):
        for channel in (0, 1, 7, 10):
            for digit in range(10):
                self.assertEqual(result_count(channel, digit, 0), digit)
                self.assertEqual(result_count(channel, digit, 9),
                                 9-digit+int(channel == 0))

    def test_partial_lift_is_not_a_midpoint_switch(self):
        self.assertEqual(result_count(0, 3, 1.5), 8)
        self.assertEqual(result_count(1, 3, 1.5), 7)

    def test_partial_selector_does_not_invent_fractional_teeth(self):
        for digit in (0.25, .5, 1.25, 3.3, 4.5, 7.8, 8.75):
            for height in (0, 1.5, 4.5, 9):
                self.assertIn(result_count(0, digit, height), range(11))
