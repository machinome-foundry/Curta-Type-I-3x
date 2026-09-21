"""Compile a provisional higher-counter candidate from independent measurements.

The generic contour-chart routines are reused, never the result-side tables.
Registering shaft -130 / crank -52 puts this source's 114-degree flat and
204-degree carry centre into those routines' -16 / 152 coordinate chart.
Output returns to actual counter coordinates. Compiling proves no geometry;
support edges and between-knot admission still require independent checks.
"""

import argparse
import hashlib
from pathlib import Path

from simulation.tools.compile_locking_profile import records
from simulation.tools.compile_higher_locking_profiles import lower_profiles, gear_profiles


SHAFT_OFFSET = 130
CRANK_OFFSET = 52
COMPONENTS = ('lower_lock', 'carry_tooth')


def compile_profiles(rows, bands, meshes):
    indexed = {}
    for row in rows:
        if (row.get('station') != 2 or row.get('carry') != 1
                or row.get('trial') is not True or row.get('kernel') != 'native'
                or row.get('component') not in COMPONENTS):
            raise ValueError('Requires independently measured native trial counter-tens pairs at full carry')
        key = row['shaft'], row['component']
        if key in indexed:
            raise ValueError('Duplicate component/shaft row')
        indexed[key] = row
    by_part = {part: {shaft for shaft, name in indexed if name == part} for part in COMPONENTS}
    if any(not shafts or min(shafts) != 114 or max(shafts) != 474
           for shafts in by_part.values()):
        raise ValueError('Each component must cover the complete 114..474 degree shaft chart')
    shafts = by_part['lower_lock']

    for row in [*bands, *meshes]:
        if (row.get('station') != 2 or row.get('carry') != 1
                or row.get('trial') is not True or 'component' in row):
            raise ValueError('Requires complete-print trial counter-tens evidence at full carry')
    if (len(bands) != 10 or {(row['index'], row['kernel']) for row in bands}
            != {(114+72*flat, kernel) for flat in range(5) for kernel in ('native', 'faceted')}):
        raise ValueError('Five indexed bands require both complete-print kernels')
    if (len(meshes) != len(shafts) or {row['shaft'] for row in meshes} != shafts
            or any(row.get('kernel') != 'faceted' for row in meshes)):
        raise ValueError('Every shaft requires its whole-print faceted observation')

    normalized_bands = []
    for index in range(114, 403, 72):
        pair = [row for row in bands if row['index'] == index]
        if any(len(row['bounds']) != 2 or row.get('crank') != 0
               or any(b['free_mm3'] > 0 or b['contact_mm3'] <= 0 for b in row['bounds'])
               for row in pair):
            raise ValueError('Indexed bands must retain free/contact endpoints at crank zero')
        low = max(row['bounds'][0]['last_free'] for row in pair)
        high = min(row['bounds'][1]['last_free'] for row in pair)
        if not low <= index <= high:
            raise ValueError('Indexed free band does not contain its source flat')
        normalized_bands.append({'index': index-SHAFT_OFFSET, 'bounds': [
            {'last_free': low-SHAFT_OFFSET}, {'last_free': high-SHAFT_OFFSET}]})

    normalized = {part: [] for part in COMPONENTS}
    for row in sorted(rows, key=lambda row: (row['shaft'], row['component'])):
        normalized[row['component']].append(row | {
            'shaft': row['shaft']-SHAFT_OFFSET,
            'samples': [(angle-CRANK_OFFSET, volume) for angle, volume in row['samples']],
            'boundaries': [b | {'left': b['left']-CRANK_OFFSET,
                                'right': b['right']-CRANK_OFFSET} for b in row['boundaries']]})
    # Before the carry-tooth region, the first full-print release observes
    # the lower disc. Do not infer the lower closing from the intervening teeth.
    openings = {}
    for row in meshes:
        boundaries = row['boundaries']
        if boundaries and not boundaries[0]['enters_contact']:
            openings[row['shaft']-SHAFT_OFFSET] = boundaries[0]['right']-CRANK_OFFSET
    needed = {row['shaft'] for row in normalized['lower_lock'] if row['boundaries']}
    if not needed <= openings.keys():
        raise ValueError('A lower-disc release lacks a complete-mesh opening')
    lower = lower_profiles(normalized['lower_lock'], normalized_bands, openings)
    gear, supports = gear_profiles(normalized['carry_tooth'])

    def actual(profiles):
        return tuple((start+SHAFT_OFFSET, end+SHAFT_OFFSET,
                      tuple((shaft+SHAFT_OFFSET, a+CRANK_OFFSET, b+CRANK_OFFSET)
                            for shaft, a, b in points)) for start, end, points in profiles)
    supports = tuple(row | {edge: tuple(p+SHAFT_OFFSET for p in row[edge])
                             for edge in ('start', 'end')} for row in supports)
    return actual(lower), actual(gear), supports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--components', type=Path, action='append', required=True)
    parser.add_argument('--refined', type=Path, action='append', default=[],
                        help='Explicitly supersede component/shaft rows with refined measurements')
    parser.add_argument('--bands', type=Path, required=True)
    parser.add_argument('--complete', type=Path, required=True)
    args = parser.parse_args()
    rows = [row for path in args.components for row in records(path) if 'component' in row]
    if args.refined:
        keyed = {(row['shaft'], row['component']): row for row in rows}
        if len(keyed) != len(rows):
            raise ValueError('Duplicate base component/shaft rows')
        for path in args.refined:
            for row in records(path):
                if 'component' in row:
                    keyed[row['shaft'], row['component']] = row
        rows = list(keyed.values())
    bands = [row for row in records(args.bands) if row.get('carry') == 1 and 'kernel' in row]
    meshes = [row for row in records(args.complete)
              if row.get('carry') == 1 and row.get('kernel') == 'faceted']
    lower, gear, supports = compile_profiles(rows, bands, meshes)
    lines = ['"""Unadopted higher-counter contact candidate from independent native curves.',
             '', 'Includes complete-mesh lower release and indexed-band intersections.',
             'Coarse support brackets and interpolation are NOT accepted geometry.',
             '"""', '']
    for path in [*args.components, *args.refined, args.bands, args.complete]:
        lines.append(f'# {path.name}: SHA-256 {hashlib.sha256(path.read_bytes()).hexdigest()}')
    for name, value in (('LOWER_LOCK_SECTORS', lower), ('CARRY_TOOTH_STRIPS', gear)):
        lines.extend(['', f'{name} = ('])
        for start, end, points in value:
            lines.append(f'    ({start!r}, {end!r}, (')
            lines.extend(f'        {point!r},' for point in points)
            lines.append('    )),')
        lines.append(')')
    lines.extend(['', 'SUPPORT_BRACKETS = ('])
    lines.extend(f'    {row!r},' for row in supports)
    lines.append(')')
    target = Path(__file__).resolve().parents[1]/'higher_counter_locking_profiles.py'
    print('*** Begin Patch')
    if target.exists():
        print(f'*** Update File: {target}\n@@')
        print('\n'.join('-'+line for line in target.read_text().splitlines()))
    else:
        print(f'*** Add File: {target}')
    print('\n'.join('+'+line for line in lines))
    print('*** End Patch')


if __name__ == '__main__':
    main()
