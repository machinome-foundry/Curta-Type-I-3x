"""Independent placed-cover/native witnesses, not a retained-motion test."""

import argparse
import hashlib
import json
import logging
from math import cos, radians, sin
from pathlib import Path
from time import process_time


def probe(rows):
    from machinome.simulation.profile import ConvexProfile, profile_overlap
    from simulation.tools.reverser_tooth_envelope import ToothEnvelopeReader, DRUMS

    records = [r for r in rows if r['kind'] == 'installed_profile']
    profiles = {id(r): ConvexProfile([[r['points'][i] for i in loop]
                                     for loop in r['polygons']]) for r in records}
    reader = ToothEnvelopeReader(1)
    gears = [r for r in records if r['path'] == reader.gear]
    drums = [r for r in records if r['path'] in DRUMS]

    def contact(crank, shaft, height, lift):
        for gear in gears:
            delta = shaft-gear['reference_shaft_angle']
            c, s = cos(radians(delta)), sin(radians(delta))
            x, y = gear['axis'][:2]
            low, high = gear['source_height']
            allowance = gear['allowance_mm']
            dz = height-gear['reference_reverser_height']
            for drum in drums:
                dlo, dhi = drum['source_height']
                da = drum['allowance_mm']
                if high+allowance+dz < dlo-da+lift or dhi+da+lift < low-allowance+dz:
                    continue
                if profile_overlap(profiles[id(gear)], profiles[id(drum)], delta, -crank,
                                   left_xy=(x-c*x+s*y, y-s*x-c*y)):
                    return True
        return False

    for crank, shaft, height, lift in (
            (0, 134, 3.9075, 0), (90, 134, 1.0775, 0),
            (90, 134, 1.0475, 0), (90, 134, 0, 0),
            (90, 231.6, -3, 0), (90, 231.6, 3.9075, 0),
            (167.5, 283.63498306274414, -3, 0), (90, 134, -6.9425, 9)):
        start = process_time()
        flag = contact(crank, shaft, height, lift)
        elapsed = process_time()-start
        volumes = reader.volumes(crank, shaft, height, lift, kernel='native')
        if any(v > 0 for v in volumes.values()) and not flag:
            raise ValueError('Positive installed native material escaped the cover')
        yield dict(crank=crank, shaft=shaft, height=height, lift=lift,
                   profile_contact=flag, native_volumes_mm3=volumes,
                   cpu_seconds=elapsed,
                   scope='Installed independent poses; not retained operating admission')


def main():
    from simulation.tools.reverser_installed_trial import EVIDENCE_SHA256

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f'Preserve existing evidence: {args.output}')
    raw = args.input.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EVIDENCE_SHA256:
        parser.error('This probe requires the complete pinned installed-cover record')
    rows = [json.loads(line) for line in raw.splitlines()]
    with args.output.open('x') as output:
        count = 0
        for row in probe(rows):
            row['input_sha256'] = digest
            print(json.dumps(row), file=output, flush=True)
            print(json.dumps(row), flush=True)
            count += 1
    print(json.dumps(dict(output=str(args.output), rows=count)), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
