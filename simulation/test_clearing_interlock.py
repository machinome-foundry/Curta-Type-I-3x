"""The clearing cam and fixed frame must admit the same pin position."""

from machinome.test import TestCase
from simulation.clearing_interlock import ClearingSeatBench


class ClearingSeatTest(TestCase):
    node = ClearingSeatBench

    def test_facing_removes_only_the_lower_tip_and_preserves_the_follower(self):
        from simulation.standard.parts import ClearingPin
        pin = self.node.carriage.carrier.upper_carriage_body_1.clearing_pin
        original, fitted = ClearingPin().shape(), pin.shape()
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        self.assertAlmostEqual(fitted.cut(original).Volume(), 0, places=7)
        removed = original.cut(fitted)
        self.assertGreater(removed.Volume(), 0)
        self.assertLessEqual(removed.BoundingBox().zmax, 2.540001)
        self.assertAlmostEqual(fitted.BoundingBox().zmin, 2.54, places=6)
        self.assertAlmostEqual(fitted.BoundingBox().zmax, original.BoundingBox().zmax, places=6)

    def test_both_ring_rests_allow_the_carriage_to_seat(self):
        pin = self.node.carriage.carrier.upper_carriage_body_1.clearing_pin
        for shift in range(0, 101, 20):
            for sweep in (0, 230, 360):
                self.node.set_state(elevation=0, shift=shift, sweep=sweep)
                self.assertFreeWithin(pin, .04, against=self.node.frame, along=(0, 0, 1))

    def test_lifted_carriage_allows_the_entire_clearing_sweep(self):
        pin = self.node.carriage.carrier.upper_carriage_body_1.clearing_pin
        for shift in (0, 40, 100):
            for sweep in range(-360, 361, 2):
                self.node.set_state(elevation=6, shift=shift, sweep=sweep)
                self.assertNotIntersecting(pin, self.node.frame)

    def test_partial_clearing_has_a_measured_axial_frame_stop(self):
        pin = self.node.carriage.carrier.upper_carriage_body_1.clearing_pin
        for shift in range(0, 101, 20):
            for sweep in (5, 14, 90, 218, 240, 348):
                self.node.set_state(elevation=6, shift=shift, sweep=sweep)
                # Pin source tip Z21.6, frame land Z21, candidate lower-end
                # facing 2.54 and named .05 mm seating gap: lift = drop - 3.09.
                self.node.set_state(elevation=pin.slide.value - 3.09)
                self.assertFreeWithin(pin, .01, against=self.node.frame, along=(0, 0, 1))
                self.assertBlockedBeyond(pin, .1, against=self.node.frame,
                                         along=(0, 0, -1), directions='forward')
