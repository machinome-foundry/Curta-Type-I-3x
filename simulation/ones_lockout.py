"""Complete source-backed bell/ones upper-stack contact bench.

Independent pose inputs are measurement instruments, not operating controls.
The operating machine continues to determine both angles through its actual
crank and tooth passages. No geometry correction is introduced here.
"""

from machinome.node import AssemblyNode
from machinome.motion.joints import Revolute
from machinome.simulation import Driver
from simulation.standard.printed import Part10221_1, TensBell1


class OnesLockoutBench(AssemblyNode):
    shaft_angle = Driver(default=4, unit='deg')
    crank_angle = Driver(default=180, unit='deg')
    ones = Part10221_1(turn=Revolute(axis=(0, 0, 1), at=(40.5, 0, 0)))
    bell = TensBell1(turn=Revolute(axis=(0, 0, 1)))
    shaft_angle.drives(ones.turn)
    crank_angle.drives(bell.turn, ratio=-1)
