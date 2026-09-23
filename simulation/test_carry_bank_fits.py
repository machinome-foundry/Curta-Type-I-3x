"""Candidate frame gates before production adoption; exact material checks."""

import logging
import unittest

import cadquery as cq

from simulation.carry_bank_fits import CarryBankPassageFrame
from simulation.carry_bank_frame import FittedCarryBankFrameBench, FirstPairCarryBankFrameBench
from simulation.carry_bank_regions import forbidden_removal, RESULT_ANGLES, COUNTER_ANGLES
from simulation.standard.parts import MainBody
from simulation.test_carry_bank_frame import CarryBankFrameTest
from simulation.test_carry_bank_regions import CarryBankRegionTest
from simulation.tools.interference import world_solids


class CarryBankFitMaterialTest(CarryBankRegionTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Run the independently mapped support/bore checks on the actual
        # candidate, not just on the larger prospective removal witness.
        cls.maximum = CarryBankPassageFrame().shape()

    def test_removal_is_positive_and_inside_independent_bounds(self):
        self.assertGreater(self.original.cut(self.maximum).Volume(), 0)
        forbidden = forbidden_removal(self.original, self.maximum)
        self.assertTrue(forbidden.isValid())
        self.assertEqual(forbidden.Volume(), 0)

    def test_fresh_adjustment_equals_built_geometry(self):
        fresh = CarryBankPassageFrame().adjust(MainBody().shape())
        self.assertTrue(fresh.isValid())
        self.assertEqual(fresh.cut(self.maximum).Volume(), 0)
        self.assertEqual(self.maximum.cut(fresh).Volume(), 0)

    def test_gap_changes_each_independently_measured_shoulder_distance(self):
        for gap in (.04, .05, .06):
            fitted = CarryBankPassageFrame(running_gap=gap).shape()
            for counter, angles in ((False, RESULT_ANGLES), (True, COUNTER_ANGLES)):
                points = ((50.5, -7.2, -21.6), (50.5, -7.2, -15.9)) if counter else (
                    (50.5, -7.2, -21.6), (52.725, -7.155, -16.35))
                for angle in angles:
                    for point in points:
                        site = cq.Vertex.makeVertex(*point).rotate((0, 0, 0), (0, 0, 1), angle)
                        with self.subTest(gap=gap, angle=angle, point=point):
                            self.assertAlmostEqual(fitted.distance(site), gap, delta=1e-6)


class CarryBankFitStrokeTest(CarryBankFrameTest):
    @classmethod
    def setUpClass(cls):
        cls.bench = FittedCarryBankFrameBench()
        cls.bench.set_state(drop_mm=0)
        cls.bench.assemble()
        cls.bench.build_stls()

    def test_fixture_matches_the_operating_root_at_rest(self):
        # The original fixture's installed-root identity is independently
        # tested by CarryBankFrameTest. This trial must change only its frame.
        original = FirstPairCarryBankFrameBench()
        original.set_state(drop_mm=0)
        original.assemble()
        self.bench.set_state(drop_mm=0)
        before = world_solids(original, include_flexible=True)
        after = self.native()
        self.assertEqual(set(before), set(after))
        for path in before:
            a, b = before[path], after[path]
            with self.subTest(path=path):
                self.assertTrue(a.isValid() and b.isValid())
                self.assertEqual(b.cut(a).Volume(), 0)
                if path == 'Curta.frame.main_body':
                    self.assertGreater(a.cut(b).Volume(), 0)
                    self.assertEqual(forbidden_removal(a, b).Volume(), 0)
                else:
                    self.assertEqual(a.cut(b).Volume(), 0)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    unittest.main()
