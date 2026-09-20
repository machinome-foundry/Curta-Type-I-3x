"""Pilot-authorized mounting fit, independently tested before operating use.

Raise the unchanged detent-bearing body while leaving the installed fastening
end at the source datum. No pocket, flat, frame bore or upstream file changes.
"""

import cadquery as cq
from machinome.node import AssemblyNode
from machinome.parameters import Length
from machinome.simulation import Driver
from machinome.motion.joints import Prismatic
from simulation.standard.parts import ReversingShaft
from simulation.standard.assembly import ReversingLeverKnob1
from simulation.standard.layers import FrameFasteners
from simulation.reverser_assembly import MovingReverser, ReverserAssemblyBench
from simulation.reverser_fits import FittedReversingActuator
from simulation.reverser_inputs import (ReversingOnes, ReversingTens, ReversingHundreds,
    ReversingFourth, ReversingFifth, ReversingSixth)


class TrialReversingShaft(ReversingShaft):
    linear_deflection = .01
    angular_deflection = .1
    seat_rise = Length(1.9, min=0, max=2)
    seat_gap = Length(.05, min=0, max=.1)
    stud_radius = Length(2, min=2, max=2.1)

    def adjust(self, shape):
        # Removal only. Preserve every detent and flat in the original solid.
        # Raising this shortened profile restores the original neck/stud ends
        # in world coordinates, while the shoulder has a .05 mm seating gap.
        shoulder = 117 - self.seat_rise - self.seat_gap
        neck_end = 121.5 - self.seat_rise
        stud_end = 127.5 - self.seat_rise
        envelope = cq.Solid.makeCylinder(10, shoulder)
        envelope = envelope.fuse(cq.Solid.makeCylinder(
            2.9375, neck_end - shoulder, cq.Vector(0, 0, shoulder)))
        envelope = envelope.fuse(cq.Solid.makeCylinder(
            # Manual p28 calls for an M4 die on the R2.1 printed blank.
            # Represent its finished nominal major envelope, not a helix.
            self.stud_radius, stud_end - neck_end, cq.Vector(0, 0, neck_end)))
        return shape.intersect(envelope).clean()


class TrialKnob(ReversingLeverKnob1):
    reversing_actuator = FittedReversingActuator()


class TrialReverser(MovingReverser):
    seat_rise = Length(1.9, min=0, max=2)
    reversing_shaft = TrialReversingShaft(seat_rise=seat_rise)
    reversing_lever_knob_1 = TrialKnob(lift=Prismatic(axis=(0, 0, 1)))

    def render(self):
        super().render()
        self.reversing_shaft.translate((0, 0, self.seat_rise))


class ReverserSeatTrial(ReverserAssemblyBench):
    seat_rise = Length(1.9, min=0, max=2)
    lever = TrialReverser(seat_rise=seat_rise)
    fasteners = FrameFasteners()
    ones = ReversingOnes()
    tens = ReversingTens()
    hundreds = ReversingHundreds()
    digit_4 = ReversingFourth()
    digit_5 = ReversingFifth()
    digit_6 = ReversingSixth()
    knob_height = Driver(default=-4.9425, range=(-6.8425, 3.9075), unit='mm')
    gear_height = Driver(default=-4.85, range=(-6.75, 4.0), unit='mm')
    crank_angle = Driver(default=101.25, range=(0, 360), unit='deg')
    reversed_counter = Driver(default=1, range=(0, 1))


class TrialShaftView(TrialReversingShaft):
    color = '#3DAD68'


class SourceShaftView(ReversingShaft):
    color = '#8C9299'


class SeatProfileComparison(AssemblyNode):
    """Left: unchanged source. Right: trial. Fastening ends share Z=0."""
    source = SourceShaftView()
    trial = TrialShaftView()

    def render(self):
        self.source.translate((0, 0, -127.5))
        self.trial.translate((12, 0, -125.6))
