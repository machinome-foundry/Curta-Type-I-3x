"""All five fitted counter stations, without changing production geometry."""

from machinome.motion.joints import Prismatic
from simulation.standard import carry
from simulation.carry_bank_frame import FittedCarryBankFrameBench
from simulation.counter_guide_shoulder import ShoulderClearedTurnsSlider


class TurnsLever1(carry.TurnsLever1):
    tens_slider_for_turns_counter = ShoulderClearedTurnsSlider(travel=Prismatic(axis=(0, 0, -1)))


class TurnsLever2(carry.TurnsLever2):
    tens_slider_for_turns_counter = ShoulderClearedTurnsSlider(travel=Prismatic(axis=(0, 0, -1)))


class TurnsLever3(carry.TurnsLever3):
    tens_slider_for_turns_counter = ShoulderClearedTurnsSlider(travel=Prismatic(axis=(0, 0, -1)))


class TurnsLever4(carry.TurnsLever4):
    tens_slider_for_turns_counter = ShoulderClearedTurnsSlider(travel=Prismatic(axis=(0, 0, -1)))


class TurnsLever5(carry.TurnsLever5):
    tens_slider_for_turns_counter = ShoulderClearedTurnsSlider(travel=Prismatic(axis=(0, 0, -1)))


class ShoulderTurnsCarry(carry.TurnsCarry):
    turns_tens_lever_assembly_1 = TurnsLever1()
    turns_tens_lever_assembly_2 = TurnsLever2()
    turns_tens_lever_assembly_3 = TurnsLever3()
    turns_tens_lever_assembly_4 = TurnsLever4()
    turns_tens_lever_assembly_5 = TurnsLever5()


class CounterShoulderTrial(FittedCarryBankFrameBench):
    turns_carries = ShoulderTurnsCarry()


def insufficient_lever(base):
    class InsufficientLever(base):
        tens_slider_for_turns_counter = ShoulderClearedTurnsSlider(
            shoulder_relief=.2, travel=Prismatic(axis=(0, 0, -1)))
    return InsufficientLever


class InsufficientTurnsCarry(carry.TurnsCarry):
    turns_tens_lever_assembly_1 = insufficient_lever(carry.TurnsLever1)()
    turns_tens_lever_assembly_2 = insufficient_lever(carry.TurnsLever2)()
    turns_tens_lever_assembly_3 = insufficient_lever(carry.TurnsLever3)()
    turns_tens_lever_assembly_4 = insufficient_lever(carry.TurnsLever4)()
    turns_tens_lever_assembly_5 = insufficient_lever(carry.TurnsLever5)()


class InsufficientCounterShoulderTrial(FittedCarryBankFrameBench):
    turns_carries = InsufficientTurnsCarry()
