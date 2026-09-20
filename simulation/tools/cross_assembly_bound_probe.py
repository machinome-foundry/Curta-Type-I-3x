"""Public-API reproduction of Curta's cross-assembly lockout constraint.

The simplified numeric bound is only a scope probe, not a mechanical law.
No framework internals or viewer APIs are used.
"""

import json
from machinome.node import AssemblyNode
from machinome.motion.joints import Revolute, Bound
from machinome.motion.ports import Port, Time
from machinome.simulation import Driver, Sim
from simulation.standard.parts import ResultsLockingDisc, TensBellSupportPlate
from simulation.fit import FittedCarryLockout


class Shaft(AssemblyNode):
    turn = Revolute(axis=(0, 0, 1))
    lockout = FittedCarryLockout()


class RelayedDrive(AssemblyNode):
    shaft_phase = Port(unit='deg')
    fixed_support = TensBellSupportPlate()
    disc = ResultsLockingDisc(turn=Revolute(axis=(0, 0, 1), range=(None, Bound(
        lambda turn, phase: 120+phase, reads=(shaft_phase,)))))


class NestedDrive(AssemblyNode):
    fixed_support = TensBellSupportPlate()
    disc = ResultsLockingDisc(turn=Revolute(axis=(0, 0, 1)))


class RelayedMachine(AssemblyNode):
    time = Time.running()
    crank = Driver(default=0)
    phase = Driver(default=4)
    drive = RelayedDrive()
    shaft = Shaft()
    crank.drives(drive.disc.turn)
    phase.drives(shaft.turn)
    shaft.turn.drives(drive.shaft_phase)


class FlatMachine(AssemblyNode):
    """Positive control: both actual joints are reachable at one declarer."""
    time = Time.running()
    crank = Driver(default=0)
    phase = Driver(default=4)
    shaft = Shaft()
    disc = ResultsLockingDisc(turn=Revolute(axis=(0, 0, 1), range=(None, Bound(
        lambda turn, phase: 120+phase, reads=(shaft.turn,)))))
    crank.drives(disc.turn)
    phase.drives(shaft.turn)


def main():
    flat = Sim(FlatMachine(), dt=.1)
    command = flat.move('crank', to=150)
    assert command.status == 'blocked' and flat.state['disc.turn'] == 124
    print(json.dumps({'route': 'flat positive control', 'status': command.status,
                      'disc_turn': flat.state['disc.turn']}), flush=True)
    try:
        class DirectDrive(AssemblyNode):
            fixed_support = TensBellSupportPlate()
            disc = ResultsLockingDisc(turn=Revolute(axis=(0, 0, 1), range=(None, Bound(
                lambda turn, phase: 120+phase, reads=(Shaft.turn,)))))
        print(json.dumps({'route': 'sibling class reference', 'constructed': True}))
    except Exception as error:
        print(json.dumps({'route': 'sibling class reference',
                          'error': type(error).__name__, 'message': str(error)}), flush=True)
    try:
        Sim(RelayedMachine(), dt=.1)
        print(json.dumps({'route': 'public port relay', 'constructed': True}))
    except Exception as error:
        print(json.dumps({'route': 'public port relay',
                          'error': type(error).__name__, 'message': str(error)}), flush=True)
    try:
        class ParentOverride(AssemblyNode):
            shaft = Shaft()
            drive = NestedDrive(disc=ResultsLockingDisc(turn=Revolute(
                axis=(0, 0, 1), range=(None, Bound(
                    lambda turn, phase: 120+phase, reads=(shaft.turn,))))))
        ParentOverride()
        print(json.dumps({'route': 'ancestor child override', 'constructed': True}))
    except Exception as error:
        print(json.dumps({'route': 'ancestor child override',
                          'error': type(error).__name__, 'message': str(error)}), flush=True)


if __name__ == '__main__':
    main()
