"""Measured inner-flank fit, preserving the ones stack's fork-capture tips.

The .43 mm inner relief clears the reversed drum passage and leaves room for
the installed outward contact covers. Outside R6 the existing .36 mm profile
is unchanged. These are simulation fits, not upstream CAD modifications.
"""

import cadquery as cq

from machinome.motion.joints import Prismatic
from machinome.parameters import Length
from simulation.counter_lockout_parts import ContactCounterOnes
from simulation.fit import FittedCounterPinion
from simulation.reverser_inputs import OnesInput
from simulation.running_parts import RetainedTransmission, TurnsShafts


class ProtectedOnesPinion(FittedCounterPinion):
    inner_flank_relief = Length(.43, min=0)
    preserved_tip_radius = Length(6., min=0)

    def adjust(self, shape):
        outer = super().adjust(shape)
        relieved = FittedCounterPinion(flank_relief=self.inner_flank_relief).shape()
        box = shape.BoundingBox()
        inner = cq.Solid.makeCylinder(self.preserved_tip_radius, box.zlen+2,
                                      (0, 0, box.zmin-1))
        removed = outer.copy().cut(relieved.copy()).intersect(inner)
        return outer.cut(removed).clean()


class ProtectedOnesInput(OnesInput):
    transmission_gear_0_5_1 = ProtectedOnesPinion()
    transmission_gear_0_5_2 = ProtectedOnesPinion()
    transmission_gear_0_5_3 = ProtectedOnesPinion()


class ReverserContactOnes(ContactCounterOnes):
    # Retain ContactCounterOnes' independently verified upper lockout fit.
    p_10218_1 = ProtectedOnesInput(travel=Prismatic(axis=(0, 0, -1)))


class ReverserContactTurns(TurnsShafts):
    ones = ReverserContactOnes()


class ReverserContactTransmission(RetainedTransmission):
    turns = ReverserContactTurns()
