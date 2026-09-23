"""Rejected orbit candidate retained as a negative whole-machine control.

It clears the bell but collides with the stationary frame. Never selected by
the project manifest or adopted as the operating positioning assembly.
"""

from machinome.motion.joints import Bound, Prismatic, Revolute
from machinome.simulation import Follow
from simulation.positioning import SeatedCarriagePositioning
from simulation.standard.parts import Part6mmBall419094
from simulation.running import StaticBallOperatingCurta, RunningCarriage


class OrbitPositioningTrial(SeatedCarriagePositioning):
    p_6mm_ball_419094 = Part6mmBall419094(turn=Revolute(axis=(0, 0, 1)))


class OrbitCarriageTrial(RunningCarriage):
    positioning = OrbitPositioningTrial()


class OrbitingBallTrial(StaticBallOperatingCurta):
    carriage = OrbitCarriageTrial()
    StaticBallOperatingCurta.carry_mechanism.tens_bell.turn.drives(
        carriage.positioning.p_6mm_ball_419094.turn)


from simulation.positioning_ball_profiles import bell_limit, collar_limit


class RadialPositioningTrial(SeatedCarriagePositioning):
    p_6mm_ball_419094 = Part6mmBall419094(slide=Prismatic(axis=(1, 0, 0)))

    def simulate(self):
        if self.p_6mm_ball_419094.slide.value is None:
            self.p_6mm_ball_419094.slide = 0


class RadialCarriageTrial(RunningCarriage):
    positioning = RadialPositioningTrial()


class RadialBallTrial(StaticBallOperatingCurta):
    """Independent adoption reference: contact pushes and free slack is retained."""
    carriage = RadialCarriageTrial()
    carriage.positioning.p_6mm_ball_419094.slide.constrain(range=(
        Bound(lambda travel, turn: bell_limit(turn),
              reads=(StaticBallOperatingCurta.carry_mechanism.tens_bell.turn,)),
        Bound(lambda travel, lift: collar_limit(lift),
              reads=(carriage.registers.lift,))))
    (StaticBallOperatingCurta.carry_mechanism.tens_bell.turn & carriage.registers.lift &
     carriage.positioning.p_6mm_ball_419094.slide).drives(
        carriage.positioning.p_6mm_ball_419094.slide,
        law=Follow(lower=lambda turn, lift: bell_limit(turn),
                   upper=lambda turn, lift: collar_limit(lift)))


class ReversedRadialPositioningTrial(RadialPositioningTrial):
    p_6mm_ball_419094 = Part6mmBall419094(slide=Prismatic(axis=(-1, 0, 0)))


class ReversedRadialCarriageTrial(RadialCarriageTrial):
    positioning = ReversedRadialPositioningTrial()


class ReversedRadialBallTrial(RadialBallTrial):
    carriage = ReversedRadialCarriageTrial()


from simulation.positioning_ball_profiles import radial_following


class PullingBallTrial(StaticBallOperatingCurta):
    """Rejected endpoint-difference law: returns pull an unsupported free ball."""
    carriage = RadialCarriageTrial()
    carriage.positioning.p_6mm_ball_419094.slide.constrain(range=(
        Bound(lambda travel, turn: bell_limit(turn),
              reads=(StaticBallOperatingCurta.carry_mechanism.tens_bell.turn,)),
        Bound(lambda travel, lift: collar_limit(lift),
              reads=(carriage.registers.lift,))))
    (StaticBallOperatingCurta.carry_mechanism.tens_bell.turn & carriage.registers.lift &
     carriage.positioning.p_6mm_ball_419094.slide).drives(
        carriage.positioning.p_6mm_ball_419094.slide, law=radial_following)
