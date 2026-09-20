"""Indexed clearances cannot be inferred from only one pentagon flat."""

import cadquery as cq

from machinome.test import TestCase
from simulation.fit import FittedCarryLockout
from simulation.contracts import assert_connected_material
from simulation.ones_lockout import OnesLockoutBench


class OnesLockoutBenchTest(TestCase):
    node = OnesLockoutBench

    def test_every_indexed_flat_clears_the_complete_closed_bell(self):
        for index in range(5):
            for crank in range(0, 361, 10):
                self.node.set_state(shaft_angle=4+72*index, crank_angle=crank)
                self.assertNotIntersecting(self.node.ones, self.node.bell)

    def test_only_a_bounded_outer_skin_changes_and_the_keyway_is_unchanged(self):
        before = FittedCarryLockout().shape()
        after = self.node.ones.pentagonal_lockout.shape()
        self.assertTrue(after.isValid())
        self.assertEqual(len(after.Solids()), 1)
        self.assertEqual(after.cut(before).Volume(), 0)
        removed = before.cut(after)
        self.assertGreater(removed.Volume(), 0)
        # At most a .01 mm skin: old surface area times that thickness is
        # a conservative volume bound independent of the new derivation.
        self.assertLessEqual(removed.Volume(), before.Area()*.01)
        box = before.BoundingBox()
        protected = cq.Solid.makeCylinder(4, box.zlen+2,
                                         cq.Vector(0, 0, box.zmin-1))
        self.assertEqual(removed.intersect(protected).Volume(), 0)
        self.assertAlmostEqual(after.BoundingBox().zmin, box.zmin, places=9)
        self.assertAlmostEqual(after.BoundingBox().zmax, box.zmax, places=9)

    def test_both_printed_groups_remain_connected_and_native_valid(self):
        for part in (self.node.ones, self.node.bell):
            assert_connected_material(part.mesh)
            self.assertTrue(part.shape().isValid())
            self.assertEqual(len(part.shape().Solids()), 1)

    def test_closed_bell_still_locks_both_sides_beyond_the_play(self):
        for index in range(5):
            for direction in (-1, 1):
                # These source parts retain the common STEP frame: rotate
                # about their actual shaft at X40.5, not the global origin.
                self.node.set_state(shaft_angle=4+72*index+4*direction,
                                    crank_angle=180)
                self.assertIntersecting(self.node.ones, self.node.bell)
