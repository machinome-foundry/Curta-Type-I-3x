"""Pawl pivot and reverser guides, retaining their original joint coordinates."""

from machinome.node.frames import Frame
from machinome.motion.joints import Prismatic, Revolute
from simulation.fit import FittedPawl, PAWL_SPRING_ANCHOR
from simulation.pawl import PIVOT
from simulation.pawl_spring import MountedPawlSpring
from simulation.running_pawl import RetainedAntiReversal
from simulation.reverser_following import (
    FollowingReverser, FollowerBall, MountedReverserSpring, RADIAL)
from simulation.reverser_seat_trial import TrialKnob
from simulation.source_frames import source_frame


class FramedPawl(FittedPawl):
    datum = Frame()


class FramedPawlSpring(MountedPawlSpring):
    datum = Frame()


class FramedRetainedAntiReversal(RetainedAntiReversal):
    pawl_seat = source_frame(
        at=(-51.702407033, 9.116529328, -143.7), angle=180,
        axis=(-.122734172, .992439582, 0))
    spring_seat = Frame(at=PAWL_SPRING_ANCHOR)
    reverse_rotation_prevention_pawl = FramedPawl(
        turn=Revolute(axis=(0, 0, 1), at=PIVOT))
    documented_spring = FramedPawlSpring()
    pawl_mount = reverse_rotation_prevention_pawl.datum.on(
        pawl_seat, reverse_rotation_prevention_pawl.turn)
    spring_mount = documented_spring.datum.on(spring_seat)

    def render(self):
        # Only unmated source fasteners and the omitted source spring remain.
        self.anti_reversal_spring.rotate(24.099851655, (0, 0, 1))
        self.anti_reversal_spring.translate((-51.702407033, 9.116529328, -143.7))
        self.anti_reversal_spring.omit()
        self.anti_reversal_m5_bolt_sleeve.rotate(180, (0, 0, 1))
        self.anti_reversal_m5_bolt_sleeve.translate((-51.702407033, 9.116529328, -152.55))
        self.m5x15_hex_bolt_2.rotate(-180, (.707106781, .707106781, 0))
        self.m5x15_hex_bolt_2.translate((-51.702407033, 9.116529328, -133.95))


class FramedFollowerBall(FollowerBall):
    datum = Frame()


class FramedReverserSpring(MountedReverserSpring):
    datum = Frame()


class FramedKnob(TrialKnob):
    datum = Frame()


class FramedRunningReverser(FollowingReverser):
    ball_seat = source_frame(
        at=(19.505705679, 59.407726119, -53.7575), angle=-91.727941072,
        axis=(.970287525, -.17108787, .17108787))
    spring_seat = source_frame(
        at=(23.325705073, 69.903088196, -53.7575), angle=91.727941072,
        axis=(.970287525, -.17108787, -.17108787))
    knob_seat = Frame()
    p_5mm_ball = FramedFollowerBall(lift=Prismatic(axis=(0, 0, 1)),
                                   follow=Prismatic(axis=RADIAL))
    selector_knob_spring = FramedReverserSpring(lift=Prismatic(axis=(0, 0, 1)))
    reversing_lever_knob_1 = FramedKnob(
        lift=Prismatic(axis=(0, 0, 1), range=(-6.9425, 3.9075)))
    ball_mount = p_5mm_ball.datum.on(ball_seat, p_5mm_ball.lift)
    spring_mount = selector_knob_spring.datum.on(spring_seat, selector_knob_spring.lift)
    knob_mount = reversing_lever_knob_1.datum.on(knob_seat, reversing_lever_knob_1.lift)

    def render(self):
        # Keep source shaft/spacer placements and their previously fitted seats.
        # Ball radial following is independent of its mated axial lift.
        self.reversing_shaft.rotate(70, (0, 0, 1))
        self.reversing_shaft.translate((17.613968679, 54.210221429, -139.2))
        self.reversing_shaft.translate((0, 0, self.seat_rise))
        self.upper_reversing_lever_spacer.rotate(-20, (0, 0, 1))
        self.upper_reversing_lever_spacer.translate((17.613968679, 54.210221429, -41.1575))
        self.upper_reversing_lever_spacer.translate((0, 0, 3.9075))
        self.lower_reversing_lever_spacer.rotate(-20, (0, 0, 1))
        self.lower_reversing_lever_spacer.translate((17.613968679, 54.210221429, -124.7573))
        self.lower_reversing_lever_spacer.translate((0, 0, -7.6427))
