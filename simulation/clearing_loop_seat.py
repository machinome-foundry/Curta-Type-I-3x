"""Diagnostic of the radial deployed pose; not an adopted loop control."""

import cadquery as cq
from machinome.node import AssemblyNode
from machinome.parameters import Length
from machinome.simulation import Driver
from simulation.clearing_loop import LoopMountBench, LoopMountAssembly, ProbeLoop
from simulation.standard.parts import ClearingRing


class SeatedLoop(ProbeLoop):
    # Actual second rivet in the loop's own frame at the radial (-90°) pose.
    # The original second clip centre is (30.5069278, 26.6378932), .9066 mm
    # away. This only opens its cavity; clipping travel still needs proof.
    seat_x = Length(31.095555539)
    seat_y = Length(25.948341482)
    seat_radius = Length(3.8, min=0)
    linear_deflection = .01
    angular_deflection = .1

    def adjust(self, shape):
        cutter = cq.Solid.makeCylinder(self.seat_radius, 5.46,
                                       cq.Vector(self.seat_x, self.seat_y, 0))
        return shape.cut(cutter).clean()


class SeatedLoopMount(LoopMountAssembly):
    seat_gap = Length(.05, min=0)
    clearing_ring = SeatedLoop()

    def render(self):
        super().render()
        # Named locational allowance at the cover, not a Boolean epsilon.
        # The fitted cavity is natively clear at source Z but its encoded
        # mesh leaves 4.702446e-6 mm³ there. Retain both rivet-head seats.
        self.clearing_ring.translate((0, 0, self.seat_gap))


class LoopSeatTrial(LoopMountBench):
    deployment = Driver(default=-90, unit='deg')
    loop = SeatedLoopMount()


def second_clip_crop(shape):
    """Inspection cut only; the complete trial retains the entire source loop."""
    return shape.intersect(cq.Solid.makeBox(23, 27, 6, cq.Vector(20, 12, -.1)))


class SourceSecondClip(ClearingRing):
    color = '#8C9299'

    def adjust(self, shape):
        return second_clip_crop(shape)


class FittedSecondClip(SeatedLoop):
    color = '#3DAD68'

    def adjust(self, shape):
        return second_clip_crop(super().adjust(shape))


class LoopSeatComparison(AssemblyNode):
    source = SourceSecondClip()
    fitted = FittedSecondClip()

    def render(self):
        self.source.translate((-46, -26, 0))
        self.fitted.translate((-16, -26, 0))
