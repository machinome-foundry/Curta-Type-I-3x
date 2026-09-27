"""Frame-mounted carry stations, preserving the measured source triads.

The slider keeps its original parent-Z travel. The bearing and spring use
rigid mates: the spring's existing spread coordinate remains an internal
deformation coordinate, not a second attachment freedom. Its nominal source
datum is placed without changing the wire law that holds the closed U.
"""

from machinome.node import Frame
from machinome.motion.joints import Prismatic
from simulation.standard import carry
from simulation.carry_heads import ResultsSlider, TurnsSlider
from simulation.carry_seat import ResultsSpringSeat, TurnsSpringSeat
from simulation.carry_spring import MountedCarrySpring
from simulation.source_frames import source_frame


class MountedResultsSlider(ResultsSlider):
    datum = Frame()


class MountedTurnsSlider(TurnsSlider):
    datum = Frame()


class MountedResultsBearing(ResultsSpringSeat):
    datum = Frame()


class MountedTurnsBearing(TurnsSpringSeat):
    datum = Frame()


class AttachedCarrySpring(MountedCarrySpring):
    datum = Frame()


class ResultsLever1(carry.ResultsLever1):
    slider_seat = source_frame(
        at=(57.225, -7.89, -2.1), angle=-120,
        axis=(0.577350269, 0.577350269, 0.577350269))
    bearing_seat = source_frame(
        at=(57.3, -11.79, 1.35), angle=-180,
        axis=(0, 0.707106781, 0.707106781))
    spring_seat = source_frame(
        at=(57.347125257, -10.472333636, -1.77550064), angle=-179.853630404,
        axis=(-0.000173983, 0.999224553, -0.03937338))
    tens_slider_for_results = MountedResultsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedResultsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_results.datum.on(slider_seat, tens_slider_for_results.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class ResultsLever2(carry.ResultsLever2):
    slider_seat = source_frame(
        at=(51.075371294, -26.98627748, 2.1), angle=-132.145070558,
        axis=(0.633687274, 0.443712606, 0.633687274))
    bearing_seat = source_frame(
        at=(49.811969681, -30.676730212, 1.35), angle=165.893955739,
        axis=(0.12372403, 0.701673843, 0.701673843))
    spring_seat = source_frame(
        at=(50.306921376, -29.454646639, -1.77550064), angle=-179.072368892,
        axis=(0.173347721, 0.98410574, -0.038554638))
    tens_slider_for_results = MountedResultsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedResultsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_results.datum.on(slider_seat, tens_slider_for_results.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class ResultsLever3(carry.ResultsLever3):
    slider_seat = source_frame(
        at=(38.765299017, -42.827611621, 2.1), angle=-145.22456333,
        axis=(0.671542934, 0.313145613, 0.671542934))
    bearing_seat = source_frame(
        at=(36.315880673, -45.863394019, 1.35), angle=152.009109282,
        axis=(0.249243569, 0.684791079, 0.684791079))
    spring_seat = source_frame(
        at=(37.198960326, -44.884294554, -1.77550064), angle=-178.319252635,
        axis=(0.341627902, 0.939123693, -0.03656591))
    tens_slider_for_results = MountedResultsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedResultsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_results.datum.on(slider_seat, tens_slider_for_results.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class ResultsLever4(carry.ResultsLever4):
    slider_seat = source_frame(
        at=(21.779559564, -53.503303732, 2.1), angle=-158.909418821,
        axis=(0.694746591, 0.186156788, 0.694746591))
    bearing_seat = source_frame(
        at=(18.439560489, -55.518255637, 1.35), angle=138.590377891,
        axis=(0.377964473, 0.654653671, 0.654653671))
    spring_seat = source_frame(
        at=(19.604255663, -54.900234124, -1.77550064), angle=-177.617141875,
        axis=(0.4995692, 0.865627276, -0.033466897))
    tens_slider_for_results = MountedResultsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedResultsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_results.datum.on(slider_seat, tens_slider_for_results.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class ResultsLever5(carry.ResultsLever5):
    slider_seat = source_frame(
        at=(2.166883796, -57.725707788, 2.1), angle=-172.933425611,
        axis=(0.705757557, 0.061745785, 0.705757557))
    bearing_seat = source_frame(
        at=(-1.660842828, -58.476796262, 1.35), angle=125.93195832,
        axis=(0.510273605, 0.608120402, 0.608120402))
    spring_seat = source_frame(
        at=(-0.355011561, -58.294395218, -1.77550064), angle=-176.987363988,
        axis=(0.642377344, 0.76582627, -0.029350834))
    tens_slider_for_results = MountedResultsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedResultsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_results.datum.on(slider_seat, tens_slider_for_results.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class ResultsLever6(carry.ResultsLever6):
    slider_seat = source_frame(
        at=(-17.707150138, -54.985539544, -2.1), angle=172.933425611,
        axis=(0.705757557, -0.061745785, 0.705757557))
    bearing_seat = source_frame(
        at=(-21.560923988, -54.382172233, 1.35), angle=114.404497338,
        axis=(0.644400478, 0.540716203, 0.540716203))
    spring_seat = source_frame(
        at=(-20.271459152, -54.657391914, -1.77550064), angle=-176.449067053,
        axis=(0.765705559, 0.642730479, -0.024341906))
    tens_slider_for_results = MountedResultsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedResultsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_results.datum.on(slider_seat, tens_slider_for_results.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class ResultsLever7(carry.ResultsLever7):
    slider_seat = source_frame(
        at=(-35.445440436, -45.613303732, 2.1), angle=158.909418821,
        axis=(0.694746591, -0.186156788, 0.694746591))
    bearing_seat = source_frame(
        at=(-38.860439511, -43.728255637, 1.35), angle=104.477512186,
        axis=(0.774596669, 0.447213595, 0.447213595))
    spring_seat = source_frame(
        at=(-37.742869594, -44.427900489, -1.77550064), angle=-176.018634684,
        axis=(0.865788662, 0.500064337, -0.018591707))
    tens_slider_for_results = MountedResultsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedResultsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_results.datum.on(slider_seat, tens_slider_for_results.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class ResultsLever8(carry.ResultsLever8):
    slider_seat = source_frame(
        at=(-48.908487498, -30.739430308, -2.1), angle=145.22456333,
        axis=(0.671542934, -0.313145613, 0.671542934))
    bearing_seat = source_frame(
        at=(-51.472812509, -27.800066051, 1.35), angle=96.717713464,
        axis=(0.889126491, 0.323615577, 0.323615577))
    spring_seat = source_frame(
        at=(-50.661932937, -28.839748578, -1.77550064), angle=-175.709180801,
        axis=(0.939562264, 0.342157976, -0.012274798))
    tens_slider_for_results = MountedResultsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedResultsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_results.datum.on(slider_seat, tens_slider_for_results.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class ResultsLever9(carry.ResultsLever9):
    slider_seat = source_frame(
        at=(-56.472449155, -12.157927924, -2.1), angle=132.145070558,
        axis=(0.633687274, -0.443712606, 0.633687274))
    bearing_seat = source_frame(
        at=(-57.876804661, -8.518778213, 1.35), angle=91.727941072,
        axis=(0.970287525, 0.17108787, 0.17108787))
    spring_seat = source_frame(
        at=(-57.470419478, -9.77309736, -1.77550064), angle=-175.530141664,
        axis=(0.984762153, 0.173816938, -0.005583447))
    tens_slider_for_results = MountedResultsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedResultsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_results.datum.on(slider_seat, tens_slider_for_results.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class ResultsLever10(carry.ResultsLever10):
    slider_seat = source_frame(
        at=(-57.225, 7.89, -2.1), angle=120,
        axis=(0.577350269, -0.577350269, 0.577350269))
    bearing_seat = source_frame(
        at=(-57.3, 11.79, 1.35), angle=90,
        axis=(1, 0, 0))
    spring_seat = source_frame(
        at=(-57.347125257, 10.472333636, -1.77550064), angle=-175.486980131,
        axis=(0.999999168, 0.000174118, 0.001278307))
    tens_slider_for_results = MountedResultsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedResultsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_results.datum.on(slider_seat, tens_slider_for_results.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class TurnsLever1(carry.TurnsLever1):
    slider_seat = source_frame(
        at=(-31.302472974, 48.436038605, -27.9), angle=-152.009109282,
        axis=(0.684791079, 0.249243569, 0.684791079))
    bearing_seat = source_frame(
        at=(-27.800066051, 51.472812509, 1.35), angle=100.288585137,
        axis=(0.834817129, -0.389281621, -0.389281621))
    spring_seat = source_frame(
        at=(-28.737258529, 50.747932299, -1.773550975), angle=-176.424953014,
        axis=(0.90626823, -0.422401603, 0.015961864))
    tens_slider_for_turns_counter = MountedTurnsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedTurnsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_turns_counter.datum.on(slider_seat, tens_slider_for_turns_counter.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class TurnsLever2(carry.TurnsLever2):
    slider_seat = source_frame(
        at=(-12.848602, 56.22106435, -27.9), angle=-165.893955739,
        axis=(0.701673843, 0.12372403, 0.701673843))
    bearing_seat = source_frame(
        at=(-8.518778213, 57.876804661, 1.35), angle=109.207479725,
        axis=(0.710564775, -0.497542812, -0.497542812))
    spring_seat = source_frame(
        at=(-9.647374703, 57.516178783, -1.773550975), angle=-176.796884445,
        axis=(0.819072059, -0.573301149, 0.021136601))
    tens_slider_for_turns_counter = MountedTurnsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedTurnsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_turns_counter.datum.on(slider_seat, tens_slider_for_turns_counter.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class TurnsLever3(carry.TurnsLever3):
    slider_seat = source_frame(
        at=(7.155, 57.225, -27.9), angle=180,
        axis=(0.707106781, 0, 0.707106781))
    bearing_seat = source_frame(
        at=(11.79, 57.3, 1.35), angle=120,
        axis=(0.577350269, -0.577350269, -0.577350269))
    spring_seat = source_frame(
        at=(10.606124892, 57.347125257, -1.773550975), angle=-177.266123197,
        axis=(0.707000796, -0.706746795, 0.025667923))
    tens_slider_for_turns_counter = MountedTurnsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedTurnsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_turns_counter.datum.on(slider_seat, tens_slider_for_turns_counter.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class TurnsLever4(carry.TurnsLever4):
    slider_seat = source_frame(
        at=(26.295603404, 51.326756099, -27.9), angle=165.893955739,
        axis=(0.701673843, -0.12372403, 0.701673843))
    bearing_seat = source_frame(
        at=(30.676730212, 49.811969681, 1.35), angle=-132.145070558,
        axis=(-0.443712606, 0.633687274, 0.633687274))
    spring_seat = source_frame(
        at=(29.580369296, 50.261162071, -1.773550975), angle=177.818391321,
        axis=(-0.573475281, 0.81869448, -0.029418539))
    tens_slider_for_turns_counter = MountedTurnsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedTurnsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_turns_counter.datum.on(slider_seat, tens_slider_for_turns_counter.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass


class TurnsLever5(carry.TurnsLever5):
    slider_seat = source_frame(
        at=(42.264568955, 39.23774791, -27.9), angle=152.009109282,
        axis=(0.684791079, -0.249243569, 0.684791079))
    bearing_seat = source_frame(
        at=(45.863394019, 36.315880673, 1.35), angle=-145.22456333,
        axis=(-0.313145613, 0.671542934, 0.671542934))
    spring_seat = source_frame(
        at=(44.986784603, 37.112960964, -1.773550975), angle=178.436898275,
        axis=(-0.422560828, 0.905759717, -0.032275094))
    tens_slider_for_turns_counter = MountedTurnsSlider(travel=Prismatic(axis=(0, 0, -1)))
    tens_slide_bearing = MountedTurnsBearing()
    carry_lever_spring = AttachedCarrySpring()
    slider_mount = tens_slider_for_turns_counter.datum.on(slider_seat, tens_slider_for_turns_counter.travel)
    bearing_mount = tens_slide_bearing.datum.on(bearing_seat)
    spring_mount = carry_lever_spring.datum.on(spring_seat)

    def render(self):
        # Every direct child is placed by its mate, not the source render.
        pass
