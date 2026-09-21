"""A measured tooth's finite support must not become a two-degree false jam.

The five birth/death brackets were measured independently on both kernels;
see higher-result-lockout-2026-09-21.md. Check the complete printed pair,
not just the ingredients from which the candidate table was compiled.
"""

import unittest

from simulation.higher_locking_laws import higher_contact_gap
from simulation.higher_lockout_trial import HigherLockoutFitBench
from simulation.tools.higher_locking_envelope import contact_reader


class HigherSupportAdmissionTest(unittest.TestCase):
    def test_free_side_of_every_measured_tooth_support_remains_admitted(self):
        # .02 degrees outside the measured supports, beyond the declared
        # .002-degree shaft guard. The crank is inside the tooth's old strip,
        # away from the other tooth and both locking discs.
        for flat in range(5):
            for shaft, crank in ((22.22+72*flat, 146.5),
                                 (49.13+72*flat, 159.5)):
                with self.subTest(flat=flat, shaft=shaft, crank=crank):
                    volume = contact_reader(1, shaft=shaft,
                                            node_type=HigherLockoutFitBench)
                    for kernel in ('faceted', 'native'):
                        self.assertLessEqual(volume(crank, kernel), 0, kernel)
                    self.assertLessEqual(higher_contact_gap(crank, shaft, 0), 0)

    def test_inside_every_measured_support_still_blocks_real_contact(self):
        for flat in range(5):
            for shaft, crank in ((22.27+72*flat, 146.5),
                                 (49.08+72*flat, 159.5)):
                with self.subTest(flat=flat, shaft=shaft, crank=crank):
                    volume = contact_reader(1, shaft=shaft,
                                            node_type=HigherLockoutFitBench)
                    for kernel in ('faceted', 'native'):
                        self.assertGreater(volume(crank, kernel), 0, kernel)
                    self.assertGreater(higher_contact_gap(crank, shaft, 0), 0)

    def test_admitted_near_support_poses_clear_across_axial_transitions(self):
        checked = 0
        for carry in (.28, .3, .5, .51, .64, .65):
            for flat in range(5):
                for phase in (22.22, 22.25, 49.08, 49.13):
                    shaft = phase+72*flat
                    volume = contact_reader(carry, shaft=shaft,
                                            node_type=HigherLockoutFitBench)
                    for crank in (145.7, 146.5, 147.2, 158.9, 159.5, 160.25):
                        if higher_contact_gap(crank, shaft, 4.2*carry-4.2) > 0:
                            continue
                        with self.subTest(carry=carry, shaft=shaft, crank=crank):
                            for kernel in ('faceted', 'native'):
                                self.assertLessEqual(volume(crank, kernel), 0, kernel)
                            checked += 1
        self.assertGreater(checked, 0, 'Admission check must not be vacuous')


if __name__ == '__main__':
    unittest.main()
