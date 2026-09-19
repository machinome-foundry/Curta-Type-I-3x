"""Diagnostic assembly, not an adopted reverser stroke or a print correction.

The isolated pinion bench omitted the yoke, shaft and frame stops. This bench
keeps all six input prints, both drum halves and the complete source lever.
All heights are displacements from the STEP pose, never detent spacing used
as an assumed displacement. Knob and gear height are independently adjustable
only to diagnose the operating model's currently disconnected placements.
"""

from machinome.node import AssemblyNode
from machinome.motion.ports import Port
from machinome.motion.joints import Prismatic, Revolute
from machinome.simulation import Driver
from simulation.standard.assembly import ReversingLever1
from simulation.standard.parts import (MainBody, BearingPlate, Part5mmBall,
                                       SelectorKnobSpring)
from simulation.standard.assembly import ReversingLeverKnob1
from simulation.standard.channels import (TurnsOnes, TurnsTens, TurnsHundreds,
    TurnsDigit4, TurnsDigit5, TurnsDigit6)
from simulation.prints import PrintedDrum
from simulation.cycle import tooth_passage, TURNS_INPUT_END
from simulation.fit import INPUT_CLOCKING


class MovingReverser(ReversingLever1):
    displacement = Port(unit='mm')
    reversing_lever_knob_1 = ReversingLeverKnob1(lift=Prismatic(axis=(0, 0, 1)))
    p_5mm_ball = Part5mmBall(lift=Prismatic(axis=(0, 0, 1)))
    selector_knob_spring = SelectorKnobSpring(lift=Prismatic(axis=(0, 0, 1)))
    displacement.drives(reversing_lever_knob_1.lift)
    displacement.drives(p_5mm_ball.lift)
    displacement.drives(selector_knob_spring.lift)

    def render(self):
        super().render()
        # Spacers float on the shaft in the video. Place them at the measured
        # frame seats, with .05 mm seating clearance, not against the knob at
        # the STEP's intermediate pose. The ball's radial following and spring
        # compression remain unmodeled; this bench cannot certify retention.
        self.upper_reversing_lever_spacer.translate((0, 0, 3.9075))
        self.lower_reversing_lever_spacer.translate((0, 0, -7.6427))


def counter_passage(index):
    def factory(sources, target):
        def angle(crank, subtract, reversed_counter):
            complement = subtract + reversed_counter - 2 * subtract * reversed_counter
            count = (1 - complement) * (index == 0) + 9 * complement
            return (130 + INPUT_CLOCKING - 20 * index +
                    72 * tooth_passage(crank, count, TURNS_INPUT_END + 20 * index))
        return angle
    return factory


class ReverserAssemblyBench(AssemblyNode):
    knob_height = Driver(default=0, unit='mm')
    gear_height = Driver(default=4.5, unit='mm')
    crank_angle = Driver(default=0, unit='deg')
    subtract = Driver(default=0, range=(0, 1))
    reversed_counter = Driver(default=0, range=(0, 1))
    lever = MovingReverser()
    upper_frame = MainBody()
    lower_frame = BearingPlate()
    drum = PrintedDrum(turn=Revolute(axis=(0, 0, 1)),
                       lift=Prismatic(axis=(0, 0, 1)))
    ones = TurnsOnes()
    tens = TurnsTens()
    hundreds = TurnsHundreds()
    digit_4 = TurnsDigit4()
    digit_5 = TurnsDigit5()
    digit_6 = TurnsDigit6()

    knob_height.drives(lever.displacement)
    crank_angle.drives(drum.turn, ratio=-1)
    subtract.drives(drum.lift, ratio=9)
    for _index, _channel in enumerate((ones, tens, hundreds, digit_4, digit_5, digit_6)):
        gear_height.drives(_channel.setting, ratio=-1 / 6)
        gear_height.drives(_channel.carry, ratio=0)
        (crank_angle & subtract & reversed_counter).drives(
            _channel.turn, law=counter_passage(_index))
    del _index, _channel

    def render(self):
        self.lower_frame.rotate(180, (1, 0, 0)).translate((0, 0, -118.35))
