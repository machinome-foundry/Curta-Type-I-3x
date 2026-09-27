"""Frame attachments for the final shoulder-fitted counter carry stations."""

from machinome.node import Frame
from machinome.motion.joints import Prismatic
from simulation import counter_guide_trial as trial
from simulation.counter_guide_shoulder import ShoulderClearedTurnsSlider
from simulation.carry_frames import MountedTurnsBearing, AttachedCarrySpring
from simulation.source_frames import source_frame


class MountedShoulderSlider(ShoulderClearedTurnsSlider):
    datum = Frame()


class TurnsLever1(trial.TurnsLever1):
    slider_seat = source_frame(
        at=(-31.302472974, 48.436038605, -27.9), angle=-152.009109282,
        axis=(0.684791079, 0.249243569, 0.684791079))
    bearing_seat = source_frame(
        at=(-27.800066051, 51.472812509, 1.35), angle=100.288585137,
        axis=(0.834817129, -0.389281621, -0.389281621))
    spring_seat = source_frame(
        at=(-28.737258529, 50.747932299, -1.773550975), angle=-176.424953014,
        axis=(0.90626823, -0.422401603, 0.015961864))
    tens_slider_for_turns_counter = MountedShoulderSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedTurnsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_turns_counter.datum.on(slider_seat, tens_slider_for_turns_counter.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class TurnsLever2(trial.TurnsLever2):
    slider_seat = source_frame(
        at=(-12.848602, 56.22106435, -27.9), angle=-165.893955739,
        axis=(0.701673843, 0.12372403, 0.701673843))
    bearing_seat = source_frame(
        at=(-8.518778213, 57.876804661, 1.35), angle=109.207479725,
        axis=(0.710564775, -0.497542812, -0.497542812))
    spring_seat = source_frame(
        at=(-9.647374703, 57.516178783, -1.773550975), angle=-176.796884445,
        axis=(0.819072059, -0.573301149, 0.021136601))
    tens_slider_for_turns_counter = MountedShoulderSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedTurnsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_turns_counter.datum.on(slider_seat, tens_slider_for_turns_counter.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class TurnsLever3(trial.TurnsLever3):
    slider_seat = source_frame(
        at=(7.155, 57.225, -27.9), angle=180,
        axis=(0.707106781, 0, 0.707106781))
    bearing_seat = source_frame(
        at=(11.79, 57.3, 1.35), angle=120,
        axis=(0.577350269, -0.577350269, -0.577350269))
    spring_seat = source_frame(
        at=(10.606124892, 57.347125257, -1.773550975), angle=-177.266123197,
        axis=(0.707000796, -0.706746795, 0.025667923))
    tens_slider_for_turns_counter = MountedShoulderSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedTurnsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_turns_counter.datum.on(slider_seat, tens_slider_for_turns_counter.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class TurnsLever4(trial.TurnsLever4):
    slider_seat = source_frame(
        at=(26.295603404, 51.326756099, -27.9), angle=165.893955739,
        axis=(0.701673843, -0.12372403, 0.701673843))
    bearing_seat = source_frame(
        at=(30.676730212, 49.811969681, 1.35), angle=-132.145070558,
        axis=(-0.443712606, 0.633687274, 0.633687274))
    spring_seat = source_frame(
        at=(29.580369296, 50.261162071, -1.773550975), angle=177.818391321,
        axis=(-0.573475281, 0.81869448, -0.029418539))
    tens_slider_for_turns_counter = MountedShoulderSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedTurnsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_turns_counter.datum.on(slider_seat, tens_slider_for_turns_counter.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class TurnsLever5(trial.TurnsLever5):
    slider_seat = source_frame(
        at=(42.264568955, 39.23774791, -27.9), angle=152.009109282,
        axis=(0.684791079, -0.249243569, 0.684791079))
    bearing_seat = source_frame(
        at=(45.863394019, 36.315880673, 1.35), angle=-145.22456333,
        axis=(-0.313145613, 0.671542934, 0.671542934))
    spring_seat = source_frame(
        at=(44.986784603, 37.112960964, -1.773550975), angle=178.436898275,
        axis=(-0.422560828, 0.905759717, -0.032275094))
    tens_slider_for_turns_counter = MountedShoulderSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedTurnsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_turns_counter.datum.on(slider_seat, tens_slider_for_turns_counter.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass
