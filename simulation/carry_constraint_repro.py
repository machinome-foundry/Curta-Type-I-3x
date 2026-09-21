"""Public-API reduction of the real carry failure under a crank restraint.

No CAD, fake travel cap, manually seeded run bank or alternative carry law.
The reduced bank keeps the source shaft, dial and self-reading lever laws;
its missing geometry is supplied by the separate full-tree reproduction.
"""

from functools import reduce
from operator import and_

from machinome.node import AssemblyNode
from machinome.parameters import Angle
from machinome.motion.joints import Bound, Revolute, Prismatic
from machinome.motion.ports import Time
from machinome.simulation import Driver
from simulation.running_laws import shaft_motion, lever_motion, dial_motion
from simulation.running_parts import RESULT_DIALS
from simulation.higher_locking_laws import higher_closing_limit
from simulation.locking_laws import closing_limit


class InitialWheel(AssemblyNode):
    zero = Angle(0)
    turn = Revolute(axis=(0, 0, 1))

    def simulate(self):
        if self.turn.value is None:
            self.turn = self.zero


class InitialLever(AssemblyNode):
    travel = Prismatic(axis=(0, 0, -1))

    def simulate(self):
        if self.travel.value is None:
            self.travel = -4.2


class CarryConstraintRepro(AssemblyNode):
    time = Time.running()
    crank_angle = Driver(default=0)
    digit = Driver(default=9)
    height = Driver(default=0)
    carriage_turn = Driver(default=0)
    carriage_lift = Driver(default=0)
    zero_setting = Driver(default=0)
    clearing = Driver(default=0)
    crank = InitialWheel()
    bell = InitialWheel()
    ones = InitialWheel(zero=4)
    tens = InitialWheel(zero=-16)
    shaft_2 = InitialWheel(zero=-36)
    shaft_3 = InitialWheel(zero=-56)
    shaft_4 = InitialWheel(zero=-76)
    shaft_5 = InitialWheel(zero=-96)
    shaft_6 = InitialWheel(zero=-116)
    shaft_7 = InitialWheel(zero=-136)
    shaft_8 = InitialWheel(zero=-156)
    shaft_9 = InitialWheel(zero=-176)
    shaft_10 = InitialWheel(zero=-196)
    lever = InitialLever()
    wheel_0 = InitialWheel(zero=RESULT_DIALS[0][1])
    wheel_1 = InitialWheel(zero=RESULT_DIALS[1][1])
    wheel_2 = InitialWheel(zero=RESULT_DIALS[2][1])
    wheel_3 = InitialWheel(zero=RESULT_DIALS[3][1])
    wheel_4 = InitialWheel(zero=RESULT_DIALS[4][1])
    wheel_5 = InitialWheel(zero=RESULT_DIALS[5][1])
    wheel_6 = InitialWheel(zero=RESULT_DIALS[6][1])
    wheel_7 = InitialWheel(zero=RESULT_DIALS[7][1])
    wheel_8 = InitialWheel(zero=RESULT_DIALS[8][1])
    wheel_9 = InitialWheel(zero=RESULT_DIALS[9][1])
    wheel_10 = InitialWheel(zero=RESULT_DIALS[10][1])
    crank_angle.drives(crank.turn, ratio=-1)
    crank_angle.drives(bell.turn, ratio=-1)
    # The existing source laws expect selector-shaft degrees, not digits.
    selector = InitialWheel()
    digit.drives(selector.turn, ratio=36)
    (crank.turn & height & selector.turn & carriage_lift).drives(
        ones.turn, law=shaft_motion(0))
    (crank.turn & height & zero_setting & lever.travel).drives(
        tens.turn, law=shaft_motion(1, lever_rest=-4.2))
    _shafts = (ones.turn, tens.turn, shaft_2.turn, shaft_3.turn, shaft_4.turn,
               shaft_5.turn, shaft_6.turn, shaft_7.turn, shaft_8.turn, shaft_9.turn,
               shaft_10.turn)
    for _index, _wheel in enumerate((wheel_0, wheel_1, wheel_2, wheel_3, wheel_4,
                                    wheel_5, wheel_6, wheel_7, wheel_8, wheel_9, wheel_10)):
        reduce(and_, (carriage_turn, carriage_lift, clearing, _wheel.turn,
                      *_shafts)).drives(_wheel.turn, law=dial_motion(_index))
    del _index, _wheel, _shafts
    reduce(and_, (crank.turn, carriage_turn, carriage_lift, lever.travel,
                  wheel_0.turn, wheel_1.turn, wheel_2.turn, wheel_3.turn,
                  wheel_4.turn, wheel_5.turn, wheel_6.turn, wheel_7.turn,
                  wheel_8.turn, wheel_9.turn, wheel_10.turn)).drives(
                      lever.travel, law=lever_motion(1, -4.2))


class ConstrainedCarryRepro(CarryConstraintRepro):
    CarryConstraintRepro.crank.turn.constrain(range=(Bound(
        higher_closing_limit, reads=(CarryConstraintRepro.bell.turn,
                                    CarryConstraintRepro.tens.turn,
                                    CarryConstraintRepro.lever.travel)), None))


class OnesAndTensCarryRepro(ConstrainedCarryRepro):
    """Also observe ones; this is not the complete operating dependency graph."""
    ConstrainedCarryRepro.crank.turn.constrain(range=(Bound(
        closing_limit, reads=(ConstrainedCarryRepro.bell.turn,
                              ConstrainedCarryRepro.ones.turn)), None))
