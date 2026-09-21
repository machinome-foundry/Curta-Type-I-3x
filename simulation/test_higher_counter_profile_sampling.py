"""Admission checks must retain interior, edge and known-failure poses."""

import unittest
import json
from pathlib import Path
from unittest.mock import patch

from simulation.counter_locking_profiles import SECTORS
from simulation.higher_counter_locking_profiles import LOWER_LOCK_SECTORS, CARRY_TOOTH_STRIPS
from simulation.tools.check_higher_counter_locking_profile import (
    sample_shafts, sample_angles, admitted_contacts, rejected_poses, sample_carries,
)


class HigherCounterProfileSamplingTest(unittest.TestCase):
    def test_station_chart_does_not_change_the_measured_machine_pose(self):
        for station in range(2, 7):
            shift = 20*(station-2)
            calls = []
            with patch('simulation.tools.check_higher_counter_locking_profile.higher_counter_contact_gap',
                       return_value=-1) as gap:
                rows = list(admitted_contacts(
                    lambda angle, kernel: calls.append((angle, kernel)) or 0,
                    1, 166-shift, 'faceted', angles=(206.5+shift,), station=station))
            gap.assert_called_once_with(206.5, 166, -1.8+4.2)
            self.assertEqual(calls, [(206.5+shift, 'faceted')])
            self.assertEqual(rows[0]['shaft'], 166-shift)
            self.assertEqual(rows[0]['crank'], 206.5+shift)
            self.assertEqual(rows[0]['station'], station)
        for station in (1, 7):
            with self.assertRaises(ValueError):
                list(admitted_contacts(lambda angle, kernel: 0, 1, 166,
                                       'native', angles=(206.5,), station=station))

    def test_axial_matrix_retains_measured_brackets_and_nominal_plane_sides(self):
        self.assertEqual(sample_carries(), (0, .5, 1))
        heights = sample_carries(supports=True)
        self.assertEqual(tuple(sorted(set(heights))), heights)
        self.assertTrue(all(0 <= height <= 1 for height in heights))
        self.assertTrue({0, .25, .5, .75, 1} <= set(heights))
        for travel in (-.6, .3, .9):
            for offset in (-.001, 0, .001):
                self.assertIn((travel+offset+1.8)/4.2, heights)
        data = json.loads((Path(__file__).parent/'docs/evidence/'
                           'counter-tens-contact-support-2026-09-21.json').read_text())
        for support in data['axial_supports']:
            for row in support['measurements']:
                self.assertIn(row['left'], heights)
                self.assertIn(row['right'], heights)
                self.assertIn((row['left']+row['right'])/2, heights)

    def test_collision_evidence_survives_changes_to_profile_knots(self):
        # Remove the candidate tables: known failures must come from the
        # evidence, not happen to survive as the current profile's edges.
        with patch('simulation.tools.check_higher_counter_locking_profile.PROFILE_SETS', ()):
            self.assertIn((182, 98.23833236694335), rejected_poses())
            self.assertIn(183, sample_shafts())
            self.assertIn(98.23833236694335, sample_angles(182))

    def test_knots_midpoints_edges_and_measured_false_stops_are_retained(self):
        for dense in (False, True):
            shafts = sample_shafts(dense=dense)
            for profiles, shift in ((SECTORS, 20), (LOWER_LOCK_SECTORS, 0),
                                    (CARRY_TOOTH_STRIPS, 0)):
                for start, end, points in profiles:
                    self.assertTrue({p[0]-shift for p in points} <= shafts)
                    self.assertTrue({(a[0]+b[0])/2-shift for a, b in zip(points, points[1:])} <= shafts)
                    self.assertTrue({edge-shift+offset for edge in (start, end)
                                     for offset in (-.001, 0, .001)} <= shafts)
            for flat in range(5):
                self.assertIn(166+72*flat, shafts)
                self.assertIn(206.5, sample_angles(166+72*flat, dense=dense))
        self.assertTrue(set(range(114, 475)) <= sample_shafts(dense=True))
        self.assertTrue(set(range(0, 361, 5)) <= sample_angles(166, dense=True))

    def test_every_positive_admitted_common_fails_without_a_volume_epsilon(self):
        with patch('simulation.tools.check_higher_counter_locking_profile.higher_counter_contact_gap',
                   side_effect=(-1, 0, 1)):
            rows = list(admitted_contacts(lambda angle, kernel: 1e-20,
                                          1, 166, 'native', angles=(204, 206, 208)))
        self.assertEqual([row['crank'] for row in rows], [204, 206])
        self.assertTrue(all(row['failure'] and row['common_mm3'] == 1e-20 for row in rows))

    def test_nonfinite_law_or_common_cannot_be_a_clear_pose(self):
        with patch('simulation.tools.check_higher_counter_locking_profile.higher_counter_contact_gap',
                   return_value=float('nan')):
            with self.assertRaises(ValueError):
                list(admitted_contacts(lambda angle, kernel: 0, 1, 166, 'native', angles=(206,)))
        with patch('simulation.tools.check_higher_counter_locking_profile.higher_counter_contact_gap',
                   return_value=-1):
            for bad in (float('nan'), float('inf'), -1):
                with self.assertRaises(ValueError):
                    list(admitted_contacts(lambda angle, kernel: bad,
                                           1, 166, 'native', angles=(206,)))


if __name__ == '__main__':
    unittest.main()
