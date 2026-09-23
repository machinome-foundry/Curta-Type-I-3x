"""A completed native prefix must not conceal missing or mismatched evidence."""

from copy import deepcopy
import unittest

from simulation.tools.refine_reverser_native import remaining_rows


def fixture():
    endpoints = dict(left=dict(shaft=1, contact=False, volumes_mm3={'top': 0}),
                     right=dict(shaft=2, contact=True, volumes_mm3={'top': 1e-30}),
                     enters_contact=True)
    seed = deepcopy(endpoints)
    rows = [dict(station=1, crank=0, height=0, lift=0, boundaries=[]),
            dict(station=1, crank=90, height=0, lift=0, boundaries=[seed])]
    completed = [dict(rows[0], kernel='native', input_sha256='pin',
                      status='not_checked_no_world64_transition'),
                 dict(rows[1], kernel='native', input_sha256='pin',
                      status='refined_observed_transitions',
                      boundaries=[dict(endpoints, world64_seed=seed)])]
    return rows, completed


class ReverserRefinementResumeTest(unittest.TestCase):
    def test_only_verified_complete_records_are_skipped_in_original_order(self):
        rows, completed = fixture()
        self.assertEqual(remaining_rows(rows, completed[:1], 'pin'), rows[1:])
        self.assertEqual(remaining_rows(rows, completed[1:], 'pin'), rows[:1])
        self.assertEqual(remaining_rows(rows, completed, 'pin'), [])

    def test_wrong_source_and_unknown_or_duplicate_poses_are_refused(self):
        rows, completed = fixture()
        for records, digest in ((completed, 'other'), (completed+completed[:1], 'pin'),
                                ([dict(completed[0], crank=5)], 'pin')):
            with self.subTest(records=records, digest=digest), self.assertRaises(ValueError):
                remaining_rows(rows, records, digest)
        with self.assertRaises(ValueError):
            remaining_rows(rows+rows[:1], [], 'pin')

    def test_unmeasured_rows_cannot_be_promoted_to_native_clearance(self):
        rows, completed = fixture()
        completed[0]['status'] = 'refined_observed_transitions'
        with self.assertRaises(ValueError):
            remaining_rows(rows, completed, 'pin')

    def test_missing_boundaries_or_endpoint_evidence_are_not_skipped(self):
        for missing in ('all', 'left', 'volumes_mm3'):
            rows, completed = fixture()
            if missing == 'all':
                completed[1]['boundaries'] = []
            elif missing == 'left':
                del completed[1]['boundaries'][0]['left']
            else:
                del completed[1]['boundaries'][0]['left']['volumes_mm3']
            with self.subTest(missing=missing), self.assertRaises(ValueError):
                remaining_rows(rows, completed, 'pin')

    def test_positive_endpoints_cannot_be_relabelled_clear(self):
        rows, completed = fixture()
        completed[1]['boundaries'][0]['right']['contact'] = False
        with self.assertRaises(ValueError):
            remaining_rows(rows, completed, 'pin')


if __name__ == '__main__':
    unittest.main()
