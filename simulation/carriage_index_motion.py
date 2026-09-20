"""Measured carriage key envelope, with named free-side contact clearances.

Native bisection: .187988..188477 degrees of seated play; outside that
vertical flank the existing chamfer clears at 5.2006..5.9501 mm lift.
The .18 degree stop retains play and a small flank gap. The axial envelope
uses a .05 mm gap above the measured chamfer, capped by the 6 mm lift where
the complete bottom face is .05 mm above the fixed keys. No input is prepared.
See tools/carriage_index.py --envelope and the independent contact contracts.
"""

from machinome.math import abs, floor, max, piecewise
from simulation.clearing_seat_fit import FREE_PIN_DROP

INDEX_PLAY = .18
INDEX_LIFT = (
    (.18, 5.2506), (.189, 5.2506), (.19, 5.2515), (.2, 5.2609),
    (.25, 5.3068), (.3, 5.3532), (.4, 5.4456), (.5, 5.5385),
    (.6, 5.6315), (.7, 5.7247), (.8, 5.8181), (.9, 5.9116),
    (1, 6), (10, 6),
)


def indexing_lift(turn):
    slot = 20 * floor((turn + 10) / 20)
    distance = abs(turn - slot)
    # Compare the original coordinate to the same represented stops returned
    # by the bound, rather than reconstructing the play with modulo rounding.
    outside = max(turn < slot - INDEX_PLAY, turn > slot + INDEX_PLAY)
    return outside * piecewise(distance, INDEX_LIFT)


def minimum_carriage_lift(own, pin_drop, turn):
    return max(max(0, pin_drop - FREE_PIN_DROP), indexing_lift(turn))
