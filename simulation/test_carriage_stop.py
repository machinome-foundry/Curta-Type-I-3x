"""Pin/frame acceptance, isolated from unrelated whole-machine overlaps."""

from machinome.test import TestCase
from simulation.carriage_stop import CarriageStopBench, PrintedCarriageStopBench


class CarriageStopTest(TestCase):
    node = CarriageStopBench

    def test_pin_does_not_penetrate_the_frame_at_rest(self):
        self.node.set_state(angle=0, elevation=0)
        pin = self.node.carrier.upper_carriage_body_1.counter_body_stop_pin
        self.assertFreeWithin(pin, .05, against=self.node.frame, along=(0, 0, 1))

    def test_pin_clears_the_frame_through_working_positions_and_lifts(self):
        pin = self.node.carrier.upper_carriage_body_1.counter_body_stop_pin
        for elevation in (0, 3, 6):
            for angle in range(101):
                self.node.set_state(angle=angle, elevation=elevation)
                self.assertNotIntersecting(pin, self.node.frame)

    def test_pin_still_meets_both_angular_end_barriers(self):
        pin = self.node.carrier.upper_carriage_body_1.counter_body_stop_pin
        for elevation in (0, 3, 6):
            for angle in (-20, 120):
                self.node.set_state(angle=angle, elevation=elevation)
                self.assertIntersecting(pin, self.node.frame)

    def test_original_pin_stays_in_its_carrier_bore(self):
        self.node.set_state(angle=0, elevation=0)
        carrier = self.node.carrier.upper_carriage_body_1
        pin = carrier.counter_body_stop_pin
        self.assertTrue(pin.mesh.is_watertight)
        self.assertEqual(len(pin.mesh.split()), 1)
        self.assertFalse(pin.exact)  # Source STL, not native STEP certification.
        self.assertAlmostEqual(pin.mesh.bounds[0, 2], 21.054410518, places=5)
        self.assertAlmostEqual(pin.mesh.bounds[1, 2] - pin.mesh.bounds[0, 2], 15, places=5)
        self.assertNotIntersecting(pin, carrier.counter_body)
        # Native bore R2.293 and pin R2.195 leave .098 mm radial clearance.
        for axis in ((1, 0, 0), (0, 1, 0)):
            self.assertFreeWithin(pin, .05, against=carrier.counter_body, along=axis)
            self.assertBlockedBeyond(pin, .15, against=carrier.counter_body, along=axis)


class PrintedCarriageStopTest(CarriageStopTest):
    node = PrintedCarriageStopBench
