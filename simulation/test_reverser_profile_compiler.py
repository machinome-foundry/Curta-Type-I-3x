"""Portable model data must retain every installed cover and its proof gate."""

from copy import deepcopy
import unittest

from simulation.tools.compile_reverser_profiles import compile_profiles, INPUT_PATHS, DRUM_PATHS


def fixture():
    rows = []
    for index, path in enumerate((*INPUT_PATHS, *DRUM_PATHS)):
        input_part = index < 6
        heights = ([[-45.35, -43.85], [-40.85, -39.35], [-36.35, -34.85]]
                   if index == 0 else [[-40.85, -39.35]] if input_part else
                   [[-54.2, -43.7]] + [[-49.7, -48.2]]*8 if index == 6 else
                   [[-72., -66.3]] + [[-67.8, -66.3]]*9)
        rows.append(dict(kind='radial_envelope', path=path, radius_mm=6.3 if input_part else 36.62,
                         native_outside_mm3=0., mesh_radius_mm=6.2 if input_part else 36.6))
        for component, height in enumerate(heights):
            rows.append(dict(kind='installed_profile', path=path, component=component,
                source_height=height, allowance_mm=.005, axial_allowance_mm=.001,
                points=[[0., 0.], [1., 0.], [0., 1.]], polygons=[[0, 1, 2]],
                axis=[40.5, 0., 0.] if input_part else [0., 0., 0.],
                reference_shaft_angle=134.-20*index if input_part else 0.,
                reference_reverser_height=3.9075))
        rows.append(dict(kind='installed_mesh_verdict', path=path, components=len(heights),
            native_remainder_mm3=0., native_remainder_after_exclusion_mm3=0.,
            uncovered_control_mm3=1., remainder_mm3=0., remainder_empty=True,
            residual_radius_mm=0., separated=True, other_outer_radius_mm=36.62 if input_part else 6.3,
            minimum_axis_radius_mm=40.5))
    rows.append(dict(kind='axial_exclusion', bottom_clip=-72.,
        minimum_input_z_in_drum_frame=-71.8,
        reverser_range=[-6.9425, 3.9075], crank_elevation_range=[0., 9.]))
    return rows


class ReverserProfileCompilerTest(unittest.TestCase):
    def test_keeps_six_phases_and_groups_only_identical_axial_bands(self):
        result = compile_profiles(fixture())
        self.assertEqual(len(result['profiles']), 8)
        self.assertEqual(len(result['gears']), 6)
        self.assertEqual(len(result['drums']), 2)
        self.assertEqual([gear['reference'] for gear in result['gears']],
                         [134., 114., 94., 74., 54., 34.])
        self.assertEqual(len(result['gears'][0]['bands']), 3)
        for actual, expected in zip(result['gears'][0]['bands'][0], (-45.351, -43.849)):
            self.assertAlmostEqual(actual, expected)
        self.assertEqual(len(result['profiles'][result['drums'][1]['profile']]['polygons']), 8)

    def test_missing_duplicate_and_failed_complete_print_proofs_refuse(self):
        rows = fixture()
        verdict = next(r for r in rows if r['kind'] == 'installed_mesh_verdict')
        for changed in ([r for r in rows if r is not verdict], rows+[deepcopy(verdict)]):
            with self.assertRaises(ValueError):
                compile_profiles(changed)
        for field, bad in (('separated', False), ('native_remainder_after_exclusion_mm3', 1e-30),
                           ('remainder_mm3', -1e-30), ('uncovered_control_mm3', 0.),
                           ('components', 2)):
            changed = deepcopy(rows)
            next(r for r in changed if r['kind'] == 'installed_mesh_verdict')[field] = bad
            with self.subTest(field=field), self.assertRaises(ValueError):
                compile_profiles(changed)

    def test_uncovered_residual_needs_geometric_separation_not_small_volume(self):
        rows = fixture()
        verdict = next(r for r in rows if r['kind'] == 'installed_mesh_verdict')
        verdict.update(remainder_empty=False, remainder_mm3=1e-30, residual_radius_mm=4.)
        with self.assertRaises(ValueError):
            compile_profiles(rows)
        verdict['residual_radius_mm'] = 3.87
        compile_profiles(rows)

    def test_profiles_and_lower_drum_cannot_silently_disappear(self):
        rows = fixture()
        with self.assertRaises(ValueError):
            compile_profiles([r for r in rows if r.get('path') != DRUM_PATHS[1]])
        for row in rows:
            if row['kind'] == 'installed_profile' and row['path'] == DRUM_PATHS[1]:
                row['source_height'] = [-45., -43.]
        with self.assertRaises(ValueError):
            compile_profiles(rows)
