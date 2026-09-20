"""Selectable, stripped inspection of the unresolved counter-reverser fit.

No new solids or print corrections. The full diagnostic remains in
reverser_assembly.py. This view retains its upper drum, tens input print,
fork, shaft and ball; omitted neighbours are NOT certified clear.

The pinion is deliberately NOT driven by the drum: prescribed rotation
would look like successful engagement even with a gap. Inputs position
parts, without collision response. Ball radial following is unmodeled.
"""

from machinome.node import AssemblyNode
from machinome.motion.joints import Prismatic, Revolute
from machinome.simulation import Driver, Instruction
from simulation.standard.assembly import ReversingLever1
from simulation.standard.parts import Part5mmBall, ReversingActuator
from simulation.standard.printed import MainAxleStepDrumTop1, Part10230_410008_1_419080


class DetentReference(ReversingLever1):
    """Source shaft and axially positioned ball, not a spring/contact law."""
    p_5mm_ball = Part5mmBall(lift=Prismatic(axis=(0, 0, 1)), name='ball')

    def render(self):
        super().render()
        self.reversing_lever_knob_1.omit()
        self.selector_knob_spring.omit()
        self.upper_reversing_lever_spacer.omit()
        self.lower_reversing_lever_spacer.omit()


class ReverserInspection(AssemblyNode):
    lever_height = Driver(default=-6.8425, range=(-7, 5.2), unit='mm')
    gear_offset = Driver(default=.185, range=(0, 2), unit='mm')
    drum_angle = Driver(default=101.25, range=(0, 360), unit='deg')
    pinion_probe = Driver(default=0, range=(-18, 18), unit='deg')

    drum = MainAxleStepDrumTop1(turn=Revolute(axis=(0, 0, 1)))
    pinion = Part10230_410008_1_419080(
        turn=Revolute(axis=(0, 0, 1), at=(-13.851815805, 38.057551142, 0)),
        lift=Prismatic(axis=(0, 0, 1)))
    fork = ReversingActuator(lift=Prismatic(axis=(0, 0, 1)))
    detent = DetentReference()

    (lever_height & gear_offset).drives(
        pinion.lift, law=lambda sources, target: lambda height, offset: height + offset)
    lever_height.drives(fork.lift)
    lever_height.drives(detent.p_5mm_ball.lift)
    drum_angle.drives(drum.turn, ratio=-1)
    # Same tens-channel clocking as the complete bench at crank 101.25,
    # normal drum height, reversed counter. The probe is an independent turn.
    pinion_probe.drives(pinion.turn, offset=155.6)

    instructions = {
        'Lower centre': Instruction(
            {'lever_height': -6.8425, 'gear_offset': 0,
             'drum_angle': 101.25, 'pinion_probe': 0}, duration=.2),
        'Best slot play': Instruction(
            {'lever_height': -6.8425, 'gear_offset': .185,
             'drum_angle': 101.25, 'pinion_probe': 0}, duration=.2),
        'Align teeth - unseated': Instruction(
            {'lever_height': -5.035, 'gear_offset': .185,
             'drum_angle': 101.25, 'pinion_probe': 0}, duration=.2),
        'Probe -12 deg': Instruction({'pinion_probe': -12}, duration=.2),
        'Probe zero': Instruction({'pinion_probe': 0}, duration=.2),
    }

    def render(self):
        # Unchanged source knob/actuator placement; the opaque knob is omitted.
        self.fork.rotate(-20, (0, 0, 1))
        self.fork.translate((-1.88117949, .647742044, -44.0075))
