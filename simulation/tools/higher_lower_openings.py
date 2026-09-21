"""Measure published complete-print lower-disc release at native sample phases.

At full lowering, before crank 90, the native ingredient survey identifies
only the lower-disc lock. Measuring the complete published prints here also
captures tessellation differences without replacing them by ingredient meshes.
"""

import argparse
import json
import logging

from simulation.tools.compile_locking_profile import records
from simulation.tools.higher_locking_envelope import contact_reader
from simulation.higher_lockout_trial import HigherLockoutFitBench


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', nargs='+')
    args = parser.parse_args()
    phases = sorted({row['shaft'] for path in args.records for row in records(path)
                     if row.get('pair') == 'lower_lock' and row.get('boundaries')})
    for shaft in phases:
        volume = contact_reader(1, shaft=shaft, node_type=HigherLockoutFitBench)
        low, high = 0., 90.
        assert volume(high, 'faceted') <= 0, shaft
        if volume(low, 'faceted') <= 0:
            assert all(volume(angle, 'faceted') <= 0 for angle in range(0, 91, 2)), shaft
            low = high = 0.
        else:
            for _ in range(25):
                middle = (low+high)/2
                if volume(middle, 'faceted') > 0:
                    low = middle
                else:
                    high = middle
        print(json.dumps({'shaft': shaft, 'kernel': 'faceted', 'carry': 1,
                          'last_contact': low, 'first_free': high}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
