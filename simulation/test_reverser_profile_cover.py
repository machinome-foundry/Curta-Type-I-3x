"""A convex decomposition must retain its input footprint, including notches."""

import unittest

from collections import Counter

from simulation.tools.reverser_profile_cover import (convex_partition, cross,
    profiles_overlap, cover_mesh_arrays, projected_mesh_triangles, posed_polygons)


def twice_area(points):
    return sum(a[0]*b[1]-a[1]*b[0]
               for a, b in zip(points, points[1:]+points[:1]))


class ReverserProfileCoverTest(unittest.TestCase):
    def test_convex_neighbours_merge_without_changing_footprint(self):
        points = [(0., 0.), (2., 0.), (2., 1.), (0., 1.)]
        result = convex_partition(points, [(0, 1, 2), (0, 3, 2)])
        self.assertEqual(len(result), 1)
        self.assertEqual(set(result[0]), {0, 1, 2, 3})
        self.assertEqual(twice_area([points[i] for i in result[0]]), 4)

    def test_concave_notch_is_not_filled_by_a_hull(self):
        points = [(0., 0.), (2., 0.), (2., 1.), (1., 1.), (1., 2.), (0., 2.)]
        triangles = [(0, 1, 3), (1, 2, 3), (0, 3, 5), (3, 4, 5)]
        result = convex_partition(points, triangles)
        self.assertGreater(len(result), 1)
        self.assertEqual(sum(twice_area([points[i] for i in polygon])
                             for polygon in result), 6)
        for polygon in result:
            vertices = [points[i] for i in polygon]
            self.assertTrue(all(cross(a, b, c) >= 0 for a, b, c in
                                zip(vertices, vertices[1:]+vertices[:1],
                                    vertices[2:]+vertices[:2])))

    def test_degenerate_or_nonfinite_input_is_refused(self):
        for points, triangles in (([(0, 0), (1, 0), (2, 0)], [(0, 1, 2)]),
                                  ([(0, 0), (1, 0), (0, float('nan'))], [(0, 1, 2)]),
                                  ([(0, 0), (1, 0), (0, 1)], [(0, 1, 3)])):
            with self.subTest(points=points, triangles=triangles):
                with self.assertRaises(ValueError):
                    convex_partition(points, triangles)

    def test_numeric_overlap_keeps_touching_inside_the_conservative_cover(self):
        square = [(0., 0.), (1., 0.), (1., 1.), (0., 1.)]
        for delta, expected in ((.5, True), (1., True), (1.001, False)):
            with self.subTest(delta=delta):
                other = [(x+delta, y) for x, y in square]
                self.assertEqual(profiles_overlap([square], [other]), expected)
        contained = [(.2, .2), (.3, .2), (.2, .3)]
        self.assertTrue(profiles_overlap([square], [contained]))

    def test_numeric_overlap_uses_edges_not_only_axis_aligned_boxes(self):
        first = [(0., 0.), (1., 0.), (0., 1.)]
        second = [(1., 1.), (.6, 1.), (1., .6)]
        self.assertFalse(profiles_overlap([first], [second]))

    def test_missing_profile_is_not_clearance(self):
        with self.assertRaises(ValueError):
            profiles_overlap([], [[(0., 0.), (1., 0.), (0., 1.)]])

    def test_cover_mesh_shares_edges_without_welding_native_face_meshes(self):
        report = dict(points=[(0., 0.), (2., 0.), (2., 1.), (0., 1.)],
                      triangles=[(0, 1, 2), (0, 3, 2)], boundary=[0, 3, 2, 1],
                      source_height=(0., 3.), allowance_mm=.005)
        vertices, faces = cover_mesh_arrays(report)
        self.assertEqual(len(vertices), 8)
        self.assertEqual(len(faces), 12)
        edges = Counter((u, v) for f in faces for u, v in zip(f, f[1:]+f[:1]))
        self.assertTrue(all(count == 1 and edges[v, u] == 1
                            for (u, v), count in edges.items()))
        self.assertEqual({p[2] for p in vertices}, {-.005, 3.005})

    def test_mesh_projection_keeps_exact_footprints_not_a_bounding_hull(self):
        vertices = [(0., 0., 0.), (1., 0., 0.), (0., 1., 0.),
                    (0., 0., 1.), (1., 0., 1.), (0., 1., 1.)]
        faces = [(0, 1, 2), (3, 5, 4), (0, 1, 4), (0, 4, 3)]
        result = projected_mesh_triangles(vertices, faces)
        self.assertEqual(result, [[(0., 0.), (1., 0.), (0., 1.)]])
        report = dict(points=[(10., 10.), (11., 10.), (10., 11.)],
                      polygons=[[0, 1, 2]], mesh_cover_polygons=result)
        placed = posed_polygons(report, translation=(2., 3.))
        self.assertEqual(len(placed), 2)
        self.assertEqual(placed[1], [(2., 3.), (3., 3.), (2., 4.)])


if __name__ == '__main__':
    unittest.main()
