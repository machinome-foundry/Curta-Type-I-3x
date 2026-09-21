"""Challenge counter-ones candidate admission on complete source-backed prints.

This finite check includes profile knots, their midpoints, support edges and
previously discovered collisions. --dense adds 1-degree shaft and 5-degree
crank grids independent of the measured knots.
Every positive-volume admitted pose fails. It certifies neither higher
counter stacks nor a continuous path between the tested poses.
"""

import argparse
import hashlib
import json
import logging
from pathlib import Path

from machinome.math import piecewise
from simulation.counter_locking_profiles import SECTORS
from simulation.counter_locking_laws import counter_contact_gap
from simulation.tools.counter_lockout_probe import station_reader


def rejected_poses():
    evidence = (Path(__file__).resolve().parents[1] / 'docs/evidence').glob(
        'counter-ones-*-profile-rejection-2026-09-21.json')
    return {(row['shaft'], row['crank'])
            for path in evidence
            for records in json.loads(path.read_text())['kernels'].values()
            for row in records if row.get('failure')}


def sample_shafts(*, dense=False):
    shafts = set(range(134, 495, 1 if dense else 6))
    shafts.update(shaft for shaft, _ in rejected_poses())
    for start, end, points in SECTORS:
        shafts.update(p[0] for p in points)
        shafts.update((a[0]+b[0])/2 for a, b in zip(points, points[1:]))
        shafts.update(edge+offset for edge in (start, end) for offset in (-.001, 0, .001))
    return shafts


def sample_angles(shaft, *, dense=False):
    angles = {0., 60., 90., 120., 150., 170., 180., 270., 360.}
    if dense:
        angles.update(range(0, 361, 5))
    angles.update(crank for rejected_shaft, crank in rejected_poses() if rejected_shaft == shaft)
    for start, end, points in SECTORS:
        if not start <= shaft <= end:
            continue
        for column in (1, 2):
            boundary = piecewise(shaft, [(p[0], p[column]) for p in points])
            angles.update(boundary+offset for offset in (-.101, -.1, 0, .1, .101))
    return angles


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel', choices=('native', 'faceted'), required=True)
    parser.add_argument('--dense', action='store_true')
    args = parser.parse_args()
    profile = Path(__file__).resolve().parents[1]/'counter_locking_profiles.py'
    print(json.dumps({'kernel': args.kernel, 'dense': args.dense,
                      'profile_sha256': hashlib.sha256(
        profile.read_bytes()).hexdigest()}), flush=True)
    checked = failures = 0
    for shaft in sorted(sample_shafts(dense=args.dense)):
        volume = station_reader(1, 0, shaft, trial=True)
        for crank in sorted(sample_angles(shaft, dense=args.dense)):
            if counter_contact_gap(crank, shaft) > 0:
                continue
            common = volume(crank, args.kernel)
            checked += 1
            if common > 0:
                failures += 1
                print(json.dumps({'failure': True, 'shaft': shaft, 'crank': crank,
                                  'common_mm3': common, 'kernel': args.kernel}), flush=True)
        print(json.dumps({'shaft_complete': shaft, 'checked': checked,
                          'failures': failures}), flush=True)
    print(json.dumps({'complete': True, 'checked': checked, 'failures': failures,
                      'kernel': args.kernel}), flush=True)
    raise SystemExit(bool(failures))


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
