"""A predicted transition is a search seed, never a measured clearance."""

import unittest

from simulation.tools.refine_reverser_intervals import refine_transition


class ReverserIntervalRefinementTest(unittest.TestCase):
    def test_expands_and_measures_actual_transition_not_interpolated_guess(self):
        result = refine_transition(1, True, lambda shaft: {'top': 1e-30 if shaft > 2 else 0})
        self.assertGreater(len(result['search_attempts']), 1)
        self.assertLessEqual(result['left']['shaft'], 2)
        self.assertGreater(result['right']['shaft'], 2)
        self.assertEqual(result['right']['volumes_mm3']['top'], 1e-30)

    def test_opposite_transition_and_unbracketed_guess_are_not_accepted(self):
        for evaluate in (lambda shaft: {'top': int(shaft < 1)},
                         lambda shaft: {'top': 0}):
            with self.assertRaises(ValueError):
                refine_transition(1, True, evaluate)


if __name__ == '__main__':
    unittest.main()
