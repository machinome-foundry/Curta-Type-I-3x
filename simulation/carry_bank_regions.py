"""Independent maximum frame-removal regions measured before fitting.

These are acceptance bounds, not production cutters. Coordinates come from
native source shoulders/contact sections. Seat edges allow at most .08 mm;
spring-contact bounds are rounded outward to .001 mm before that allowance.
Counter profiles and their different lowered Z band are recorded separately.
"""

import cadquery as cq
from simulation.test_frame_fits import permitted_regions as first_pair_regions

RESULT_ANGLES = tuple(-20*i for i in range(10))
COUNTER_ANGLES = (130, 110, 90, 70, 50)


def region(low, high):
    return cq.Solid.makeBox(*(b-a for a, b in zip(low, high)), cq.Vector(*low))


def counter_regions():
    upper = ((48.225, -7.89), (54.225, -7.89), (54.225, -6.42), (48.225, -6.42))
    lower = ((45.225, -11.354101615), (51.225, -7.89), (54.225, -7.89),
             (54.225, -6.42), (45.225, -6.42))
    for polygon, z in ((upper, -22.28), (lower, -15.98)):
        prism = cq.Workplane('XY', origin=(0, 0, z)).polyline(polygon).close().offset2D(.08).extrude(.76).val()
        yield prism.intersect(region((47, -12, z), (52.88, -6, z+.76)))
    # Separate lower spring legs; never the bridge between them. The
    # independently measured counter spread is wider than the result one.
    yield region((53.411, -11.413, -19.350), (54.283, -10.93, -15.82))
    yield region((60.321, -11.413, -19.350), (61.194, -10.93, -15.82))


def permitted_regions():
    first = list(first_pair_regions())[:4]
    for angle in RESULT_ANGLES:
        for shape in first:
            yield shape.rotate((0, 0, 0), (0, 0, 1), angle)
    for angle in COUNTER_ANGLES:
        for shape in counter_regions():
            yield shape.rotate((0, 0, 0), (0, 0, 1), angle)


def seat_edge_regions(angle, *, counter=False):
    for z in (-21.6, -15.9 if counter else -16.8):
        yield region((52.72, -7.97, z-.08), (52.88, -6.34, z+.08)).rotate(
            (0, 0, 0), (0, 0, 1), angle)


def forbidden_removal(original, fitted):
    removed = original.cut(fitted)
    for permitted in permitted_regions():
        if not removed.Vertices():
            break
        removed = removed.cut(permitted)
    return removed


def maximally_relieved(original):
    """A prospective preservation witness, never the production frame."""
    remaining = original
    for zone in permitted_regions():
        remaining = remaining.cut(zone)
    return remaining
