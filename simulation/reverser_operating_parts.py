"""Measured inner-flank fit, preserving the ones stack's fork-capture tips.

The .43 mm inner relief clears the reversed drum passage and leaves room for
the installed outward contact covers. Outside R6 the existing .36 mm profile
is unchanged. These are simulation fits, not upstream CAD modifications.
"""

import cadquery as cq

from machinome.node.frames import Frame
from machinome.motion.joints import Prismatic
from machinome.parameters import Length
from simulation.counter_lockout_parts import ContactCounterOnesUpper
from simulation.fit import FittedCounterPinion
from simulation.reverser_inputs import OnesInput
from simulation.running_parts import RetainedTransmission, TurnsShafts
from simulation import channel_frames


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


class ReverserContactOnes(channel_frames.TurnsOnes):
    # Retain ContactCounterOnes' independently verified upper lockout fit.
    guide_seat = Frame(at=channel_frames.TurnsOnes.spindle.at, z=(0, 0, -1))
    p_10218_1 = ProtectedOnesInput(travel=Prismatic(axis=(0, 0, -1)))
    p_10222_1 = ContactCounterOnesUpper(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10218_1.guide.on(guide_seat, p_10218_1.travel)
    carry_mount = p_10222_1.guide.on(guide_seat, p_10222_1.travel)


class ReverserContactTurns(TurnsShafts):
    ones_seat = Frame(at=ReverserContactOnes.spindle.at)
    tens_seat = Frame(at=channel_frames.TurnsTens.spindle.at)
    hundreds_seat = Frame(at=channel_frames.TurnsHundreds.spindle.at)
    digit_4_seat = Frame(at=channel_frames.TurnsDigit4.spindle.at)
    digit_5_seat = Frame(at=channel_frames.TurnsDigit5.spindle.at)
    digit_6_seat = Frame(at=channel_frames.TurnsDigit6.spindle.at)
    ones = ReverserContactOnes()
    tens = channel_frames.TurnsTens()
    hundreds = channel_frames.TurnsHundreds()
    digit_4 = channel_frames.TurnsDigit4()
    digit_5 = channel_frames.TurnsDigit5()
    digit_6 = channel_frames.TurnsDigit6()
    ones_mount = ones.spindle.on(ones_seat, ones.turn)
    tens_mount = tens.spindle.on(tens_seat, tens.turn)
    hundreds_mount = hundreds.spindle.on(hundreds_seat, hundreds.turn)
    digit_4_mount = digit_4.spindle.on(digit_4_seat, digit_4.turn)
    digit_5_mount = digit_5.spindle.on(digit_5_seat, digit_5.turn)
    digit_6_mount = digit_6.spindle.on(digit_6_seat, digit_6.turn)


class ReverserContactTransmission(RetainedTransmission):
    turns = ReverserContactTurns()
