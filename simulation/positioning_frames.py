"""The installed carriage ring, coil and radial ball attached at their seats."""

from math import cos, sin, radians
from machinome.node.frames import Frame
from machinome.motion.joints import Prismatic
from simulation.positioning import RadialCarriagePositioning, RING_BOTTOM, SPRING_BOTTOM
from simulation.thrust_ring_parts import BallPassageThrustRing
from simulation.flexibles import MountedCarriageSpring
from simulation.standard.parts import Part6mmBall419094
from simulation.source_frames import source_frame


class FramedThrustRing(BallPassageThrustRing):
    datum = Frame()


class FramedCarriageSpring(MountedCarriageSpring):
    datum = Frame()


class FramedPositioningBall(Part6mmBall419094):
    datum = Frame()


class FramedCarriagePositioning(RadialCarriagePositioning):
    ring_seat = source_frame(at=(0, 0, RING_BOTTOM),
                             angle=35.717779468, axis=(0, 0, 1))
    spring_seat = source_frame(
        at=(13.2*cos(radians(35.717779468)),
            13.2*sin(radians(35.717779468)), SPRING_BOTTOM),
        angle=35.717779468, axis=(0, 0, 1))
    ball_seat = source_frame(at=(9.627860318, 0, 30), angle=-180,
                             axis=(.707106781, 0, -.707106781))
    thrust_ring = FramedThrustRing(slide=Prismatic(axis=(0, 0, 1)))
    carriage_spring = FramedCarriageSpring(slide=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419094 = FramedPositioningBall(slide=Prismatic(axis=(1, 0, 0)))
    ring_mount = thrust_ring.datum.on(ring_seat, thrust_ring.slide)
    spring_mount = carriage_spring.datum.on(spring_seat, carriage_spring.slide)
    ball_mount = p_6mm_ball_419094.datum.on(ball_seat, p_6mm_ball_419094.slide)

    def render(self):
        self.carriage_spring_sleeve.rotate(180, (1, 0, 0))
        self.carriage_spring_sleeve.translate((0, 0, 57.6))
        self.spring_sleeve_c_clip.translate((0, 0, 57.6))
