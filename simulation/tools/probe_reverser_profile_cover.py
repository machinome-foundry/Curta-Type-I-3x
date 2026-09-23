"""Eight source-placed profile witnesses; not a retained whole-print fixture."""

import argparse
import hashlib
import json
import logging
from math import cos, radians, sin
from pathlib import Path
from time import process_time

from machinome.exact import intersect_shapes
from simulation.fit import FittedCounterPinion
from simulation.standard.parts import (OneToothTurnsStepDrumSegment,
                                        NineToothTurnsStepDrumSegment)
from simulation.tools.reverser_profile_cover import posed_polygons, profiles_overlap


def probe(reports):
    gear = FittedCounterPinion().shape()
    axis = (-26.032898192, 31.024799946)
    for cls in (OneToothTurnsStepDrumSegment, NineToothTurnsStepDrumSegment):
        drum = cls().shape()
        for crank, shaft in ((90, 134), (90, 231.6), (167.5, 283.63498306274414), (0, 134)):
            c, s = cos(radians(-crank)), sin(radians(-crank))
            x, y = -.016356142, .223394941
            center = (c*x-s*y, s*x+c*y)
            first = gear.rotate((0, 0, 0), (0, 0, 1), shaft).translate((*axis, 0))
            second = drum.rotate((0, 0, 0), (0, 0, 1), 2.604082802-crank).translate((*center, 0))
            common = intersect_shapes(first, second, 'ones-pinion-profile', cls.__name__)
            volume = common.Volume()
            if not common.isValid() or not 0 <= volume < float('inf'):
                raise ValueError(f'Unresolved native profile common: {cls.__name__}, '
                                 f'crank={crank}, shaft={shaft}, volume={volume}')
            start = process_time()
            contact = profiles_overlap(
                posed_polygons(reports['FittedCounterPinion'], shaft, axis),
                posed_polygons(reports[cls.__name__], 2.604082802-crank, center))
            elapsed = process_time()-start
            if volume > 0 and not contact:
                raise ValueError('Positive native material escaped the profile cover')
            yield dict(drum=cls.__name__, crank=crank, shaft=shaft,
                       native_volume_mm3=volume, cover_contact=contact,
                       cover_cpu_seconds=elapsed,
                       includes_source_mesh=bool(reports[cls.__name__].get('mesh_cover_polygons')),
                       scope='Source-placed profiles, not complete installed-print admission')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f'Preserve existing evidence: {args.output}')
    raw = args.input.read_bytes()
    records = [json.loads(line) for line in raw.splitlines()]
    reports = {r['part']: r for r in records}
    if len(reports) != len(records):
        parser.error('Duplicate source profile')
    with args.output.open('x') as output:
        count = 0
        for record in probe(reports):
            record['input_sha256'] = hashlib.sha256(raw).hexdigest()
            print(json.dumps(record), file=output, flush=True)
            print(json.dumps(record), flush=True)
            count += 1
    print(json.dumps(dict(output=str(args.output), rows=count)), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
