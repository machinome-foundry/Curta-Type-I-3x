"""Independent printable-shaft checks; native pocket commons are unreliable."""

import unittest
from pathlib import Path
import numpy as np
import trimesh
import manifold3d as manifold
from math import pi, degrees
from OCP.BRepAdaptor import BRepAdaptor_Surface
from simulation.standard.parts import ReversingShaft, SelectorKnobSpring
from simulation.cover_fits import mesh_solid
from simulation.reverser_detent_motion import (ball_radius_at, spring_height,
    BALL_RADIUS, FREE_HEIGHT, COIL_TURNS, WIRE_RADIUS)


class ReverserDetentMotionTest(unittest.TestCase):
    def test_profile_constants_match_native_pockets_and_spring(self):
        cones = [BRepAdaptor_Surface(face.wrapped).Cone()
                 for face in ReversingShaft().shape().Faces() if face.geomType() == 'CONE']
        self.assertEqual(len(cones), 2)
        np.testing.assert_allclose(sorted(c.Location().Z() for c in cones), (78.6, 90.6), atol=1e-8)
        for cone in cones:
            self.assertAlmostEqual(cone.Apex().X(), .81, places=7)
            self.assertAlmostEqual(degrees(cone.SemiAngle()), 63, places=7)
        spring = SelectorKnobSpring().shape()
        caps = [f for f in spring.Faces() if f.geomType() == 'PLANE']
        self.assertEqual(len(caps), 2)
        for cap in caps:
            self.assertAlmostEqual(cap.Area(), pi*WIRE_RADIUS**2, places=7)
        self.assertAlmostEqual(abs(caps[0].Center().z - caps[1].Center().z), FREE_HEIGHT, places=7)
        edge = next(e for e in spring.Edges() if e.geomType() == 'BSPLINE')
        points = np.array([edge.positionAt(i/100).toTuple() for i in range(101)])
        angles = np.unwrap(np.arctan2(points[:, 1], points[:, 0]))
        self.assertAlmostEqual(abs(angles[-1] - angles[0])/(2*pi), COIL_TURNS, places=7)

    def test_ball_follows_original_print_with_free_and_blocked_radial_play(self):
        path = Path(__file__).resolve().parents[1] / 'STLs/27 - Assemble Reversing Lever/reversing shaft.stl'
        shaft = mesh_solid(trimesh.load_mesh(path))
        sphere = mesh_solid(trimesh.creation.icosphere(subdivisions=4, radius=BALL_RADIUS))
        for z in np.linspace(76.5, 87.55, 112):
            radius = ball_radius_at(float(z))
            for displacement in (-.01, .01):
                common = shaft ^ sphere.translate((radius + displacement, 0, z))
                self.assertEqual(common.status(), manifold.Error.NoError)
                self.assertLessEqual(common.volume(), 0, (z, radius, displacement))
            blocked = shaft ^ sphere.translate((radius - .15, 0, z))
            self.assertEqual(blocked.status(), manifold.Error.NoError)
            self.assertGreater(blocked.volume(), 0, (z, radius))

    def test_lower_pocket_is_a_radial_minimum_and_upper_flank_biases_toward_stop(self):
        self.assertLess(ball_radius_at(78.6), ball_radius_at(78.5))
        self.assertLess(ball_radius_at(78.6), ball_radius_at(78.7))
        # Upper actual stop lies below the pocket centre, on its lower flank.
        self.assertGreater(ball_radius_at(87.35), ball_radius_at(87.45))
        self.assertGreater(ball_radius_at(87.45), ball_radius_at(87.55))

    def test_spring_keeps_compression_without_coil_binding(self):
        for z in np.linspace(76.6, 87.45, 110):
            height = spring_height(ball_radius_at(float(z)))
            self.assertLess(height, FREE_HEIGHT)
            self.assertGreater(height / COIL_TURNS, 2*WIRE_RADIUS + .05)
