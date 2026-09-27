"""Original register-ball guides and the complete spider mounted by frames."""

from machinome.node import Frame
from machinome.motion.joints import Prismatic
from simulation.register_detents import RegisterDetents
from simulation.standard.parts import Part6mmBall419241
from simulation.spider import FlexibleSpider, SEAT_GAP
from simulation.source_frames import source_frame


class MountedDetentBall(Part6mmBall419241):
    datum = Frame()


class MountedSpider(FlexibleSpider):
    datum = Frame()


class FramedRegisterDetents(RegisterDetents):
    ball_1_seat = source_frame(
        at=(41.611836805, -14.543025222, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_2_seat = source_frame(
        at=(-27.78108269, 33.060447395, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_3_seat = source_frame(
        at=(-6.614320319, -43.007025353, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_4_seat = source_frame(
        at=(-32.560903643, -28.356981008, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_5_seat = source_frame(
        at=(-40.536394735, 14.466670656, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_6_seat = source_frame(
        at=(28.215994571, 33.59791604, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_7_seat = source_frame(
        at=(-20.879211024, -37.969544529, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_8_seat = source_frame(
        at=(-43.02027263, -0.456253672, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_9_seat = source_frame(
        at=(0.119644646, 43.519816382, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_10_seat = source_frame(
        at=(15.042568974, 41.035938487, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_11_seat = source_frame(
        at=(8.513212127, -42.861828947, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_12_seat = source_frame(
        at=(44.0957147, 0.379899106, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_13_seat = source_frame(
        at=(34.173814358, -27.716450819, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_14_seat = source_frame(
        at=(-14.752853499, 40.749957394, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_15_seat = source_frame(
        at=(38.051011892, 22.102884323, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_16_seat = source_frame(
        at=(22.678782641, -37.551468141, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    ball_17_seat = source_frame(
        at=(-40.250413642, -15.328751817, 43.35), angle=-180,
        axis=(-0.004798912, 0.999988485, 0))
    spider_seat = source_frame(
        at=(0.537721035, -0.038177283, 45.2 + SEAT_GAP),
        angle=0.549916905, axis=(0, 0, 1))

    p_6mm_ball_419241_1 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_2 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_3 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_4 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_5 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_6 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_7 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_8 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_9 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_10 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_11 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_12 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_13 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_14 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_15 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_16 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    p_6mm_ball_419241_17 = MountedDetentBall(lift=Prismatic(axis=(0, 0, 1)))
    spider_spring = MountedSpider()

    ball_1_mount = p_6mm_ball_419241_1.datum.on(ball_1_seat, p_6mm_ball_419241_1.lift)
    ball_2_mount = p_6mm_ball_419241_2.datum.on(ball_2_seat, p_6mm_ball_419241_2.lift)
    ball_3_mount = p_6mm_ball_419241_3.datum.on(ball_3_seat, p_6mm_ball_419241_3.lift)
    ball_4_mount = p_6mm_ball_419241_4.datum.on(ball_4_seat, p_6mm_ball_419241_4.lift)
    ball_5_mount = p_6mm_ball_419241_5.datum.on(ball_5_seat, p_6mm_ball_419241_5.lift)
    ball_6_mount = p_6mm_ball_419241_6.datum.on(ball_6_seat, p_6mm_ball_419241_6.lift)
    ball_7_mount = p_6mm_ball_419241_7.datum.on(ball_7_seat, p_6mm_ball_419241_7.lift)
    ball_8_mount = p_6mm_ball_419241_8.datum.on(ball_8_seat, p_6mm_ball_419241_8.lift)
    ball_9_mount = p_6mm_ball_419241_9.datum.on(ball_9_seat, p_6mm_ball_419241_9.lift)
    ball_10_mount = p_6mm_ball_419241_10.datum.on(ball_10_seat, p_6mm_ball_419241_10.lift)
    ball_11_mount = p_6mm_ball_419241_11.datum.on(ball_11_seat, p_6mm_ball_419241_11.lift)
    ball_12_mount = p_6mm_ball_419241_12.datum.on(ball_12_seat, p_6mm_ball_419241_12.lift)
    ball_13_mount = p_6mm_ball_419241_13.datum.on(ball_13_seat, p_6mm_ball_419241_13.lift)
    ball_14_mount = p_6mm_ball_419241_14.datum.on(ball_14_seat, p_6mm_ball_419241_14.lift)
    ball_15_mount = p_6mm_ball_419241_15.datum.on(ball_15_seat, p_6mm_ball_419241_15.lift)
    ball_16_mount = p_6mm_ball_419241_16.datum.on(ball_16_seat, p_6mm_ball_419241_16.lift)
    ball_17_mount = p_6mm_ball_419241_17.datum.on(ball_17_seat, p_6mm_ball_419241_17.lift)
    spider_mount = spider_spring.datum.on(spider_seat)

    def render(self):
        # The eighteen mates own all direct-child placements. The spider's
        # internal fingertip coordinates continue to describe deformation.
        pass

