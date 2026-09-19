"""Native confirmation of the measured, bilateral zero-capture band."""

from machinome.test import TestCase
from simulation.clearing_gap import ClearingGapBench


class ClearingGapTest(TestCase):
    node = ClearingGapBench

    def test_half_degree_band_clears_both_rows_through_their_passage(self):
        interfaces = (
            (self.node.clearing.tooth_stack.outer_teeth,
             self.node.results.p_10203_1.results_dial_type_1),
            (self.node.clearing.tooth_stack.inner_teeth,
             self.node.results.p_10205_1.results_dial_type_2),
        )
        for quarter in range(321):
            self.node.set_state(digit=0, clear=.1 + .8 * (quarter / 4) / 360)
            for row, dial in interfaces:
                self.assertFreeWithin(dial, .5, against=row)
