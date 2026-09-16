"""A reversal must engage the complement teeth, not just avoid collisions."""

from solid_node.test import TestCase
from simulation.counter_reversal import CounterReversalBench


class CounterReversalTest(TestCase):
    node = CounterReversalBench

    def test_reversed_higher_counter_is_driven_by_the_nine_tooth_row(self):
        tooth = self.node.counter
        drum = self.node.drum.main_axle_step_drum_top_1
        # Same within-passage station as InputMeshTest's 120 degrees:
        # 6.5 degrees after a tooth begins, not its temporal midpoint.
        for angle in (101.25, 146.25, 191.25):
            self.node.set_state(crank_angle=angle, subtract=0)
            try:
                self.assertNotIntersecting(drum, tooth)
                self.assertFreeWithin(tooth, .1, against=drum)
                # The drum pushes this flank forward; a pinion lagging the
                # prescribed positive rotation must meet the driving tooth.
                # Leading the tooth is not proof of this unilateral contact.
                self.assertBlockedBeyond(tooth, 12, against=drum,
                                         axis=(0, 0, -1), directions='forward')
            except AssertionError as error:
                error.add_note(f'reverser stroke={self.node.stroke} mm; crank={angle} deg')
                raise

    def test_complete_reversed_counter_passage(self):
        for angle in range(0, 361, 3):
            self.node.set_state(crank_angle=angle, subtract=0)
            try:
                self.assertNotIntersecting(self.node.drum.main_axle_step_drum_top_1,
                                           self.node.counter)
            except AssertionError as error:
                error.add_note(f'reverser stroke={self.node.stroke} mm; crank={angle} deg')
                raise
