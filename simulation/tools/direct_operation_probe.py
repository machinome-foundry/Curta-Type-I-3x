"""Public-API probes for the direct-operation migration; no geometry changes.

Run from the project root with the workspace Python. The first probe confirms
the independent crank freedoms. The second isolates a clearing wheel whose
missing tooth must disengage the rack at zero, from its retained wheel angle.
These are capability diagnostics, not mechanical acceptance tests.
"""

import json

from machinome.math import floor
from machinome.motion.joints import Prismatic, Revolute
from machinome.motion.ports import Time
from machinome.node import AssemblyNode
from machinome.parameters import Angle
from machinome.simulation import Button, Driver, Instruction, Sim, Slide, Turn


class Crank(AssemblyNode):
    rotation = Revolute(axis=(0, 0, 1))
    elevation = Prismatic(axis=(0, 0, 1), range=(0, 9))


class CrankControls(AssemblyNode):
    time = Time.running()
    crank_rotation = Driver(default=0, unit='deg')
    crank_elevation = Driver(default=0, unit='mm')
    crank = Crank()
    crank_rotation.drives(crank.rotation)
    crank_elevation.drives(crank.elevation)
    instructions = {'Turn once': Instruction(by={'crank_rotation': -360}, duration=1)}
    controls = {
        'turn': Turn(crank, crank_rotation, coordinate=crank.rotation),
        'lift': Slide(crank, crank_elevation, coordinate=crank.elevation),
        'revolution': Button(crank, 'Turn once', coordinate=crank.rotation),
    }


class ClearingWheel(AssemblyNode):
    initial_angle = Angle(108)
    rotation = Revolute(axis=(0, 0, 1))

    def simulate(self):
        if self.rotation.value is None:
            self.rotation = self.initial_angle


def missing_tooth(sources, target):
    # ADR-121 requires a finite band, entered from either side. The half-degree
    # width is deliberately schematic, not the Curta's measured tooth clearance.
    def law(rack, wheel):
        shifted = wheel + .5
        return rack * (shifted - 360 * floor(shifted / 360) >= 1)
    return law


def clearing_fixture(initial_angle=108):
    class Clearing(AssemblyNode):
        time = Time.running()
        rack = Driver(default=0, unit='deg')
        wheel = ClearingWheel(initial_angle=initial_angle)
        (rack & wheel.rotation).drives(wheel.rotation, law=missing_tooth)

    return Clearing()


def probe():
    sim = Sim(CrankControls(), dt=.02)
    lift = sim.move('crank_elevation', to=9)
    command, = sim.trigger('Turn once')
    sim.run(1)
    result = {
        'selected_crank_controls': {
            'lift': sim.state['crank.elevation'],
            'rotation': sim.state['crank.rotation'],
            'statuses': [lift.status, command.status],
        },
    }
    try:
        Sim(clearing_fixture(), dt=.02)
    except (TypeError, ValueError, RuntimeError) as error:
        result['retained_wheel_engagement'] = {
            'error': type(error).__name__, 'message': str(error),
        }
    else:
        result['retained_wheel_engagement'] = {'constructed': True}
    return result


if __name__ == '__main__':
    print(json.dumps(probe(), indent=2))
