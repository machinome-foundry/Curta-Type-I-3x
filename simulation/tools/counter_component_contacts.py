"""Identify higher-counter contact surfaces without omitting complete prints.

Each record retains the complete native/faceted common alongside diagnostic
ingredient labels. This proposes no contact law, fit or operating adoption.
"""

import argparse
import json
import logging

from simulation.tools.counter_lockout_probe import STATIONS, station_bench, station_reader
from simulation.tools.higher_locking_envelope import component_contacts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--station', type=int, choices=range(1, 7), required=True)
    parser.add_argument('--shaft', type=float, required=True)
    parser.add_argument('--carry', type=float, action='append')
    parser.add_argument('--crank', type=float, action='append', required=True)
    parser.add_argument('--trial', action='store_true')
    args = parser.parse_args()
    carries = args.carry or (0, .5, 1)
    if any(not 0 <= carry <= 1 for carry in carries):
        parser.error('carry must be 0..1')
    node_type = station_bench(args.station, trial=args.trial)
    path = ('shaft', STATIONS[args.station-1][1])
    for carry in carries:
        read = station_reader(args.station, carry, args.shaft, trial=args.trial)
        for crank in args.crank:
            contacts = component_contacts(carry, crank, args.shaft, node_type, stack_path=path)
            print(json.dumps({'station': args.station, 'carry': carry,
                              'shaft': args.shaft, 'crank': crank, 'trial': args.trial,
                              'complete_mm3': {kernel: read(crank, kernel)
                                               for kernel in ('native', 'faceted')},
                              'contacts': contacts}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
