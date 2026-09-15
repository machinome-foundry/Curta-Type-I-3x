"""Check actual published decals, not just Python declarations.

Run after ``solid build`` or pass an exported ``manifest.json``. An optional
baseline records the material artifacts before adding markings; it is evidence,
not a golden file that changes the expected mechanical design.
"""

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import unittest

import numpy as np
import trimesh


def entries(node, parent=''):
    path = parent + '.' + node['name']
    yield path, node
    for child in node.get('children', []):
        yield from entries(child, path)


@lru_cache(maxsize=None)
def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def material_record(document, directory):
    return {
        path: {'model': node['model'], 'piece': node.get('piece'),
               'stl': digest(directory / node['model']),
               'brep': digest((directory / node['model']).with_suffix('.brep'))
               if (directory / node['model']).with_suffix('.brep').exists() else None}
        for path, node in entries(document['root']) if 'model' in node
    }


class PublishedMarkingsTest(unittest.TestCase):
    def test_digit_ink_contrasts_with_the_original_sheet_ground(self):
        inputs = registers = 0
        for _, node in entries(DOCUMENT['root']):
            if node['name'] == 'number_roll':
                self.assertEqual(node['color'], '#222831')
                mark, = node['markings']
                self.assertEqual(mark['color'], '#FFFFFF')
                inputs += 1
            elif node['name'].startswith('results_dial'):
                self.assertEqual(node['color'], '#eadfc6')
                mark, = node['markings']
                self.assertEqual(mark['color'], '#111111')
                registers += 1
        self.assertEqual((inputs, registers), (8, 17))

    def test_all_supported_occurrences_carry_artwork(self):
        counts = Counter()
        for _, node in entries(DOCUMENT['root']):
            for mark in node.get('markings', []):
                counts[mark['name']] += 1
        self.assertEqual(counts, {'digits': 25, 'input_places': 1,
                                  'branding': 1, 'reversing_arrows': 1})

    def test_decals_are_portable_surfaces_on_the_measured_bands(self):
        seen = set()
        for _, node in entries(DOCUMENT['root']):
            for mark in node.get('markings', []):
                self.assertNotIn('piece', mark)
                self.assertNotIn('placement', mark)
                self.assertFalse(Path(mark['model']).is_absolute())
                path = DIRECTORY / mark['model']
                self.assertTrue(path.is_file(), path)
                if path in seen:
                    continue
                seen.add(path)
                mesh = trimesh.load_mesh(path)
                self.assertGreater(len(mesh.faces), 0)
                self.assertFalse(mesh.is_watertight)
                self.assertTrue(np.isfinite(mesh.vertices).all())
                if node['name'].startswith('results_dial'):
                    radius, low, high = 9.45, .9, 11.4
                elif node['name'] == 'number_roll':
                    radius, low, high = 9.3, 0, 15
                elif node['name'] == 'lower_housing':
                    radius, low, high = 68.1625, 36, 49.8
                elif node['name'] == 'upper_outer_sleeve':
                    radius, low, high = 71.25, 2.55, 64.5
                elif node['name'] == 'bottom_housing':
                    radius, low, high = 68.1, 0, 132
                else:
                    self.fail(f'Unexpected marked part: {node["name"]}')
                # STL vertices land on the nominal analytic cylinder; triangles
                # are chords within the framework's tessellation tolerance.
                np.testing.assert_allclose(np.linalg.norm(mesh.vertices[:, :2], axis=1),
                                           radius, atol=1e-5, rtol=0)
                self.assertGreaterEqual(mesh.bounds[0, 2], low - 1e-5)
                self.assertLessEqual(mesh.bounds[1, 2], high + 1e-5)
        self.assertEqual(len(seen), 6)  # Two dial types, roll, three housing parts.

    def test_no_material_or_piece_changes(self):
        if BASELINE is None:
            self.skipTest('Pass --baseline for the before/after material comparison')
        actual = material_record(DOCUMENT, DIRECTORY)
        expected = json.loads(BASELINE.read_text())
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path, nargs='?', default=Path('_build/viewer.json'))
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--record-baseline', type=Path)
    args = parser.parse_args()
    DOCUMENT = json.loads(args.manifest.read_text())
    DIRECTORY = args.manifest.parent
    BASELINE = args.baseline
    if args.record_baseline:
        args.record_baseline.write_text(json.dumps(material_record(DOCUMENT, DIRECTORY), indent=2) + '\n')
    else:
        unittest.main(argv=['check_markings'], verbosity=2)
