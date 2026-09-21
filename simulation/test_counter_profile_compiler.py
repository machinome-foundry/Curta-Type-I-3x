"""Measured counter curves must retain both kernels and every source flat."""

import unittest

from simulation.tools.compile_counter_locking_profile import compile_profile


def fixture():
    bands, rows = [], []
    for flat in range(5):
        index = 134+72*flat
        for kernel in ('native', 'faceted'):
            bands.append({'station': 1, 'carry': 0, 'crank': 0, 'trial': True,
                          'kernel': kernel, 'index': index,
                          'bounds': [{'last_free': index-2, 'first_contact': index-2.001,
                                      'free_mm3': 0, 'contact_mm3': 1e-20},
                                     {'last_free': index+.2, 'first_contact': index+.201,
                                      'free_mm3': 0, 'contact_mm3': 1e-20}]})
            for offset in (2, 36, 68):
                rows.append({'station': 1, 'carry': 0, 'trial': True,
                             'kernel': kernel, 'shaft': index+offset,
                             'boundaries': [
                                 {'left': 60, 'right': 60.1 if kernel == 'native' else 60.2,
                                  'enters_contact': False},
                                 {'left': 174 if kernel == 'native' else 173.9,
                                  'right': 174.1, 'enters_contact': True}]})
    return rows, bands


class CounterProfileCompilerTest(unittest.TestCase):
    def test_combines_the_free_sides_of_both_kernels_without_repeating_a_flat(self):
        rows, bands = fixture()
        sectors = compile_profile(rows, bands)
        self.assertEqual(len(sectors), 5)
        for flat, (start, end, points) in enumerate(sectors):
            self.assertAlmostEqual(start, 134+72*flat+.2-.002)
            self.assertAlmostEqual(end, 134+72*(flat+1)-2+.002)
            self.assertEqual(points, tuple((134+72*flat+offset, 60.2, 173.9)
                                          for offset in (2, 36, 68)))

    def test_missing_kernel_or_flat_refuses_the_profile(self):
        rows, bands = fixture()
        for incomplete_rows, incomplete_bands in ((rows[:-1], bands), (rows, bands[:-1])):
            with self.subTest(rows=len(incomplete_rows), bands=len(incomplete_bands)):
                with self.assertRaises(ValueError):
                    compile_profile(incomplete_rows, incomplete_bands)

    def test_extra_contact_island_is_not_discarded(self):
        rows, bands = fixture()
        rows[0]['boundaries'].extend([
            {'left': 200, 'right': 201, 'enters_contact': False},
            {'left': 202, 'right': 203, 'enters_contact': True}])
        with self.assertRaisesRegex(ValueError, 'two boundaries'):
            compile_profile(rows, bands)

    def test_unmatched_geometry_is_not_merged(self):
        rows, bands = fixture()
        rows[0]['trial'] = False
        with self.assertRaisesRegex(ValueError, 'trial counter ones'):
            compile_profile(rows, bands)


if __name__ == '__main__':
    unittest.main()
