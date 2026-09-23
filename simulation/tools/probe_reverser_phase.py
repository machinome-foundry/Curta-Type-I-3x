"""Try linear interpolation between measured knots; positive common rejects it.

This is an independent geometry experiment, never an operating controller.
Even all-zero probes would not prove continuous or unmeasured clearance.
"""

import argparse
import hashlib
import json
import logging
from math import isfinite
from pathlib import Path

from simulation.tools.reverser_tooth_envelope import ToothEnvelopeReader


def interpolated_edges(rows, crank, height, lift, sector, guard):
    if sector not in range(5) or not isfinite(guard) or guard < 0:
        raise ValueError('Use a measured sector and finite nonnegative guard')
    ordered = sorted((row for row in rows if row['height'] == height
                      and row['lift'] == lift), key=lambda row: row['crank'])
    for left, right in zip(ordered, ordered[1:]):
        if left['crank'] < crank < right['crank']:
            if left['chart'] is None or right['chart'] is None:
                raise ValueError('Cannot interpolate across an unmeasured row')
            fraction = (crank-left['crank'])/(right['crank']-left['crank'])
            edges = {name: (1-fraction)*left['chart'][sector][name]
                     + fraction*right['chart'][sector][name]+6.4*crank+delta
                     for name, delta in (('lower', guard), ('upper', -guard))}
            if not edges['lower'] < edges['upper']:
                raise ValueError('Guard closes the measured free interval')
            return dict(edges, bracket=(left['crank'], right['crank']))
    raise ValueError('An interior crank pose between two existing rows is required')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--crank', type=float, action='append', required=True)
    parser.add_argument('--height', type=float, default=0)
    parser.add_argument('--lift', type=float, default=0)
    parser.add_argument('--sector', type=int, choices=range(5), action='append')
    parser.add_argument('--guard', type=float, default=.01)
    parser.add_argument('--kernel', choices=('native', 'world64'), action='append')
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f'Preserve existing evidence: {args.output}')
    raw = args.input.read_bytes()
    candidate = json.loads(raw)
    stations = {row['station'] for row in candidate['rows']}
    if len(stations) != 1:
        parser.error('One source station per probe run')
    reader = ToothEnvelopeReader(stations.pop())
    samples = []
    for crank in args.crank:
        for sector in args.sector or range(5):
            edges = interpolated_edges(candidate['rows'], crank, args.height,
                                       args.lift, sector, args.guard)
            for edge in ('lower', 'upper'):
                for kernel in args.kernel or ('world64',):
                    volumes = reader.volumes(crank, edges[edge], args.height,
                                             args.lift, kernel=kernel)
                    samples.append(dict(crank=crank, shaft=edges[edge],
                                        height=args.height, lift=args.lift,
                                        sector=sector, edge=edge, kernel=kernel,
                                        bracket=edges['bracket'], volumes_mm3=volumes,
                                        contact=any(v > 0 for v in volumes.values())))
    contacts = sum(sample['contact'] for sample in samples)
    report = dict(scope='Finite interpolation probes; NOT a clearance certificate',
                  input_sha256=hashlib.sha256(raw).hexdigest(),
                  guard_deg=args.guard, samples=samples, contacts=contacts,
                  candidate_rejected=bool(contacts))
    with args.output.open('x') as output:
        output.write(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(output=str(args.output), probes=len(samples),
                          contacts=contacts)), flush=True)
    return int(bool(contacts))


if __name__ == '__main__':
    logging.disable(logging.INFO)
    raise SystemExit(main())
