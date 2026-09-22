"""Contact probes must offer a precision-preserving placed-mesh path."""

from types import SimpleNamespace
from unittest.mock import patch
import unittest

import trimesh

from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.higher_locking_envelope import contact_reader, faceted_common_volume


def shoulder_meshes():
    lower = trimesh.creation.box(extents=(1, 1, 1))
    upper = trimesh.creation.box(extents=(1, 1, 1))
    lower.apply_translation((0, 0, -138.95))
    upper.apply_translation((0, 0, -137.95000038146972))
    return lower, upper


class ContactProbePrecisionTest(unittest.TestCase):
    def test_mesh_conversion_does_not_collapse_positive_placed_contact(self):
        lower, upper = shoulder_meshes()
        common = mesh_solid(lower, world_precision=64) ^ mesh_solid(upper, world_precision=64)
        self.assertGreater(faceted_common_volume(common), 0)
        rounded = mesh_solid(lower, world_precision=32) ^ mesh_solid(upper, world_precision=32)
        self.assertEqual(faceted_common_volume(rounded), 0)

    def test_contact_reader_preserves_requested_mesh_precision(self):
        lower, upper = shoulder_meshes()
        node = SimpleNamespace(set_state=lambda **kw: None, assemble=lambda: None,
                               build_stls=lambda: None)
        leaves = [('lower', SimpleNamespace(mesh=lower)), ('upper', SimpleNamespace(mesh=upper))]
        with patch('simulation.tools.higher_locking_envelope.world_solids', return_value={}), \
             patch('simulation.tools.higher_locking_envelope.rigid_leaves', return_value=leaves):
            read = contact_reader(reference=0, node_type=lambda: node,
                                  stack_path='upper', bell_path='lower', world_precision=64)
            self.assertGreater(read(0, 'faceted'), 0)


if __name__ == '__main__':
    unittest.main()
