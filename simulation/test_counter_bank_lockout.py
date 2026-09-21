"""Every installed counter lockout must clear its five indexed positions."""

import unittest

from simulation.cycle import tooth_passage, TURNS_INPUT_END, TURNS_CARRY_END
from simulation.tools.counter_lockout_probe import station_reader


class CounterBankContactTest(unittest.TestCase):
    # Remains red on the installed fit until all candidate gates pass.
    trial = False
    stations = range(1, 7)

    def test_input_and_carry_passages_keep_the_complete_upper_print_clear(self):
        for station in self.stations:
            input_end = TURNS_INPUT_END+20*(station-1)
            carry_end = TURNS_CARRY_END+20*(station-1)
            for carry in (0, .5, 1):
                for count in (0, 1, 9):
                    angles = set(range(0, 361, 10))
                    for tooth in range(count):
                        angles.update(input_end-11.25*tooth-offset
                                      for offset in (0, 5.625, 11.25))
                    if station > 1:
                        angles.update(carry_end-offset for offset in (0, 5.625, 11.25))
                    for flat in range(5):
                        for crank in sorted(angles):
                            advance = tooth_passage(crank, count, input_end)
                            if station > 1 and carry >= .61:
                                advance += tooth_passage(crank, 1, carry_end)
                            shaft = 134-20*(station-1)+72*(flat+advance)
                            volume = station_reader(station, carry, shaft,
                                                    reference=crank, trial=self.trial)
                            for kernel in ('native', 'faceted'):
                                with self.subTest(station=station, carry=carry, count=count,
                                                  flat=flat, crank=crank, kernel=kernel):
                                    self.assertLessEqual(volume(crank, kernel), 0)
                        print(f'passage sampled: station={station}, carry={carry}, '
                              f'count={count}, flat={flat}, poses={len(angles)}', flush=True)

    def test_frozen_engaged_carry_gear_is_a_negative_control(self):
        for station in self.stations:
            if station == 1:
                continue
            end = TURNS_CARRY_END+20*(station-1)
            crank = end-11.25/2
            base = 134-20*(station-1)
            advanced = base+72*tooth_passage(crank, 1, end)
            frozen = station_reader(station, 1, base, reference=crank, trial=self.trial)
            moving = station_reader(station, 1, advanced, reference=crank, trial=self.trial)
            for kernel in ('native', 'faceted'):
                with self.subTest(station=station, kernel=kernel):
                    self.assertGreater(frozen(crank, kernel), 0)
                    self.assertLessEqual(moving(crank, kernel), 0)

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
