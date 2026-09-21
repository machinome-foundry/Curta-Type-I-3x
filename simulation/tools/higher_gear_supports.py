"""Refine the observed carry-tooth strip birth/death at all five source flats.

These are finite native measurements. Angular peak neighborhoods are refined
alongside the shaft bracket; complete-print acceptance must still check them.
"""

import argparse
import json
import logging

from simulation.tools.higher_locking_envelope import pair_reader, contact_reader
from simulation.higher_lockout_trial import HigherLockoutFitBench


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel', choices=('native', 'faceted'), default='native')
    args = parser.parse_args()
    for flat in range(5):
        for side, outside, inside, left, right in (
                ('birth', 22.2, 22.5, 145, 150),
                ('death', 49.25, 49, 158, 161)):
            outside += 72*flat
            inside += 72*flat

            def peak(shaft, near=None):
                if args.kernel == 'native':
                    volume = pair_reader(1, shaft, 'carry_tooth', HigherLockoutFitBench)
                else:
                    # These local windows precede the independently measured
                    # lower-disc closing (above 162 degrees near death).
                    # Use the complete published pair, not a re-tessellation
                    # of its ingredients, to retain its real mesh boundaries.
                    complete = contact_reader(1, shaft=shaft, node_type=HigherLockoutFitBench)
                    volume = lambda angle: complete(angle, 'faceted')
                angles = [left+.1*i for i in range(round((right-left)*10)+1)]
                if near is not None:
                    angles += [near+.01*i for i in range(-10, 11)]
                best = max(((volume(angle), angle) for angle in angles))
                # Resolve the local maximum more finely. Repeated zero is
                # not promoted to clearance outside this sampled window.
                if best[0] > 0:
                    best = max([best]+[(volume(best[1]+.005*i), best[1]+.005*i)
                                      for i in range(-20, 21)])
                return best

            highest, angle = peak(inside)
            assert highest > 0, (flat, side, inside)
            assert peak(outside, angle)[0] <= 0, (flat, side, outside)
            for _ in range(12):
                middle = (outside+inside)/2
                highest, found_angle = peak(middle, angle)
                if highest > 0:
                    inside, angle = middle, found_angle
                else:
                    outside = middle
            print(json.dumps({'kernel': args.kernel, 'flat': flat, 'side': side, 'outside': outside,
                              'inside': inside, 'peak_crank': angle,
                              'width': abs(outside-inside)}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
