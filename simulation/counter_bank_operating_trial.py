"""Unadopted complete higher-counter trial; never the default operating root.

Each upper remains its source-specific print. Profile evidence alone is not
adoption: actual withdrawal, carry, replay, arithmetic and browser checks are
still required. No user input, source gear or retained coordinate is replaced.
"""

from machinome.motion.joints import Bound, Prismatic
from machinome.parameters import Count, Length
from simulation.fit import FittedCarryLockout
from simulation.standard import printed
from simulation.reverser_inputs import (
    ReversingTens, ReversingHundreds, ReversingFourth, ReversingFifth, ReversingSixth)
from simulation.running import OperatingCurta
from simulation.running_parts import TurnsShafts, RetainedTransmission, CHANNEL_NAMES
from simulation.higher_counter_locking_laws import counter_bank_closing_limit


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
    _readings = []
    for _station, (_, _upper_name) in enumerate(COUNTER_TRIAL_STATIONS, 2):
        _shaft = getattr(transmission.turns, CHANNEL_NAMES[_station-1])
        _readings.extend((_shaft.turn, getattr(_shaft, _upper_name).travel))
    OperatingCurta.main_drive.crank.turn.constrain(range=(Bound(
        counter_bank_closing_limit,
        reads=(OperatingCurta.carry_mechanism.tens_bell.turn, *_readings)), None))
    del _station, _upper_name, _shaft, _readings
