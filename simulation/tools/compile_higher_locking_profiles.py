"""Emit a candidate profile patch from measured native tens contact pairs.

This is a diagnostic compiler, not acceptance. In particular, the carry-tooth
support brackets and between-knot curves must be refined and checked against
both complete-print kernels before an operating restraint can be adopted.
"""

import argparse
from pathlib import Path

from simulation.tools.compile_locking_profile import records, compact


def lower_profiles(rows, bands, mesh_openings=None):
    profiles = []
    for index, band in enumerate(bands):
        start = band['bounds'][1]['last_free']-.002
        following = bands[(index+1) % 5]
        end = following['bounds'][0]['last_free']+.002+(360 if index == 4 else 0)
        points = []
        for row in rows:
            shaft = row['shaft']
            if not start < shaft < end:
                continue
            opening = [b['right'] for b in row['boundaries'] if not b['enters_contact']]
            closing = [b['left'] for b in row['boundaries'] if b['enters_contact']]
            assert len(opening) == len(closing) == 1, row
            assert opening[0] < 90 < closing[0], row
            if mesh_openings is not None:
                opening[0] = max(opening[0], mesh_openings[shaft])
            points.append((shaft, opening[0], closing[0]))
        assert len(points) >= 3, (start, end)
        profiles.append((start, end, compact(points)))
    return profiles


def gear_profiles(rows, support_brackets=None):
    """Track the two adjacent gear teeth independently through each source flat.

    The measured carry centre is crank 152; the source ratio is 72/11.25.
    These numbers only label measured contour branches. They supply no contact
    coordinate and never substitute the prescribed motion for measured limits.
    """
    profiles, supports = [], []
    periodic = {row['shaft']: row for row in rows}
    for row in rows:
        for shift in (-360, 360):
            periodic.setdefault(row['shaft']+shift, row | {'shaft': row['shaft']+shift})
    for flat in range(5):
        base = -16+72*flat
        # Overlap neighbouring charts with actual measured rows. Merely
        # cutting every strip at an indexed angle would make its phase-gap
        # zero there and falsely admit the very real indexed gear contact.
        # The +/-360 aliases are the same physical pose, not assumed 72-degree
        # tooth symmetry; all five source flats retain their own measurements.
        chart_start = max(p for p in periodic if p < base)
        chart_end = min(p for p in periodic if p > base+72)
        selected = sorted((row for p, row in periodic.items()
                           if chart_start <= p <= chart_end), key=lambda r: r['shaft'])
        assert len(selected) >= 3, flat
        strips = ([], [])
        for row in selected:
            boundaries = row['boundaries']
            assert len(boundaries) in (0, 2, 4), row
            assert row['samples'][0][1] <= 0 and row['samples'][-1][1] <= 0, row
            assigned = set()
            for start, end in zip(boundaries[::2], boundaries[1::2]):
                assert start['enters_contact'] and not end['enters_contact'], row
                middle = (start['left']+end['right'])/2
                phase = row['shaft']-base
                centres = (152+phase/(72/11.25), 152+(phase-72)/(72/11.25))
                slot = min(range(2), key=lambda i: abs(middle-centres[i]))
                assert slot not in assigned, row
                assigned.add(slot)
                strips[slot].append((row['shaft'], start['left'], end['right']))
        measured_phases = [row['shaft'] for row in selected]
        for slot, points in enumerate(strips):
            assert len(points) >= 3, (flat, slot)
            present = {p[0] for p in points}
            assert all(p in present for p in measured_phases
                       if points[0][0] <= p <= points[-1][0]), (flat, slot, points)
            # Bracket each birth/death with its nearest measured absent phase.
            # Hold endpoint curves over that bracket conservatively. This is
            # explicitly provisional and must survive the geometry controls;
            # it is not an inferred two-degree manufacturing clearance.
            lo = max((p for p in measured_phases if p < points[0][0]), default=chart_start)
            hi = min((p for p in measured_phases if p > points[-1][0]), default=chart_end)
            if support_brackets is not None:
                side = 'birth' if slot == 1 else 'death'
                measured = support_brackets[flat, side]
                assert measured['width'] < .0001, measured
                edge = points[0][0] if slot == 1 else points[-1][0]
                assert abs(edge-measured['inside']) < 1e-8, (flat, side, edge, measured)
                # Same explicit .002-degree free-side shaft guard as the
                # indexed locking bands, not a discarded positive volume.
                if slot == 1:
                    lo = measured['outside']-.002
                else:
                    hi = measured['outside']+.002
            profiles.append((lo, hi, compact(points)))
            supports.append({'flat': flat, 'tooth': slot,
                             'start': (lo, points[0][0]), 'end': (points[-1][0], hi)})
    return profiles, supports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pairs', help='Native lower_lock and carry_tooth records')
    parser.add_argument('bands', help='Native indexed-band brackets')
    parser.add_argument('--extra', action='append', default=[],
                        help='Additional/refined pair records, overriding the same shaft sample')
    parser.add_argument('--mesh-openings', help='Complete-print faceted lower-disc release brackets')
    parser.add_argument('--supports', help='Refined native strip birth/death brackets; requires near-edge curve rows')
    args = parser.parse_args()
    raw = records(args.pairs)
    for path in args.extra:
        raw.extend(records(path))
    indexed = {(r['pair'], r['shaft']): r for r in raw
               if r.get('kernel') in ('native', 'dual')
               and r.get('pair') in ('lower_lock', 'carry_tooth')}
    raw = list(indexed.values())
    grouped = {pair: sorted((r for r in raw if r.get('pair') == pair
                            and r.get('kernel') in ('native', 'dual')), key=lambda r: r['shaft'])
               for pair in ('lower_lock', 'carry_tooth')}
    for pair, rows in grouped.items():
        assert rows and rows[0]['shaft'] == -16 and rows[-1]['shaft'] == 344, pair
        assert len({r['shaft'] for r in rows}) == len(rows), pair
    bands = sorted((r for r in records(args.bands) if r.get('pair') == 'lower_lock'),
                   key=lambda r: r['index'])
    assert len(bands) == 5
    mesh_openings = ({r['shaft']: r['first_free'] for r in records(args.mesh_openings)}
                     if args.mesh_openings else None)
    lower = lower_profiles(grouped['lower_lock'], bands, mesh_openings)
    brackets = ({(r['flat'], r['side']): r for r in records(args.supports)}
                if args.supports else None)
    if brackets is not None:
        assert len(brackets) == 10
    gear, supports = gear_profiles(grouped['carry_tooth'], brackets)
    lines = ['"""Measured diagnostic tens profiles; geometry acceptance remains mandatory.',
             '', 'Native ingredient-pair curves plus measured complete-mesh lower release.',
             'These are not whole-print clearance certification.',
             'Carry-tooth support brackets are provisional; see the generating tool.',
             '"""', '']
    for name, profiles in (('LOWER_LOCK_SECTORS', lower), ('CARRY_TOOTH_STRIPS', gear)):
        lines.append(f'{name} = (')
        for start, end, points in profiles:
            lines.append(f'    ({start:.9f}, {end:.9f}, (')
            lines.extend(f'        ({x:.9f}, {a:.9f}, {b:.9f}),' for x, a, b in points)
            lines.append('    )),')
        lines.extend([')', ''])
    lines.append(f'SUPPORT_BRACKETS = {supports!r}')
    target = Path(__file__).resolve().parents[1] / 'higher_locking_profiles.py'
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
