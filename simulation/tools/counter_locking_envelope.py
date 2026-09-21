"""Measure complete counter-print contact intervals, without proposing a law.

Angles are actual machine coordinates. A finite angular grid can miss a
narrow contact island; add samples and independently check any eventual
interpolation before adoption. No positive intersection volume is ignored.
"""

import argparse
import json
import logging

from simulation.tools.counter_lockout_probe import station_reader


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--station', type=int, choices=range(1, 7), required=True)
    parser.add_argument('--shaft', type=float, required=True)
    parser.add_argument('--carry', type=float, default=0)
    parser.add_argument('--step', type=float, default=10)
    parser.add_argument('--sample-angle', type=float, action='append', default=[])
    parser.add_argument('--kernel', choices=('native', 'faceted'), action='append')
    parser.add_argument('--trial', action='store_true')
    args = parser.parse_args()
    if not 0 <= args.carry <= 1 or not 0 < args.step <= 10:
        parser.error('carry must be 0..1 and step must be greater than 0 and at most 10')
    if any(not 0 <= angle <= 360 for angle in args.sample_angle):
        parser.error('sample angles must be 0..360')
    volume = station_reader(args.station, args.carry, args.shaft, trial=args.trial)
    angles = sorted({0, 360, *args.sample_angle} |
                    {args.step*i for i in range(int(360/args.step)+1)})
    for kernel in args.kernel or ('native', 'faceted'):
        samples = [(angle, volume(angle, kernel)) for angle in angles]
        boundaries = []
        for (left, vl), (right, vr) in zip(samples, samples[1:]):
            if (vl > 0) == (vr > 0):
                continue
            enters = vr > 0
            for _ in range(18):
                middle = (left+right)/2
                if (volume(middle, kernel) > 0) == enters:
                    right = middle
                else:
                    left = middle
            boundaries.append({'left': left, 'right': right, 'enters_contact': enters})
        print(json.dumps({
            'station': args.station, 'shaft': args.shaft, 'carry': args.carry,
            'trial': args.trial, 'kernel': kernel, 'step': args.step,
            'samples': samples, 'boundaries': boundaries,
        }), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
