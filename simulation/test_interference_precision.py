"""A world-coordinate float32 cast must not hide a supplied mesh contact."""

from types import SimpleNamespace
import unittest

import trimesh

from simulation.tools.interference import inventory


class InterferencePrecisionTest(unittest.TestCase):
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
