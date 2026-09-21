"""Higher-counter candidates use their own measured rows and all five flats."""

from copy import deepcopy
import unittest

from simulation.tools.compile_higher_counter_profiles import compile_profiles


def fixture():
    rows, bands, meshes = [], [], []
    for shaft in range(114, 475, 6):
        phase = (shaft-114) % 72
        common = dict(station=2, shaft=shaft, carry=1, trial=True, kernel='native')
        lower = ([] if phase == 0 else [
            dict(left=90+phase/10, right=90.01+phase/10, enters_contact=False),
            dict(left=210+phase/10, right=210.01+phase/10, enters_contact=True)])
        rows.append(common | dict(component='lower_lock', boundaries=lower,
                                  samples=[(0, int(bool(phase))), (360, int(bool(phase)))]))
        teeth = []
        centres = ([204+(phase-72)/6.4] if phase >= 12 else [])
        centres += ([204+phase/6.4] if phase <= 60 else [])
        for centre in centres:
            teeth.extend([dict(left=centre-2, right=centre-1.99, enters_contact=True),
                          dict(left=centre+1.99, right=centre+2, enters_contact=False)])
        rows.append(common | dict(component='carry_tooth', boundaries=teeth,
                                  samples=[(0, 0), (360, 0)]))
        meshes.append(common | dict(kernel='faceted', boundaries=deepcopy(lower)))
    for index in range(114, 403, 72):
        for kernel in ('native', 'faceted'):
            bands.append(dict(station=2, carry=1, crank=0, trial=True, kernel=kernel,
                              index=index, bounds=[
                                  dict(last_free=index-1, first_contact=index-1.001,
                                       free_mm3=0, contact_mm3=1e-20),
                                  dict(last_free=index+1, first_contact=index+1.001,
                                       free_mm3=0, contact_mm3=1e-20)]))
    return rows, bands, meshes


class HigherCounterProfileCompilerTest(unittest.TestCase):
    def test_measured_counter_coordinates_survive_chart_registration(self):
        lower, gear, supports = compile_profiles(*fixture())
        self.assertEqual(len(lower), 5)
        self.assertEqual(len(gear), 10)
        self.assertEqual(len(supports), 10)
        for flat, (start, end, points) in enumerate(lower):
            self.assertAlmostEqual(start, 115+72*flat-.002)
            self.assertAlmostEqual(end, 185+72*flat+.002)
            for shaft, opening, closing in points:
                phase = (shaft-114) % 72
                self.assertAlmostEqual(opening, 90.01+phase/10)
                self.assertAlmostEqual(closing, 210+phase/10)
        for start, end, points in gear:
            self.assertLess(start, end)
            self.assertTrue(all(185 < entering < leaving < 220
                                for _, entering, leaving in points))

    def test_wrong_station_height_geometry_or_duplicate_rows_are_refused(self):
        for field, value in (('station', 3), ('carry', .5), ('trial', False),
                             ('kernel', 'faceted'), ('component', 'upper_lock')):
            rows, bands, meshes = fixture()
            rows[0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                compile_profiles(rows, bands, meshes)
        rows, bands, meshes = fixture()
        with self.assertRaises(ValueError):
            compile_profiles(rows+[rows[0]], bands, meshes)

    def test_missing_whole_mesh_or_indexed_band_evidence_is_refused(self):
        rows, bands, meshes = fixture()
        for incomplete_bands, incomplete_meshes in ((bands[:-1], meshes), (bands, meshes[:-1])):
            with self.assertRaises(ValueError):
                compile_profiles(rows, incomplete_bands, incomplete_meshes)
        bands[0]['component'] = 'lower_lock'
        with self.assertRaises(ValueError):
            compile_profiles(rows, bands, meshes)

    def test_tooth_refinement_does_not_require_remeasuring_an_unrelated_lower_curve(self):
        rows, bands, meshes = fixture()
        extra = deepcopy(next(row for row in rows
                              if row['shaft'] == 162 and row['component'] == 'carry_tooth'))
        extra['shaft'] = 166
        lower, gear, _ = compile_profiles(rows+[extra], bands, meshes)
        self.assertEqual(len(lower), 5)
        self.assertEqual(len(gear), 10)


if __name__ == '__main__':
    unittest.main()
