"""Counter-profile arithmetic is separate from its geometric admission proof."""

import unittest
import json
from pathlib import Path

from simulation.counter_locking_laws import counter_contact_gap, counter_closing_limit
from simulation.cycle import tooth_passage, TURNS_INPUT_END


class CounterLockingLawTest(unittest.TestCase):
    def test_measured_between_knot_collisions_are_refused(self):
        evidence = json.loads((Path(__file__).parent / 'docs/evidence/'
            'counter-ones-coarse-profile-rejection-2026-09-21.json').read_text())
        for kernel, records in evidence['kernels'].items():
            for row in records:
                if not row.get('failure'):
                    continue
                self.assertGreater(row['common_mm3'], 0)
                shaft, crank = row['shaft'], row['crank']
                with self.subTest(kernel=kernel, shaft=shaft, crank=crank):
                    self.assertGreater(counter_contact_gap(crank, shaft), 0)
                    self.assertGreater(counter_closing_limit(-crank, -crank, shaft), -crank)

    def test_measured_withdrawal_is_free_then_blocked_on_every_revolution(self):
        for revolution in (-2, -1, 0, 1, 2):
            shift = 360*revolution
            self.assertLessEqual(counter_contact_gap(170+shift, 167.6), 0)
            self.assertGreater(counter_contact_gap(180+shift, 167.6), 0)
            stop = -counter_closing_limit(-170-shift, -170-shift, 167.6)
            self.assertGreater(stop, 174.7+shift)
            self.assertLess(stop, 174.9+shift)

    def test_all_indexed_flats_are_free_through_a_revolution(self):
        for flat in range(5):
            shaft = 134+72*flat
            for crank in range(361):
                self.assertLessEqual(counter_contact_gap(crank, shaft), 0)
                self.assertLess(counter_closing_limit(-crank, -crank, shaft), -crank)

    def test_source_input_passages_are_admitted_from_every_flat(self):
        for count in (0, 1, 9):
            for flat in range(5):
                for step in range(1441):
                    crank = step/4
                    shaft = 134+72*(flat+tooth_passage(crank, count, TURNS_INPUT_END))
                    with self.subTest(count=count, flat=flat, crank=crank):
                        self.assertLessEqual(counter_contact_gap(crank, shaft), 0)
                        self.assertLessEqual(counter_closing_limit(-crank, -crank, shaft), -crank)


if __name__ == '__main__':
    unittest.main()
