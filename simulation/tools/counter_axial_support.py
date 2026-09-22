"""Bracket a complete higher-counter print's axial contact entry or exit.

Uses each independently posed source bench, not a translated surrogate.
The finite height grid screens for multiple transitions; it is not a proof
against narrower contact islands or a proposed operating restraint.
"""

import argparse
import json
import logging
import math

from simulation.tools.counter_lockout_probe import station_reader


def axial_boundary(station, shaft, crank, *, trial=False, world_precision=64):
    if station not in range(2, 7):
        raise ValueError('axial support requires a sliding counter station 2..6')
    readers = {}

    def at(carry, kernel):
        if carry not in readers:
            readers[carry] = station_reader(station, carry, shaft, reference=crank, trial=trial,
                                            world_precision=world_precision)
        volume = readers[carry](crank, kernel)
        if not math.isfinite(volume):
            raise ValueError('non-finite common in axial measurement')
        return volume

    for kernel in ('native', 'faceted'):
        samples = [(i/16, at(i/16, kernel)) for i in range(17)]
        changes = [(left, right, vr > 0)
                   for (left, vl), (right, vr) in zip(samples, samples[1:])
                   if (vl > 0) != (vr > 0)]
        if len(changes) != 1:
            raise ValueError(f'expected one sampled axial transition, got {len(changes)}')
        left, right, enters = changes[0]
        for _ in range(20):
            middle = (left+right)/2
            if (at(middle, kernel) > 0) == enters:
                right = middle
            else:
                left = middle
        yield {'station': station, 'shaft': shaft, 'crank': crank, 'trial': trial,
               'world_precision_bits': world_precision,
               'kernel': kernel, 'samples': samples, 'enters_contact': enters,
               'left': left, 'right': right, 'left_mm3': at(left, kernel),
               'right_mm3': at(right, kernel),
               'travel_bracket': [-1.8+4.2*left, -1.8+4.2*right]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--station', type=int, choices=range(2, 7), required=True)
    parser.add_argument('--shaft', type=float, required=True)
    parser.add_argument('--crank', type=float, required=True)
    parser.add_argument('--trial', action='store_true')
    parser.add_argument('--world-precision', type=int, choices=(32, 64), default=64)
    args = parser.parse_args()
    for record in axial_boundary(args.station, args.shaft, args.crank, trial=args.trial,
                                 world_precision=args.world_precision):
        print(json.dumps(record), flush=True)
    print(json.dumps({'complete': True, 'station': args.station,
                      'shaft': args.shaft, 'crank': args.crank, 'kernels': 2}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
