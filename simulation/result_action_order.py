"""Retained two-channel diagnostic for deliberately wrong-order requests.

No new stops are declared here: source contact must identify them first.
"""

from machinome.motion.ports import Time
from machinome.motion.joints import Revolute
from simulation.result_engagement import ResultEngagement
from simulation.standard.channels import ResultOnes, ResultTens
from simulation.fit import INPUT_CLOCKING
from simulation.standard.printed import TensBell1


class RetainedResultOnes(ResultOnes):
    def simulate(self):
        if self.turn.value is None:
            self.turn = INPUT_CLOCKING


class RetainedResultTens(ResultTens):
    def simulate(self):
        if self.turn.value is None:
            self.turn = INPUT_CLOCKING-20


class ResultActionOrder(ResultEngagement):
    time = Time.running()
    ones = RetainedResultOnes()
    tens = RetainedResultTens()
    bell = TensBell1(turn=Revolute(axis=(0, 0, 1)))
    ResultEngagement.crank_angle.drives(bell.turn, ratio=-1)
