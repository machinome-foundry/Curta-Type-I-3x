"""Preserve installed spring seats and hook capture at every carry station."""

import numpy as np

from machinome.test import TestCase
from simulation.carry_bank_frame import FittedCarryBankFrameBench, stations


class CarryBankCaptureTest(TestCase):
    node = FittedCarryBankFrameBench

    def test_closed_folds_stay_at_their_original_fixed_seats(self):
        self.node.set_state(drop_mm=0)
        before = {}
        for path, node, _ in stations(self.node):
            centers = node.carry_lever_spring.wire.mesh.vertices[:-2].reshape(-1, 24, 3).mean(axis=1)
            held = centers[:, 2] < centers[:, 2].min()+.5
            self.assertGreater(held.sum(), 20)
            before[path] = (centers, held)
        for drop in (1.05, 2.1, 2.562, 3.15, 4.2):
            self.node.set_state(drop_mm=drop)
            for path, node, _ in stations(self.node):
                centers = node.carry_lever_spring.wire.mesh.vertices[:-2].reshape(-1, 24, 3).mean(axis=1)
                original, held = before[path]
                np.testing.assert_allclose(centers[held], original[held], atol=1e-5, rtol=0,
                                           err_msg=path)

    def test_hooks_keep_the_existing_free_and_blocked_play(self):
        for engaged in (.5, .6, 1):
            self.node.set_state(drop_mm=4.2*engaged)
            for path, node, slider in stations(self.node):
                wire = node.carry_lever_spring.wire
                # Perturbation directions are node-local: the public test
                # API applies every installed rotation itself. Pre-rotating
                # this direction would test a different physical freedom.
                self.assertFreeWithin(wire, .01, against=getattr(node, slider), along=(1, 0, 0))
                self.assertBlockedBeyond(wire, .2, against=getattr(node, slider), along=(1, 0, 0))

    def test_springs_keep_clear_of_the_unchanged_guide_seats(self):
        for drop in (0, 1.05, 2.1, 2.562, 3.15, 4.2):
            self.node.set_state(drop_mm=drop)
            for path, node, _ in stations(self.node):
                self.assertNotIntersecting(node.carry_lever_spring.wire, node.tens_slide_bearing)
