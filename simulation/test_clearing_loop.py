"""Calibrate the diagnostic's frame before using its contact measurements."""

import math
import numpy as np
from machinome.test import TestCase
from simulation.clearing_loop import LoopMountBench


class LoopMountTest(TestCase):
    node = LoopMountBench

    def test_first_clip_is_a_captive_bearing_while_attached(self):
        loop = self.node.loop.clearing_ring
        peg = self.node.loop.clearing_ring_rivet_1
        for angle in (0, -45, -75):
            self.node.set_state(deployment=angle, release_height=0)
            self.assertNotIntersecting(loop, peg)
            for direction in ((1, 0, 0), (0, 1, 0)):
                self.assertFreeWithin(loop, .02, against=peg, along=direction)
                self.assertBlockedBeyond(loop, .2, against=peg, along=direction)
            self.assertFreeWithin(loop, .2, against=peg, along=(0, 0, 1))
            # Source loop local -Z is upward. The unchanged head retains it.
            self.assertBlockedBeyond(loop, .7, against=peg,
                                     along=(0, 0, -1), directions='forward')

    def test_release_height_moves_only_the_loop_up_in_the_assembly_frame(self):
        self.node.set_state(deployment=0, release_height=0)
        loop = self.node.loop.clearing_ring
        before = loop.mesh.vertices.copy()
        peg = self.node.loop.clearing_ring_rivet_1
        fixed = peg.mesh.vertices.copy()
        self.node.set_state(release_height=3)
        np.testing.assert_allclose(loop.mesh.vertices, before + (0, 0, 3), rtol=0, atol=.00001)
        np.testing.assert_array_equal(peg.mesh.vertices, fixed)

    def test_swivel_is_about_the_actual_first_mounted_rivet(self):
        self.node.set_state(deployment=0, release_height=0)
        loop = self.node.loop.clearing_ring
        before = loop.mesh.vertices.copy()
        peg = self.node.loop.clearing_ring_rivet_1
        center = peg.mesh.bounds.mean(axis=0)
        angle = math.radians(5)
        rotation = np.array(((math.cos(angle), -math.sin(angle), 0),
                             (math.sin(angle), math.cos(angle), 0), (0, 0, 1)))
        self.node.set_state(deployment=5)
        expected = (before - center) @ rotation.T + center
        np.testing.assert_allclose(loop.mesh.vertices, expected, rtol=0, atol=.00001)
