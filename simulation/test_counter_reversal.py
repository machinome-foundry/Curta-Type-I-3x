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
                self.assertBlockedBeyond(tooth, 12, against=drum)
            except AssertionError as error:
                error.add_note(f'reverser stroke={self.node.stroke} mm; crank={angle} deg')
                raise
