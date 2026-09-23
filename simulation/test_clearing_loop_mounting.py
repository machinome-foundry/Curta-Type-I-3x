"""Replacement mounting acceptance, distinct from the source clip studies."""

import cadquery as cq
from machinome.test import TestCase
from simulation.clearing_loop_mounting import ReplacementLoopBench
from simulation.standard.parts import ClearingRing, ClearingRingRivet
from simulation.tools.interference import rigid_leaves


class ReplacementLoopMountTest(TestCase):
    node = ReplacementLoopBench

    def test_material_is_connected_and_finger_loop_is_unchanged(self):
        original = ClearingRing().shape()
        fitted = self.node.loop.clearing_ring.shape()
        allowed = cq.Solid.makeCylinder(8, 5.66, cq.Vector(40.5, 0, -.1))
        for part in (self.node.loop.clearing_ring,
                     self.node.loop.clearing_ring_rivet_1,
                     self.node.loop.clearing_ring_rivet_2):
            shape = part.shape()
            self.assertTrue(shape.isValid())
            self.assertEqual(len(shape.Solids()), 1)
        # Equivalence tolerance here concerns BREP identity, never clearance.
        for changed in (original.cut(fitted), fitted.cut(original)):
            self.assertAlmostEqual(changed.cut(allowed).Volume(), 0, delta=1e-8)
        finger = cq.Solid.makeBox(100, 100, 10, cq.Vector(66, -50, -1))
        self.assertAlmostEqual(original.intersect(finger).Volume(),
                               fitted.intersect(finger).Volume(), delta=1e-8)

    def test_both_original_cover_studs_are_preserved(self):
        original = ClearingRingRivet().shape()
        lower = cq.Solid.makeBox(20, 20, 6.4, cq.Vector(-10, -10, -.1))
        expected = original.intersect(lower)
        for part in (self.node.loop.clearing_ring_rivet_1,
                     self.node.loop.clearing_ring_rivet_2):
            actual = part.shape().intersect(lower)
            self.assertAlmostEqual(actual.cut(expected).Volume(), 0, delta=1e-8)
            self.assertAlmostEqual(expected.cut(actual).Volume(), 0, delta=1e-8)

    def test_every_degree_of_working_travel_clears_installed_neighbours(self):
        neighbours = (self.node.loop.clearing_ring_rivet_1,
                      self.node.loop.clearing_ring_rivet_2,
                      self.node.loop.clearing_cover,
                      self.node.carrier.crank_collar,
                      self.node.carrier.crank_collar_washer,
                      self.node.carrier.crank_collar_nut,
                      self.node.covers.upper_housing,
                      self.node.covers.digits_cover,
                      *(part for _, part in rigid_leaves(self.node.crank)))
        for angle in range(-90, 1):
            self.node.set_state(deployment=angle, release_height=0)
            for neighbour in neighbours:
                with self.subTest(angle=angle, neighbour=neighbour.name):
                    self.assertNotIntersecting(self.node.loop.clearing_ring, neighbour)

    def test_pivot_retains_radial_and_axial_capture_throughout_travel(self):
        for angle in (-90, -75, -45, -15, 0):
            self.node.set_state(deployment=angle, release_height=0)
            loop = self.node.loop.clearing_ring
            peg = self.node.loop.clearing_ring_rivet_1
            for direction in ((1, 0, 0), (0, 1, 0)):
                self.assertFreeWithin(loop, .02, against=peg, along=direction)
                self.assertBlockedBeyond(loop, .2, against=peg, along=direction)
            self.assertFreeWithin(loop, .2, against=peg, along=(0, 0, -1),
                                  directions='forward')
            self.assertBlockedBeyond(loop, .7, against=peg, along=(0, 0, -1),
                                     directions='forward')
            self.assertFreeWithin(loop, .02, against=self.node.loop.clearing_cover,
                                  along=(0, 0, 1), directions='forward')
            self.assertBlockedBeyond(loop, .1, against=self.node.loop.clearing_cover,
                                     along=(0, 0, 1), directions='forward')

    def test_second_mount_clears_the_body_side_passage(self):
        for angle in (-84, -67):
            with self.subTest(angle=angle):
                self.node.set_state(deployment=angle, release_height=0)
                self.assertNotIntersecting(self.node.loop.clearing_ring,
                                           self.node.loop.clearing_ring_rivet_2)

    def test_first_pivot_physically_stops_both_overtravel_directions(self):
        for angle in (-91, 1):
            with self.subTest(angle=angle):
                self.node.set_state(deployment=angle, release_height=0)
                self.assertIntersecting(self.node.loop.clearing_ring,
                                        self.node.loop.clearing_ring_rivet_1)

    def test_end_stop_play_has_clear_and_blocked_sides(self):
        for angle in (-90.4, .4):
            self.node.set_state(deployment=angle, release_height=0)
            self.assertNotIntersecting(self.node.loop.clearing_ring,
                                       self.node.loop.clearing_ring_rivet_1)
        for angle in (-90.6, .6):
            self.node.set_state(deployment=angle, release_height=0)
            self.assertIntersecting(self.node.loop.clearing_ring,
                                    self.node.loop.clearing_ring_rivet_1)
