"""A conservative path check cannot accept a contact between sample poses."""

import unittest
from simulation.tools.clearing_loop_sweep import certify_rotation


class LoopSweepCertificateTest(unittest.TestCase):
    def test_constant_separation_covers_the_entire_interval(self):
        rows = certify_rotation(lambda angle, cap: min(.05, cap), 80)
        rows.sort(key=lambda row: row['from'])
        self.assertEqual(rows[0]['from'], -90)
        self.assertEqual(rows[-1]['to'], 0)
        for first, second in zip(rows, rows[1:]):
            self.assertEqual(first['to'], second['from'])
        for row in rows:
            self.assertGreater(row['gap'], row['displacement_bound'] + 1e-5)

    def test_contact_between_integer_poses_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'no strict separation'):
            certify_rotation(lambda angle, cap: min(abs(angle+.25)*.01, cap),
                             1, low=-1, high=0)

    def test_nonfinite_or_zero_distance_is_not_clearance(self):
        for distance in (0, -1, float('nan'), float('inf')):
            with self.subTest(distance=distance), self.assertRaises(AssertionError):
                certify_rotation(lambda angle, cap: distance, 1)

    def test_exhausting_subdivision_is_a_failure(self):
        with self.assertRaisesRegex(AssertionError, 'unproved interval'):
            certify_rotation(lambda angle, cap: .001, 80, max_depth=0)
