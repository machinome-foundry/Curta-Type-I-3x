"""The carriage lifts against a spring whose upper seat stays on the shaft."""

from machinome.simulation import Driver
from machinome.motion.joints import Prismatic
from machinome.motion.ports import Port
from simulation.standard.layers import CarriagePositioning as SourcePositioning
from simulation.standard.parts import ThrustRing
from simulation.flexibles import MountedCarriageSpring
from math import cos, sin, radians


# Installed faces measured from the unmodified collar and sleeve. See
# docs/thrust-seat-investigation-2026-09-21.md. These specify a geometric
# seat, not spring preload or a force model.
SEAT_GAP = .05
COLLAR_LEDGE_Z = 33
SLEEVE_SEAT_Z = 54.3
RING_THICKNESS = 1.5
WIRE_RADIUS = .9
RING_BOTTOM = COLLAR_LEDGE_Z + SEAT_GAP
SPRING_BOTTOM = RING_BOTTOM + RING_THICKNESS + WIRE_RADIUS + SEAT_GAP
SPRING_TOP = SLEEVE_SEAT_Z - WIRE_RADIUS - SEAT_GAP


class CarriagePositioning(SourcePositioning):
    lift = Port(unit='mm')
    thrust_ring = ThrustRing(slide=Prismatic(axis=(0, 0, 1)))
    carriage_spring = MountedCarriageSpring(slide=Prismatic(axis=(0, 0, 1)))
    lift.drives(thrust_ring.slide)
    lift.drives(carriage_spring.slide)
    spring_compression = lift.drives(carriage_spring.height, ratio=-1, offset=24)

    def render(self):
        super().render()
        # Molejo's helix begins on its wire, not at the spring's central axis.
        phase = radians(35.717779468)
        self.carriage_spring.translate((13.2 * cos(phase), 13.2 * sin(phase), 0))


class SeatedCarriagePositioning(CarriagePositioning):
    """Seat the unchanged ring and source-sized coil on their actual supports.

    The ring rises with the collar, while the sleeve stays on the main shaft.
    The source-pose bench is retained above as an independent negative control.
    """
    spring_compression = CarriagePositioning.lift.drives(
        CarriagePositioning.carriage_spring.height,
        ratio=-1, offset=SPRING_TOP - SPRING_BOTTOM)

    def render(self):
        super().render()
        self.thrust_ring.translate((0, 0, RING_BOTTOM - 25.5225))
        self.carriage_spring.translate((0, 0, SPRING_BOTTOM - 27.0225))


class PositioningBench(CarriagePositioning):
    travel = Driver(default=0, range=(0, 6), unit='mm')
    travel.drives(CarriagePositioning.lift)
