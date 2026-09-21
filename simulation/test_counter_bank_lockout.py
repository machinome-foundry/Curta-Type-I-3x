"""Every installed counter lockout must clear its five indexed positions."""

import unittest

from simulation.tools.counter_lockout_probe import station_reader


class CounterBankContactTest(unittest.TestCase):
    # Remains red on the installed fit until all candidate gates pass.
    trial = False

    def test_both_locking_flanks_remain_at_every_height_and_indexed_flat(self):
        for station in range(1, 7):
            for carry in (0, .25, .5, .75, 1):
                for flat in range(5):
                    for side in (-4, 4):
                        shaft = 134-20*(station-1)+72*flat+side
                        volume = station_reader(station, carry, shaft, trial=self.trial)
                        for kernel in ('native', 'faceted'):
                            with self.subTest(station=station, carry=carry, flat=flat,
                                              side=side, kernel=kernel):
                                self.assertGreater(volume(0, kernel), 0)

    def test_indexed_flats_clear_at_the_parked_crank_and_both_carry_seats(self):
        for station in range(1, 7):
            for carry in (0, 1):
                for flat in range(5):
                    shaft = 134-20*(station-1)+72*flat
                    volume = station_reader(station, carry, shaft, trial=self.trial)
                    for kernel in ('native', 'faceted'):
                        with self.subTest(station=station, carry=carry,
                                          flat=flat, kernel=kernel):
                            self.assertLessEqual(volume(0, kernel), 0)


if __name__ == '__main__':
    unittest.main()
