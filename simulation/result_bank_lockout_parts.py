"""Measured remaining-result upper prints, separated from diagnostic tools.

Each channel retains its own source pivot, lower shaft and carry placement.
The declared station distinguishes the imported fusion's artifact identity;
only its existing pentagonal locking outline receives the .16 mm fit.
"""

from machinome.node import Frame
from machinome.motion.joints import Prismatic
from machinome.parameters import Count
from simulation.higher_lockout_parts import ContactTensLockout
from simulation.standard import channels, printed


RESULT_CONTACT_STATIONS = (
    (channels.ResultHundreds, 'p_10220_410003_1_419086'),
    (channels.ResultDigit4, 'p_10220_410003_1_419234'),
    (channels.ResultDigit5, 'p_10220_410003_1_419093'),
    (channels.ResultDigit6, 'p_10220_410003_1_419064'),
    (channels.ResultDigit7, 'p_10220_410003_1_419039'),
    (channels.ResultDigit8, 'p_10220_410003_1_419074'),
    (channels.ResultDigit9, 'p_10220_410003_1_419139'),
    (channels.ResultDigit10, 'p_10220_410003_1_419117'),
    (channels.ResultDigit11, 'p_10220_410003_1_419114'),
)


def contact_result_upper(station):
    """Construct the fitted print independently of a channel attachment."""
    if station not in range(3, 12):
        raise ValueError('Choose a remaining result station 3..11')
    channel, upper_name = RESULT_CONTACT_STATIONS[station-3]
    upper = getattr(printed, 'Part'+upper_name[2:])

    class ContactUpper(upper):
        guide = Frame(at=channel.turn.at, z=(0, 0, -1))
        source_station = Count(station, min=station, max=station)
        linear_deflection = .01
        angular_deflection = .1
        pentagonal_lockout = ContactTensLockout()

    return ContactUpper


def contact_result_channel(station):
    """Select a verified source-specific upper print for station 3..11."""
    upper = contact_result_upper(station)
    channel, upper_name = RESULT_CONTACT_STATIONS[station-3]

    class ContactChannel(channel):
        source_station = Count(station, min=station, max=station)
        locals()[upper_name] = upper(travel=Prismatic(axis=(0, 0, -1)))

    return ContactChannel
