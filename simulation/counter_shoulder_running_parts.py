"""Retained carry bindings with only the five shoulder shapes substituted."""

from simulation.running_parts import RetainedCarries, RetainedTurnsCarries, retained_lever
from simulation import shoulder_carry_frames as framed


class ShoulderRetainedTurnsCarries(RetainedTurnsCarries):
    turns_tens_lever_assembly_1 = retained_lever(framed.TurnsLever1, -1.8, True)()
    turns_tens_lever_assembly_2 = retained_lever(framed.TurnsLever2, -1.8, True)()
    turns_tens_lever_assembly_3 = retained_lever(framed.TurnsLever3, -1.8, True)()
    turns_tens_lever_assembly_4 = retained_lever(framed.TurnsLever4, -1.8, True)()
    turns_tens_lever_assembly_5 = retained_lever(framed.TurnsLever5, -1.8, True)()


class ShoulderRetainedCarries(RetainedCarries):
    turns_carries = ShoulderRetainedTurnsCarries()
