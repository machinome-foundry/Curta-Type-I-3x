"""One selectable drum row and its transmission pinion, in the source frame."""

from machinome.node import AssemblyNode
from machinome.motion.joints import Revolute
from machinome.simulation import Driver
from machinome.math import clamp01
from simulation.standard.parts import OneToothStepDrumSegment, TransmissionGear0_5
from simulation.fit import FittedInputPinion


def input_step(source, target):
    return lambda angle: 4 + 72 * clamp01((angle - 113.5) / 11.25)


class InputMesh(AssemblyNode):
    crank_angle = Driver(default=100, range=(100, 140), unit='deg')
    drum_row = OneToothStepDrumSegment(turn=Revolute(axis=(0, 0, 1)))
    pinion = FittedInputPinion(turn=Revolute(axis=(0, 0, 1), at=(40.5, 0, 0)))

    crank_angle.drives(drum_row.turn, ratio=-1)
    crank_angle.drives(pinion.turn, law=input_step)

    def render(self):
        self.drum_row.rotate(170.104082802, (0, 0, 1)).translate((0, 0, -70.8))
        self.pinion.translate((40.5, 0, -70.92499975))
