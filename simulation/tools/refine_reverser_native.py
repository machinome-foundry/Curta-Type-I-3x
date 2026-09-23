"""Independently refine native boundaries near observed world64 transitions.

This does not certify unmeasured clear rows or exclude additional native
islands. It records those limitations rather than copying mesh clearance.
"""

import argparse
import hashlib
import json
import logging
from pathlib import Path

from simulation.tools.reverser_tooth_envelope import ToothEnvelopeReader, phase_boundaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--crank', type=float, action='append')
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f'Preserve existing evidence: {args.output}')
    raw = args.input.read_bytes()
    rows = [json.loads(line) for line in raw.splitlines()]
    if not rows or any(row['kernel'] != 'world64' for row in rows):
        parser.error('Input must contain world64 boundary records')
    stations = {row['station'] for row in rows}
    if len(stations) != 1:
        parser.error('One source station per refinement run')
    reader = ToothEnvelopeReader(stations.pop())
    source_digest = hashlib.sha256(raw).hexdigest()
    count = 0
    with args.output.open('x') as output:
        for row in rows:
            if args.crank and row['crank'] not in args.crank:
                continue
            result = dict(station=row['station'], crank=row['crank'], height=row['height'],
                          lift=row['lift'], kernel='native', input_sha256=source_digest,
                          scope='Native transition refinement, not a continuous clearance proof')
            if not row['boundaries']:
                result.update(status='not_checked_no_world64_transition', boundaries=[])
            else:
                def evaluate(shaft):
                    return reader.volumes(row['crank'], shaft, row['height'], row['lift'],
                                          kernel='native')
                found = []
                for seed in row['boundaries']:
                    center = (seed['left']['shaft']+seed['right']['shaft'])/2
                    attempts = []
                    for half_width in (.25, .5, 1, 2, 4):
                        report = phase_boundaries((center-half_width, center+half_width),
                                                  evaluate, iterations=0)
                        attempts.append(report)
                        if report['boundaries']:
                            break
                    else:
                        raise ValueError(f'No native bracket near {center}: {row}')
                    if report['boundaries'][0]['enters_contact'] != seed['enters_contact']:
                        raise ValueError('Native transition direction disagrees; inspect geometry')
                    refined = phase_boundaries((center-half_width, center+half_width), evaluate)
                    found.append(dict(world64_seed=seed, attempts=attempts,
                                      **refined['boundaries'][0]))
                result.update(status='refined_observed_transitions', boundaries=found)
            print(json.dumps(result), file=output, flush=True)
            count += 1
            if row['boundaries']:
                print(json.dumps(dict(crank=row['crank'], height=row['height'],
                                      boundaries=len(result['boundaries']))), flush=True)
    print(json.dumps(dict(output=str(args.output), rows=count)), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
