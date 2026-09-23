"""Join measured phase boundaries without promoting them to a runtime law.

Candidate data only: unmeasured native rows and between-knot interpolation
remain explicit obligations. Every measured source sector stays independent.
"""

import argparse
import hashlib
import json
from math import floor
from pathlib import Path

from simulation.tools.refine_reverser_native import remaining_rows, row_key


def common_boundary(world64, native):
    """Boundary of the UNION of positive commons in the two kernels."""
    if native['world64_seed'] != world64:
        raise ValueError('Native boundary has a different world64 seed')
    enters = world64['enters_contact']
    if native['enters_contact'] != enters:
        raise ValueError('Different transition direction')
    # Enter contact as soon as either kernel meets material; leave only after
    # both are clear. No comparison uses a tolerated positive volume.
    combine = min if enters else max
    return dict(left=combine(world64['left']['shaft'], native['left']['shaft']),
                right=combine(world64['right']['shaft'], native['right']['shaft']),
                enters_contact=enters)


def free_windows(boundaries, period=360):
    """Keep each independently measured free interval, including the seam."""
    if not boundaries:
        raise ValueError('No boundary is not proof of native clearance')
    ordered = sorted(boundaries, key=lambda b: b['left'])
    if any(b['left'] > b['right'] for b in ordered):
        raise ValueError('Reversed boundary bracket')
    windows = []
    for index, boundary in enumerate(ordered):
        following = ordered[(index+1) % len(ordered)]
        if boundary['enters_contact'] == following['enters_contact']:
            raise ValueError('Transitions do not alternate; do not discard an island')
        if not boundary['enters_contact']:
            low = boundary['right']
            high = following['left']+(period if index == len(ordered)-1 else 0)
            if not low < high:
                raise ValueError('No common free interval between adjacent boundaries')
            windows.append((low, high))
    return tuple(windows)


def chart_windows(windows, crank, station=1):
    """Unwrap five source windows in a moving coordinate chart, not a fit.

    Subtracting 6.4*crank removes the nominal tooth-passage slope from the
    chart. It imposes no motion on a shaft and makes no symmetry assertion.
    All five actual measured intervals are retained and must match uniquely.
    """
    if len(windows) != 5 or station not in range(1, 7):
        raise ValueError('Five separately measured windows and station 1..6 required')
    rest = 134-20*(station-1)
    datum = rest-6.4*(176+20*(station-1)-9*11.25)
    chosen, used = [], set()
    for sector in range(5):
        target = datum+72*sector
        candidates = []
        for index, (low, high) in enumerate(windows):
            low, high = low-6.4*crank, high-6.4*crank
            shift = 360*floor((target-(low+high)/2)/360+.5)
            low, high = low+shift, high+shift
            candidates.append((abs((low+high)/2-target), index, low, high))
        distance, index, low, high = min(candidates)
        if distance >= 36 or index in used:
            raise ValueError('Ambiguous phase chart; retain measurements and inspect topology')
        used.add(index)
        chosen.append(dict(source_window=index, lower=low, upper=high))
    return tuple(chosen)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--world64', type=Path, required=True)
    parser.add_argument('--native', type=Path, action='append', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f'Preserve existing evidence: {args.output}')
    raw = args.world64.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    rows = [json.loads(line) for line in raw.splitlines()]
    native = [json.loads(line) for path in args.native for line in path.read_bytes().splitlines()]
    if remaining_rows(rows, native, digest):
        parser.error('Native refinement records are incomplete')
    observed = {row_key(row): row for row in native}
    candidates = []
    for row in rows:
        item = dict(station=row['station'], crank=row['crank'], height=row['height'],
                    lift=row['lift'])
        if not row['boundaries']:
            item.update(status='native_clearance_unmeasured', chart=None)
        else:
            other = observed[row_key(row)]
            merged = [common_boundary(a, b) for a, b in
                      zip(row['boundaries'], other['boundaries'], strict=True)]
            windows = free_windows(merged)
            item.update(status='measured_knot_only', windows=windows,
                        chart=chart_windows(windows, row['crank'], row['station']))
        candidates.append(item)
    report = dict(scope='Candidate measured knots; NOT an adopted running restraint',
                  world64_sha256=digest,
                  native_sha256=[hashlib.sha256(path.read_bytes()).hexdigest()
                                 for path in args.native],
                  outstanding=['native clearance outside measured transitions',
                               'between-knot contact and play validation',
                               'all higher counter stations and operating histories'],
                  rows=candidates)
    with args.output.open('x') as output:
        output.write(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(output=str(args.output), rows=len(candidates))), flush=True)


if __name__ == '__main__':
    main()
