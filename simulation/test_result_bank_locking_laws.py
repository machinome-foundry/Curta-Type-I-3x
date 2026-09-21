"""Bank restraint coordinates must retain each source station's angular frame."""

import unittest

from simulation.higher_locking_laws import higher_closing_limit, result_bank_closing_limit
from simulation.running_parts import RESULT_RESTS


class ResultBankLockingLawTest(unittest.TestCase):
    def test_each_station_can_supply_the_tightest_bound_in_its_own_frame(self):
        for active in range(3, 12):
            shift = 20*(active-2)
            bell = -150-shift
            for travel in (-4.2, -2.1, 0):
                readings = []
                limits = []
                for station in range(3, 12):
                    offset = 20*(station-2)
                    shaft = (169.6 if station == active else -16)-offset
                    height = travel if station == active else -4.2
                    # The source upper origins differ axially: five stations
                    # have zero travel at rest, the others have -4.2 mm.
                    raw_travel = height+RESULT_RESTS[station-2]+4.2
                    readings.extend((shaft, raw_travel))
                    limits.append(higher_closing_limit(
                        bell+offset, bell+offset, shaft+offset, height)-offset)
                with self.subTest(station=active, travel=travel):
                    self.assertGreater(limits[active-3], bell)
                    self.assertEqual(max(limits), limits[active-3])
                    self.assertEqual(result_bank_closing_limit(bell, bell, *readings),
                                     limits[active-3])

    def test_combines_all_nine_complete_coordinate_pairs(self):
        for crank in (0, 140, 180, 300, 360, 860):
            readings = [(169.6-20*(station-2), RESULT_RESTS[station-2]+(station%3)*2.1)
                        for station in range(3, 12)]
            expected = max(higher_closing_limit(
                -crank+20*(station-2), -crank+20*(station-2),
                shaft+20*(station-2), travel-RESULT_RESTS[station-2]-4.2)-20*(station-2)
                for station, (shaft, travel) in enumerate(readings, 3))
            self.assertEqual(result_bank_closing_limit(
                -crank, -crank, *(value for pair in readings for value in pair)), expected)
        for length in (0, 2, 17, 19, 20):
            with self.subTest(length=length), self.assertRaises(ValueError):
                result_bank_closing_limit(0, 0, *([0]*length))


if __name__ == '__main__':
    unittest.main()
