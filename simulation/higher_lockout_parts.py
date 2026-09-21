"""T07 result-tens contact parts, adopted after the trial arithmetic gate.

The .16 mm outer-profile fit removes the source-indexed sliver while keeping
the keyed core and axial extent. Refined meshes resolve the actual contact
surfaces; tessellation changes no native material. This is a simulation fit,
not a manufacturing recommendation or adoption for the remaining bank.
"""

from machinome.motion.joints import Prismatic
from machinome.parameters import Length
from simulation.fit import FittedCarryLockout
from simulation.standard.channels import ResultTens
from simulation.standard.printed import Part10220_410003_1_419227, TensBell1


class ContactTensLockout(FittedCarryLockout):
    flank_relief = Length(.16, min=0)


class ContactTensUpper(Part10220_410003_1_419227):
    linear_deflection = .01
    angular_deflection = .1
    pentagonal_lockout = ContactTensLockout()


class ContactTens(ResultTens):
    p_10220_410003_1_419227 = ContactTensUpper(travel=Prismatic(axis=(0, 0, -1)))


class ContactBell(TensBell1):
    linear_deflection = .01
    angular_deflection = .1
