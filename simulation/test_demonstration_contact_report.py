"""Contact evidence must retain small changes and unsuccessful intersections."""

import unittest

from simulation.tools.operating_demonstration_contacts import compare_inventory


class DemonstrationContactReportTest(unittest.TestCase):
    def test_tracks_added_removed_and_changed_positive_pairs_without_epsilon(self):
        rest = dict(overlap_mm3={'held': 2, 'gone': 3, 'changed': 1}, refusals={})
        sample = dict(overlap_mm3={'held': 2, 'new': 1e-30, 'changed': 1.0000000000000002},
                      refusals={'bad': 'intersection refused'})
        difference = compare_inventory(rest, sample)
        self.assertEqual(difference['added'], {'new': 1e-30})
        self.assertEqual(difference['removed'], {'gone': 3})
        self.assertEqual(difference['changed'], {'changed': [1, 1.0000000000000002]})
        self.assertEqual(difference['refusals'], sample['refusals'])

    def test_equal_inventory_is_not_claimed_to_be_clear(self):
        rest = dict(overlap_mm3={'unresolved': 20}, refusals={})
        result = compare_inventory(rest, rest)
        self.assertEqual(result['positive_pairs'], 1)
        self.assertEqual(result['added'], {})
