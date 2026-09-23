"""Compiled model covers keep the independently tested installed limit law."""

import unittest

from simulation.reverser_profile_laws import lower_limit, upper_limit
from simulation.reverser_profile_data import DATA, EVIDENCE_SHA256


class ReverserProfileLawsTest(unittest.TestCase):
    def test_cover_record_is_the_completed_inner_flank_candidate(self):
        self.assertEqual(EVIDENCE_SHA256,
            '22335517e243651826084aa60aacd38911b647b79a14d8001cb690e226186327')
        self.assertEqual(len(DATA['covered_paths']), 8)
        self.assertEqual(len(DATA['profiles']), 8)
        self.assertEqual(len(DATA['gears']), 6)

    def test_held_shaft_blocks_axial_entry_at_the_measured_band(self):
        args = (3.9075, -90., 134., 114., 94., 74., 54., 34., 0.)
        self.assertAlmostEqual(lower_limit(*args), 1.0595)
        self.assertEqual(upper_limit(*args), 3.9075)

    def test_alternate_history_keeps_its_free_withdrawal_path(self):
        for own in (-4.9425, -3., 0., 1.0675, 3.9075):
            args = (own, -90., 231.6, 114., 94., 74., 54., 34., 0.)
            with self.subTest(own=own):
                self.assertLessEqual(lower_limit(*args), own)
                self.assertGreaterEqual(upper_limit(*args), own)

    def test_no_current_profile_contact_leaves_geometric_travel(self):
        args = (3.9075, 0., 134., 114., 94., 74., 54., 34., 0.)
        self.assertEqual(lower_limit(*args), -6.9425)
        self.assertEqual(upper_limit(*args), 3.9075)

    def test_native_and_mesh_clear_tens_passage_is_not_a_false_stop(self):
        # Independently placed complete prints have zero common in both
        # representations and .005438883588495964 mm native gap at 103°.
        args = (-4.9425, -103., 314.8, 166.8, 94., 74., 54., 34., 0.)
        self.assertLessEqual(lower_limit(*args), args[0])
        self.assertGreaterEqual(upper_limit(*args), args[0])
