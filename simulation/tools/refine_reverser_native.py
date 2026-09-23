"""Independently refine native boundaries near observed world64 transitions.

This does not certify unmeasured clear rows or exclude additional native
islands. It records those limitations rather than copying mesh clearance.
"""

import argparse
import hashlib
import json
import logging
from math import isfinite
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from pathlib import Path

from simulation.tools.reverser_tooth_envelope import ToothEnvelopeReader, phase_boundaries


_reader = None


def setup_reader(station):
    global _reader
    logging.disable(logging.INFO)
    _reader = ToothEnvelopeReader(station)


def refine_row(row):
    result = dict(station=row['station'], crank=row['crank'], height=row['height'],
                  lift=row['lift'], kernel='native',
                  scope='Native transition refinement, not a continuous clearance proof')
    if not row['boundaries']:
        return dict(result, status='not_checked_no_world64_transition', boundaries=[])

    def evaluate(shaft):
        return _reader.volumes(row['crank'], shaft, row['height'], row['lift'],
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
    return dict(result, status='refined_observed_transitions', boundaries=found)


def row_key(row):
    return tuple(row[name] for name in ('station', 'crank', 'height', 'lift'))


def remaining_rows(rows, completed, digest):
    """Resume only matching complete records; never discard a malformed tail."""
    source = {row_key(row): row for row in rows}
    if len(source) != len(rows):
        raise ValueError('Duplicate input pose')
    seen = set()
    for record in completed:
        key = row_key(record)
        if key not in source or key in seen:
            raise ValueError('Unknown or duplicate completed pose')
        if record.get('input_sha256') != digest or record.get('kernel') != 'native':
            raise ValueError('Resume source/kernel mismatch')
        original = source[key]['boundaries']
        if original:
            if record.get('status') != 'refined_observed_transitions':
                raise ValueError('Observed transitions are not fully refined')
            if [item.get('world64_seed') for item in record['boundaries']] != original:
                raise ValueError('Resume is missing or mismatches an original boundary')
            for item in record['boundaries']:
                left, right = item.get('left', {}), item.get('right', {})
                if (not all(isinstance(end.get('shaft'), (int, float))
                            and isfinite(end['shaft']) for end in (left, right))
                        or not left['shaft'] < right['shaft']):
                    raise ValueError('Incomplete native boundary bracket')
                for end in (left, right):
                    volumes = end.get('volumes_mm3', {})
                    if (not volumes or any(not isinstance(v, (int, float))
                                           or not isfinite(v) or v < 0 for v in volumes.values())
                            or end.get('contact') != any(v > 0 for v in volumes.values())):
                        raise ValueError('Incomplete native endpoint evidence')
                if (left['contact'] == right['contact']
                        or right['contact'] != item.get('enters_contact')
                        or item['enters_contact'] != item['world64_seed']['enters_contact']):
                    raise ValueError('Native boundary does not retain the stated transition')
        elif (record.get('status') != 'not_checked_no_world64_transition'
              or record.get('boundaries') != []):
            raise ValueError('Unmeasured row has been relabelled')
        seen.add(key)
    return [row for row in rows if row_key(row) not in seen]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--crank', type=float, action='append')
    parser.add_argument('--resume', type=Path, action='append', default=[],
                        help='Preserve and skip matching complete records in prior outputs')
    parser.add_argument('--workers', type=int, default=1,
                        help='Independent spawned native readers; output stays in input order')
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f'Preserve existing evidence: {args.output}')
    if not 1 <= args.workers <= 8:
        parser.error('--workers must be in 1..8')
    raw = args.input.read_bytes()
    rows = [json.loads(line) for line in raw.splitlines()]
    if not rows or any(row['kernel'] != 'world64' for row in rows):
        parser.error('Input must contain world64 boundary records')
    stations = {row['station'] for row in rows}
    if len(stations) != 1:
        parser.error('One source station per refinement run')
    station = stations.pop()
    source_digest = hashlib.sha256(raw).hexdigest()
    completed = [json.loads(line) for path in args.resume for line in path.read_bytes().splitlines()]
    rows = remaining_rows(rows, completed, source_digest)
    if args.crank:
        rows = [row for row in rows if row['crank'] in args.crank]
    count = 0
    executor = None
    if args.workers == 1:
        setup_reader(station)
        results = map(refine_row, rows)
    else:
        executor = ProcessPoolExecutor(max_workers=args.workers,
                                       mp_context=get_context('spawn'),
                                       initializer=setup_reader, initargs=(station,))
        results = executor.map(refine_row, rows)
    try:
        with args.output.open('x') as output:
            for result in results:
                result['input_sha256'] = source_digest
                print(json.dumps(result), file=output, flush=True)
                count += 1
                if result['boundaries']:
                    print(json.dumps(dict(crank=result['crank'], height=result['height'],
                                          boundaries=len(result['boundaries']))), flush=True)
    finally:
        if executor is not None:
            executor.shutdown(wait=True, cancel_futures=True)
    print(json.dumps(dict(output=str(args.output), rows=count)), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
