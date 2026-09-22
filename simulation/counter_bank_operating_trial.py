"""Independent complete-print counterpart of the adopted higher-counter bank.

Each upper remains its source-specific print. Its measured trial definitions
remain separate from the production parts for equivalence checks. The root now
inherits the adopted bank restraint; do not install the same Bound twice.
"""

from machinome.motion.joints import Prismatic
from machinome.parameters import Count, Length
from simulation.fit import FittedCarryLockout
from simulation.standard import printed
from simulation.reverser_inputs import (
    ReversingTens, ReversingHundreds, ReversingFourth, ReversingFifth, ReversingSixth)
from simulation.running import OperatingCurta
from simulation.running_parts import TurnsShafts, RetainedTransmission, CHANNEL_NAMES


COUNTER_TRIAL_STATIONS = (
    (ReversingTens, 'p_10220_410003_1_419081'),
    (ReversingHundreds, 'p_10220_410003_1_419070'),
    (ReversingFourth, 'p_10220_410003_1_419181'),
    (ReversingFifth, 'p_10220_410003_1_419107'),
    (ReversingSixth, 'p_10220_410003_1_419238'),
)


class BankTrialLockout(FittedCarryLockout):
    flank_relief = Length(.16, min=0)


def trial_counter_channel(station):
    if station not in range(2, 7):
        raise ValueError('Choose a higher counter station 2..6')
    channel, upper_name = COUNTER_TRIAL_STATIONS[station-2]
    upper = getattr(printed, 'Part'+upper_name[2:])

    class TrialUpper(upper):
        source_station = Count(station, min=station, max=station)
        linear_deflection = .01
        angular_deflection = .1
        pentagonal_lockout = BankTrialLockout()

    class TrialChannel(channel):
        source_station = Count(station, min=station, max=station)
        locals()[upper_name] = TrialUpper(travel=Prismatic(axis=(0, 0, -1)))

    return TrialChannel


class TrialCounterShafts(TurnsShafts):
    for _station in range(2, 7):
        locals()[CHANNEL_NAMES[_station-1]] = trial_counter_channel(_station)()
    del _station


class TrialCounterTransmission(RetainedTransmission):
    turns = TrialCounterShafts()


class CounterBankOperatingTrial(OperatingCurta):
    transmission = TrialCounterTransmission()
