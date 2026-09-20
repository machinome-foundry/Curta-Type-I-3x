"""Mounting acceptance and unchanged-pocket bounds for a trial, not a release."""

import cadquery as cq
from machinome.test import TestCase
from simulation.reverser_seat_trial import ReverserSeatTrial
from simulation.standard.parts import ReversingShaft
from simulation.test_reverser_assembly import INPUTS


class ReverserSeatTrialTest(TestCase):
    node = ReverserSeatTrial

    def test_raised_shaft_clears_original_mounts(self):
        shaft = self.node.lever.reversing_shaft
        for part in (self.node.upper_frame, self.node.lower_frame,
                     self.node.fasteners.m4_nut_2):
            self.assertNotIntersecting(shaft, part)

    def test_fastening_end_stays_at_source_installed_height(self):
        self.assertAlmostEqual(self.node.lever.reversing_shaft.mesh.bounds[1, 2],
                               -11.7, delta=.001)

    def test_shoulder_is_captured_not_floating_through_frame(self):
        shaft = self.node.lever.reversing_shaft
        self.assertFreeWithin(shaft, .025, against=self.node.upper_frame, along=(0, 0, 1))
        self.assertBlockedBeyond(shaft, .1, against=self.node.upper_frame,
                                 along=(0, 0, 1), directions='forward')

    def test_only_upper_mounting_region_changes(self):
        original = ReversingShaft().shape()
        fitted = self.node.lever.reversing_shaft.shape()
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        self.assertAlmostEqual(fitted.cut(original).Volume(), 0, delta=1e-8)
        # This whole protected region contains both pockets (78.6/90.6),
        # lower flats and bearing land. The bound is independent of the fit.
        protected = cq.Solid.makeBox(20, 20, 110, cq.Vector(-10, -10, 0))
        self.assertAlmostEqual(original.intersect(protected).cut(fitted).Volume(), 0, delta=1e-8)
        removed = original.cut(fitted)
        self.assertGreater(removed.Volume(), 0)
        self.assertGreaterEqual(removed.BoundingBox().zmin, 115.0)

    def check_bank(self, lower, subtract):
        self.node.set_state(knob_height=-4.9425 if lower else 3.9075,
                            gear_height=-4.85 if lower else 4,
                            crank_angle=101.25, subtract=subtract,
                            reversed_counter=int(lower))
        errors = []
        fork = self.node.lever.reversing_lever_knob_1.reversing_actuator
        for name, member in INPUTS:
            gear = getattr(getattr(self.node, name), member)
            for label, part in (('fork', fork), ('upper frame', self.node.upper_frame),
                                ('lower frame', self.node.lower_frame),
                                ('upper drum', self.node.drum.main_axle_step_drum_top_1),
                                ('lower drum', self.node.drum.main_axle_step_drum_bottom_1)):
                try:
                    self.assertNotIntersecting(gear, part)
                except AssertionError as error:
                    errors.append(f'{name} / {label}: {error}')
            try:
                self.assertBlockedBeyond(gear, .3, against=fork, along=(0, 0, 1))
            except AssertionError as error:
                errors.append(f'{name} / capture: {error}')
        self.assertFalse(errors, '\n'.join(errors))

    def test_lower_bank_addition(self):
        self.check_bank(True, 0)

    def test_lower_bank_subtraction(self):
        self.check_bank(True, 1)

    def test_upper_bank_addition(self):
        self.check_bank(False, 0)

    def test_upper_bank_subtraction(self):
        self.check_bank(False, 1)

    def test_lower_position_reaches_nine_tooth_row(self):
        self.node.set_state(knob_height=-4.9425, gear_height=-4.85,
                            crank_angle=101.25, subtract=0, reversed_counter=1)
        tooth = self.node.tens.p_10230_410008_1_419080.transmission_gear_0_5
        self.assertBlockedBeyond(tooth, 12, against=self.node.drum.main_axle_step_drum_top_1,
                                 axis=(0, 0, -1), directions='forward')

    def check_knob(self, height):
        self.node.set_state(knob_height=height)
        knob = self.node.lever.reversing_lever_knob_1.reversing_lever_knob
        for part in (self.node.upper_frame, self.node.lower_frame,
                     self.node.lever.upper_reversing_lever_spacer,
                     self.node.lever.lower_reversing_lever_spacer):
            self.assertNotIntersecting(knob, part)

    def test_lower_knob_clears_frame_stops(self):
        self.check_knob(-4.9425)

    def test_upper_knob_clears_frame_stops(self):
        self.check_knob(3.9075)
