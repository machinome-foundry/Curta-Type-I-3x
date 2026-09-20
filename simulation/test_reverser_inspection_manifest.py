"""The inspection is selectable without replacing the operating model."""

from pathlib import Path
import tomllib
import unittest


class InspectionManifestTest(unittest.TestCase):
    def test_inspection_is_available_and_operating_default_is_preserved(self):
        manifest = tomllib.loads((Path(__file__).parents[1] / 'pyproject.toml').read_text())
        config = manifest['tool']['machinome']
        self.assertEqual(config['model'], 'operating_curta')
        self.assertEqual(config['models']['reverser_inspection'],
                         'simulation.reverser_inspection:ReverserInspection')
