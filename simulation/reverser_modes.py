"""Counter engagement from actual axial overlap, including unseated positions.

The first counter has three pinions; higher counters have one. The seven
upper-drum bands are source measurements, not a midpoint mode switch.
"""

from machinome.math import max

ROW_STARTS = (-54.2, -52.7, -51.2, -49.7, -48.2, -46.7, -45.2)
PINION_STARTS = (-49.35, -40.35, -44.85)
THICKNESS = 1.5


def overlaps(gear_bottom, row_bottom):
    return (gear_bottom < row_bottom + THICKNESS) * (gear_bottom + THICKNESS > row_bottom)


def any_overlap(values):
    result = 0
    for value in values:
        result = max(result, value)
    return result


def counter_count(channel, gear_height, drum_lift):
    gears = PINION_STARTS if channel == 0 else (-44.85,)
    nine = any_overlap(overlaps(bottom + gear_height, -49.7 + drum_lift) for bottom in gears)
    one = any_overlap(overlaps(bottom + gear_height, row + drum_lift)
                for bottom in gears for row in ROW_STARTS if row != -49.7)
    return 9*nine + one*(1-nine)
