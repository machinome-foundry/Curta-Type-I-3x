"""Provisional fixed-height counter-ones restraint, not an operating adoption.

Counter measurements are independent of result-side envelopes. The explicit
free-side angular stand-off still requires complete-print admission checks;
higher counter stacks and axial motion are outside this law's scope.
"""

from machinome.math import min, max, piecewise, floor
from simulation.counter_locking_profiles import SECTORS


CONTACT_STANDOFF = .1


def counter_contact_gap(crank, shaft):
    shaft = shaft-360*floor((shaft-134)/360)
    crank = crank-360*floor((crank-120)/360)
    gaps = []
    for start, end, points in SECTORS:
        opening = piecewise(shaft, [(p[0], p[1]) for p in points])
        closing = piecewise(shaft, [(p[0], p[2]) for p in points])
        gaps.append(min(min(crank-closing+CONTACT_STANDOFF,
                            opening+360+CONTACT_STANDOFF-crank),
                        min(shaft-start, end-shaft)))
    gap = gaps[0]
    for other in gaps[1:]:
        gap = max(gap, other)
    return gap


def counter_closing_limit(own, rotating_part, shaft):
    shaft = shaft-360*floor((shaft-134)/360)
    crank = -rotating_part
    free = rotating_part-1
    limit = free
    for start, end, points in SECTORS:
        opening = piecewise(shaft, [(p[0], p[1]) for p in points])+CONTACT_STANDOFF
        closing = piecewise(shaft, [(p[0], p[2]) for p in points])-CONTACT_STANDOFF
        revolution = floor((crank-opening)/360)
        active = (shaft >= start)*(shaft <= end)
        limit += active*(-360*revolution-closing-free)
    return limit
