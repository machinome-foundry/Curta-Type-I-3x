"""Isolated inner-flank fit candidate; not adopted in the operating root.

The retained reversed-counter path intersects the nine-tooth drum at crank
82.432377 degrees with the existing .36 mm fit. A native pair survey still
finds contact at .41 mm but none at .415 mm over 80--88 degrees at .1 degree
spacing. That sampling does not establish whole-stroke clearance or capture.
Uniform .415 relief loses axial fork capture at crank 75. That capture uses
the outer tips at radii 6.1657--6.2262, whereas the crank-83 drum collision
is at radii 4.5083--4.6195. Retain the existing .36 profile outside R6 and
test .415 relief only inside that radius. No fork or tooth phase changes.
This fixture keeps every current operating part except the three ones teeth.
"""

import cadquery as cq
from machinome.parameters import Length
from machinome.motion.joints import Prismatic
from simulation.fit import FittedCounterPinion
from simulation.reverser_inputs import OnesInput, ReversingOnes
from simulation.counter_lockout_parts import ContactCounterOnes
from simulation.reverser_mapped import MappedReverserTrial
from simulation.running_parts import TurnsShafts, RetainedTransmission
from simulation.running import OperatingCurta


class TrialOnesPinion(FittedCounterPinion):
    inner_flank_relief = Length(.415, min=0)
    preserved_tip_radius = Length(6., min=0)

    def adjust(self, shape):
        outer = super().adjust(shape)
        relieved = FittedCounterPinion(flank_relief=self.inner_flank_relief).shape()
        box = shape.BoundingBox()
        inner = cq.Solid.makeCylinder(self.preserved_tip_radius, box.zlen+2,
                                      (0, 0, box.zmin-1))
        # Remove only the additional inner-flank skin. Keeping the outer
        # source-derived material avoids shrinking the fork-capture tips.
        removed = outer.copy().cut(relieved.copy()).intersect(inner)
        return outer.cut(removed).clean()


class TrialOnesInput(OnesInput):
    transmission_gear_0_5_1 = TrialOnesPinion()
    transmission_gear_0_5_2 = TrialOnesPinion()
    transmission_gear_0_5_3 = TrialOnesPinion()


class TrialOnes(ReversingOnes):
    p_10218_1 = TrialOnesInput(travel=Prismatic(axis=(0, 0, -1)))


class TrialSeat(MappedReverserTrial):
    ones = TrialOnes()


class TrialRetainedOnes(ContactCounterOnes):
    p_10218_1 = TrialOnesInput(travel=Prismatic(axis=(0, 0, -1)))


class TrialTurns(TurnsShafts):
    ones = TrialRetainedOnes()


class TrialTransmission(RetainedTransmission):
    turns = TrialTurns()


class TrialOperatingCurta(OperatingCurta):
    transmission = TrialTransmission()
