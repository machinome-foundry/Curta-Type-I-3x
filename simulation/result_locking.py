"""Experimental ones closing restraint on the source-backed two-shaft bench.

Not selected by the project manifest. Both angles belong to real parts: the
bell and the source drum co-rotate, and the retained shaft determines which
locking flank is presented. There is no fake joint or one-turn travel cap.
"""

from machinome.motion.joints import Bound
from simulation.locking_laws import CONTACT_STANDOFF, contact_gap, closing_limit
from simulation.result_action_order import ResultActionOrder


class ResultLocking(ResultActionOrder):
    ResultActionOrder.bell.turn.constrain(range=(Bound(
        closing_limit,
        reads=(ResultActionOrder.drum.turn, ResultActionOrder.ones.turn)), None))
