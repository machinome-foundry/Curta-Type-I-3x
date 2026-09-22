"""Measured higher-counter uppers, separate from the operating trial.

Keep each source pivot, lower input, carry travel and complete upper print.
Only the existing pentagonal outline receives the independently checked
.16 mm flank fit; station identity distinguishes imported fusion artifacts.
"""

from machinome.motion.joints import Prismatic
from machinome.parameters import Count, Length
from simulation.fit import FittedCarryLockout
from simulation.reverser_inputs import (
    ReversingTens, ReversingHundreds, ReversingFourth, ReversingFifth, ReversingSixth)
from simulation.standard import printed


COUNTER_CONTACT_STATIONS = (
    (ReversingTens, 'p_10220_410003_1_419081'),
    (ReversingHundreds, 'p_10220_410003_1_419070'),
    (ReversingFourth, 'p_10220_410003_1_419181'),
    (ReversingFifth, 'p_10220_410003_1_419107'),
    (ReversingSixth, 'p_10220_410003_1_419238'),
)


class ContactCounterBankLockout(FittedCarryLockout):
    flank_relief = Length(.16, min=0)


def contact_counter_channel(station):
    if station not in range(2, 7):
        raise ValueError('Choose a higher counter station 2..6')
    channel, upper_name = COUNTER_CONTACT_STATIONS[station-2]
    upper = getattr(printed, 'Part'+upper_name[2:])

    class ContactUpper(upper):
        source_station = Count(station, min=station, max=station)
        linear_deflection = .01
        angular_deflection = .1
        pentagonal_lockout = ContactCounterBankLockout()

    class ContactChannel(channel):
        source_station = Count(station, min=station, max=station)
        locals()[upper_name] = ContactUpper(travel=Prismatic(axis=(0, 0, -1)))

    return ContactChannel
