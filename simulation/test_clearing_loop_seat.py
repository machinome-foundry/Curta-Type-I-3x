"""The deployed printed loop must fit both actual glued rivets."""

import cadquery as cq
from machinome.test import TestCase
from simulation.clearing_loop_seat import LoopSeatTrial
from simulation.standard.parts import ClearingRing


class LoopSeatTrialTest(TestCase):
    node = LoopSeatTrial

    def test_radial_deployed_loop_clears_both_rivets(self):
        self.node.set_state(deployment=-90, release_height=0)
        for peg in (self.node.loop.clearing_ring_rivet_1,
                    self.node.loop.clearing_ring_rivet_2):
            self.assertNotIntersecting(self.node.loop.clearing_ring, peg)

    def test_only_second_cavity_material_is_removed(self):
        original = ClearingRing().shape()
        fitted = self.node.loop.clearing_ring.shape()
        allowed = cq.Solid.makeCylinder(3.8, 5.46,
                                        cq.Vector(31.095555539, 25.948341482, 0))
        protected = cq.Solid.makeCylinder(10, 5.46, cq.Vector(40.5, 0, 0))
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        self.assertAlmostEqual(fitted.cut(original).Volume(), 0, delta=1e-8)
        removed = original.cut(fitted)
        self.assertGreater(removed.Volume(), 0)
        self.assertAlmostEqual(removed.cut(allowed).Volume(), 0, delta=1e-8)
        self.assertAlmostEqual(removed.intersect(protected).Volume(), 0, delta=1e-8)

    def test_seated_loop_retains_first_bearing_and_both_heads(self):
        self.node.set_state(deployment=-90, release_height=0)
        loop = self.node.loop.clearing_ring
        for direction in ((1, 0, 0), (0, 1, 0)):
            self.assertFreeWithin(loop, .02,
                                  against=self.node.loop.clearing_ring_rivet_1,
                                  along=direction)
            self.assertBlockedBeyond(loop, .2,
                                     against=self.node.loop.clearing_ring_rivet_1,
                                     along=direction)
        for peg in (self.node.loop.clearing_ring_rivet_1,
                    self.node.loop.clearing_ring_rivet_2):
            self.assertFreeWithin(loop, .2, against=peg, along=(0, 0, -1),
                                  directions='forward')
            self.assertBlockedBeyond(loop, .7, against=peg, along=(0, 0, -1),
                                     directions='forward')

    def test_deployed_loop_clears_cover_collar_and_housing(self):
        self.node.set_state(deployment=-90, release_height=0)
        for neighbour in (self.node.loop.clearing_cover, self.node.carrier.crank_collar,
                          self.node.carrier.crank_collar_washer, self.node.carrier.crank_collar_nut,
                          self.node.covers.upper_housing, self.node.covers.digits_cover):
            self.assertNotIntersecting(self.node.loop.clearing_ring, neighbour)
