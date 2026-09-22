"""Rejected orbit candidate retained as a negative whole-machine control.

It clears the bell but collides with the stationary frame. Never selected by
the project manifest or adopted as the operating positioning assembly.
"""

from machinome.motion.joints import Revolute
from simulation.positioning import SeatedCarriagePositioning
from simulation.standard.parts import Part6mmBall419094
from simulation.running import OperatingCurta, RunningCarriage


class OrbitPositioningTrial(SeatedCarriagePositioning):
    p_6mm_ball_419094 = Part6mmBall419094(turn=Revolute(axis=(0, 0, 1)))


class OrbitCarriageTrial(RunningCarriage):
    positioning = OrbitPositioningTrial()


class OrbitingBallTrial(OperatingCurta):
    carriage = OrbitCarriageTrial()
    OperatingCurta.carry_mechanism.tens_bell.turn.drives(
        carriage.positioning.p_6mm_ball_419094.turn)
