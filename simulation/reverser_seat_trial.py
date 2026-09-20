"""Pilot-authorized mounting-shoulder trial; not adopted in OperatingCurta.

Raise the unchanged detent-bearing body while leaving the installed fastening
end at the source datum. No pocket, flat, frame bore or upstream file changes.
"""

import cadquery as cq
from machinome.node import AssemblyNode
from machinome.parameters import Length
from machinome.simulation import Driver
from simulation.standard.parts import ReversingShaft
from simulation.standard.layers import FrameFasteners
from simulation.reverser_assembly import MovingReverser, ReverserAssemblyBench


class TrialReversingShaft(ReversingShaft):
    seat_rise = Length(1.9, min=0, max=2)
    seat_gap = Length(.05, min=0, max=.1)

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
            2.1, stud_end - neck_end, cq.Vector(0, 0, neck_end)))
        return shape.intersect(envelope).clean()


class TrialReverser(MovingReverser):
    seat_rise = Length(1.9, min=0, max=2)
    reversing_shaft = TrialReversingShaft(seat_rise=seat_rise)

    def render(self):
        super().render()
        self.reversing_shaft.translate((0, 0, self.seat_rise))


class ReverserSeatTrial(ReverserAssemblyBench):
    seat_rise = Length(1.9, min=0, max=2)
    lever = TrialReverser(seat_rise=seat_rise)
    fasteners = FrameFasteners()
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
