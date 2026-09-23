"""Do not lose contact islands or reinterpret positive commons as clearance."""

import unittest

from simulation.tools.reverser_tooth_envelope import phase_boundaries


class ReverserPhaseBoundaryTest(unittest.TestCase):
    def test_retains_both_contact_islands_and_positive_endpoint_volumes(self):
        def evaluate(shaft):
            return {'top': 1e-30 if 1 < shaft < 3 or 5 < shaft < 7 else 0,
                    'bottom': 0}
        report = phase_boundaries(range(9), evaluate)
        self.assertEqual(len(report['samples']), 9)
        self.assertEqual(len(report['boundaries']), 4)
        self.assertEqual([b['enters_contact'] for b in report['boundaries']],
                         [True, False, True, False])
        for boundary, expected in zip(report['boundaries'], (1, 3, 5, 7)):
            self.assertLessEqual(boundary['left']['shaft'], expected)
            self.assertGreaterEqual(boundary['right']['shaft'], expected)
            self.assertLessEqual(boundary['right']['shaft']-boundary['left']['shaft'],
                                 1/65536)
            self.assertNotEqual(boundary['left']['contact'], boundary['right']['contact'])
            self.assertEqual(sorted((boundary['left']['volumes_mm3']['top'],
                                     boundary['right']['volumes_mm3']['top'])), [0, 1e-30])

    def test_no_observed_transition_is_reported_without_inventing_one(self):
        report = phase_boundaries((0, 1), lambda shaft: {'top': 0, 'bottom': 0})
        self.assertEqual(report['boundaries'], [])

    def test_bad_order_and_unresolved_measurements_are_refused(self):
        for shafts in ((0,), (1, 0), (0, 0)):
            with self.subTest(shafts=shafts), self.assertRaises(ValueError):
                phase_boundaries(shafts, lambda shaft: {'top': 0})
        for volume in (-1e-30, float('nan'), float('inf')):
            with self.subTest(volume=volume), self.assertRaises(ValueError):
                phase_boundaries((0, 1), lambda shaft: {'top': volume})


if __name__ == '__main__':
    unittest.main()
