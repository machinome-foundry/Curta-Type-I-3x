"""Original contact bench with only the isolated counter shoulder fitted."""

from simulation.carry_contact import CarryContactBench
from simulation.counter_guide_trial import TurnsLever1


class CounterShoulderContactBench(CarryContactBench):
    turns_lever = TurnsLever1()
