"""Source positioning stack measured against its unchanged enclosing collar.

This instrument has no seating correction. It adds the actual collar frame
to the existing positioning bench; both follow the same carriage lift.
"""

from math import cos, sin, radians
from machinome.motion.joints import Prismatic, Revolute
from machinome.simulation import Driver
from simulation.positioning import PositioningBench
from simulation.print_parts import CrankCollar
from simulation.standard.layers import CarriagePositioning as SourcePositioning
from simulation.standard.parts import ThrustRing
from simulation.flexibles import MountedCarriageSpring

SEAT_GAP = .05
RING_BOTTOM = 33 + SEAT_GAP
RING_THICKNESS = 1.5
WIRE_RADIUS = .9
SPRING_BOTTOM = RING_BOTTOM + RING_THICKNESS + WIRE_RADIUS + SEAT_GAP
SPRING_TOP = 54.3 - WIRE_RADIUS - SEAT_GAP
SPRING_HEIGHT = SPRING_TOP - SPRING_BOTTOM


class ThrustSeatBench(PositioningBench):
    shift = Driver(default=0, range=(-100, 100), unit='deg')
    collar = CrankCollar(lift=Prismatic(axis=(0, 0, 1)),
                         turn=Revolute(axis=(0, 0, 1)))
    PositioningBench.travel.drives(collar.lift)
    shift.drives(collar.turn)

    def render(self):
        super().render()
        self.collar.rotate(-144.282220532, (0, 0, 1)).translate((0, 0, 7.8))


class SeatedThrustBench(SourcePositioning):
    """Placement-only candidate using the collar ledge and sleeve underside.

    Source ring/collar/sleeve geometry is unchanged. The existing 1.8 mm-wire,
    four-turn analytic spring retains its radius and phase; the two actual
    seats prescribe its installed height, not an inferred spring force.
    This class is an isolated instrument, not an operating-model replacement.
    """
    travel = Driver(default=0, range=(0, 6), unit='mm')
    shift = Driver(default=0, range=(-100, 100), unit='deg')
    thrust_ring = ThrustRing(slide=Prismatic(axis=(0, 0, 1)))
    carriage_spring = MountedCarriageSpring(slide=Prismatic(axis=(0, 0, 1)))
    collar = CrankCollar(lift=Prismatic(axis=(0, 0, 1)),
                         turn=Revolute(axis=(0, 0, 1)))
    travel.drives(thrust_ring.slide)
    travel.drives(carriage_spring.slide)
    travel.drives(carriage_spring.height, ratio=-1, offset=SPRING_HEIGHT)
    travel.drives(collar.lift)
    shift.drives(collar.turn)

    def render(self):
        super().render()
        self.collar.rotate(-144.282220532, (0, 0, 1)).translate((0, 0, 7.8))
        self.thrust_ring.translate((0, 0, RING_BOTTOM - 25.5225))
        phase = radians(35.717779468)
        self.carriage_spring.translate((13.2*cos(phase), 13.2*sin(phase),
                                       SPRING_BOTTOM - 27.0225))
