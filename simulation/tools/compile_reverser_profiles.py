"""Emit readable model data from a complete, pinned installed-cover record.

This compiler checks the record's completeness, not CAD containment itself.
The independent native/mesh probe owns that proof. No angular sectors are
mirrored, interpolated or dropped; only equal axial bands are grouped.
"""

import argparse
from collections import defaultdict
import hashlib
import json
from math import isfinite
from pathlib import Path
from pprint import pformat

from simulation.tools.reverser_profile_cover import axial_allowance


INPUT_PATHS = tuple('Curta.transmission.turns.'+name+'.'+part for name, part in (
    ('ones', 'p_10218_1'), ('tens', 'p_10230_410008_1_419080'),
    ('hundreds', 'p_10230_410008_1_419068'), ('digit_4', 'p_10230_410008_1_419182'),
    ('digit_5', 'p_10230_410008_1_419105'), ('digit_6', 'p_10230_410008_1_419237')))
DRUM_PATHS = tuple('Curta.main_drive.stepped_drum.main_axle_step_drum_1.'+name
                  for name in ('main_axle_step_drum_top_1', 'main_axle_step_drum_bottom_1'))
LOW, HIGH = -6.9425, 3.9075


def number(value):
    if type(value) not in (int, float) or not isfinite(value):
        raise ValueError('Expected finite measured cover value')
    return value


def compile_profiles(rows):
    from machinome.simulation.profile import ConvexProfile

    paths = (*INPUT_PATHS, *DRUM_PATHS)

    def complete(kind):
        records = [r for r in rows if r['kind'] == kind]
        if len(records) != len(paths) or {r['path'] for r in records} != set(paths):
            raise ValueError(f'{kind} requires one complete record for every print')
        return {r['path']: r for r in records}

    envelopes, verdicts = complete('radial_envelope'), complete('installed_mesh_verdict')
    by_path = defaultdict(list)
    for row in rows:
        if row['kind'] == 'installed_profile':
            by_path[row['path']].append(row)
    if set(by_path) != set(paths):
        raise ValueError('Profiles must retain all six inputs and both drum halves')
    for path, count in zip(paths, (3, 1, 1, 1, 1, 1, 9, 10)):
        envelope, verdict = envelopes[path], verdicts[path]
        if (number(envelope['native_outside_mm3']) != 0
                or number(envelope['mesh_radius_mm']) > number(envelope['radius_mm'])):
            raise ValueError('Failed complete-print radial envelope')
        if (verdict['separated'] is not True
                or number(verdict['native_remainder_after_exclusion_mm3']) != 0
                or number(verdict['native_remainder_mm3']) < 0
                or number(verdict['uncovered_control_mm3']) <= 0
                or number(verdict['remainder_mm3']) < 0):
            raise ValueError('Failed complete-print coverage verdict')
        if verdict['remainder_empty'] is True:
            if verdict['remainder_mm3'] != 0:
                raise ValueError('Empty remainder must have zero volume')
        elif not (number(verdict['residual_radius_mm'])+number(verdict['other_outer_radius_mm'])
                  < number(verdict['minimum_axis_radius_mm'])):
            raise ValueError('Uncovered mesh material is not radially separated')
        parts = by_path[path]
        if (len(parts) != count or verdict['components'] != count
                or {r['component'] for r in parts} != set(range(count))):
            raise ValueError('Missing or duplicate installed component profile')
        for row in parts:
            low, high = map(number, row['source_height'])
            if not low < high:
                raise ValueError('Invalid axial band')
            axial_allowance(row)
            for point in row['points']:
                if len(point) != 2:
                    raise ValueError('Expected XY points')
                for value in point:
                    number(value)
            for polygon in row['polygons']:
                if any(type(i) is not int or not 0 <= i < len(row['points']) for i in polygon):
                    raise ValueError('Invalid profile point index')
            ConvexProfile([[row['points'][i] for i in polygon] for polygon in row['polygons']])

    exclusions = [r for r in rows if r['kind'] == 'axial_exclusion']
    if len(exclusions) != 1:
        raise ValueError('Expected the complete-print lower axial exclusion')
    exclusion = exclusions[0]
    if (exclusion['reverser_range'] != [LOW, HIGH]
            or exclusion['crank_elevation_range'] != [0, 9]
            or not number(exclusion['minimum_input_z_in_drum_frame']) > number(exclusion['bottom_clip'])):
        raise ValueError('Axial exclusion or driver ranges changed')
    inputs = [r for p in INPUT_PATHS for r in by_path[p]]
    lowest = min(r['source_height'][0]-axial_allowance(r)+LOW
                 -number(r['reference_reverser_height']) for r in inputs)
    highest = max(r['source_height'][1]+axial_allowance(r)+9 for r in by_path[DRUM_PATHS[1]])
    if not lowest > highest:
        raise ValueError('Covered lower drum is not axially separated')

    profiles, gears, drums = [], [], []
    for path in INPUT_PATHS:
        parts = by_path[path]
        first = parts[0]
        if any(any(row[key] != first[key] for key in
                   ('points', 'polygons', 'axis', 'reference_shaft_angle', 'reference_reverser_height'))
               for row in parts):
            raise ValueError('Input bands must share the same measured XY cover and reference')
        profiles.append(dict(points=first['points'], polygons=first['polygons']))
        gears.append(dict(profile=len(profiles)-1, axis=list(map(number, first['axis'][:2])),
            reference=number(first['reference_shaft_angle']),
            height=number(first['reference_reverser_height']),
            bands=[(r['source_height'][0]-axial_allowance(r),
                    r['source_height'][1]+axial_allowance(r)) for r in parts]))
    groups = defaultdict(list)
    for row in by_path[DRUM_PATHS[0]]:
        groups[tuple(row['source_height'])].append(row)
    for (low, high), parts in groups.items():
        points, polygons = [], []
        for row in parts:
            offset = len(points)
            points.extend(row['points'])
            polygons.extend([[i+offset for i in polygon] for polygon in row['polygons']])
        profiles.append(dict(points=points, polygons=polygons))
        allowance = max(axial_allowance(r) for r in parts)
        drums.append(dict(profile=len(profiles)-1, low=low-allowance, high=high+allowance))
    return dict(profiles=profiles, gears=gears, drums=drums, range=[LOW, HIGH],
                covered_paths=list(paths), lower_axial_separation=[lowest, highest])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    if hashlib.sha256(raw).hexdigest() != args.sha256:
        parser.error('Evidence digest differs from the explicitly accepted complete record')
    data = compile_profiles([json.loads(line) for line in raw.splitlines()])
    target = Path(__file__).resolve().parents[1]/'reverser_profile_data.py'
    lines = ['"""Measured installed reverser covers; generated by compile_reverser_profiles.',
             '', 'Model data, not a continuous-contact certificate. Reprove native and actual',
             'published mesh containment after any change to the covered parts or placement.',
             '"""', '', f'EVIDENCE_SHA256 = {args.sha256!r}', '', 'DATA = '+pformat(data, width=100)]
    text = '\n'.join(lines)
    print('*** Begin Patch')
    if target.exists():
        print(f'*** Update File: {target}\n@@')
        print('\n'.join('-'+line for line in target.read_text().splitlines()))
    else:
        print(f'*** Add File: {target}')
    print('\n'.join('+'+line for line in text.splitlines()))
    print('*** End Patch')


if __name__ == '__main__':
    main()
