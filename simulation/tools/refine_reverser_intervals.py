"""Measure additional world64 transitions between existing native/mesh knots.

Interpolation predicts a search location only. Every returned bracket has
independently evaluated free/positive endpoints. These finite local searches
do not exclude additional islands and do not measure native geometry.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
import logging
from multiprocessing import get_context
from pathlib import Path

from simulation.tools.probe_reverser_phase import interpolated_edges
from simulation.tools.reverser_tooth_envelope import ToothEnvelopeReader, phase_boundaries


_reader = None


def refine_transition(center, enters, evaluate):
    attempts = []
    for half_width in (.125, .25, .5, 1, 2, 4, 8):
        report = phase_boundaries((center-half_width, center+half_width),
                                  evaluate, iterations=0)
        attempts.append(report)
        if not report['boundaries']:
            continue
        if report['boundaries'][0]['enters_contact'] != enters:
            raise ValueError('Predicted transition meets a different island; inspect geometry')
        refined = phase_boundaries((center-half_width, center+half_width), evaluate)
        return dict(refined['boundaries'][0], search_center=center,
                    search_attempts=attempts)
    raise ValueError('No observed transition near the prediction; use a full independent sweep')


def setup_reader(station):
    global _reader
    logging.disable(logging.INFO)
    _reader = ToothEnvelopeReader(station)


def refine_pose(job):
    crank, height, lift, seeds = job
    observed = {}

    def evaluate(shaft):
        if shaft not in observed:
            observed[shaft] = _reader.volumes(crank, shaft, height, lift, kernel='world64')
        return observed[shaft]

    boundaries = [refine_transition(center, enters, evaluate) for center, enters in seeds]
    boundaries.sort(key=lambda b: b['left']['shaft'])
    samples = [dict(shaft=shaft, volumes_mm3=volumes,
                    contact=any(v > 0 for v in volumes.values()))
               for shaft, volumes in sorted(observed.items())]
    return dict(station=_reader.station, crank=crank, height=height, lift=lift,
                kernel='world64', samples=samples, boundaries=boundaries,
                scope='Measured local transitions; unsampled islands and native geometry unproved')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--crank', type=float, action='append')
    parser.add_argument('--height', type=float, action='append')
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f'Preserve existing evidence: {args.output}')
    if not 1 <= args.workers <= 8:
        parser.error('--workers must be in 1..8')
    raw = args.input.read_bytes()
    rows = json.loads(raw)['rows']
    stations = {row['station'] for row in rows}
    if len(stations) != 1:
        parser.error('One source station per refinement run')
    station = stations.pop()
    rest = 134-20*(station-1)
    jobs = []
    for height, lift in sorted({(row['height'], row['lift']) for row in rows}):
        if args.height is not None and height not in args.height:
            continue
        ordered = sorted((row for row in rows if row['height'] == height
                          and row['lift'] == lift), key=lambda row: row['crank'])
        cranks = args.crank or [(a['crank']+b['crank'])/2 for a, b in zip(ordered, ordered[1:])
                               if a['chart'] is not None and b['chart'] is not None]
        for crank in cranks:
            seeds = []
            for sector in range(5):
                edges = interpolated_edges(rows, crank, height, lift, sector, 0)
                seeds.extend(((edges[edge]-rest) % 360+rest, enters)
                             for edge, enters in (('lower', False), ('upper', True)))
            jobs.append((crank, height, lift, sorted(seeds)))
    if not jobs:
        parser.error('No measurable intervals selected')
    executor = None
    if args.workers == 1:
        setup_reader(station)
        results = map(refine_pose, jobs)
    else:
        executor = ProcessPoolExecutor(max_workers=args.workers,
                                       mp_context=get_context('spawn'),
                                       initializer=setup_reader, initargs=(station,))
        results = executor.map(refine_pose, jobs)
    try:
        with args.output.open('x') as output:
            for result in results:
                result['candidate_sha256'] = hashlib.sha256(raw).hexdigest()
                print(json.dumps(result), file=output, flush=True)
                print(json.dumps(dict(crank=result['crank'], height=result['height'],
                                      boundaries=len(result['boundaries']))), flush=True)
    finally:
        if executor is not None:
            executor.shutdown(wait=True, cancel_futures=True)
    print(json.dumps(dict(output=str(args.output), rows=len(jobs))), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
