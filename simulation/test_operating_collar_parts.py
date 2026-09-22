"""Source-seat facings remove only their independently bounded axial skins."""

import io
import unittest

import cadquery as cq
import manifold3d as manifold
import numpy as np
import trimesh

from simulation.contracts import assert_connected_material
from simulation.cover_fits import mesh_solid
from simulation.collar_seat_trial import TrialShoulderCollar
from simulation.standard.parts import CrankCollarWasher
from simulation.operating_collar_parts import SeatedCollar, SeatedCollarWasher


class CollarSeatFacingTest(unittest.TestCase):
    def test_collar_bottom_has_real_clearance_without_moving_the_spider_seat(self):
        source = trimesh.load_mesh(SeatedCollar.stl_source)
        shoulder = TrialShoulderCollar().adjust(source.copy())
        fitted = SeatedCollar().adjust(source.copy())
        assert_connected_material(fitted)
        encoded = trimesh.load_mesh(io.BytesIO(fitted.export(file_type='stl')),
                                    file_type='stl')
        assert_connected_material(encoded)
        np.testing.assert_allclose(encoded.bounds, fitted.bounds, atol=.00001, rtol=0)
        self.assertAlmostEqual(fitted.bounds[0, 2], .05, delta=.00001)
        np.testing.assert_allclose(fitted.bounds[1], shoulder.bounds[1], atol=.00001)
        before, after = mesh_solid(shoulder), mesh_solid(fitted)
        # Coplanar triangulation can leave signed zero-volume surface scraps
        # after a mesh difference. Locate every reported added vertex and face
        # centre on the pre-existing surface; no positive interior is waived.
        added = (after-before).to_mesh64()
        if len(added.tri_verts):
            vertices = added.vert_properties[:, :3]
            points = np.concatenate((vertices, vertices[added.tri_verts].mean(axis=1)))
            _, distances, _ = trimesh.proximity.closest_point(shoulder, points)
            self.assertLess(distances.max(), .00001)
        removed = before-after
        self.assertGreater(removed.volume(), 0)
        # The source bottom is local Z0. No thread, pin bore or shoulder
        # material above the .05 mm bottom-seat facing may disappear.
        protected = manifold.Manifold.cube((100, 100, 100)).translate((-50, -50, .05001))
        outside = (removed ^ protected).to_mesh64()
        if len(outside.tri_verts):
            vertices = outside.vert_properties[:, :3]
            points = np.concatenate((vertices, vertices[outside.tri_verts].mean(axis=1)))
            for surface in (shoulder, fitted):
                _, distances, _ = trimesh.proximity.closest_point(surface, points)
                self.assertLess(distances.max(), .00001)

    def test_washer_seat_facings_preserve_its_radial_profile_and_middle(self):
        source = CrankCollarWasher().shape()
        fitted = SeatedCollarWasher().adjust(source)
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        self.assertEqual(fitted.cut(source).Volume(), 0)
        before, after = source.BoundingBox(), fitted.BoundingBox()
        self.assertAlmostEqual(before.zmin, 0, delta=.00001)
        self.assertAlmostEqual(after.zmin, .05, delta=.00001)
        self.assertAlmostEqual(before.zmax, 3.2, delta=.00001)
        self.assertAlmostEqual(after.zmax, 3.15, delta=.00001)
        for name in ('xmin', 'xmax', 'ymin', 'ymax'):
            self.assertAlmostEqual(getattr(before, name), getattr(after, name), delta=.00001)
        removed = source.cut(fitted)
        self.assertGreater(removed.Volume(), 0)
        permitted = cq.Solid.makeBox(100, 100, .05001, cq.Vector(-50, -50, -.000001))
        permitted = permitted.fuse(cq.Solid.makeBox(
            100, 100, .05001, cq.Vector(-50, -50, 3.149999)))
        self.assertEqual(removed.cut(permitted).Volume(), 0)


if __name__ == '__main__':
    unittest.main()
