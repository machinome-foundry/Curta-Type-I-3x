"""Measure complete counter-print contact intervals, without proposing a law.

Angles are actual machine coordinates. A finite angular grid can miss a
narrow contact island; add samples and independently check any eventual
interpolation before adoption. No positive intersection volume is ignored.
"""

import argparse
import json
import logging
import math

from simulation.tools.counter_lockout_probe import station_reader


def indexed_bands(station, carry, *, crank=0, trial=False):
    """Bracket complete-print clearance around all five source shaft flats.

    The bracket width is angular measurement resolution, not a volume epsilon.
    Both endpoint volumes are retained so an absent flank or blocked centre
    cannot be reported as a successful free-band measurement.
    """
    for flat in range(5):
        centre = 134-20*(station-1)+72*flat
        readers = {}

        def at(shaft, kernel):
            if shaft not in readers:
                readers[shaft] = station_reader(
                    station, carry, shaft, reference=crank, trial=trial)
            volume = readers[shaft](crank, kernel)
            if not math.isfinite(volume):
                raise ValueError(f'non-finite common at shaft {shaft}, {kernel}')
            return volume

        for kernel in ('native', 'faceted'):
            if at(centre, kernel) > 0:
                raise ValueError(f'indexed position {centre} has contact in {kernel}')
            bounds = []
            for direction in (-1, 1):
                free, contact = centre, centre+5*direction
                if at(contact, kernel) <= 0:
                    raise ValueError(f'outer bracket {contact} has no contact in {kernel}')
                for _ in range(18):
                    middle = (free+contact)/2
                    if at(middle, kernel) > 0:
                        contact = middle
                    else:
                        free = middle
                bounds.append({'last_free': free, 'first_contact': contact,
                               'free_mm3': at(free, kernel),
                               'contact_mm3': at(contact, kernel)})
            yield {'station': station, 'carry': carry, 'crank': crank,
                   'trial': trial, 'kernel': kernel, 'index': centre,
                   'bounds': bounds}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--station', type=int, choices=range(1, 7), required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--shaft', type=float)
    mode.add_argument('--bands', action='store_true',
                      help='Bracket the five indexed free bands at --crank.')
    parser.add_argument('--crank', type=float, default=0)
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
    if args.bands:
        if not 0 <= args.crank <= 360:
            parser.error('crank must be 0..360')
        if args.kernel or args.sample_angle:
            parser.error('--bands measures both kernels and does not use --sample-angle')
        for record in indexed_bands(args.station, args.carry,
                                    crank=args.crank, trial=args.trial):
            print(json.dumps(record), flush=True)
        return
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
