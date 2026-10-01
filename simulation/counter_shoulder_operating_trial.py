"""Full-root trial and explicit pre-fit reference for shoulder adoption."""

from simulation.mechanistic import MechanisticCurta, StaticBallOperatingCurta
from simulation.running_parts import RetainedCarries
from simulation.counter_shoulder_running_parts import ShoulderRetainedCarries


class OriginalShoulderOperatingCurta(MechanisticCurta):
    carry_mechanism = RetainedCarries()


class CounterShoulderOperatingTrial(MechanisticCurta):
    carry_mechanism = ShoulderRetainedCarries()


class ShoulderFittedStaticBallReference(StaticBallOperatingCurta):
    """Current shoulder fit with the original static positioning-ball model."""
    carry_mechanism = ShoulderRetainedCarries()
