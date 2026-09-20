"""Experimental ones closing restraint on the source-backed two-shaft bench.

Not selected by the project manifest. Both angles belong to real parts: the
bell and the source drum co-rotate, and the retained shaft determines which
locking flank is presented. There is no fake joint or one-turn travel cap.
"""

from machinome.math import min, max, piecewise, floor
from machinome.motion.joints import Bound
from simulation.running_laws import phase
from simulation.locking_profiles import SECTORS
from simulation.result_action_order import ResultActionOrder

# Free-side angular stand-off, to be checked against complete native solids
# and published meshes BETWEEN profile knots before operating adoption.
CONTACT_STANDOFF = .1


def contact_gap(crank, shaft):
    """Positive only inside the measured forbidden angle region.

    Put the crank's cyclic cut in the common open window at 90 degrees,
    never in the closed circular land. The five source flats are separate
    measured sectors rather than an assumed regular pentagon.
    """
    crank = phase(crank-90)+90
    shaft = phase(shaft-4)+4
    gaps = []
    for start, end, points in SECTORS:
        opening = piecewise(shaft, [(p[0], p[1]) for p in points])
        closing = piecewise(shaft, [(p[0], p[2]) for p in points])
        gap = min(crank-closing+CONTACT_STANDOFF,
                  opening+360+CONTACT_STANDOFF-crank)
        gaps.append(min(gap, min(shaft-start, end-shaft)))
    gap = gaps[0]
    for other in gaps[1:]:
        gap = max(gap, other)
    return gap


def closing_limit(own, rotating_part, shaft):
    # State the next actual closing surface directly. The previous signed-gap
    # formulation (rotating_part + contact_gap) triggered a run invariant on
    # a 120 -> 840 request, despite stopping the short request correctly.
    shaft = phase(shaft-4)+4
    angle = -rotating_part
    free = rotating_part-1
    limit = free
    for start, end, points in SECTORS:
        opening = piecewise(shaft, [(p[0], p[1]) for p in points])+CONTACT_STANDOFF
        closing = piecewise(shaft, [(p[0], p[2]) for p in points])-CONTACT_STANDOFF
        cycle = floor((angle-opening)/360)
        active = (shaft >= start)*(shaft <= end)
        limit += active*(-360*cycle-closing-free)
    # The inactive branch follows the co-rotating real joint, so its one-degree
    # algebraic slack is not a one-degree (or one-turn) travel limit.
    return limit


class ResultLocking(ResultActionOrder):
    ResultActionOrder.bell.turn.constrain(range=(Bound(
        closing_limit,
        reads=(ResultActionOrder.drum.turn, ResultActionOrder.ones.turn)), None))
