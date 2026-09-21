"""A higher-counter candidate must retain contacts without blocking legal paths."""

import json
from pathlib import Path
import unittest

from simulation.cycle import tooth_passage, TURNS_INPUT_END, TURNS_CARRY_END
from simulation.higher_counter_locking_laws import higher_counter_contact_gap


class HigherCounterLockingLawTest(unittest.TestCase):
    def test_measured_free_carry_poses_do_not_become_false_stops(self):
        data = json.loads((Path(__file__).parent/'docs/evidence/'
                           'higher-counter-coarse-profile-rejection-2026-09-21.json').read_text())
        self.assertEqual(len(data['false_stops']), 5)
        for row in data['false_stops']:
            self.assertEqual(row['complete_mm3'], {'native': 0, 'faceted': 0})
            with self.subTest(flat=row['flat']):
                self.assertLessEqual(higher_counter_contact_gap(
                    row['crank'], row['shaft'], -1.8+4.2*row['carry']), 0)

    def test_measured_positive_component_endpoints_are_refused(self):
        data = json.loads((Path(__file__).parent/'docs/evidence/'
                           'counter-tens-component-coarse-2026-09-21.json').read_text())
        checked = 0
        for row in data['rows']:
            for boundary in row['boundaries']:
                side = 'right' if boundary['enters_contact'] else 'left'
                self.assertGreater(boundary[side+'_mm3'], 0)
                self.assertGreater(higher_counter_contact_gap(
                    boundary[side], row['shaft'], -1.8+4.2*row['carry']), 0,
                    (row['shaft'], row['carry'], row['component'], boundary))
                checked += 1
        self.assertGreater(checked, 200)

    def test_distinct_axial_supports_and_free_tooth_interval_remain(self):
        # Complete-print readings, not a guess based on one component.
        for crank, shaft, travel, blocked in (
                (204, 156, -1.8, True), (204, 156, 2.4, False),
                (94, 156, -1.8, False), (94, 156, 2.4, True),
                (205, 114, -1.8, False), (205, 114, 2.4, True),
                (198, 156, 2.4, True), (202, 156, 2.4, True),
                (206, 156, 2.4, True)):
            for revolution in (-2, -1, 0, 1, 2):
                self.assertEqual(higher_counter_contact_gap(
                    crank+360*revolution, shaft, travel) > 0, blocked,
                    (crank, shaft, travel, revolution))

    def test_source_input_and_carry_paths_are_admitted_at_every_flat(self):
        for flat in range(5):
            for carry in (0, 1):
                for count in (0, 1, 9):
                    for half_degree in range(721):
                        crank = half_degree/2
                        shaft = 114+72*flat+72*(
                            tooth_passage(crank, count, TURNS_INPUT_END+20)
                            +carry*tooth_passage(crank, 1, TURNS_CARRY_END+20))
                        self.assertLessEqual(higher_counter_contact_gap(
                            crank, shaft, -1.8+4.2*carry), 0,
                            (flat, carry, count, crank, shaft))


if __name__ == '__main__':
    unittest.main()
