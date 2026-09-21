"""CAD-free diagnostic retaining the whole result bank's carry dependencies.

Use the production shaft, dial and lever laws verbatim. The previous reduction
drives only ones/tens and one carry lever; this one also drives the other nine
shafts and carry levers. It does not replace any operating mechanism.
"""

from functools import reduce
from operator import and_

from machinome.parameters import Length
from machinome.motion.joints import Bound
from simulation.carry_constraint_repro import CarryConstraintRepro, InitialLever
from simulation.running_parts import RESULT_RESTS
from simulation.running_laws import shaft_motion, lever_motion
from simulation.locking_laws import closing_limit
from simulation.higher_locking_laws import higher_closing_limit


class SourceRestLever(InitialLever):
    rest = Length(-4.2)

    def simulate(self):
        if self.travel.value is None:
            self.travel = self.rest


class ResultCarryGraphRepro(CarryConstraintRepro):
    for _index in range(2, 11):
        _rest = RESULT_RESTS[_index-1]
        _lever = SourceRestLever(rest=_rest)
        locals()[f'lever_{_index}'] = _lever
        (CarryConstraintRepro.crank.turn & CarryConstraintRepro.height
         & CarryConstraintRepro.zero_setting & _lever.travel).drives(
             getattr(CarryConstraintRepro, f'shaft_{_index}').turn,
             law=shaft_motion(_index, lever_rest=_rest))
        reduce(and_, (CarryConstraintRepro.crank.turn,
                      CarryConstraintRepro.carriage_turn,
                      CarryConstraintRepro.carriage_lift, _lever.travel,
                      *(getattr(CarryConstraintRepro, f'wheel_{i}').turn
                        for i in range(11)))).drives(
                            _lever.travel, law=lever_motion(_index, _rest))
    del _index, _rest, _lever


class ConstrainedResultCarryGraphRepro(ResultCarryGraphRepro):
    ResultCarryGraphRepro.crank.turn.constrain(range=(Bound(
        closing_limit, reads=(ResultCarryGraphRepro.bell.turn,
                              ResultCarryGraphRepro.ones.turn)), None))
    ResultCarryGraphRepro.crank.turn.constrain(range=(Bound(
        higher_closing_limit, reads=(ResultCarryGraphRepro.bell.turn,
                                    ResultCarryGraphRepro.tens.turn,
                                    ResultCarryGraphRepro.lever.travel)), None))
