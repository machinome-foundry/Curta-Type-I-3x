"""Independent shoulder-removal allowance, not a production cutter.

Coordinates are the first counter's installed rest frame rotated -130 degrees
about world Z. The earlier fork-fit helper additionally lowers that frame by
14.7 mm; undo only that documented normalization here.
"""

import cadquery as cq
from simulation.carry_fits import in_first_result_station


def region(low, high):
    return cq.Solid.makeBox(*(b-a for a, b in zip(low, high)), cq.Vector(*low))


def in_counter_station(shape, *, inverse=False):
    if inverse:
        return in_first_result_station(shape.translate((0, 0, -14.7)),
                                       counter=True, inverse=True)
    return in_first_result_station(shape, counter=True).translate((0, 0, 14.7))


def maximum_shoulder_removal():
    return in_counter_station(region((60.25, -7.95, -12.95),
                                     (61.80, -6.35, -12.55)), inverse=True)


def maximum_relieved(original):
    """Prospective preservation witness; never installed by the model."""
    return original.cut(maximum_shoulder_removal())
