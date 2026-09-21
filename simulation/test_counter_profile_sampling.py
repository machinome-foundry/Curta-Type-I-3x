"""Admission probes retain source boundaries and independently sampled interiors."""

import unittest

from simulation.counter_locking_profiles import SECTORS
from simulation.tools.check_counter_locking_profile import sample_shafts, sample_angles


class CounterProfileSamplingTest(unittest.TestCase):
    def test_dense_grid_includes_independent_shafts_and_cranks(self):
        self.assertTrue(set(range(134, 495)) <= sample_shafts(dense=True))
        self.assertTrue(set(range(0, 361, 5)) <= sample_angles(143, dense=True))

    def test_both_modes_keep_knots_midpoints_and_support_edges(self):
        for dense in (False, True):
            shafts = sample_shafts(dense=dense)
            for start, end, points in SECTORS:
                self.assertTrue({p[0] for p in points} <= shafts)
                self.assertTrue({(a[0]+b[0])/2 for a, b in zip(points, points[1:])} <= shafts)
                self.assertTrue({edge+offset for edge in (start, end)
                                 for offset in (-.001, 0, .001)} <= shafts)

    def test_measured_failed_pose_survives_later_profile_refinement(self):
        for dense in (False, True):
            self.assertIn(143., sample_shafts(dense=dense))
            self.assertIn(171.50060064697266, sample_angles(143., dense=dense))
            self.assertIn(141., sample_shafts(dense=dense))
            self.assertIn(171.2062967529297, sample_angles(141., dense=dense))


if __name__ == '__main__':
    unittest.main()
