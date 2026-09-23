"""Joint-site witnesses must use the parent frame, not the imported leaf frame."""

from types import SimpleNamespace
import unittest

import numpy as np
from simulation.tools.moving_seats import world_frames


class WorldFramesTest(unittest.TestCase):
    def test_optional_assembly_frames_preserve_default_leaf_inventory(self):
        leaf = SimpleNamespace(name='slider', rigid=True, operations=[
            SimpleNamespace(angle=90, axis=(1, 0, 0)),
            SimpleNamespace(translation=(4, 5, 6))])
        group = SimpleNamespace(name='station', rigid=False, children=[leaf],
                                operations=[SimpleNamespace(translation=(1, 2, 3))])
        root = SimpleNamespace(rigid=False, operations=[], children=[group])
        ordinary = world_frames(root)
        expanded = world_frames(root, include_assemblies=True)
        self.assertEqual(set(ordinary), {'Curta.station.slider'})
        self.assertEqual(set(expanded), {'Curta', 'Curta.station', 'Curta.station.slider'})
        np.testing.assert_array_equal(ordinary['Curta.station.slider'],
                                      expanded['Curta.station.slider'])
        np.testing.assert_array_equal(expanded['Curta.station'][:3, 3], (1, 2, 3))
        np.testing.assert_array_equal(expanded['Curta.station.slider'][:3, 3], (5, 7, 9))
        np.testing.assert_array_equal(expanded['Curta.station'][:3, :3] @ (0, 0, -1),
                                      (0, 0, -1))
        # The leaf's own rotated -Z is not the parent-frame prismatic axis.
        self.assertGreater((expanded['Curta.station.slider'][:3, :3] @ (0, 0, -1))[1], .99)


if __name__ == '__main__':
    unittest.main()
