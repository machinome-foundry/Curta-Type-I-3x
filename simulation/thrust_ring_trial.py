"""Ring/support fixture using the current operating collar, not an older print."""

from machinome.motion.joints import Prismatic, Revolute
from simulation.operating_collar_parts import SeatedCollar
from simulation.thrust_seat_trial import SeatedThrustBench
from simulation.thrust_ring_parts import BallPassageThrustRing
from simulation.positioning_ball_trial import RadialBallTrial, RadialCarriageTrial, RadialPositioningTrial
from simulation.positioning import SeatedCarriagePositioning, RadialCarriagePositioning
from simulation.standard.parts import ThrustRing
from simulation.running import OperatingCurta, StaticBallOperatingCurta, RunningCarriage, RadialRunningCarriage


class InstalledThrustBench(SeatedThrustBench):
    collar = SeatedCollar(lift=Prismatic(axis=(0, 0, 1)),
                          turn=Revolute(axis=(0, 0, 1)))

    def render(self):
        super().render()
        self.collar.rotate(54.282220532, (0, 0, 1))


class FittedThrustBench(InstalledThrustBench):
    thrust_ring = BallPassageThrustRing(slide=Prismatic(axis=(0, 0, 1)))


class FittedRadialPositioningTrial(RadialPositioningTrial):
    thrust_ring = BallPassageThrustRing(slide=Prismatic(axis=(0, 0, 1)))


class FittedRadialCarriageTrial(RadialCarriageTrial):
    positioning = FittedRadialPositioningTrial()


class FittedRadialBallTrial(RadialBallTrial):
    carriage = FittedRadialCarriageTrial()


class OriginalRingPositioning(SeatedCarriagePositioning):
    thrust_ring = ThrustRing(slide=Prismatic(axis=(0, 0, 1)))


class OriginalRingCarriage(RunningCarriage):
    positioning = OriginalRingPositioning()


class OriginalRingOperatingReference(StaticBallOperatingCurta):
    carriage = OriginalRingCarriage()


class FittedRingPositioning(SeatedCarriagePositioning):
    thrust_ring = BallPassageThrustRing(slide=Prismatic(axis=(0, 0, 1)))


class FittedRingCarriage(RunningCarriage):
    positioning = FittedRingPositioning()


class FittedRingOperatingTrial(StaticBallOperatingCurta):
    carriage = FittedRingCarriage()


class OriginalRingRadialPositioning(RadialCarriagePositioning):
    thrust_ring = ThrustRing(slide=Prismatic(axis=(0, 0, 1)))


class OriginalRingRadialCarriage(RadialRunningCarriage):
    positioning = OriginalRingRadialPositioning()


class OriginalRingRadialOperatingReference(OperatingCurta):
    carriage = OriginalRingRadialCarriage()
