"""The covers must fit at the already verified window/axle placement."""

from machinome.test import TestCase
from simulation.housing_thread import HousingThreadBench


class HousingThreadTest(TestCase):
    node = HousingThreadBench

    def test_threaded_covers_clear_at_the_installed_datum(self):
        self.assertNotIntersecting(self.node.digits_cover, self.node.upper_housing)

    def test_thread_seat_has_small_axial_play_but_remains_captured(self):
        cover, housing = self.node.digits_cover, self.node.upper_housing
        self.assertFreeWithin(cover, .02, against=housing, along=(0, 0, 1))
        self.assertBlockedBeyond(cover, .3, against=housing, along=(0, 0, 1))

    def test_fitting_only_removes_material_inside_the_measured_thread_seat_zone(self):
        import numpy as np
        import trimesh
        import manifold3d as manifold
        from simulation.cover_fits import FittedUpperHousing, mesh_solid
        from simulation.contracts import assert_connected_material
        raw = trimesh.load_mesh(self.node.upper_housing.stl_source)
        original = FittedUpperHousing(thread_gap=0).adjust(raw.copy())
        fitted = self.node.upper_housing.adjust(raw.copy())
        assert_connected_material(fitted)
        before, after = mesh_solid(original), mesh_solid(fitted)
        removed, added = before - after, after - before
        self.assertEqual(removed.status(), manifold.Error.NoError)
        self.assertEqual(added.status(), manifold.Error.NoError)
        # Coplanar Boolean shells can have a signed floating volume even
        # without finite-thickness added material. Audit their vertices AND
        # face interiors against the source surface at STL length precision;
        # this is not a clearance/interference volume epsilon.
        added_mesh = added.to_mesh64()
        vertices = added_mesh.vert_properties[:, :3]
        if len(vertices):
            samples = np.concatenate((vertices, vertices[added_mesh.tri_verts].mean(axis=1)))
            for start in range(0, len(samples), 128):
                _, distance, _ = trimesh.proximity.closest_point(original, samples[start:start+128])
                self.assertLess(distance.max(), .00001)
        self.assertGreater(removed.volume(), 200)
        self.assertLess(removed.volume(), 400)
        removed_mesh = removed.to_mesh64()
        vertices = removed_mesh.vert_properties[:, :3]
        points = np.concatenate((vertices, vertices[removed_mesh.tri_verts].mean(axis=1)))
        radius = np.linalg.norm(points[:, :2], axis=1)
        # Bounds include polygonal-cylinder chord sag, not contact tolerance.
        permitted = ((radius >= 71.899) & (radius <= 75.00001) &
                     (points[:, 2] >= 35.89999) & (points[:, 2] <= 42.40001))
        protected = points[~permitted]
        # As above, reject finite removal outside the zone; coincident shells
        # must lie on BOTH the before and after surfaces within STL precision.
        for surface in (original, fitted):
            for start in range(0, len(protected), 128):
                _, distance, _ = trimesh.proximity.closest_point(surface, protected[start:start+128])
                self.assertLess(distance.max(), .00001)

        built = trimesh.load_mesh(self.node.upper_housing.stl_file)
        self.assertEqual(len(built.faces), len(fitted.faces))
        import io
        encoded = trimesh.load_mesh(io.BytesIO(fitted.export(file_type='stl')), file_type='stl')
        assert_connected_material(encoded)
        assert_connected_material(built)
        from scipy.spatial import cKDTree
        for first, second in ((built, fitted), (fitted, built)):
            expected = np.concatenate((second.vertices, second.triangles_center))
            actual = np.concatenate((first.vertices, first.triangles_center))
            self.assertLess(cKDTree(expected).query(actual)[0].max(), .00001)
