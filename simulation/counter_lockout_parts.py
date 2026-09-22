"""Admitted T08 counter-ones fit, separated from diagnostic tools.

Only the fixed-height ones channel is selected here. The .16 mm outer skin
and refined complete-print mesh match its measured candidate; the remaining
counter stations require their own admission and operating checks.
"""

from machinome.motion.joints import Prismatic
from machinome.parameters import Length

from simulation.fit import FittedCarryLockout
from simulation.reverser_inputs import ReversingOnes
from simulation.standard.printed import Part10222_1


class ContactCounterLockout(FittedCarryLockout):
    flank_relief = Length(.16, min=0)


class ContactCounterOnesUpper(Part10222_1):
    linear_deflection = .01
    angular_deflection = .1
    pentagonal_lockout = ContactCounterLockout()


class ContactCounterOnes(ReversingOnes):
    p_10222_1 = ContactCounterOnesUpper(travel=Prismatic(axis=(0, 0, -1)))
