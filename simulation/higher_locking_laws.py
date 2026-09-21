"""Measured tens contact restraint and an unadopted remaining-bank candidate.

Each angular region is intersected with its measured axial overlap. The
tens law is installed in OperatingCurta. Sharing it with the remaining bank
requires each station's independent complete-print and operating acceptance.
"""

from machinome.math import min, max, piecewise
from simulation.running_laws import phase
from simulation.locking_laws import CONTACT_STANDOFF, contact_gap
from simulation.higher_locking_profiles import LOWER_LOCK_SECTORS, CARRY_TOOTH_STRIPS
from simulation.running_parts import RESULT_RESTS


def higher_contact_gap(crank, shaft, travel):
    crank = phase(crank-110)+110
    shaft = phase(shaft+16)-16
    gap = min(contact_gap(crank-20, shaft+20), -travel-1.5)
    for start, end, points in LOWER_LOCK_SECTORS:
        opening = piecewise(shaft, [(p[0], p[1]) for p in points])
        closing = piecewise(shaft, [(p[0], p[2]) for p in points])
        contact = min(min(crank-closing+CONTACT_STANDOFF,
                          opening+360+CONTACT_STANDOFF-crank),
                      min(min(shaft-start, end-shaft), travel+3))
        gap = max(gap, contact)
    for start, end, points in CARRY_TOOTH_STRIPS:
        entering = piecewise(shaft, [(p[0], p[1]) for p in points])
        leaving = piecewise(shaft, [(p[0], p[2]) for p in points])
        contact = min(min(crank-entering+CONTACT_STANDOFF,
                          leaving+CONTACT_STANDOFF-crank),
                      min(min(shaft-start, end-shaft), travel+2.1))
        gap = max(gap, contact)
    return max(gap, -1)


def higher_closing_limit(own, rotating_part, shaft, travel):
    return rotating_part+higher_contact_gap(-rotating_part, shaft, travel)


def result_bank_closing_limit(own, rotating_part, *coordinates):
    """Intersect stations 3..11 in actual crank coordinates, not tens-local.

    Coordinates are nine ordered (shaft turn, upper travel) pairs. The
    production ones/tens bounds remain separate. This declaration candidate
    is not an assertion that the whole bank has passed geometry or operation.
    """
    if len(coordinates) != 18:
        raise ValueError('result bank requires shaft/travel pairs for stations 3..11')
    limit = rotating_part-1
    for station, (shaft, travel) in enumerate(zip(coordinates[::2], coordinates[1::2]), 3):
        shift = 20*(station-2)
        # Five source prints start raised at raw travel 0, not -4.2.
        # Their common physical carry stroke still spans 4.2 mm downward.
        normalized_travel = travel-RESULT_RESTS[station-2]-4.2
        candidate = higher_closing_limit(
            own+shift, rotating_part+shift, shaft+shift, normalized_travel)-shift
        limit = max(limit, candidate)
    return limit
