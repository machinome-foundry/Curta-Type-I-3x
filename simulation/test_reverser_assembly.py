"""Red acceptance checks for placements the isolated pinion bench omitted.

These tests intentionally expose the outstanding operating-model discrepancy.
Do not weaken them or modify the shaft to make a chosen stroke pass.
"""

from machinome.test import TestCase
from simulation.reverser_assembly import ReverserAssemblyBench


INPUTS = (
    ('ones', 'p_10218_1'), ('tens', 'p_10230_410008_1_419080'),
    ('hundreds', 'p_10230_410008_1_419068'), ('digit_4', 'p_10230_410008_1_419182'),
    ('digit_5', 'p_10230_410008_1_419105'), ('digit_6', 'p_10230_410008_1_419237'),
)


class ReverserAssemblyTest(TestCase):
    node = ReverserAssemblyBench

    def test_operating_normal_position_is_captured_by_the_yoke(self):
        # Current operating implementation lifts the inputs, not the lever.
        self.node.set_state(knob_height=0, gear_height=4.5, crank_angle=0,
                            subtract=0, reversed_counter=0)
        yoke = self.node.lever.reversing_lever_knob_1.reversing_actuator
        for name, member in INPUTS:
            gear = getattr(getattr(self.node, name), member)
            try:
                self.assertNotIntersecting(gear, yoke)
                # The .185 mm source slot play cannot permit a .3 mm axial
                # displacement in either direction while a pinion is captured.
                self.assertBlockedBeyond(gear, .3, against=yoke, along=(0, 0, 1))
            except AssertionError as error:
                error.add_note(f'counter channel {name}')
                raise

    def test_lifting_the_complete_lever_to_the_assumed_normal_position_clears_frame(self):
        self.node.set_state(knob_height=4.5, gear_height=4.5)
        self.assertNotIntersecting(self.node.lever.reversing_lever_knob_1.reversing_lever_knob,
                                   self.node.lever.upper_reversing_lever_spacer)

    def test_lower_detent_position_engages_complement_row(self):
        # Source ball Z -53.7575 and fixed lower detent Z -60.6.
        # This is not a 12 mm subtraction from the independently assumed normal.
        self.node.set_state(knob_height=-6.8425, gear_height=-6.8425,
                            crank_angle=101.25, subtract=0, reversed_counter=1)
        # Perturb the local-origin tooth ingredient, not its world-framed
        # fused stack: rotation of the latter would orbit the main shaft.
        gear = self.node.tens.p_10230_410008_1_419080.transmission_gear_0_5
        self.assertBlockedBeyond(gear, 12, against=self.node.drum.main_axle_step_drum_top_1,
                                 axis=(0, 0, -1), directions='forward')
