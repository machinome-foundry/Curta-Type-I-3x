"""Candidate tens contact restraint; isolated from OperatingCurta.

Each angular region is intersected with its measured axial overlap. The
carry-tooth strips remain provisional until complete-print admission checks.
"""

from machinome.math import min, max, piecewise
from simulation.running_laws import phase
from simulation.locking_laws import CONTACT_STANDOFF, contact_gap
from simulation.higher_locking_profiles import LOWER_LOCK_SECTORS, CARRY_TOOTH_STRIPS


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
