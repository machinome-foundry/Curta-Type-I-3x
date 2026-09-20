"""Trial lever with source-sized spring and radial ball following.

Only prescribed kinematics: pocket slope and compression establish the
restoring direction, not a spring force, friction or automatic snap action.
"""

from math import cos, sin, radians
from molejo import Circle, Shape, Helix, P
from machinome.node import AssemblyNode, MolejoNode
from machinome.parameters import Length
from machinome.motion.joints import Prismatic
from machinome.motion.ports import Port
from simulation.colors import STEEL
from simulation.standard.parts import Part5mmBall
from simulation.reverser_seat_trial import TrialReverser, ReverserSeatTrial
from simulation.reverser_detent_motion import (ball_radius_at, spring_height,
    SOURCE_BALL_Z, SOURCE_BALL_RADIUS, COIL_RADIUS, COIL_TURNS, WIRE_RADIUS, SEAT_GAP)

RADIAL = (cos(radians(70)), sin(radians(70)), 0)


class ReverserSpringWire(MolejoNode):
    height = Port(unit='mm')
    color = STEEL

    def render(self):
        return Shape(profile=Circle(WIRE_RADIUS),
                     path=[Helix(radius=COIL_RADIUS, turns=COIL_TURNS, height=P.height)],
                     path_samples=416, profile_samples=24)


class MountedReverserSpring(AssemblyNode):
    height = Port(unit='mm')
    wire = ReverserSpringWire()
    height.drives(wire.height)

    def render(self):
        # Original spring placement points its local Z inward from the bore's
        # blind end. Keep the back wire .05 mm clear of that end throughout.
        self.wire.translate((COIL_RADIUS, 0, WIRE_RADIUS + SEAT_GAP))


class FollowerBall(Part5mmBall):
    linear_deflection = .01
    angular_deflection = .1


def follower(source, target):
    rise = source.seat_rise
    return lambda height: ball_radius_at(SOURCE_BALL_Z + height - rise) - SOURCE_BALL_RADIUS


def compression(source, target):
    rise = source.seat_rise
    return lambda height: spring_height(ball_radius_at(SOURCE_BALL_Z + height - rise))


class FollowingReverser(TrialReverser):
    p_5mm_ball = FollowerBall(lift=Prismatic(axis=(0, 0, 1)),
                           follow=Prismatic(axis=RADIAL))
    selector_knob_spring = MountedReverserSpring(lift=Prismatic(axis=(0, 0, 1)))
    TrialReverser.displacement.drives(p_5mm_ball.follow, law=follower)
    TrialReverser.displacement.drives(selector_knob_spring.height, law=compression)


class ReverserFollowerTrial(ReverserSeatTrial):
    seat_rise = Length(1.9, min=0, max=2)
    lever = FollowingReverser(seat_rise=seat_rise)


class SectionedFollower(FollowingReverser):
    def render(self):
        super().render()
        self.reversing_lever_knob_1.omit()


class FollowerSection(ReverserFollowerTrial):
    """Inspection only: omit the opaque knob and unrelated machine neighbours."""

    seat_rise = Length(1.9, min=0, max=2)
    lever = SectionedFollower(seat_rise=seat_rise)

    def render(self):
        super().render()
        for child in (self.upper_frame, self.lower_frame, self.fasteners,
                      self.drum, self.ones, self.tens, self.hundreds,
                      self.digit_4, self.digit_5, self.digit_6):
            child.omit()
