"""Full-root trial and explicit pre-fit reference for shoulder adoption."""

from simulation.running import OperatingCurta, StaticBallOperatingCurta
from simulation.running_parts import RetainedCarries
from simulation.counter_shoulder_running_parts import ShoulderRetainedCarries


class OriginalShoulderOperatingCurta(OperatingCurta):
    carry_mechanism = RetainedCarries()


class CounterShoulderOperatingTrial(OperatingCurta):
    carry_mechanism = ShoulderRetainedCarries()


class ShoulderFittedStaticBallReference(StaticBallOperatingCurta):
    """Current shoulder fit with the original static positioning-ball model."""
    carry_mechanism = ShoulderRetainedCarries()
