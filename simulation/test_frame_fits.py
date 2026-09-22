"""Spatial source preservation is independent of the production cutters."""

import cadquery as cq
import numpy as np
from machinome.test import TestCase
from simulation.frame_fits import CarryPassageFrame
from simulation.standard.parts import MainBody
from simulation.carry_frame import CarryFrameBench
from simulation.tools.interference import world_solids
from simulation.tools.open_run_transitions import bounds


def region(low, high):
    return cq.Solid.makeBox(*(b-a for a, b in zip(low, high)), cq.Vector(*low))


def permitted_regions():
    # Independently recorded source shoulder vertices, deliberately not read
    # from frame_fits. A maximum .08 mm envelope bounds trials at .04–.06 mm.
    vertices = [(54.225, -6.42), (47.8575, -6.42), (47.8575, -8.25052213578731),
                (48.5925, -9.523579479350438), (51.42194265643687, -7.89),
                (54.225, -7.89)]
    shoulder = (cq.Workplane('XY', origin=(0, 0, -22.28)).polyline(vertices).close()
                .offset2D(.08).extrude(.76).val())
    shoulder = shoulder.intersect(region((47, -10, -23), (52.88, -6, -21)))
    first = [shoulder,
        region((52.645, -7.97, -16.88), (52.88, -6.34, -15.82)),
        region((53.421, -11.402, -19.546), (54.277, -10.93, -15.82)),
        region((60.328, -11.402, -19.546), (61.184, -10.93, -15.82))]
    for angle in (0, -20):
        for shape in first:
            yield shape.rotate((0, 0, 0), (0, 0, 1), angle)


def forbidden_removal(original, fitted):
    removed = original.cut(fitted)
    for permitted in permitted_regions():
        if not removed.Vertices():
            break
        removed = removed.cut(permitted)
    return removed


def registration_lands(frame, guide):
    """Actual native contact patches; includes the adjacent corner faces."""
    for a in frame.Faces():
        if a.geomType() != 'PLANE':
            continue
        normal = np.array(a.normalAt().toTuple())
        for b in guide.Faces():
            if b.geomType() != 'PLANE':
                continue
            if abs(np.dot(normal, b.normalAt().toTuple())) < 1-1e-8:
                continue
            if abs(np.dot(normal, np.array(a.Center().toTuple())-b.Center().toTuple())) > 1e-5:
                continue
            ab, bb = bounds(a), bounds(b)
            if np.any(np.minimum(ab[1], bb[1])+1e-5 < np.maximum(ab[0], bb[0])):
                continue
            common = a.intersect(b)
            if not common.isValid():
                raise ValueError('Invalid native guide/frame face intersection')
            if common.Area() > 0:
                yield common


def seat_edge_exceptions(angle):
    # Independent maximum envelope about the two measured source segments.
    for z in (-21.6, -16.8):
        yield region((52.72, -7.97, z-.08), (52.88, -6.34, z+.08)).rotate(
            (0, 0, 0), (0, 0, 1), angle)


class FrameFitTest(TestCase):
    node = CarryPassageFrame

    def test_gap_outside_the_measured_trial_range_is_rejected(self):
        for gap in (0, .039, .061, .1):
            with self.assertRaisesRegex(ValueError, 'running_gap'):
                CarryPassageFrame(running_gap=gap)

    def test_one_valid_frame_no_added_material(self):
        original, fitted = MainBody().shape(), self.node.shape()
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        self.assertEqual(fitted.cut(original).Volume(), 0)
        self.assertGreater(original.Volume() - fitted.Volume(), 0)

    def test_no_removed_material_outside_independent_passage_bounds(self):
        outside = forbidden_removal(MainBody().shape(), self.node.shape())
        self.assertTrue(outside.isValid())
        self.assertEqual(outside.Volume(), 0)

    def test_fresh_adjustment_matches_built_geometry(self):
        fresh = self.node.adjust(MainBody().shape())
        built = self.node.shape()
        self.assertTrue(fresh.isValid())
        self.assertEqual(len(fresh.Solids()), 1)
        self.assertAlmostEqual(fresh.Volume(), built.Volume(), delta=1e-7)
        self.assertEqual(fresh.cut(built).Volume(), 0)
        self.assertEqual(built.cut(fresh).Volume(), 0)

    def test_remaining_registration_lands_keep_their_source_contact(self):
        model = CarryFrameBench()
        model.set_state(drop_mm=0)
        model.assemble()
        guides = world_solids(model, selected={'Curta.first.tens_slide_bearing',
                                               'Curta.second.tens_slide_bearing'})
        original, fitted = MainBody().shape(), self.node.shape()
        for station, angle in (('first', 0), ('second', -20)):
            total, retained, protected = 0, 0, 0
            for land in registration_lands(original, guides['Curta.'+station+'.tens_slide_bearing']):
                total += land.Area()
                retained += land.intersect(fitted).Area()
                remainder = land
                for exception in seat_edge_exceptions(angle):
                    remainder = remainder.cut(exception)
                protected += remainder.Area()
                lost = remainder.cut(fitted)
                self.assertTrue(lost.isValid())
                self.assertAlmostEqual(lost.Area(), 0, delta=1e-7, msg=station)
            # Includes the lower 20.43 mm² side land, two front patches and
            # the other native upper/side seats found by the complete map.
            self.assertGreater(total, 34.1)
            self.assertGreater(protected, .98*total)
            self.assertGreaterEqual(retained+1e-7, protected)

    def test_gap_parameter_moves_the_measured_slider_walls(self):
        # Native distances at independent source surface points, not cutter
        # extents or a comparison against a second call to the fitter.
        for gap in (.04, .05, .06):
            fitted = CarryPassageFrame(running_gap=gap).shape()
            for angle in (0, -20):
                for point in ((52.725, -7.155, -16.35), (50.5, -7.2, -21.6)):
                    site = cq.Vertex.makeVertex(*point).rotate((0, 0, 0), (0, 0, 1), angle)
                    self.assertAlmostEqual(fitted.distance(site), gap, delta=1e-6)

    def test_spring_back_walls_have_bounded_normal_gaps(self):
        model = CarryFrameBench()
        model.set_state(drop_mm=2.562)  # maximum spread in the complete detent law
        model.assemble()
        wires = world_solids(model, include_flexible=True,
                            selected={'Curta.'+s+'.carry_lever_spring.wire' for s in ('first', 'second')})
        for station, angle in (('first', 0), ('second', 20)):
            frame = self.node.shape().rotate((0, 0, 0), (0, 0, 1), angle)
            wire = wires['Curta.'+station+'.carry_lever_spring.wire'].rotate((0, 0, 0), (0, 0, 1), angle)
            for xmin, xmax in ((53.4, 54.3), (60.3, 61.2)):
                walls = [face for face in frame.Faces() if face.geomType() == 'PLANE'
                         and abs(face.normalAt().y) > .999999
                         and xmin < face.Center().x < xmax and -11.5 < face.Center().y < -11.2]
                self.assertEqual(len(walls), 1)
                distance = wire.distance(walls[0])
                self.assertGreaterEqual(distance, self.node.running_gap-1e-6)
                # Outward source-bound rounding contributes less than .001 mm.
                self.assertLessEqual(distance, self.node.running_gap+.001)
