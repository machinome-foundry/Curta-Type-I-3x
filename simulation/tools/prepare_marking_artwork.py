"""Extract paint regions from upstream cutting sheets without changing glyphs.

``--check`` verifies the tracked assets. Otherwise print an apply_patch patch
for missing/outdated assets; apply it explicitly, never during a model build.
All source coordinates, path data and ancestor transforms are preserved.
"""

import argparse
from pathlib import Path
from xml.etree import ElementTree as ET

PROJECT = Path(__file__).resolve().parents[2]
OUTPUT = PROJECT / 'simulation/artwork'
SHEETS = {
    'input-digits.svg': ('Input_Digits-new.svg', {
        'path6', 'path10', 'path12', 'path14', 'path16', 'path20',
        'path22', 'path28', 'path32', 'path36'}),
    'sleeve-branding.svg': ('upper_outer_sleeve.svg', {
        'path6', 'path8', 'path12', 'path14', 'path16', 'path24', 'path26'}),
    'input-places.svg': ('lower_housing.svg', {
        'path4185', 'path4189', 'path4191', 'path4193', 'path4195',
        'path4199', 'path4201', 'path4207'}),
}


def prepared(source, identifiers):
    original = ET.parse(PROJECT / 'Drawings' / source).getroot()
    found = {e.get('id') for e in original.iter()} & identifiers
    if found != identifiers:
        raise ValueError(f'{source}: missing selected paths {identifiers - found}')
    attrs = {key: original.attrib[key] for key in ('width', 'height', 'viewBox')}
    if source == 'upper_outer_sleeve.svg':
        # Author's Cricut README specifies 62 mm, not 62 inches. Its numeric
        # viewBox is already millimetres; only the physical unit is wrong.
        attrs['width'] = attrs['width'].removesuffix('in') + 'mm'
        attrs['height'] = attrs['height'].removesuffix('in') + 'mm'
    root = ET.Element('svg', {'xmlns': 'http://www.w3.org/2000/svg', **attrs})
    root.append(ET.Comment(f' Derived from Drawings/{source}; see README.md. '))

    def selected(element):
        children = [result for child in element if (result := selected(child)) is not None]
        if element.get('id') not in identifiers and not children:
            return None
        tag = element.tag.rsplit('}', 1)[-1]
        kept = ET.Element(tag, {key: value for key, value in element.attrib.items()
                               if key in ('id', 'd', 'transform', 'style')})
        kept.extend(children)
        return kept

    root.extend(result for child in original if (result := selected(child)) is not None)
    ET.indent(root, space='  ')
    return ET.tostring(root, encoding='unicode') + '\n'


def artwork():
    for target, (source, identifiers) in SHEETS.items():
        yield OUTPUT / target, prepared(source, identifiers)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changes = [(path, content) for path, content in artwork()
               if not path.exists() or path.read_text() != content]
    if args.check:
        if changes:
            raise SystemExit('Outdated marking artwork: ' + ', '.join(p.name for p, _ in changes))
        print('All three derived artwork files match their upstream paths.')
    elif changes:
        print('*** Begin Patch')
        for path, content in changes:
            if path.exists():
                print(f'*** Delete File: {path}')
            print(f'*** Add File: {path}')
            for line in content.splitlines():
                print('+' + line)
        print('*** End Patch')
