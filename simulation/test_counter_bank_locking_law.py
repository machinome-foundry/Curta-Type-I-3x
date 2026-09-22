"""A bank bound must retain every independently measured station's frame."""

import unittest

from simulation import higher_counter_locking_laws as laws


class CounterBankLockingLawTest(unittest.TestCase):
    def test_intersects_all_five_limits_in_actual_crank_coordinates(self):
        for crank in (0, 94, 194.8, 214.8, 254.8, 274.8, 920):
            for travel in (-1.8, -.601, -.6000000715255738, .3, 2.4):
                readings = tuple(value for station in range(2, 7)
                                 for value in (147.6-20*(station-2), travel))
                expected = max(laws.higher_counter_closing_limit(
                    -crank+20*(station-2), -crank+20*(station-2),
                    readings[2*(station-2)]+20*(station-2), travel)-20*(station-2)
                    for station in range(2, 7))
                self.assertEqual(laws.counter_bank_closing_limit(
                    -crank, -crank, *readings), expected)

    def test_requires_one_shaft_travel_pair_per_higher_counter(self):
        for count in (0, 2, 8, 9, 11, 12):
            with self.subTest(count=count), self.assertRaises(ValueError):
                laws.counter_bank_closing_limit(0, 0, *([0]*count))
