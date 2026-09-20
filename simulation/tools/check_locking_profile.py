"""Check experimental contact interpolation against complete printed solids.

Reports every failing boundary sample, not just the first. This is geometry
acceptance for a candidate table, not a substitute for retained run tests.
"""

import argparse
import json
import logging

from machinome.math import piecewise
from simulation.result_locking import CONTACT_STANDOFF, contact_gap
from simulation.locking_profiles import SECTORS
from simulation.tools.locking_envelope import contact_reader


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel', choices=('exact', 'faceted'), required=True)
    parser.add_argument('--step', type=float, default=.5)
    args = parser.parse_args()
    assert 0 < args.step <= 1
    reader = contact_reader(args.kernel)
    failures, checked = 0, 0
    for index, (start, end, points) in enumerate(SECTORS):
        samples = {start + .01 + args.step*i
                   for i in range(int((end-start-.02)/args.step)+1)}
        samples.update(p[0] for p in points)
        samples.update((a[0]+b[0])/2 for a, b in zip(points, points[1:]))
        opening = [(p[0], p[1]) for p in points]
        closing = [(p[0], p[2]) for p in points]
        for shaft in sorted(samples):
            volume = reader(shaft)
            for side, crank in (
                    ('opening', piecewise(shaft, opening)+CONTACT_STANDOFF),
                    ('closing', piecewise(shaft, closing)-CONTACT_STANDOFF)):
                overlap = volume(crank)
                checked += 1
                if overlap > 0:
                    failures += 1
                    print(json.dumps({'kernel': args.kernel, 'sector': index,
                                      'shaft': shaft, 'side': side,
                                      'crank': crank, 'overlap_mm3': overlap}), flush=True)
            # Both endpoints are free-side stopping coordinates. Admission
            # must reject the closed land independently of profile curvature.
            assert contact_gap(180, shaft) > 0, (index, shaft)
        print(json.dumps({'kernel': args.kernel, 'sector_complete': index,
                          'checked': checked, 'failures': failures}), flush=True)
    print(json.dumps({'complete': True, 'kernel': args.kernel,
                      'checked': checked, 'failures': failures}), flush=True)
    raise SystemExit(bool(failures))


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
