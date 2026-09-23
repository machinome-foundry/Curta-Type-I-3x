"""A positive spatial STL seat overlap is not waived as a small number."""

import hashlib
import json
import logging
import unittest

import cadquery as cq
import numpy as np
from machinome.simulation import Sim
from simulation.reverse_nose_seat import UnseatedReverseNoseReference
from simulation.running import OperatingCurta
from simulation.standard.parts import ReverseNosePlate
from simulation.contracts import assert_connected_material
from simulation.tools.interference import world_solids, rigid_leaves
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume

PLATE = 'Curta.frame.lower_bearing_plate.reverse_nose_plate'
DRUM = 'Curta.main_drive.stepped_drum.main_axle_step_drum_1.main_axle_step_drum_bottom_1'


class ReverseNoseSeatTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sim = Sim(OperatingCurta(), dt=.1, meshes=True)
        cls.native = world_solids(cls.sim.node, selected={PLATE, DRUM})
        leaves = dict(rigid_leaves(cls.sim.node))
        cls.facets = {name: mesh_solid(leaves[name].mesh) for name in (PLATE, DRUM)}

    def test_seat_clears_rotating_drum_in_both_modes(self):
        for lift in (0, 9):
            for angle in (0, 18, 36, 54, 90, 180, 270, 360):
                with self.subTest(lift=lift, angle=angle):
                    drum = self.native[DRUM].rotate((0, 0, 0), (0, 0, 1), -angle).translate((0, 0, lift))
                    common = self.native[PLATE].intersect(drum)
                    self.assertTrue(common.isValid())
                    self.assertEqual(common.Volume(), 0)
                    drum_mesh = self.facets[DRUM].rotate((0, 0, -angle)).translate((0, 0, lift))
                    self.assertEqual(faceted_common_volume(self.facets[PLATE] ^ drum_mesh), 0)

    def test_relief_is_limited_to_the_source_drum_seat(self):
        part = self.sim.node.frame.lower_bearing_plate.reverse_nose_plate
        source, fitted = ReverseNosePlate().shape(), part.shape()
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        assert_connected_material(part.mesh)
        self.assertEqual(fitted.cut(source).Volume(), 0)
        removed = source.cut(fitted)
        self.assertGreater(removed.Volume(), 0)
        # Drum's swept upper land is R9 at world Z-119.85. Transform that
        # axis to the plate's source frame; add .05 radial/axial seat gap.
        zone = cq.Solid.makeCylinder(9.05, .15, cq.Vector(-14.4, 0, 2.95))
        self.assertEqual(removed.cut(zone).Volume(), 0)
        for name in ('xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax'):
            self.assertAlmostEqual(getattr(source.BoundingBox(), name),
                                   getattr(fitted.BoundingBox(), name), places=7)

    def test_seat_keeps_free_gap_and_axial_capture(self):
        drum = self.native[DRUM].rotate((0, 0, 0), (0, 0, 1), -180)
        drum_mesh = self.facets[DRUM].rotate((0, 0, -180))
        # Relief is only on the lower face. The original upper face remains
        # flush with the other side of the source's 3 mm slot: upward travel
        # is intentionally still blocked, not an extra face to trim.
        for shift in (-.02,):
            common = self.native[PLATE].translate((0, 0, shift)).intersect(drum)
            self.assertTrue(common.isValid())
            self.assertEqual(common.Volume(), 0)
            self.assertEqual(faceted_common_volume(self.facets[PLATE].translate((0, 0, shift)) ^ drum_mesh), 0)
        common = self.native[PLATE].translate((0, 0, -.1)).intersect(drum)
        self.assertTrue(common.isValid())
        self.assertGreater(common.Volume(), 0)
        self.assertGreater(faceted_common_volume(self.facets[PLATE].translate((0, 0, -.1)) ^ drum_mesh), 0)
        common = self.native[PLATE].translate((0, 0, .02)).intersect(drum)
        self.assertTrue(common.isValid())
        self.assertGreater(common.Volume(), 0)
        self.assertGreater(faceted_common_volume(self.facets[PLATE].translate((0, 0, .02)) ^ drum_mesh), 0)

    def test_initial_bank_is_unchanged(self):
        bank = dict(self.sim.state)
        self.assertEqual(len(bank), 213)
        self.assertEqual(hashlib.sha256(json.dumps(bank, sort_keys=True,
            separators=(',', ':')).encode()).hexdigest(),
            'ea39d95d50f06580db66c894f5b3f700ab6ed930cee113b2b9ffe4689935f5b7')

    def test_unrelated_motion_and_meshes_are_unchanged(self):
        baseline = Sim(UnseatedReverseNoseReference(), dt=.1, meshes=True)
        self.sim.reset()
        try:
            for angle in (0, 180):
                for sim in (baseline, self.sim):
                    if angle:
                        command = sim.move('crank_rotation', to=angle, duration=1)
                        sim.run(1)
                        self.assertEqual(command.status, 'completed')
                self.assertEqual(dict(baseline.state), dict(self.sim.state))
                before, after = dict(rigid_leaves(baseline.node)), dict(rigid_leaves(self.sim.node))
                self.assertEqual(set(before), set(after))
                for path in before:
                    if path != PLATE:
                        np.testing.assert_array_equal(before[path].mesh.vertices,
                                                      after[path].mesh.vertices, err_msg=path)
                        np.testing.assert_array_equal(before[path].mesh.faces,
                                                      after[path].mesh.faces, err_msg=path)
        finally:
            self.sim.reset()


if __name__ == '__main__':
    logging.disable(logging.INFO)
    unittest.main()
