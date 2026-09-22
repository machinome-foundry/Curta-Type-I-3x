"""Original T08 counter-ones parts as an independent acceptance fixture.

The operating root now supplies the verified fixed-height ones restraint.
This wrapper keeps the original candidate parts for geometric comparison,
without declaring the same crank bound twice. Higher counters stay separate.
"""

from machinome.motion.joints import Prismatic
from simulation.standard.printed import Part10222_1
from simulation.reverser_inputs import ReversingOnes
from simulation.running_parts import TurnsShafts, RetainedTransmission
from simulation.running import OperatingCurta
from simulation.tools.counter_lockout_probe import TrialCounterLockout


class TrialCounterOnesUpper(Part10222_1):
    linear_deflection = .01
    angular_deflection = .1
    pentagonal_lockout = TrialCounterLockout()


class TrialCounterOnes(ReversingOnes):
    p_10222_1 = TrialCounterOnesUpper(travel=Prismatic(axis=(0, 0, -1)))


class TrialTurnsShafts(TurnsShafts):
    ones = TrialCounterOnes()


class TrialCounterTransmission(RetainedTransmission):
    turns = TrialTurnsShafts()


class CounterOperatingTrial(OperatingCurta):
    transmission = TrialCounterTransmission()
