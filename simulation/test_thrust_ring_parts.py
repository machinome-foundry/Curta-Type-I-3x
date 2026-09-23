"""Independent material bounds, entire radial/lift enclosure and negatives."""

import logging
import unittest

import cadquery as cq

from simulation.thrust_ring_parts import BallPassageThrustRing, radial_passage
from simulation.thrust_ring_regions import permitted_local
from simulation.standard.parts import ThrustRing
from simulation.contracts import assert_connected_material
from simulation.test_follow_ball_ring import FollowBallRingTest as _FollowContract
from simulation.thrust_ring_trial import FittedRadialBallTrial


def world(shape):
    return shape.rotate((0, 0, 0), (0, 0, 1), 35.717779468).translate((0, 0, 33.05))


def sphere(x, radius=3.75):
    return cq.Solid.makeSphere(radius, (x, 0, 30), angleDegrees1=-90)


class ThrustRingMaterialTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ThrustRing().shape()
        cls.part = BallPassageThrustRing()
        cls.part.assemble()
        cls.part.build_stls()
        cls.fitted = cls.part.shape()

    def test_only_independently_bounded_material_is_removed(self):
        source, fitted = self.source, self.fitted
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        assert_connected_material(self.part.mesh)
        self.assertEqual(fitted.cut(source).Volume(), 0)
        removed = source.cut(fitted)
        self.assertGreater(removed.Volume(), 0)
        self.assertEqual(removed.cut(permitted_local()).Volume(), 0)
        # Preserve the complete upper half and outer support annulus exactly.
        protected = cq.Solid.makeBox(40, 40, .7, (-20, -20, .8)).fuse(
            cq.Solid.makeCylinder(16.35, 1.5).cut(cq.Solid.makeCylinder(14.5, 1.5)))
        self.assertEqual(removed.intersect(protected).Volume(), 0)
        for face in source.Faces():
            if face.geomType() == 'PLANE' and abs(face.Center().z-1.5) < 1e-9:
                self.assertEqual(face.cut(fitted).Area(), 0)

    def test_fresh_and_built_geometry_match(self):
        fresh = BallPassageThrustRing().adjust(self.source)
        self.assertTrue(fresh.isValid())
        self.assertEqual(fresh.cut(self.fitted).Volume(), 0)
        self.assertEqual(self.fitted.cut(fresh).Volume(), 0)

    def test_gap_has_measurable_effect_at_outer_radial_limit(self):
        for gap in (.04, .05, .06):
            fitted = BallPassageThrustRing(running_gap=gap).shape()
            self.assertEqual(self.source.cut(fitted).cut(permitted_local()).Volume(), 0)
            self.assertAlmostEqual(world(fitted).distance(sphere(11.949090957641602)),
                                   gap, delta=1e-7)

    def test_complete_continuous_radial_and_lift_path_is_enclosed(self):
        # Deliberately outward-rounded independent centre/radius bounds include
        # the measured source mesh's 0.000000116 mm radial overshoot. The convex
        # sphere also encloses every triangle between its enclosed vertices.
        radius, start, end = 3.751, 8.332, 11.950
        envelope = cq.Solid.makeCylinder(radius, end-start, (start, 0, 30), (1, 0, 0))
        envelope = envelope.fuse(sphere(start, radius), sphere(end, radius)).clean()
        common = world(self.fitted).intersect(envelope)
        self.assertTrue(common.isValid())
        self.assertEqual(common.Volume(), 0)
        # For ring Z >=33.05 > ball Z30, lowering the ball in the ring's
        # frame only shrinks each horizontal sphere section. Thus this zero-
        # lift enclosure includes every relative lift in [0,6], unsampled too.
        self.assertGreater(self.source.BoundingBox().zmin+33.05, 30)

    def test_omitted_misplaced_and_excessive_passages_are_rejected(self):
        ball = sphere(11.841003148078919)
        self.assertGreater(world(self.source).intersect(ball).Volume(), 0)
        wrong = self.source.cut(radial_passage(.05).rotate((0, 0, 0), (0, 0, 1), 20))
        self.assertGreater(world(wrong).intersect(ball).Volume(), 0)
        excessive = self.fitted.cut(cq.Solid.makeBox(40, 40, .2, (-20, -20, 1.3)))
        self.assertGreater(self.source.cut(excessive).cut(permitted_local()).Volume(), 0)


class FittedFollowBallRingTest(_FollowContract):
    model = FittedRadialBallTrial


if __name__ == '__main__':
    logging.disable(logging.INFO)
    unittest.main()
