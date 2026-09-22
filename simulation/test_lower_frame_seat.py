"""Positive shell/frame commons are findings, not ignored intended contacts."""

from machinome.test import TestCase
import cadquery as cq
import hashlib
import json
from math import cos, sin, radians
from machinome.simulation import Sim
from simulation.standard.parts import BottomHousing
from simulation.contracts import assert_connected_material
from simulation.lower_frame_seat import LowerFrameSeatBench


class LowerFrameSeatTest(TestCase):
    node = LowerFrameSeatBench

    def test_initial_bank_retains_fixed_pre_fit_witness(self):
        sim = Sim(self.node, dt=.1)
        bank = dict(sim.state)
        self.assertEqual(len(bank), 213)
        self.assertEqual(hashlib.sha256(json.dumps(bank, sort_keys=True,
                         separators=(',', ':')).encode()).hexdigest(),
                         'ea39d95d50f06580db66c894f5b3f700ab6ed930cee113b2b9ffe4689935f5b7')

    def test_bottom_housing_clears_main_body_at_actual_datum(self):
        self.assertNotIntersecting(self.node.enclosure.lower_housing_1.bottom_housing,
                                   self.node.frame.upper_frame.main_body)

    def test_bottom_housing_clears_lower_bearing_plate(self):
        self.assertNotIntersecting(self.node.enclosure.lower_housing_1.bottom_housing,
                                   self.node.frame.lower_bearing_plate.bearing_plate)

    def test_lower_bearing_shoulder_has_positive_seat_gap_and_stop(self):
        body = self.node.enclosure.lower_housing_1.bottom_housing
        plate = self.node.frame.lower_bearing_plate.bearing_plate
        self.assertFreeWithin(body, .02, against=plate, along=(0, 0, 1))
        self.assertBlockedBeyond(body, .1, against=plate, along=(0, 0, 1),
                                 directions='forward')

    def test_only_declared_key_flank_and_bearing_seat_have_bounded_relief(self):
        body = self.node.enclosure.lower_housing_1.bottom_housing
        original = BottomHousing().shape()
        fitted = body.shape()
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        assert_connected_material(body.mesh)
        self.assertEqual(fitted.cut(original).Volume(), 0)
        removed = original.cut(fitted)
        self.assertGreater(removed.Volume(), 0)
        # Source key flank is u=11.4; frame's mating flank is u=11.01.
        # u points at -40 degrees; v is its perpendicular. Only the final
        # 3.8 mm of the 9+ mm deep key seat may change, with .05 mm gaps.
        zone = cq.Solid.makeBox(.49, 4, 3.9, cq.Vector(10.96, 61, 128.2)).rotate(
            (0, 0, 0), (0, 0, 1), -40)
        key = zone.intersect(cq.Solid.makeCylinder(64.4805, 4, cq.Vector(0, 0, 128.2)))
        shoulder = cq.Solid.makeCylinder(64.111, .1, cq.Vector(0, 0, 11.95))
        self.assertGreater(removed.intersect(key).Volume(), 0)
        self.assertGreater(removed.intersect(shoulder).Volume(), 0)
        self.assertEqual(removed.cut(key).cut(shoulder).Volume(), 0)
        for bound in ('xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax'):
            self.assertAlmostEqual(getattr(fitted.BoundingBox(), bound),
                                   getattr(original.BoundingBox(), bound), places=7)

    def test_fitted_key_retains_lateral_capture(self):
        body = self.node.enclosure.lower_housing_1.bottom_housing
        frame = self.node.frame.upper_frame.main_body
        normal = (cos(radians(40)), -sin(radians(40)), 0)
        self.assertFreeWithin(body, .02, against=frame, along=normal)
        self.assertBlockedBeyond(body, .1, against=frame, along=normal,
                                 directions='forward')
