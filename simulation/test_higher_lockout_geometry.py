"""A reduced measuring instrument must reproduce the actual installed solids."""

import unittest

from simulation.tools.higher_locking_envelope import contact_reader


class HigherLockoutGeometryTest(unittest.TestCase):
    def test_normal_seat_matches_independently_prepared_operating_root(self):
        # Publish the mesh at the same contact pose as the operating root;
        # rotating already-rounded float32 vertices is a different mesh.
        volume = contact_reader(0, reference=170)
        for kernel, expected in (('native', .30868623127003425),
                                 ('faceted', .21392486170149)):
            with self.subTest(kernel=kernel):
                self.assertEqual(volume(140, kernel), 0)
                self.assertGreater(volume(170, kernel), 0)
                self.assertAlmostEqual(volume(170, kernel), expected, places=9)

    def test_lowered_seat_matches_actual_carry_then_withdrawal(self):
        # The operating carry adds 72 degrees between crank 500 and 530.
        # Its final geometry must be measured at 241.6, not the initial 169.6.
        volume = contact_reader(1, reference=530, shaft=241.6)
        for kernel, expected in (('native', .9496263373477174),
                                 ('faceted', .7603711547340599)):
            with self.subTest(kernel=kernel):
                self.assertGreater(volume(530, kernel), 0)
                self.assertAlmostEqual(volume(530, kernel), expected, places=9)


if __name__ == '__main__':
    unittest.main()
