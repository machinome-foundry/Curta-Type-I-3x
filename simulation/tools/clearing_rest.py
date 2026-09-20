"""Small public-API reproduction of bidirectional cam-following at a rest."""

import argparse
import json
from machinome.node import AssemblyNode
from machinome.motion.joints import Bound, Prismatic, Revolute
from machinome.motion.ports import Time
from machinome.math import max, piecewise
from machinome.simulation import Driver, Sim
from simulation.clearing_stop_motion import following, PIN_DROP


class Pin(AssemblyNode):
    slide = Prismatic(axis=(0, 0, -1))


class Ring(AssemblyNode):
    turn = Revolute(axis=(0, 0, 1))


class Carrier(AssemblyNode):
    pin = Pin()
    ring = Ring()
    lift = Prismatic(axis=(0, 0, 1), range=(
        Bound(lambda own, drop: max(0, drop - 3.09), reads=(pin.slide,)), 6))
    follower = ring.turn.drives(pin.slide, law=following)


class Bench(AssemblyNode):
    time = Time.running()
    sweep = Driver(default=0)
    elevation = Driver(default=0)
    carrier = Carrier()
    sweep.drives(carrier.ring.turn, ratio=-1)
    elevation.drives(carrier.lift)


class RawRemainderCarrier(Carrier):
    follower = Carrier.ring.turn.drives(Carrier.pin.slide,
        law=lambda source, target: lambda turn: piecewise((-turn) % 360, PIN_DROP))


class RawRemainderBench(Bench):
    carrier = RawRemainderCarrier()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-remainder', action='store_true',
                        help='Reproduce the rejected negative-phase expression without editing production')
    args = parser.parse_args()
    sim = Sim(RawRemainderBench() if args.raw_remainder else Bench(), dt=.1)
    for rest in (0, 230, 360):
        for direction in (-1, 1):
            sim.move('elevation', to=6)
            sim.move('sweep', to=rest)
            sim.move('elevation', to=0)
            initial = dict(sim.state)
            command = sim.move('sweep', to=rest + direction * 90, duration=.2)
            sim.run(.2)
            print(json.dumps({'rest': rest, 'direction': direction,
                              'status': command.status, 'before': initial,
                              'after': dict(sim.state)}), flush=True)
