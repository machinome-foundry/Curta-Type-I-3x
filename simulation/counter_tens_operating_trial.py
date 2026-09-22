"""Isolated counter-tens T08/contact-law experiment, never the default root.

This challenges the existing candidate against an actual partial-input
withdrawal. Complete native profile, carried/action-order and browser gates
remain prerequisites for adoption; a passing raised-stack case is not those
gates. No other counter station is changed or claimed by this experiment.
"""

from machinome.motion.joints import Bound, Prismatic
from simulation.standard.printed import Part10220_410003_1_419081
from simulation.reverser_inputs import ReversingTens
from simulation.running_parts import TurnsShafts, RetainedTransmission
from simulation.running import OperatingCurta
from simulation.higher_counter_locking_laws import higher_counter_closing_limit
from simulation.tools.counter_lockout_probe import TrialCounterLockout


class TrialCounterTensUpper(Part10220_410003_1_419081):
    linear_deflection = .01
    angular_deflection = .1
    pentagonal_lockout = TrialCounterLockout()


class TrialCounterTens(ReversingTens):
    p_10220_410003_1_419081 = TrialCounterTensUpper(
        travel=Prismatic(axis=(0, 0, -1)))


class TrialTensShafts(TurnsShafts):
    tens = TrialCounterTens()


class TrialTensTransmission(RetainedTransmission):
    turns = TrialTensShafts()


class CounterTensOperatingTrial(OperatingCurta):
    transmission = TrialTensTransmission()
    OperatingCurta.main_drive.crank.turn.constrain(range=(Bound(
        higher_counter_closing_limit,
        reads=(OperatingCurta.carry_mechanism.tens_bell.turn,
               transmission.turns.tens.turn,
               transmission.turns.tens.p_10220_410003_1_419081.travel)), None))
