"""Seating must clear the bearing bosses without removing the indexing keys."""

from machinome.test import TestCase
from simulation.carriage_frame import CarriageFrameBench


class CarriageFrameTest(TestCase):
    node = CarriageFrameBench

    def test_measured_envelope_clears_and_preserves_the_axial_stops(self):
        from simulation.carriage_index_motion import indexing_lift
        body = self.node.carrier.upper_carriage_body_1.counter_body
        for working in range(0, 101, 20):
            for direction in (-1, 1):
                for play in (.18, .2, .35, .5, .65, .8, .95, 1, 5, 10):
                    angle = working + direction * play
                    height = indexing_lift(angle)
                    self.node.set_state(angle=angle, elevation=height)
                    self.assertFreeWithin(body, .01, against=self.node.frame, along=(0, 0, 1))
                    if play > .18:
                        self.assertBlockedBeyond(body, .1, against=self.node.frame,
                                                 along=(0, 0, 1), directions='forward')
                    else:
                        self.assertBlockedBeyond(body, .02, against=self.node.frame,
                                                 axis=(0, 0, -direction), directions='forward')

    def test_only_the_measured_underside_regions_are_relieved(self):
        import cadquery as cq
        from simulation.standard.parts import CounterBody
        original = CounterBody().shape()
        fitted = self.node.carrier.upper_carriage_body_1.counter_body.shape()
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        self.assertAlmostEqual(fitted.cut(original).Volume(), 0, places=6)
        removed = original.cut(fitted)
        self.assertGreater(removed.Volume(), 0)
        # The only deeper exception is .05 mm of existing pocket ceiling,
        # native Z14.05..14.1, not a slit through the indexing-key flanks.
        roof_zone = cq.Solid.makeCylinder(34.25, .05, cq.Vector(0, 0, 14.05)).cut(
            cq.Solid.makeCylinder(21.9, .05, cq.Vector(0, 0, 14.05)))
        roof_removed = removed.intersect(roof_zone)
        self.assertGreater(roof_removed.Volume(), 0)
        self.assertAlmostEqual(roof_removed.intersect(original.translate((0, 0, -.05))).Volume(),
                               0, places=6)
        # Independent point classification catches a valid-looking Boolean
        # cutter that accidentally slices the seventeen key roots.
        import math
        for angle in range(0, 360, 20):
            for radius in (22.5, 25, 31, 33):
                point = (radius * math.cos(math.radians(angle + 10)),
                         radius * math.sin(math.radians(angle + 10)), 14.075)
                if original.isInside((point[0], point[1], 14.125)):
                    self.assertTrue(fitted.isInside(point), (radius, angle))
        removed = removed.cut(roof_zone)
        # The guide/key region below local Z20.05 and inside R31.7 is protected.
        inner = cq.Solid.makeCylinder(31.7, 20.05)
        self.assertAlmostEqual(removed.intersect(inner).Volume(), 0, places=6)
        # Beyond the shallow general face, removal is only in the boss annulus.
        below = cq.Solid.makeBox(100, 100, 19.15, cq.Vector(-50, -50, 0))
        self.assertAlmostEqual(removed.intersect(below).Volume(), 0, places=6)
        outer = cq.Solid.makeCylinder(34.25, 20.05)
        low = cq.Solid.makeBox(100, 100, 20.05, cq.Vector(-50, -50, 0))
        self.assertAlmostEqual(removed.intersect(low).cut(outer).Volume(), 0, places=6)
        self.assertAlmostEqual(fitted.BoundingBox().zmin, original.BoundingBox().zmin, places=6)
        self.assertAlmostEqual(fitted.BoundingBox().zmax, 20.05, places=6)

    def test_all_six_positions_seat_above_the_fixed_bearing_bosses(self):
        body = self.node.carrier.upper_carriage_body_1.counter_body
        for angle in range(0, 101, 20):
            self.node.set_state(angle=angle, elevation=0)
            self.assertFreeWithin(body, .04, against=self.node.frame, along=(0, 0, 1))

    def test_full_lift_frees_the_body_for_the_entire_shift(self):
        body = self.node.carrier.upper_carriage_body_1.counter_body
        for angle in range(101):
            self.node.set_state(angle=angle, elevation=6)
            self.assertFreeWithin(body, .01, against=self.node.frame, along=(0, 0, 1))

    def test_indexing_keys_still_block_lowering_between_working_positions(self):
        body = self.node.carrier.upper_carriage_body_1.counter_body
        for angle in range(10, 100, 20):
            for elevation in (0, 3, 5.8):
                self.node.set_state(angle=angle, elevation=elevation)
                self.assertIntersecting(body, self.node.frame)
