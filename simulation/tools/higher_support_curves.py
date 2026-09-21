"""Measure both representations near the carry-tooth strip birth/death.

Native ingredient scans retain both teeth. In each small support-edge window
the other tooth and both locking lands are absent, so the published complete
prints give an independent mesh boundary for the tooth being refined.
"""

import argparse
import json
import logging

from simulation.tools.compile_locking_profile import records
from simulation.tools.higher_locking_envelope import pair_reader, contact_reader
from simulation.higher_lockout_trial import HigherLockoutFitBench


def boundaries(volume, samples):
    found = []
    for (left, vl), (right, vr) in zip(samples, samples[1:]):
        if (vl > 0) == (vr > 0):
            continue
        enters = vr > 0
        for _ in range(18):
            middle = (left+right)/2
            if (volume(middle) > 0) == enters:
                right = middle
            else:
                left = middle
        found.append({'left': left, 'right': right, 'enters_contact': enters})
    return found


def combined_boundaries(native_bounds, mesh_bounds, left, right):
    """Union measured contact intervals, preserving every resolved free gap.

    Faceting can split one grazing tooth contact into several islands. Native
    contact may cover those gaps, but its absence must never be replaced by a
    convex envelope. Only overlapping outer measurement brackets are joined;
    the original per-kernel brackets remain in each output record for review.
    """
    intervals = []
    for bounds in (native_bounds, mesh_bounds):
        assert len(bounds) % 2 == 0, bounds
        for start, end in zip(bounds[::2], bounds[1::2]):
            assert start['enters_contact'] and not end['enters_contact'], bounds
            assert start['left'] < end['right'], bounds
            if bounds is mesh_bounds:
                assert left <= start['left'] < end['right'] <= right, bounds
            intervals.append((start, end))
    merged = []
    for start, end in sorted(intervals, key=lambda pair: pair[0]['left']):
        if merged and start['left'] <= merged[-1]['right']:
            if end['right'] > merged[-1]['right']:
                merged[-1] = end
        else:
            merged.extend((start, end))
    return merged


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('brackets')
    parser.add_argument('--flat', type=int, action='append')
    parser.add_argument('--side', choices=('birth', 'death'))
    args = parser.parse_args()
    for support in records(args.brackets):
        if args.flat is not None and support['flat'] not in args.flat:
            continue
        if args.side is not None and support['side'] != args.side:
            continue
        birth = support['side'] == 'birth'
        for offset in (0, .002, .005, .01, .02, .05, .1, .2, .4, .8, 1.2):
            shaft = support['inside']+offset*(1 if birth else -1)
            native = pair_reader(1, shaft, 'carry_tooth', HigherLockoutFitBench)
            complete = contact_reader(1, shaft=shaft, node_type=HigherLockoutFitBench)
            mesh = lambda angle: complete(angle, 'faceted')
            angles = sorted({140+.25*i for i in range(101)} | {support['peak_crank']})
            samples = [(angle, native(angle)) for angle in angles]
            native_bounds = boundaries(native, samples)
            left, right = (144., 152.) if birth else (157., 161.)
            mesh_angles = sorted({left+.1*i for i in range(round((right-left)*10)+1)}
                                 | {support['peak_crank']})
            mesh_samples = [(angle, mesh(angle)) for angle in mesh_angles]
            assert mesh_samples[0][1] <= 0 and mesh_samples[-1][1] <= 0, support
            mesh_bounds = boundaries(mesh, mesh_samples)
            merged = combined_boundaries(native_bounds, mesh_bounds, left, right)
            print(json.dumps({'kernel': 'dual', 'pair': 'carry_tooth', 'trial': True,
                              'shaft': shaft, 'carry': 1, 'support': support['side'],
                              'flat': support['flat'], 'samples': samples,
                              'boundaries': merged, 'native_boundaries': native_bounds,
                              'mesh_local_boundaries': mesh_bounds}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
