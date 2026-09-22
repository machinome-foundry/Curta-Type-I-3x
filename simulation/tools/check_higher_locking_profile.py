"""Check candidate admission against complete native or published T07 prints.

Every measured-profile boundary is challenged, including between knots and
strip support edges. A positive common at an admitted pose fails, with no
volume epsilon. This finite diagnostic does not establish continuous contact.
"""

import argparse
import hashlib
import json
import logging
import math
from pathlib import Path

from machinome.math import piecewise
from simulation.higher_locking_laws import higher_contact_gap
from simulation.locking_profiles import SECTORS
from simulation.higher_locking_profiles import LOWER_LOCK_SECTORS, CARRY_TOOTH_STRIPS
from simulation.higher_lockout_trial import HigherLockoutFitBench
from simulation.tools.higher_locking_envelope import contact_reader
from simulation.tools.result_bank_lockout_probe import station_reader


def candidate_angles(shaft):
    angles = {0., 90., 110., 140., 145., 150., 155., 160., 180., 270.}
    for profiles, shift in ((SECTORS, 20), (LOWER_LOCK_SECTORS, 0),
                            (CARRY_TOOTH_STRIPS, 0)):
        for start, end, points in profiles:
            if not start <= shaft+shift <= end:
                continue
            for column in (1, 2):
                boundary = piecewise(shaft+shift, [(p[0], p[column]) for p in points])
                boundary += shift if shift else 0
                angles.update(boundary+offset for offset in (-.101, -.1, 0, .1, .101))
    return sorted(angles)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel', choices=('native', 'faceted'), required=True)
    parser.add_argument('--world-precision', type=int, choices=(32, 64), default=64,
                        help='64 preserves placed STL coordinates; 32 reproduces historical probes')
    parser.add_argument('--carry', type=float, action='append')
    parser.add_argument('--step', type=float, default=6)
    parser.add_argument('--knots', action='store_true')
    parser.add_argument('--station', type=int, choices=range(2, 12),
                        help='Check the candidate at another source result station; '
                             'uses its own print, pivot and carry seating.')
    args = parser.parse_args()
    assert 0 < args.step <= 12
    profile_path = Path(__file__).resolve().parents[1]/'higher_locking_profiles.py'
    print(json.dumps({'kernel': args.kernel, 'carry': args.carry, 'step': args.step,
                      'world_precision_bits': args.world_precision,
                      'station': args.station or 2,
                      'knots': args.knots, 'profile_sha256': hashlib.sha256(
                          profile_path.read_bytes()).hexdigest(),
                      'probe_sha256': {name: hashlib.sha256((profile_path.parent/name).read_bytes()).hexdigest()
                          for name in ('tools/check_higher_locking_profile.py',
                                       'tools/higher_locking_envelope.py',
                                       'tools/ancestor_lockout_contact.py',
                                       'tools/result_bank_lockout_probe.py')}}), flush=True)
    shafts = {-16+args.step*i for i in range(int(360/args.step)+1)}
    if args.knots:
        for profiles, shift in ((SECTORS, 20), (LOWER_LOCK_SECTORS, 0),
                                (CARRY_TOOTH_STRIPS, 0)):
            for start, end, points in profiles:
                shafts.update(p[0]-shift for p in points)
                shafts.update((a[0]+b[0])/2-shift for a, b in zip(points, points[1:]))
                shafts.update(edge-shift+offset for edge in (start, end)
                              for offset in (-.001, 0, .001))
    checked = failures = 0
    for carry in args.carry or (0, .5, 1):
        assert 0 <= carry <= 1
        for shaft in sorted(shafts):
            volume = (station_reader(args.station, carry, shaft, trial=True,
                                     world_precision=args.world_precision)
                      if args.station else
                      contact_reader(carry, shaft=shaft, node_type=HigherLockoutFitBench,
                                     world_precision=args.world_precision))
            for crank in candidate_angles(shaft):
                if higher_contact_gap(crank, shaft, carry*4.2-4.2) > 0:
                    continue
                overlap = volume(crank, args.kernel)
                if not math.isfinite(overlap) or overlap < 0:
                    raise ValueError(f'Invalid common at {carry}, {shaft}, {crank}: {overlap}')
                checked += 1
                if overlap > 0:
                    failures += 1
                    print(json.dumps({'failure': True, 'kernel': args.kernel,
                                      'carry': carry, 'shaft': shaft, 'crank': crank,
                                      'overlap_mm3': overlap}), flush=True)
            print(json.dumps({'shaft_complete': shaft, 'carry': carry,
                              'checked': checked, 'failures': failures}), flush=True)
    print(json.dumps({'complete': True, 'kernel': args.kernel,
                      'checked': checked, 'failures': failures}), flush=True)
    raise SystemExit(bool(failures))


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
