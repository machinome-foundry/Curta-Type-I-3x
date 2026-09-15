"""Public-API probes for the direct-operation migration; no geometry changes.

Run from the project root with the workspace Python. The first probe confirms
the independent crank freedoms. The second isolates a clearing wheel whose
missing tooth must disengage the rack at zero, from its retained wheel angle.
These are capability diagnostics, not mechanical acceptance tests.
"""

import json

from solid_node.motion.joints import Prismatic, Revolute
from solid_node.motion.ports import Time
from solid_node.node import AssemblyNode
from solid_node.simulation import Button, Driver, Instruction, Sim, Slide, Turn


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
    rotation = Revolute(axis=(0, 0, 1))

    def simulate(self):
        if self.rotation.value is None:
            self.rotation = 108  # A three at the start of this reduced fixture.


def missing_tooth(sources, target):
    # Deliberately reduced to the engagement question. This is not the Curta's
    # measured tooth profile: rack travel stops contributing at the zero gap.
    return lambda rack, wheel: rack * (wheel % 360 < 359)


def clearing_fixture():
    class Clearing(AssemblyNode):
        time = Time.running()
        rack = Driver(default=0, unit='deg')
        wheel = ClearingWheel()
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
