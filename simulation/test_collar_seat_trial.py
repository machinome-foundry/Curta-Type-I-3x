"""A bounded shoulder fit must seat AND retain the unchanged spider ring."""

from machinome.test import TestCase
from simulation.collar_seat_trial import CollarShoulderBench


class CollarShoulderTest(TestCase):
    node = CollarShoulderBench

    def test_spider_mount_clears_the_collar_at_the_measured_carrier_seat(self):
        self.assertNotIntersecting(self.node.spider, self.node.collar)
        self.assertFreeWithin(self.node.spider, .04, against=self.node.collar,
                              along=(0, 0, 1))

    def test_collar_still_captures_the_ring_above_its_small_seat_gap(self):
        self.assertBlockedBeyond(self.node.spider, .1, against=self.node.collar,
                                 along=(0, 0, 1), directions='forward')

    def test_facing_keeps_source_material_outside_the_shoulder_skin(self):
        import io
        import numpy as np
        import trimesh
        from simulation.contracts import assert_connected_material
        from simulation.cover_fits import mesh_solid

        raw = trimesh.load_mesh(self.node.collar.stl_source)
        fitted = self.node.collar.adjust(raw.copy())
        assert_connected_material(fitted)
        encoded = trimesh.load_mesh(io.BytesIO(fitted.export(file_type='stl')),
                                   file_type='stl')
        assert_connected_material(encoded)
        built = trimesh.load_mesh(self.node.collar.stl_file)
        assert_connected_material(built)
        from scipy.spatial import cKDTree
        self.assertEqual(len(built.faces), len(encoded.faces))
        for first, second in ((built, encoded), (encoded, built)):
            a = np.concatenate((first.vertices, first.triangles_center))
            b = np.concatenate((second.vertices, second.triangles_center))
            self.assertLess(cKDTree(a).query(b)[0].max(), .00001)
        before, after = mesh_solid(raw), mesh_solid(fitted)
        removed, added = before - after, after - before
        self.assertGreater(removed.volume(), 500)
        self.assertLess(removed.volume(), 650)
        # Length precision only for coplanar source-surface artifacts, never
        # an overlap-volume epsilon. Finite removed material must lie in the
        # measured radial shoulder skin; the entire bore and thread are kept.
        for common, surfaces, restrict in (
                (added, (raw,), False), (removed, (raw, fitted), True)):
            mesh = common.to_mesh64()
            vertices = mesh.vert_properties[:, :3]
            if not len(vertices):
                continue
            points = np.concatenate((vertices, vertices[mesh.tri_verts].mean(axis=1)))
            if restrict:
                radius = np.linalg.norm(points[:, :2], axis=1)
                # The source stem's R17.941 vertices have flat chords;
                # face-interior samples reach R17.937050, not R17.941.
                permitted = ((radius >= 17.936) & (radius <= 24.051) &
                             (points[:, 2] >= 38.99999) &
                             (points[:, 2] <= 39.72001))
                points = points[~permitted]
            for surface in surfaces:
                for start in range(0, len(points), 128):
                    _, distance, _ = trimesh.proximity.closest_point(
                        surface, points[start:start+128])
                    self.assertLess(distance.max(), .00001)
        np.testing.assert_allclose(fitted.bounds, raw.bounds, atol=.00001, rtol=0)

    def test_zero_facing_keeps_the_source_and_reproduces_the_contact(self):
        import numpy as np
        import trimesh
        from simulation.collar_seat_trial import (TrialShoulderCollar,
                                                   UnfittedCollarShoulderBench)
        raw = trimesh.load_mesh(self.node.collar.stl_source)
        unchanged = TrialShoulderCollar(shoulder_facing=0).adjust(raw.copy())
        np.testing.assert_array_equal(raw.vertices, unchanged.vertices)
        np.testing.assert_array_equal(raw.faces, unchanged.faces)
        baseline = UnfittedCollarShoulderBench()
        baseline.assemble()
        baseline.build_stls()
        self.assertIntersecting(baseline.spider, baseline.collar)
