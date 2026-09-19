"""Reduce operating-carriage bank/pose disagreement using public interfaces."""

import json
import argparse
from machinome.node import AssemblyNode
from machinome.motion.joints import Revolute
from machinome.motion.ports import Time
from machinome.simulation import Driver, Sim


class HeldWheel(AssemblyNode):
    def simulate(self):
        if self.turn.value is None:
            self.turn = -146


class NestedRing(AssemblyNode):
    wheel = HeldWheel(turn=Revolute(axis=(1, 0, 0)))


class NestedCarrier(AssemblyNode):
    ring = NestedRing(turn=Revolute(axis=(0, 0, 1)))


class NestedPoseProbe(AssemblyNode):
    time = Time.running()
    rotation = Driver(default=0)
    clearing = Driver(default=0)
    carrier = NestedCarrier(turn=Revolute(axis=(0, 0, 1)))
    rotation.drives(carrier.turn)
    clearing.drives(carrier.ring.turn, ratio=-1)


def minimal_probe():
    node = NestedPoseProbe()
    sim = Sim(node, dt=.1)
    joints = {'carrier.turn': node.carrier.turn,
              'carrier.ring.turn': node.carrier.ring.turn,
              'carrier.ring.wheel.turn': node.carrier.ring.wheel.turn}
    for driver, value in ((None, 0), ('rotation', 20), ('clearing', 90)):
        if driver:
            sim.move(driver, to=value)
        print(json.dumps({'request': [driver, value], 'coordinates': {
            key: {'bank': sim.state[key], 'pose': joint.value}
            for key, joint in joints.items()}}), flush=True)


def probe():
    # The framework-only reduction does not import the complete Curta graph.
    from simulation.running import RunningCarriage

    class CarriagePoseProbe(AssemblyNode):
        time = Time.running()
        elevation = Driver(default=0)
        rotation = Driver(default=0)
        clearing = Driver(default=0)
        stationary_markers = Driver(default=0)
        carriage = RunningCarriage()
        elevation.drives(carriage.registers.lift)
        rotation.drives(carriage.registers.turn)
        clearing.drives(carriage.registers.clearing_ring.turn, ratio=-1)
        for _index in range(6, 11):
            stationary_markers.drives(getattr(carriage.registers.clearing_ring.decimal_markers,
                                             f'decimal_marker_{_index}').turn)
        del _index

    node = CarriagePoseProbe()
    sim = Sim(node, dt=.1)
    joints = {
        'carriage.registers.turn': node.carriage.registers.turn,
        'carriage.registers.clearing_ring.turn': node.carriage.registers.clearing_ring.turn,
        'carriage.registers.result_register.p_10203_1.turn':
            node.carriage.registers.result_register.p_10203_1.turn,
    }
    for driver, value in ((None, 0), ('elevation', 6), ('rotation', 20), ('clearing', 90)):
        if driver:
            sim.move(driver, to=value)
        print(json.dumps({'request': [driver, value], 'coordinates': {
            key: {'bank': sim.state[key], 'pose': joint.value}
            for key, joint in joints.items()}}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--minimal', action='store_true')
    args = parser.parse_args()
    minimal_probe() if args.minimal else probe()
