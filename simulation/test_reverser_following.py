"""Mounted follower: whole-travel contact, spring seats and independent motion."""

import numpy as np
from math import pi
import manifold3d as manifold
from machinome.test import TestCase
from simulation.reverser_following import ReverserFollowerTrial, RADIAL
from simulation.reverser_detent_motion import ball_radius_at, SOURCE_BALL_Z
from simulation.reverser_detent_motion import WIRE_RADIUS
from simulation.cover_fits import mesh_solid


class ReverserFollowerTest(TestCase):
    node = ReverserFollowerTrial

    def test_ball_follows_radially_in_installed_coordinates(self):
        for height in (-6.9425, -5.5, -4.9425, -3, 0, 2, 3.9075):
            self.node.set_state(knob_height=height)
            ball = self.node.lever.p_5mm_ball.mesh
            # Use bounds midpoint for the sphere centre, not tessellation's
            # surface-area centroid; source-pole orientation is asymmetric.
            center = ball.bounds.mean(axis=0)
            relative = center - np.array((17.613968679, 54.210221429, -53.7575+height))
            radius = ball_radius_at(SOURCE_BALL_Z + height - self.node.seat_rise)
            np.testing.assert_allclose(relative, np.array(RADIAL)*radius, atol=.015)

    def test_ball_and_spring_clear_each_other_and_the_knob(self):
        lever = self.node.lever
        wire = lever.selector_knob_spring.wire
        knob = lever.reversing_lever_knob_1.reversing_lever_knob
        for height in np.linspace(-6.9425, 3.9075, 23):
            self.node.set_state(knob_height=float(height))
            self.assertNotIntersecting(wire, lever.p_5mm_ball)
            self.assertNotIntersecting(wire, knob)
            self.assertNotIntersecting(lever.p_5mm_ball, knob)

    def test_spring_is_captured_between_ball_and_blind_end(self):
        lever = self.node.lever
        wire = lever.selector_knob_spring.wire
        knob = lever.reversing_lever_knob_1.reversing_lever_knob
        for height in (-6.9425, -4.9425, -2, 0, 3.9075):
            self.node.set_state(knob_height=height)
            for neighbour in (lever.p_5mm_ball, knob):
                self.assertFreeWithin(wire, .01, against=neighbour, along=(0, 0, 1))
            # Perturbations use the wire's local frame: +Z points inward.
            self.assertBlockedBeyond(wire, .2, against=knob, along=(0, 0, -1), directions='forward')
            self.assertBlockedBeyond(wire, .2, against=lever.p_5mm_ball,
                                     along=(0, 0, 1), directions='forward')

    def test_ball_is_captured_on_actual_shaft_mesh(self):
        # Explicit faceted audit even on --exact: the unchanged source's cone
        # native Boolean is unreliable, as the independent print probe records.
        lever = self.node.lever
        shaft = mesh_solid(lever.reversing_shaft.mesh)
        for height in np.linspace(-6.9425, 3.9075, 45):
            self.node.set_state(knob_height=float(height))
            ball = mesh_solid(lever.p_5mm_ball.mesh)
            common = shaft ^ ball
            self.assertEqual(common.status(), manifold.Error.NoError)
            self.assertLessEqual(common.volume(), 0, height)
            inward = tuple(-.15*v for v in RADIAL)
            blocked = shaft ^ ball.translate(inward)
            self.assertEqual(blocked.status(), manifold.Error.NoError)
            self.assertGreater(blocked.volume(), 0, height)

    def test_spring_preserves_one_source_sized_wire_through_travel(self):
        for height in (-6.9425, -4.9425, 0, 3.9075):
            self.node.set_state(knob_height=height)
            shape = self.node.lever.selector_knob_spring.wire.shape()
            self.assertTrue(shape.isValid())
            self.assertEqual(len(shape.Solids()), 1)
            caps = [f.Area() for f in shape.Faces() if f.geomType() == 'PLANE']
            self.assertEqual(len(caps), 2)
            for area in caps:
                self.assertAlmostEqual(area, pi*WIRE_RADIUS**2, places=5)

    def test_upper_stop_blocks_the_pocket_flanks_restoring_direction(self):
        self.node.set_state(knob_height=3.9075)
        lever = self.node.lever
        knob = lever.reversing_lever_knob_1.reversing_lever_knob
        # Source knob's local -X points upward in the installed machine.
        self.assertBlockedBeyond(knob, .1, against=lever.upper_reversing_lever_spacer,
                                 along=(-1, 0, 0), directions='forward')
