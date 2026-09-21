"""Every result station needs its own complete-print contact evidence."""

import unittest

from simulation.higher_lockout_trial import HigherLockoutFitBench
from simulation.tools.higher_locking_envelope import contact_reader
from simulation.tools.result_bank_lockout_probe import station_reader


class ResultBankContactTest(unittest.TestCase):
    # Deliberately red handoff fixture: .15 mm simulation fit has measured
    # indexed overlaps. Do not hide them or select the .16 mm trial until
    # its whole-bank material/engagement/admission checks justify adoption.
    trial = False

    def test_all_indexed_flats_clear_at_both_actual_carry_seats(self):
        for station in range(2, 12):
            for carry in (0, 1):
                for flat in range(5):
                    read = station_reader(station, carry, -16+72*flat, self.trial)
                    for kernel in ('native', 'faceted'):
                        with self.subTest(station=station, carry=carry, flat=flat, kernel=kernel):
                            self.assertLessEqual(read(180, kernel), 0)

    def test_both_locking_flanks_remain_present_at_every_station(self):
        for station in range(2, 12):
            for carry in (0, .25, .5, .75, 1):
                for flat in range(5):
                    for side in (-4, 4):
                        read = station_reader(station, carry, -16+72*flat+side, self.trial)
                        for kernel in ('native', 'faceted'):
                            with self.subTest(station=station, carry=carry, flat=flat,
                                              side=side, kernel=kernel):
                                self.assertGreater(read(180, kernel), 0)

    def test_generalized_tens_fixture_matches_the_original_trial(self):
        for carry, shaft in ((0, 169.6), (1, 169.6), (1, 22.22), (1, 49.08)):
            old = contact_reader(carry, shaft=shaft, node_type=HigherLockoutFitBench)
            new = station_reader(2, carry, shaft, trial=True)
            for crank in (145, 146.5, 159.5, 180):
                for kernel in ('native', 'faceted'):
                    with self.subTest(carry=carry, shaft=shaft, crank=crank, kernel=kernel):
                        self.assertEqual(new(crank, kernel), old(crank, kernel))


if __name__ == '__main__':
    unittest.main()
