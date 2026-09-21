"""Source-backed tens contact instruments, not operating inputs or restraints.

The complete source channel retains its own shaft datum, fitted print and
assembly translation. Carry moves the actual upper stack through its declared
4.2 mm stroke. This bench measures both seats before any operating law is
proposed; it does not reuse the fixed-height ones contact table.
"""

from machinome.node import AssemblyNode
from machinome.motion.joints import Revolute
from machinome.simulation import Driver
from simulation.standard.channels import ResultTens
from simulation.standard.printed import TensBell1


class HigherLockoutBench(AssemblyNode):
    shaft_angle = Driver(default=169.6, unit='deg')
    crank_angle = Driver(default=140, unit='deg')
    carry_position = Driver(default=0, range=(0, 1))
    tens = ResultTens()
    bell = TensBell1(turn=Revolute(axis=(0, 0, 1)))
    shaft_angle.drives(tens.turn)
    shaft_angle.drives(tens.setting, ratio=0)
    carry_position.drives(tens.carry)
    crank_angle.drives(bell.turn, ratio=-1)
