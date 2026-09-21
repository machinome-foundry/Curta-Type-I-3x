"""Historical T07 pose bench and aliases for the adopted tens contact parts.

The unfitted HigherLockoutBench remains an independent source-fit comparator.
Only result tens is adopted; generalized bank candidates remain isolated.
"""

from machinome.motion.joints import Revolute
from simulation.higher_lockout import HigherLockoutBench
from simulation.higher_lockout_parts import (
    ContactTensLockout as TrialTensLockout,
    ContactTensUpper as TrialTensUpper,
    ContactTens as TrialTens,
    ContactBell as TrialContactBell,
)


class HigherLockoutFitBench(HigherLockoutBench):
    tens = TrialTens()
    bell = TrialContactBell(turn=Revolute(axis=(0, 0, 1)))
