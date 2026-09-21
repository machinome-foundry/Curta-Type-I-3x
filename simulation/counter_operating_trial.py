"""Full-machine T08 counter-ones experiment; not the manifest's default root.

Only the fixed-height counter-ones upper fit and its crank restraint are
added. The production result-ones/tens/pawl constraints and every actual input
remain inherited. Higher counter stacks are not covered by this experiment.
"""

from machinome.motion.joints import Bound, Prismatic
from simulation.standard.printed import Part10222_1
from simulation.reverser_inputs import ReversingOnes
from simulation.running_parts import TurnsShafts, RetainedTransmission
from simulation.running import OperatingCurta
from simulation.counter_locking_laws import counter_closing_limit
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
    OperatingCurta.main_drive.crank.turn.constrain(range=(Bound(
        counter_closing_limit,
        reads=(OperatingCurta.carry_mechanism.tens_bell.turn,
               transmission.turns.ones.turn)), None))
