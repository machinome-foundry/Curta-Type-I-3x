"""Simulation-only captive loop mounting, not the source elastic clip.

The pilot authorized this replacement on 2026-09-23. The source finger loop
and both cover-hole datums are preserved; only the first bearing neighbourhood
and the two mounting posts change. Production adoption awaits installed proof.
"""

from math import cos, sin, radians
import cadquery as cq
from machinome.parameters import Length
from machinome.motion.joints import Prismatic, Revolute
from simulation.standard.parts import ClearingRing, ClearingRingRivet
from simulation.clearing_loop import LoopMountAssembly, LoopMountBench


MOUNT_SHOULDER_GAP = .01


def _polar(radius, angle):
    theta = radians(angle)
    return radius * cos(theta), radius * sin(theta)


def stop_slot(radius, half_width, depth):
    """A round-ended 89-degree arc in the loop's top face.

    The pin's .1 mm radial clearance leaves a small physical end allowance
    beyond the nominal -90..0 degree working stroke; tests pin both sides.
    """
    start, middle, end = -89.5, -45, -.5
    outer, inner = radius + half_width, radius - half_width
    sector = (cq.Workplane('XY').moveTo(*_polar(outer, start))
              .threePointArc(_polar(outer, middle), _polar(outer, end))
              .lineTo(*_polar(inner, end))
              .threePointArc(_polar(inner, middle), _polar(inner, start))
              .close().extrude(depth).val())
    for angle in (start, end):
        x, y = _polar(radius, angle)
        sector = sector.fuse(cq.Solid.makeCylinder(
            half_width, depth, cq.Vector(x, y, 0)))
    return sector.translate((40.5, 0, -.1)).clean()


class CaptiveLoopShape(ClearingRing):
    boss_radius = Length(8)
    bore_radius = Length(3.85)
    stop_radius = Length(6)
    slot_radius = Length(.7)
    slot_depth = Length(1.5)
    linear_deflection = .01
    angular_deflection = .1

    def adjust(self, shape):
        boss = cq.Solid.makeCylinder(self.boss_radius, 5.46,
                                     cq.Vector(40.5, 0, 0))
        bore = cq.Solid.makeCylinder(self.bore_radius, 5.66,
                                     cq.Vector(40.5, 0, -.1))
        return (shape.fuse(boss).cut(bore)
                .cut(stop_slot(self.stop_radius, self.slot_radius,
                               self.slot_depth)).clean())


class CaptiveSimulationLoop(CaptiveLoopShape):
    """Diagnostic pose joints; the production part has no release-height joint."""
    swivel = Revolute(axis=(0, 0, -1), at=(40.5, 0, 0))
    rise = Prismatic(axis=(0, 0, -1))


class SeatedSimulationRivet(ClearingRingRivet):
    # Cover-hole centres measured independently in the installed world frame.
    # Rotate their common world offset (-.38651158, .02841236) into the
    # source rivet's local frame. Only the lower stud moves, not its bearing.
    stem_x = Length(-.132055617)
    stem_y = Length(-.364362148)

    def adjust(self, shape):
        lower_box = cq.Solid.makeBox(20, 20, 6.7, cq.Vector(-10, -10, -.1))
        stem = shape.intersect(lower_box).translate((self.stem_x, self.stem_y, 0))
        return shape.cut(lower_box).fuse(stem).clean()


class SimulationPivot(SeatedSimulationRivet):
    cap_radius = Length(8)
    stop_radius = Length(6)
    pin_radius = Length(.6)
    linear_deflection = .01
    angular_deflection = .1

    def adjust(self, shape):
        shape = super().adjust(shape)
        # At the unchanged source placements, peg-local -X is loop-local +X.
        cap = cq.Solid.makeCylinder(self.cap_radius, 1,
                                    cq.Vector(0, 0, 12.6))
        pin = cq.Solid.makeCylinder(self.pin_radius, 1.6,
                                    cq.Vector(-self.stop_radius, 0, 11.1))
        return shape.fuse(cap).fuse(pin).clean()


class SimulationFlushPlug(SeatedSimulationRivet):
    height = Length(6.5)

    def adjust(self, shape):
        shape = super().adjust(shape)
        # Preserve the seated/glued source stud; replace its projecting head
        # and bearing with a flush top below the unchanged cover face.
        return shape.cut(cq.Solid.makeBox(20, 20, 20,
                                         cq.Vector(-10, -10, self.height))).clean()


class ReplacementLoopMount(LoopMountAssembly):
    seat_gap = Length(.05)
    clearing_ring = CaptiveSimulationLoop()
    clearing_ring_rivet_1 = SimulationPivot()
    clearing_ring_rivet_2 = SimulationFlushPlug()

    def render(self):
        super().render()
        self.clearing_ring.translate((0, 0, self.seat_gap))
        self.clearing_ring_rivet_1.translate((0, 0, MOUNT_SHOULDER_GAP))
        self.clearing_ring_rivet_2.translate((0, 0, MOUNT_SHOULDER_GAP))


class ReplacementLoopBench(LoopMountBench):
    """Unbounded diagnostic pose inputs permit explicit overtravel proofs."""
    loop = ReplacementLoopMount()


class ReplacementMountView(ReplacementLoopBench):
    """Inspection only: expose the loop, pivot and cover without neighbours."""

    def render(self):
        self.carrier.omit()
        self.covers.omit()
        self.crank.omit()


class ReplacementPivotExplodedView(ReplacementMountView):
    """Inspection only: lift the pivot 6 mm to expose its pin and arc recess."""

    def render(self):
        super().render()
        self.loop.clearing_ring_rivet_1.translate((0, 0, 6))
