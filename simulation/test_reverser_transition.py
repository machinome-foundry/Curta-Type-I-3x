"""Changing mode must clear the actual drum, frame and housing opening."""

import numpy as np
from machinome.test import TestCase
from simulation.reverser_transition import EnclosedReverserTrial
from simulation.test_reverser_assembly import INPUTS


class ReverserTransitionTest(TestCase):
    node = EnclosedReverserTrial

    def test_lower_window_stop_is_beyond_the_working_detent(self):
        self.node.set_state(knob_height=-6.9425, gear_height=-6.85)
        knob = self.node.lever.reversing_lever_knob_1.reversing_lever_knob
        housing = self.node.enclosure.lower_housing_1.bottom_housing
        self.assertNotIntersecting(knob, housing)
        # Knob local +X is installed downward. Pocket centre is not a hard stop.
        self.assertFreeWithin(knob, .01, against=housing, along=(1, 0, 0))
        self.assertBlockedBeyond(knob, .1, against=housing,
                                 along=(1, 0, 0), directions='forward')

    def test_complete_lever_travel_at_parked_crank_in_both_drum_modes(self):
        lever = self.node.lever
        knob = lever.reversing_lever_knob_1.reversing_lever_knob
        fork = lever.reversing_lever_knob_1.reversing_actuator
        for subtract in (0, 1):
            for height in np.linspace(-6.9425, 3.9075, 45):
                self.node.set_state(knob_height=float(height), gear_height=float(height + .0925),
                                    crank_angle=0, subtract=subtract, reversed_counter=0)
                for name, member in INPUTS:
                    gear = getattr(getattr(self.node, name), member)
                    for neighbour in (self.node.drum.main_axle_step_drum_top_1,
                                      self.node.drum.main_axle_step_drum_bottom_1,
                                      self.node.upper_frame, self.node.lower_frame, fork):
                        try:
                            self.assertNotIntersecting(gear, neighbour)
                        except AssertionError as error:
                            raise AssertionError(f'height={height}, subtract={subtract}, {name}: {error}') from error
                for moving in (knob, fork, lever.p_5mm_ball, lever.selector_knob_spring.wire):
                    for fixed in (self.node.enclosure.lower_housing_1.bottom_housing,
                                  self.node.enclosure.upper_outer_sleeve):
                        self.assertNotIntersecting(moving, fixed)
