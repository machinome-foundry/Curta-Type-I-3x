"""Measured-contact experiment on the retained, source-backed T07 tens bench.

Not selected by the manifest; production geometry and controls are unchanged.
"""

from machinome.motion.joints import Bound
from simulation.higher_result_action_order import HigherResultActionOrder
from simulation.higher_locking_laws import higher_closing_limit


class HigherResultLocking(HigherResultActionOrder):
    HigherResultActionOrder.bell.turn.constrain(range=(Bound(
        higher_closing_limit,
        reads=(HigherResultActionOrder.drum.turn,
               HigherResultActionOrder.tens.turn,
               HigherResultActionOrder.tens.p_10220_410003_1_419227.travel)), None))
