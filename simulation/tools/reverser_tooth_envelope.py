"""Survey complete installed input prints against both installed drum prints.

Independent pose instrument, not an operating controller or an adopted bound.
One untouched production root supplies the native shapes and published meshes.
Subsequent queries rigidly transform those shapes about their declared axes;
they never modify the retained run. Fixture tests compare real requests first.
"""

import argparse
import json
import logging
from pathlib import Path

from machinome.exact import intersect_shapes
from machinome.simulation import Sim
from simulation.cover_fits import mesh_solid
from simulation.running import OperatingCurta
from simulation.test_reverser_assembly import INPUTS
from simulation.tools.higher_locking_envelope import faceted_common_volume
from simulation.tools.interference import rigid_leaves, world_solids


DRUMS = tuple('Curta.main_drive.stepped_drum.main_axle_step_drum_1.'
              f'main_axle_step_drum_{half}_1' for half in ('top', 'bottom'))


def phase_boundaries(shafts, evaluate, iterations=16):
    """Refine every observed sign change; never assume one contact interval.

    A finite scan cannot exclude islands between samples. Records keep the
    coarse samples and both endpoints, and are not a continuous certificate.
    """
    shafts = tuple(shafts)
    if len(shafts) < 2 or any(a >= b for a, b in zip(shafts, shafts[1:])):
        raise ValueError('Provide at least two strictly increasing shaft samples')
    if not isinstance(iterations, int) or not 0 <= iterations <= 40:
        raise ValueError('Boundary refinement must use 0..40 iterations')

    def read(shaft):
        volumes = evaluate(shaft)
        if any(not isinstance(v, (int, float)) or not 0 <= v < float('inf')
               for v in volumes.values()):
            raise ValueError('Refuse nonfinite or negative common volumes')
        return dict(shaft=shaft, volumes_mm3=volumes,
                    contact=any(v > 0 for v in volumes.values()))

    samples = [read(shaft) for shaft in shafts]
    boundaries = []
    for first, second in zip(samples, samples[1:]):
        if first['contact'] == second['contact']:
            continue
        left, right = first, second
        for _ in range(iterations):
            middle = read((left['shaft']+right['shaft'])/2)
            if middle['contact'] == left['contact']:
                left = middle
            else:
                right = middle
        boundaries.append(dict(left=left, right=right,
                               enters_contact=right['contact']))
    return dict(samples=samples, boundaries=boundaries)


class ToothEnvelopeReader:
    def __init__(self, station=1):
        if station not in range(1, 7):
            raise ValueError('Counter station must be 1..6')
        self.station = station
        name, member = INPUTS[station-1]
        self.gear = f'Curta.transmission.turns.{name}.{member}'
        self.paths = (self.gear, *DRUMS)
        sim = Sim(OperatingCurta(), dt=.1, meshes=True)
        self.initial = sim.snapshot()
        self.bank = dict(sim.state)
        shaft = getattr(sim.node.transmission.turns, name)
        self.axis = tuple(type(shaft).turn.at)
        self.shaft = sim.state[f'transmission.turns.{name}.turn']
        self.height = sim.state['reverser_height']
        self.native = world_solids(sim.node, selected=set(self.paths))
        leaves = dict(rigid_leaves(sim.node))
        self.faceted = {p: mesh_solid(leaves[p].mesh) for p in self.paths}

    def posed(self, crank, shaft, height, lift=0, *, kernel='world64'):
        if kernel not in ('world64', 'native'):
            raise ValueError('Use native or world64')
        angle = shaft-self.shaft
        displacement = height-self.height
        origin = self.axis
        if kernel == 'native':
            tip = (origin[0], origin[1], origin[2]+1)
            gear = self.native[self.gear].rotate(origin, tip, angle).translate(
                (0, 0, displacement))
            drums = {p: self.native[p].rotate((0, 0, 0), (0, 0, 1), -crank).translate(
                (0, 0, lift)) for p in DRUMS}
        else:
            gear = self.faceted[self.gear].translate(tuple(-x for x in origin)).rotate(
                (0, 0, angle)).translate(origin).translate((0, 0, displacement))
            drums = {p: self.faceted[p].rotate((0, 0, -crank)).translate(
                (0, 0, lift)) for p in DRUMS}
        return {self.gear: gear, **drums}

    def volumes(self, crank, shaft, height, lift=0, *, kernel='world64'):
        bodies = self.posed(crank, shaft, height, lift, kernel=kernel)
        values = {}
        for drum in DRUMS:
            if kernel == 'native':
                common = intersect_shapes(bodies[self.gear], bodies[drum], self.gear, drum)
                if not common.isValid():
                    raise ValueError('Invalid native common')
                values[drum] = common.Volume()
            else:
                values[drum] = faceted_common_volume(bodies[self.gear] ^ bodies[drum])
        return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--station', type=int, choices=range(1, 7), default=1)
    parser.add_argument('--crank', type=float, action='append', required=True)
    parser.add_argument('--shaft', type=float, action='append')
    parser.add_argument('--shaft-step', type=float,
                        help='Survey a full 360° shaft revolution from its actual rest')
    parser.add_argument('--height', type=float, action='append', required=True)
    parser.add_argument('--lift', type=float, default=0)
    parser.add_argument('--kernel', choices=('world64', 'native'), default='world64')
    parser.add_argument('--output', type=Path,
                        help='Write a new JSONL evidence file instead of stdout')
    parser.add_argument('--boundaries', action='store_true',
                        help='Retain samples and refine every observed phase transition')
    args = parser.parse_args()
    if args.shaft_step is not None and not 0 < args.shaft_step <= 360:
        parser.error('--shaft-step must be in (0, 360]')
    if args.shaft_step is not None and args.shaft:
        parser.error('Choose explicit shafts or --shaft-step')
    if args.boundaries and args.shaft_step is None and len(args.shaft or ()) < 2:
        parser.error('--boundaries needs --shaft-step or two or more --shaft values')
    if args.output is not None and args.output.exists():
        parser.error(f'Preserve existing evidence: {args.output}')
    reader = ToothEnvelopeReader(args.station)
    shafts = args.shaft or (reader.shaft,)
    if args.shaft_step is not None:
        shafts = [reader.shaft+i*args.shaft_step
                  for i in range(int(360/args.shaft_step)+1)]
        if shafts[-1] < reader.shaft+360:
            shafts.append(reader.shaft+360)
    output = args.output.open('x') if args.output is not None else None
    try:
        for crank in args.crank:
            if args.boundaries:
                for height in args.height:
                    result = phase_boundaries(shafts, lambda shaft: reader.volumes(
                        crank, shaft, height, args.lift, kernel=args.kernel))
                    print(json.dumps(dict(
                        station=args.station, crank=crank, height=height,
                        lift=args.lift, kernel=args.kernel, **result,
                        scope='Complete-print angular samples; unsampled islands not excluded',
                    )), file=output, flush=True)
                continue
            for shaft in shafts:
                for height in args.height:
                    print(json.dumps(dict(
                        station=args.station, crank=crank, shaft=shaft, height=height,
                        lift=args.lift, kernel=args.kernel,
                        volumes_mm3=reader.volumes(crank, shaft, height, args.lift,
                                                   kernel=args.kernel),
                        scope='Independent pose instrument; not a retained request',
                    )), file=output, flush=True)
        if output is not None:
            print(json.dumps(dict(output=str(args.output),
                                  rows=len(args.crank)*len(args.height)*(
                                      1 if args.boundaries else len(shafts)))),
                  flush=True)
    finally:
        if output is not None:
            output.close()


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
