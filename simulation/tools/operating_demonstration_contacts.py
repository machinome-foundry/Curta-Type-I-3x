"""Inventory rigid contacts during actual retained demonstration requests.

This diagnostic does not waive rest overlaps, claim continuous clearance, or
cover flexible leaves. It records every positive spatial common and refused
intersection at each selected run-time sample, using the existing world64 or
native-with-STL-fallback inventory. New/changed contacts are findings, not
automatically adopted fits. JSON lines remain useful if a later sample fails.
"""

import argparse
import json
import logging
import time

from machinome.simulation import Sim
from simulation.operating_demonstrations import DEMONSTRATIONS, replay
from simulation.running import OperatingCurta
from simulation.tools.interference import inventory


def compare_inventory(rest, sample):
    before, after = rest['overlap_mm3'], sample['overlap_mm3']
    return dict(positive_pairs=len(after),
                added={key: value for key, value in after.items() if key not in before},
                removed={key: value for key, value in before.items() if key not in after},
                changed={key: [before[key], value] for key, value in after.items()
                         if key in before and value != before[key]},
                refusals=sample['refusals'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demonstrations', nargs='+', choices=tuple(DEMONSTRATIONS),
                        default=list(DEMONSTRATIONS))
    parser.add_argument('--interval', type=float, default=.1)
    parser.add_argument('--exact', action='store_true')
    args = parser.parse_args()
    assert 0 < args.interval <= .2
    logging.disable(logging.INFO)
    started = time.monotonic()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    initial = sim.snapshot()
    rest = inventory(sim.node, exact=args.exact, world_precision=64)
    print(json.dumps(dict(kind='rest', inventory=rest, interval=args.interval,
                          scope='all rigid pairs; flexible leaves not covered')), flush=True)
    current = None
    sample_count = 0

    def sample():
        nonlocal sample_count
        observed = inventory(sim.node, exact=args.exact, world_precision=64)
        sample_count += 1
        print(json.dumps(dict(kind='sample', demonstration=current, time=sim.time,
                              inventory=observed, comparison=compare_inventory(rest, observed),
                              wall_seconds=time.monotonic()-started)), flush=True)

    sim.every(args.interval, sample)
    for name in args.demonstrations:
        current = name
        before = sample_count
        outcomes = replay(sim, name, initial)
        assert sample_count > before, ('no sampled motion', name)
        print(json.dumps(dict(kind='demonstration-completed', name=name,
                              samples=sample_count-before, outcomes=outcomes)), flush=True)
    print(json.dumps(dict(kind='finished', samples=sample_count,
                          wall_seconds=time.monotonic()-started,
                          acceptance='diagnostic completed; positive contacts remain unwaived')),
          flush=True)


if __name__ == '__main__':
    main()
