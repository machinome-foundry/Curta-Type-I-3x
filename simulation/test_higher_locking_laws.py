"""The measured candidate must admit every ordinary source tooth passage."""

import unittest

from simulation.cycle import tooth_passage, RESULT_INPUT_END, RESULT_CARRY_END
from simulation.higher_locking_laws import higher_contact_gap


class HigherLockingLawTest(unittest.TestCase):
    def test_all_flats_counts_and_carry_seats_admit_the_source_trajectory(self):
        for flat in range(5):
            for carry in (0, 1):
                for count in range(11):
                    for half_degree in range(721):
                        crank = half_degree/2
                        shaft = -16+72*flat+72*(
                            tooth_passage(crank, count, RESULT_INPUT_END+20)
                            +carry*tooth_passage(crank, 1, RESULT_CARRY_END+20))
                        self.assertLessEqual(higher_contact_gap(crank, shaft, 4.2*carry-4.2),
                                             0, (flat, carry, count, crank, shaft))


if __name__ == '__main__':
    unittest.main()
