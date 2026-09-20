"""Result input from the actual lower-drum bands, including unseated inputs.

All source tooth trains share their terminal tooth. Simultaneous axial
engagement takes their union (the longest train), never a fractional digit
or a half-lift mode switch. The source-bound geometry test guards this table.
"""

from machinome.math import max
from simulation.reverser_modes import overlaps

# Descending 1.5 mm source bands, beginning at Z=-67.8. Two source segments
# share -73.8; their union is the nine-tooth train, not ten teeth.
ROW_COUNTS = (10, 1, 1, 1, 9, 2, 2, 2, 8, 3, 3, 3, 7, 4, 4, 4, 6,
              5, 5, 5, 5, 5, 6, 4, 4, 4, 7, 3, 3, 3, 8, 2, 2, 2, 9, 1, 1)
ROWS = tuple((-67.8 - 1.5*index, count) for index, count in enumerate(ROW_COUNTS))
PINION_START = -64.92499975


def result_count(channel, digit, drum_lift):
    gears = (PINION_START, PINION_START + 6) if channel == 0 else (PINION_START,)
    count = 0
    for gear in gears:
        for row, teeth in ROWS:
            count = max(count, teeth*overlaps(gear-6*digit, row+drum_lift))
    return count
