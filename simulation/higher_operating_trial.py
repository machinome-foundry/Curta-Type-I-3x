"""Full-tree T07 tens experiment; the manifest still selects OperatingCurta.

Only the tens outer fit and bell mesh are changed here. All physical inputs,
carry levers, initial shaft seating and original restraints are inherited.
"""

from machinome.motion.joints import Bound, Revolute
from simulation.higher_lockout_trial import TrialTens, TrialContactBell
from simulation.higher_locking_laws import higher_closing_limit
from simulation.mechanism import TensBellAssembly
from simulation.running_parts import ResultShafts, RetainedTransmission, RetainedCarries
from simulation.running import OperatingCurta


class TrialResultShafts(ResultShafts):
    tens = TrialTens()


class TrialTransmission(RetainedTransmission):
    result = TrialResultShafts()


class TrialBellAssembly(TensBellAssembly):
    tens_bell_1 = TrialContactBell()


class TrialCarries(RetainedCarries):
    tens_bell = TrialBellAssembly(turn=Revolute(axis=(0, 0, 1)))


class HigherOperatingTrial(OperatingCurta):
    transmission = TrialTransmission()
    carry_mechanism = TrialCarries()
    OperatingCurta.main_drive.crank.turn.constrain(range=(Bound(
        higher_closing_limit,
        reads=(carry_mechanism.tens_bell.turn, transmission.result.tens.turn,
               transmission.result.tens.p_10220_410003_1_419227.travel)), None))
