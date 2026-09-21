"""T07 must clear indexed positions without losing either locking flank."""

import cadquery as cq

from machinome.test import TestCase
from simulation.contracts import assert_connected_material
from simulation.fit import FittedCarryLockout
from simulation.higher_lockout_trial import HigherLockoutFitBench
from simulation.standard.printed import TensBell1
from simulation.cycle import tooth_passage, RESULT_CARRY_END


class HigherLockoutFitTest(TestCase):
    node = HigherLockoutFitBench

    def test_all_five_starting_flats_clear_both_seats_and_carry_transfer(self):
        stack = self.node.tens.p_10220_410003_1_419227
        for carry in (0, .25, .5, .75, 1):
            for shaft in (-16, 56, 128, 200, 272):
                for crank in range(0, 361, 10):
                    # An engaged carry tooth drives the shaft. Freezing that
                    # gear through its tooth passage invents a jam, not an
                    # indexed clearance requirement. Use the unchanged
                    # source passage and latch threshold from shaft_motion.
                    advance = (72*tooth_passage(crank, 1, RESULT_CARRY_END+20)
                               if carry >= .61 else 0)
                    self.node.set_state(shaft_angle=shaft+advance, crank_angle=crank,
                                        carry_position=carry)
                    try:
                        self.assertNotIntersecting(stack, self.node.bell)
                    except AssertionError as error:
                        raise AssertionError(f'carry={carry}, shaft={shaft}, crank={crank}: '
                                             f'{error}') from error

    def test_freezing_the_engaged_carry_gear_is_a_negative_control(self):
        stack = self.node.tens.p_10220_410003_1_419227
        self.node.set_state(shaft_angle=-16, crank_angle=150, carry_position=.75)
        self.assertIntersecting(stack, self.node.bell)
        advance = 72*tooth_passage(150, 1, RESULT_CARRY_END+20)
        self.node.set_state(shaft_angle=-16+advance)
        self.assertNotIntersecting(stack, self.node.bell)

    def test_bounded_skin_preserves_keyway_and_axial_extent(self):
        before = FittedCarryLockout().shape()
        after = self.node.tens.p_10220_410003_1_419227.pentagonal_lockout.shape()
        self.assertTrue(after.isValid())
        self.assertEqual(len(after.Solids()), 1)
        self.assertEqual(after.cut(before).Volume(), 0)
        removed = before.cut(after)
        self.assertGreater(removed.Volume(), 0)
        self.assertLessEqual(removed.Volume(), before.Area()*.01)
        box = before.BoundingBox()
        protected = cq.Solid.makeCylinder(4, box.zlen+2, cq.Vector(0, 0, box.zmin-1))
        self.assertEqual(removed.intersect(protected).Volume(), 0)
        self.assertAlmostEqual(after.BoundingBox().zmin, box.zmin, places=9)
        self.assertAlmostEqual(after.BoundingBox().zmax, box.zmax, places=9)

    def test_complete_upper_stack_remains_connected(self):
        stack = self.node.tens.p_10220_410003_1_419227
        assert_connected_material(stack.mesh)
        self.assertTrue(stack.shape().isValid())
        self.assertEqual(len(stack.shape().Solids()), 1)

    def test_bell_refinement_changes_no_native_material(self):
        source = TensBell1()
        source.assemble()
        before, after = source.shape(), self.node.bell.shape()
        self.assertEqual(before.cut(after).Volume(), 0)
        self.assertEqual(after.cut(before).Volume(), 0)
        self.assertTrue(after.isValid())
        self.assertEqual(len(after.Solids()), 1)

    def test_closed_bell_still_locks_both_sides_at_all_carry_heights(self):
        stack = self.node.tens.p_10220_410003_1_419227
        for carry in (0, .25, .5, .75, 1):
            for shaft in (-16, 56, 128, 200, 272):
                for direction in (-1, 1):
                    self.node.set_state(shaft_angle=shaft+4*direction,
                                        crank_angle=180, carry_position=carry)
                    self.assertIntersecting(stack, self.node.bell)
