"""Diagnostic: does the source reversing stroke actually select nine teeth?

This pose bench does not change the operating model or fit the source shaft.
Its stroke is the knob/yoke displacement from the verified normal-counter pose.
"""

from machinome.node import AssemblyNode
from machinome.motion.joints import Revolute, Prismatic
from machinome.parameters import Length
from machinome.simulation import Driver
from simulation.cycle import tooth_passage, TURNS_INPUT_END
from simulation.fit import INPUT_CLOCKING, FittedCounterPinion
from simulation.prints import PrintedDrum


def reversed_counter_motion(sources, target):
    return lambda angle, subtract: (130 + INPUT_CLOCKING - 20
        + 72 * tooth_passage(angle, 9 * (1 - subtract), TURNS_INPUT_END + 20))


class CounterReversalBench(AssemblyNode):
    stroke = Length(12, min=0)
    crank_angle = Driver(default=101.25, range=(0, 360), unit='deg')
    subtract = Driver(default=0, range=(0, 1))
    drum = PrintedDrum(turn=Revolute(axis=(0, 0, 1)),
                       lift=Prismatic(axis=(0, 0, 1)))
    counter = FittedCounterPinion(turn=Revolute(
        axis=(0, 0, 1), at=(-13.851815805, 38.057551142, 0)))
    crank_angle.drives(drum.turn, ratio=-1)
    subtract.drives(drum.lift, ratio=9)
    (crank_angle & subtract).drives(counter.turn, law=reversed_counter_motion)

    def render(self):
        self.counter.translate((-13.851815805, 38.057551142, -40.35 - self.stroke))
