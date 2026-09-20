"""Source result rows at partial selector and crank-lift positions.

Pose diagnostic: geometry checks precede any new operating admission limits.
"""

from machinome.node import AssemblyNode
from machinome.motion.joints import Revolute, Prismatic
from machinome.simulation import Driver
from simulation.prints import PrintedDrum
from simulation.standard.channels import ResultOnes, ResultTens
from simulation.running_laws import shaft_motion


def result_pose(channel):
    def law(sources, target):
        advance = shaft_motion(channel)(sources, target)
        return lambda crank, height, digit, latch: advance(-crank, height, 36*digit, latch)
    return law


class ResultEngagement(AssemblyNode):
    digit = Driver(default=3, unit='digit')
    crank_angle = Driver(default=0, unit='deg')
    crank_height = Driver(default=4.5, unit='mm')
    carry_latch = Driver(default=0, unit='mm')
    drum = PrintedDrum(turn=Revolute(axis=(0, 0, 1)),
                       lift=Prismatic(axis=(0, 0, 1)))
    ones = ResultOnes()
    tens = ResultTens()
    crank_angle.drives(drum.turn, ratio=-1)
    crank_height.drives(drum.lift)
    digit.drives(ones.setting)
    digit.drives(tens.setting)
    digit.drives(ones.carry, ratio=0)
    digit.drives(tens.carry, ratio=0)
    (crank_angle & crank_height & digit & carry_latch).drives(ones.turn, law=result_pose(0))
    (crank_angle & crank_height & digit & carry_latch).drives(tens.turn, law=result_pose(1))
