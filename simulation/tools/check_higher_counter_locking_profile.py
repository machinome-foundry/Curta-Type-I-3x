"""Challenge higher-counter candidate admission on both complete printed bodies.

This is finite geometric evidence for the selected station, not continuous
certification or an operating adoption. False stops are tested separately against
measured free poses and ordinary paths; an angular stand-off intentionally
refuses some physically clear poses near contact.
"""

import argparse
import hashlib
import json
import logging
import math
from pathlib import Path

from machinome.math import piecewise
from simulation.counter_locking_profiles import SECTORS
from simulation.higher_counter_locking_profiles import LOWER_LOCK_SECTORS, CARRY_TOOTH_STRIPS
from simulation.higher_counter_locking_laws import higher_counter_contact_gap
from simulation.tools.counter_lockout_probe import station_reader


PROFILE_SETS = ((SECTORS, 20), (LOWER_LOCK_SECTORS, 0), (CARRY_TOOTH_STRIPS, 0))


def sample_carries(*, supports=False):
    if not supports:
        return (0, .5, 1)
    heights = {0, .25, .5, .75, 1}
    for travel in (-.6, .3, .9):
        heights.update((travel+offset+1.8)/4.2 for offset in (-.001, 0, .001))
    evidence = Path(__file__).resolve().parents[1]/'docs/evidence'
    data = json.loads((evidence/'counter-tens-contact-support-2026-09-21.json').read_text())
    for support in data['axial_supports']:
        for row in support['measurements']:
            if (row['station'] != 2 or row['trial'] is not True
                    or row['kernel'] not in ('native', 'faceted')
                    or not 0 <= row['left'] < row['right'] <= 1):
                raise ValueError('Requires measured trial counter-tens support brackets')
            heights.update((row['left'], row['right'], (row['left']+row['right'])/2))
    return tuple(sorted(heights))


def rejected_poses():
    evidence = Path(__file__).resolve().parents[1]/'docs/evidence'
    return {(row['shaft'], row['crank'])
            for path in evidence.glob('higher-counter-*-profile-rejection-*.json')
            for records in (json.loads(path.read_text()),)
            for category in ('false_stops', 'admitted_collisions')
            for row in records.get(category, [])}


def sample_shafts(*, dense=False):
    shafts = set(range(114, 475, 1 if dense else 6))
    shafts.update(shaft for shaft, _ in rejected_poses())
    for profiles, shift in PROFILE_SETS:
        for start, end, points in profiles:
            shafts.update(p[0]-shift for p in points)
            shafts.update((a[0]+b[0])/2-shift for a, b in zip(points, points[1:]))
            shafts.update(edge-shift+offset for edge in (start, end) for offset in (-.001, 0, .001))
    return shafts


def sample_angles(shaft, *, dense=False):
    angles = {0., 90., 140., 180., 195., 200., 205., 210., 215., 220., 270., 360.}
    if dense:
        angles.update(range(0, 361, 5))
    angles.update(crank for failed_shaft, crank in rejected_poses() if failed_shaft == shaft)
    normalized = (shaft-114) % 360+114
    for profiles, shift in PROFILE_SETS:
        for start, end, points in profiles:
            if not start <= normalized+shift <= end:
                continue
            for column in (1, 2):
                boundary = piecewise(normalized+shift, [(p[0], p[column]) for p in points])+shift
                angles.update(boundary+offset for offset in (-.101, -.1, 0, .1, .101))
    return angles


def admitted_contacts(volume, carry, shaft, kernel, *, angles, station=2):
    if station not in range(2, 7):
        raise ValueError('Choose a sliding higher-counter station 2..6')
    shift = 20*(station-2)
    for crank in sorted(angles):
        gap = higher_counter_contact_gap(crank-shift, shaft+shift, -1.8+4.2*carry)
        if not math.isfinite(gap):
            raise ValueError(f'Non-finite candidate gap at {carry}, {shaft}, {crank}')
        if gap > 0:
            continue
        common = volume(crank, kernel)
        if not math.isfinite(common) or common < 0:
            raise ValueError(f'Invalid complete-print common at {carry}, {shaft}, {crank}: {common}')
        yield {'station': station, 'carry': carry, 'shaft': shaft, 'crank': crank, 'kernel': kernel,
               'gap': gap, 'common_mm3': common, 'failure': common > 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--station', type=int, choices=range(2, 7), default=2)
    parser.add_argument('--kernel', choices=('native', 'faceted'), required=True)
    carry_group = parser.add_mutually_exclusive_group()
    carry_group.add_argument('--carry', type=float, action='append')
    carry_group.add_argument('--support-heights', action='store_true',
                             help='Include intermediate heights and measured axial-support brackets')
    parser.add_argument('--shaft', type=float, action='append',
                        help='Limit a diagnostic to explicit shafts; not the full matrix')
    parser.add_argument('--dense', action='store_true')
    args = parser.parse_args()
    carries = args.carry if args.carry is not None else sample_carries(supports=args.support_heights)
    if any(not math.isfinite(carry) or not 0 <= carry <= 1 for carry in carries):
        parser.error('carry must be finite and within 0..1')
    if args.shaft and any(not math.isfinite(shaft) for shaft in args.shaft):
        parser.error('shaft must be finite')
    source = Path(__file__).resolve().parents[1]
    print(json.dumps({'station': args.station, 'trial': True, 'kernel': args.kernel,
                      'carry': carries, 'support_heights': args.support_heights,
                      'shafts': args.shaft, 'dense': args.dense,
                      'source_sha256': {name: hashlib.sha256((source/name).read_bytes()).hexdigest()
                                        for name in ('higher_counter_locking_profiles.py',
                                                     'higher_counter_locking_laws.py',
                                                     'counter_locking_profiles.py',
                                                     'tools/counter_lockout_probe.py',
                                                     'tools/check_higher_counter_locking_profile.py',
                                                     'docs/evidence/counter-tens-contact-support-2026-09-21.json')}}), flush=True)
    checked = failures = 0
    shift = 20*(args.station-2)
    shafts = args.shaft or {shaft-shift for shaft in sample_shafts(dense=args.dense)}
    for carry in carries:
        for shaft in sorted(shafts):
            volume = station_reader(args.station, carry, shaft, trial=True)
            for row in admitted_contacts(volume, carry, shaft, args.kernel,
                                         angles={angle+shift for angle in sample_angles(
                                             shaft+shift, dense=args.dense)},
                                         station=args.station):
                checked += 1
                if row['failure']:
                    failures += 1
                    print(json.dumps(row), flush=True)
            print(json.dumps({'carry': carry, 'shaft_complete': shaft,
                              'checked': checked, 'failures': failures}), flush=True)
    print(json.dumps({'complete': True, 'station': args.station, 'kernel': args.kernel,
                      'checked': checked, 'failures': failures}), flush=True)
    raise SystemExit(bool(failures))


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
