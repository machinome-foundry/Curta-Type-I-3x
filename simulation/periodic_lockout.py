"""Narrow source-backed reproduction of long-request stop location.

Not an operating law. Only the prepared ones phase 189.6 is certified here;
125.22 degrees is on the measured free side of its closing contact. Compare
the periodic physical surface to a fixed local surface on identical parts.
"""

from machinome.math import floor
from machinome.motion.joints import Bound
from simulation.result_action_order import ResultActionOrder


def periodic_surface(own, drum, shaft):
    active = (shaft >= 189.599)*(shaft <= 189.601)
    closing = -360*floor((-drum-10.8)/360)-125.22
    return active*closing+(1-active)*(drum-1)


def fixed_surface(own, shaft):
    active = (shaft >= 189.599)*(shaft <= 189.601)
    # Historical local diagnostic fallback, intentionally not a general law.
    return active*(-125.22)+(1-active)*(own-360)


class PeriodicLockoutBench(ResultActionOrder):
    ResultActionOrder.bell.turn.constrain(range=(Bound(
        periodic_surface,
        reads=(ResultActionOrder.drum.turn, ResultActionOrder.ones.turn)), None))


class FixedLockoutBench(ResultActionOrder):
    ResultActionOrder.bell.turn.constrain(range=(Bound(
        fixed_surface, reads=(ResultActionOrder.ones.turn,)), None))
