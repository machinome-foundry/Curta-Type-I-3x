"""Named frame failures first; no collision-volume tolerance or hidden frame."""

import numpy as np
from machinome.test import TestCase
from simulation.carry_frame import CarryFrameBench
from simulation.curta import Curta
from simulation.detents import RESULTS
from simulation.tools.interference import world_solids


class CarryFrameTest(TestCase):
    node = CarryFrameBench

    def clear(self, station, part, drop):
        self.node.set_state(drop_mm=drop)
        carry = getattr(self.node, station)
        moving = (carry.carry_lever_spring.wire if part == 'spring'
                  else carry.tens_slider_for_results)
        self.assertNotIntersecting(moving, self.node.frame.main_body)

    def test_first_spring_clears_frame_at_ninety_nine(self):
        self.clear('first', 'spring', 1.1630815)

    def test_second_spring_clears_frame_at_ninety_nine(self):
        self.clear('second', 'spring', 1.1630815)

    def test_first_raised_slider_clears_frame(self):
        self.clear('first', 'slider', 0)

    def test_second_raised_slider_clears_frame(self):
        self.clear('second', 'slider', 0)

    def test_first_lowered_slider_clears_frame(self):
        self.clear('first', 'slider', 4.2)

    def test_second_lowered_slider_clears_frame(self):
        self.clear('second', 'slider', 4.2)

    def test_actual_stroke_and_stationary_supports(self):
        self.node.set_state(drop_mm=0)
        fixed = [self.node.frame.main_body,
                 self.node.first.tens_slide_bearing, self.node.second.tens_slide_bearing]
        before = [part.mesh.vertices.copy() for part in fixed]
        sliders = [self.node.first.tens_slider_for_results,
                   self.node.second.tens_slider_for_results]
        raised = [part.mesh.vertices.copy() for part in sliders]
        for drop in (1.1630815, 2.562, 4.2, 0):
            self.node.set_state(drop_mm=drop)
            for part, expected in zip(fixed, before):
                np.testing.assert_allclose(part.mesh.vertices, expected, atol=1e-5, rtol=0)
            for part, expected in zip(sliders, raised):
                np.testing.assert_allclose(part.mesh.vertices, expected-(0,0,drop),
                                           atol=1e-5, rtol=0)

    def test_bench_matches_the_installed_station_frames(self):
        root = Curta()
        root.set_state(initial_result=99, initial_turns=0, operand=1, crank_turns=0,
                       subtract=0, carriage_position=0, carriage_lift=0, clear=0)
        root.assemble()
        self.node.set_state(drop_mm=1.1630815)
        self.node.assemble()
        mapping = {'Curta.frame.main_body': 'Curta.frame.upper_frame.main_body'}
        for index, station in enumerate(('first', 'second'), 1):
            for part in ('tens_slider_for_results', 'tens_slide_bearing',
                         'carry_lever_spring.wire'):
                mapping['Curta.'+station+'.'+part] = (
                    'Curta.carry_mechanism.result_carries.results_tens_lever_assembly_'
                    +str(index)+'.'+part)
        bench = world_solids(self.node, include_flexible=True, selected=set(mapping))
        installed = world_solids(root, include_flexible=True, selected=set(mapping.values()))
        self.assertEqual(set(bench), set(mapping))
        self.assertEqual(set(installed), set(mapping.values()))
        for path, source in mapping.items():
            a, b = bench[path], installed[source]
            self.assertAlmostEqual(a.Volume(), b.Volume(), delta=1e-5, msg=path)
            np.testing.assert_allclose(a.Center().toTuple(), b.Center().toTuple(), atol=1e-5, rtol=0)
            for attribute in ('xmin','ymin','zmin','xmax','ymax','zmax'):
                self.assertAlmostEqual(getattr(a.BoundingBox(), attribute),
                                       getattr(b.BoundingBox(), attribute), delta=1e-5, msg=path)

    def test_frame_is_one_valid_solid(self):
        shape = self.node.frame.main_body.shape()
        self.assertTrue(shape.isValid())
        self.assertEqual(len(shape.Solids()), 1)

    def test_full_stroke_grid_and_every_detent_knot_clear_the_frame(self):
        drops = sorted({4.2*i/40 for i in range(41)} |
                       {4.2*engaged for engaged, _ in RESULTS} | {1.1630815})
        for drop in drops:
            for station in ('first', 'second'):
                for part in ('spring', 'slider'):
                    try:
                        self.clear(station, part, drop)
                    except AssertionError as error:
                        raise AssertionError(f'{station} {part}, drop={drop}: {error}') from error
