"""T07: isolated tens outer-skin trial; not selected by OperatingCurta.

The normal shaft-200 indexed pose leaves a native-only sliver in the existing
.15 mm profile fit. Keep the complete source upper stack, shaft datum and
axial travel while testing the same bounded additional skin as ones F18.
Upstream CAD and the production tens stack remain unchanged.
"""

from machinome.motion.joints import Prismatic, Revolute
from machinome.parameters import Length
from simulation.fit import FittedCarryLockout
from simulation.higher_lockout import HigherLockoutBench
from simulation.standard.channels import ResultTens
from simulation.standard.printed import Part10220_410003_1_419227, TensBell1


class TrialTensLockout(FittedCarryLockout):
    flank_relief = Length(.16, min=0)


class TrialTensUpper(Part10220_410003_1_419227):
    # At intermediate carry heights the coarse upper-print mesh extends
    # into an opening that is clear natively. Resolve its profile as well
    # as the bell; neither tessellation setting changes native material.
    linear_deflection = .01
    angular_deflection = .1
    pentagonal_lockout = TrialTensLockout()


class TrialTens(ResultTens):
    p_10220_410003_1_419227 = TrialTensUpper(travel=Prismatic(axis=(0, 0, -1)))


class TrialContactBell(TensBell1):
    # Existing coarse circular facets miss native contact on the lower-angle
    # locking flank even before T07. Refine the mesh, not the native bell.
    linear_deflection = .01
    angular_deflection = .1


class HigherLockoutFitBench(HigherLockoutBench):
    tens = TrialTens()
    bell = TrialContactBell(turn=Revolute(axis=(0, 0, 1)))
