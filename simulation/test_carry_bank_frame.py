"""Full-bank frame failures, with independently checked installed fixtures."""

import logging
import unittest

import numpy as np
from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.carry_bank_frame import CarryBankFrameBench, stations
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume
# The public node runner discovers TestCase classes in this companion file.
# The fixture-identity/red witnesses below remain ordinary unittest tests.
from simulation.test_carry_bank_capture import CarryBankCaptureTest as _CaptureContract


class CarryBankCaptureTest(_CaptureContract):
    node = _CaptureContract.node


class CarryBankFrameTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bench = CarryBankFrameBench()
        cls.bench.set_state(drop_mm=0)
        cls.bench.assemble()
        cls.bench.build_stls()

    def native(self):
        return world_solids(self.bench, include_flexible=True)

    def test_fixture_matches_the_operating_root_at_rest(self):
        self.bench.set_state(drop_mm=0)
        sim = Sim(OperatingCurta(), dt=.1, meshes=True)
        installed = world_solids(sim.node, include_flexible=True)
        bench = self.native()
        mapping = {'Curta.frame.main_body': 'Curta.frame.upper_frame.main_body'}
        for path, node, slider in stations(self.bench):
            for suffix in (slider, 'tens_slide_bearing', 'carry_lever_spring.wire'):
                mapping['Curta.'+path+'.'+suffix] = 'Curta.carry_mechanism.'+path+'.'+suffix
        for path, counterpart in mapping.items():
            with self.subTest(path=path):
                a, b = bench[path], installed[counterpart]
                self.assertTrue(a.isValid() and b.isValid())
                self.assertEqual(a.cut(b).Volume(), 0)
                self.assertEqual(b.cut(a).Volume(), 0)

    def test_actual_stroke_and_fixed_supports(self):
        self.bench.set_state(drop_mm=0)
        leaves = dict(rigid_leaves(self.bench))
        initial = {path: node.mesh.vertices.copy() for path, node in leaves.items()}
        for drop in (1.1630815, 2.562, 4.2, 0):
            self.bench.set_state(drop_mm=drop)
            for path, node in rigid_leaves(self.bench):
                moving = path.endswith(('tens_slider_for_results', 'tens_slider_for_turns_counter'))
                expected = initial[path] - (0, 0, drop) if moving else initial[path]
                np.testing.assert_allclose(node.mesh.vertices, expected, atol=1e-8, rtol=0,
                                           err_msg=path)

    def check_clearance(self, spring, drop):
        self.bench.set_state(drop_mm=drop)
        shapes = self.native()
        frame = shapes['Curta.frame.main_body']
        frame_mesh = mesh_solid(self.bench.frame.main_body.mesh)
        for path, node, slider in stations(self.bench):
            part = node.carry_lever_spring.wire if spring else getattr(node, slider)
            suffix = 'carry_lever_spring.wire' if spring else slider
            common = shapes['Curta.'+path+'.'+suffix].intersect(frame)
            with self.subTest(station=path, drop=drop, kernel='native'):
                self.assertTrue(common.isValid())
                self.assertEqual(common.Volume(), 0)
            with self.subTest(station=path, drop=drop, kernel='world64'):
                self.assertEqual(faceted_common_volume(mesh_solid(part.mesh) ^ frame_mesh), 0)

    def test_all_slider_endpoints_clear_the_complete_frame(self):
        for drop in (0, 4.2):
            self.check_clearance(False, drop)

    def test_all_springs_clear_at_preload_and_maximum_spread(self):
        for drop in (1.1630815, 2.562):
            self.check_clearance(True, drop)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    unittest.main()
