"""A world-coordinate float32 cast must not hide a supplied mesh contact."""

from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

import manifold3d as manifold
import trimesh

from simulation.tools.interference import inventory


class InterferencePrecisionTest(unittest.TestCase):
    def test_positive_signed_sum_requires_positive_extent_in_every_axis(self):
        root = SimpleNamespace(rigid=False, children=[
            SimpleNamespace(name=name, rigid=True,
                            mesh=trimesh.creation.box(extents=(1, 1, 1)))
            for name in ('a', 'b')])
        key = 'Curta.a / Curta.b'
        for height in (0, 1e-15):
            solid = MagicMock()
            solid.status.return_value = manifold.Error.NoError
            common = solid.__xor__.return_value
            common.status.return_value = manifold.Error.NoError
            common.volume.return_value = 1e-30
            common.bounding_box.return_value = (0, 0, 0, 1, 1, height)
            with patch('simulation.tools.interference.manifold.Manifold', return_value=solid):
                report = inventory(root, world_precision=64)
            with self.subTest(height=height):
                if height == 0:
                    self.assertEqual(report['overlap_mm3'], {})
                    self.assertEqual(report['nonspatial_contact_sums'][key], {
                        'signed_sum_mm3': 1e-30, 'bounds': [0, 0, 0, 1, 1, 0]})
                else:
                    self.assertEqual(report['overlap_mm3'], {key: 1e-30})
                    self.assertEqual(report['nonspatial_contact_sums'], {})

    def test_world_double_precision_retains_rounded_local_stl_shoulder_overlap(self):
        lower = trimesh.creation.box(extents=(1, 1, 1))
        upper = trimesh.creation.box(extents=(1, 1, 1))
        lower.apply_translation((0, 0, -138.95))
        upper.apply_translation((0, 0, -137.95000038146972))
        root = SimpleNamespace(rigid=False, children=[
            SimpleNamespace(name='lower', rigid=True, mesh=lower),
            SimpleNamespace(name='upper', rigid=True, mesh=upper),
        ])
        report = inventory(root, world_precision=64)
        self.assertFalse(report['refusals'])
        self.assertGreater(report['overlap_mm3']['Curta.lower / Curta.upper'], 0)
        self.assertAlmostEqual(report['overlap_mm3']['Curta.lower / Curta.upper'],
                               .00000038146972, places=12)
        # The old diagnostic rounds both world faces to one coordinate.
        self.assertEqual(inventory(root, world_precision=32)['overlap_mm3'], {})


if __name__ == '__main__':
    unittest.main()
