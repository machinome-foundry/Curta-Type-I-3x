"""Retained source-backed tens action orders with a movable real carry stack.

The carry instrument holds the actual stack at an independently declared
height; it does not purport to simulate the whole carry lever bank. The full
operating probe separately provides actual-latch acceptance. T07 geometry and
the refined diagnostic bell remain isolated from the operating model.
"""

from machinome.node import AssemblyNode
from machinome.motion.joints import Revolute, Prismatic
from machinome.motion.ports import Time
from machinome.simulation import Driver
from simulation.fit import INPUT_CLOCKING
from simulation.higher_lockout_trial import TrialTens, TrialContactBell
from simulation.prints import PrintedDrum
from simulation.result_engagement import result_pose


class RetainedTrialTens(TrialTens):
    def simulate(self):
        if self.turn.value is None:
            self.turn = INPUT_CLOCKING-20


class HigherResultActionOrder(AssemblyNode):
    time = Time.running()
    digit = Driver(default=3, unit='digit')
    crank_angle = Driver(default=0, unit='deg')
    crank_height = Driver(default=0, unit='mm')
    carry_latch = Driver(default=0, range=(0, 4.2), unit='mm')
    drum = PrintedDrum(turn=Revolute(axis=(0, 0, 1)),
                       lift=Prismatic(axis=(0, 0, 1)))
    tens = RetainedTrialTens()
    bell = TrialContactBell(turn=Revolute(axis=(0, 0, 1)))
    crank_angle.drives(drum.turn, ratio=-1)
    crank_angle.drives(bell.turn, ratio=-1)
    crank_height.drives(drum.lift)
    digit.drives(tens.setting)
    carry_latch.drives(tens.carry, ratio=1/4.2)
    (crank_angle & crank_height & digit & carry_latch).drives(
        tens.turn, law=result_pose(1))
