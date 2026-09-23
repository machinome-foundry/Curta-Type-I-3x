"""The crank grip has a real seating gap, not a tiny-volume exemption."""

import logging
import unittest

import cadquery as cq
from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.operating_demonstrations import replay
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.tools.crank_handle_contact import CRANK, HANDLE
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume
from simulation.standard.parts import CrankHandle, CrankHandlePinScrew
from simulation.contracts import assert_connected_material


class CrankGripSeatTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sim = Sim(OperatingCurta(), dt=.1, meshes=True)

    def test_actual_addition_keeps_grip_clear_of_crank(self):
        sim = self.sim
        sim.reset()
        initial = sim.snapshot()
        sampled = []

        def sample():
            sampled.append(sim.time)
            native = world_solids(sim.node, selected={CRANK, HANDLE})
            common = native[CRANK].intersect(native[HANDLE])
            self.assertTrue(common.isValid())
            self.assertEqual(common.Volume(), 0)
            leaves = dict(rigid_leaves(sim.node))
            self.assertEqual(faceted_common_volume(mesh_solid(leaves[CRANK].mesh) ^
                                                  mesh_solid(leaves[HANDLE].mesh)), 0)

        sim.every(.1, sample)
        outcomes = replay(sim, 'addition', initial)
        self.assertEqual(len(sampled), 44)
        self.assertEqual(outcomes[-1][-1], (5, 2))
        sim.reset()

    def test_only_lower_face_changes_and_material_remains_connected(self):
        part = self.sim.node.main_drive.crank.crank_handle_1.crank_handle
        original, fitted = CrankHandle().shape(), part.shape()
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        assert_connected_material(part.mesh)
        self.assertEqual(fitted.cut(original).Volume(), 0)
        removed = original.cut(fitted)
        self.assertGreater(removed.Volume(), 0)
        box = original.BoundingBox()
        zone = cq.Solid.makeBox(box.xlen + 2, box.ylen + 2, .1,
                               cq.Vector(box.xmin - 1, box.ymin - 1, box.zmin - .05))
        self.assertEqual(removed.cut(zone).Volume(), 0)
        for key in ('xmin', 'xmax', 'ymin', 'ymax', 'zmax'):
            self.assertAlmostEqual(getattr(box, key), getattr(fitted.BoundingBox(), key), places=7)
        self.assertAlmostEqual(fitted.BoundingBox().zmin, box.zmin + .05, places=7)

    def test_lower_seat_has_measured_free_play_and_retained_stop(self):
        self.sim.reset()
        native = world_solids(self.sim.node, selected={CRANK, HANDLE})
        leaves = dict(rigid_leaves(self.sim.node))
        for shift, blocked in ((-.02, False), (-.1, True)):
            common = native[CRANK].intersect(native[HANDLE].translate((0, 0, shift)))
            self.assertTrue(common.isValid())
            volume = faceted_common_volume(mesh_solid(leaves[CRANK].mesh) ^
                                          mesh_solid(leaves[HANDLE].mesh).translate((0, 0, shift)))
            if blocked:
                self.assertGreater(common.Volume(), 0)
                self.assertGreater(volume, 0)
            else:
                self.assertEqual(common.Volume(), 0)
                self.assertEqual(volume, 0)

    def test_source_retaining_screw_common_is_geometrically_unchanged(self):
        source = CrankHandle().shape()
        fitted = self.sim.node.main_drive.crank.crank_handle_1.crank_handle.shape()
        pin = CrankHandlePinScrew().shape().rotate((0, 0, 0), (0, 1, 0), 90)
        pin = pin.translate((50.720609937 - 49.319648043, 0, 115.35 - 94.35))
        before, after = source.intersect(pin), fitted.intersect(pin)
        self.assertTrue(before.isValid())
        self.assertTrue(after.isValid())
        # This source overlap remains a finding. Prove the local seat cut
        # neither enlarges nor removes it, not that the screw is clear.
        self.assertGreater(before.Volume(), 0)
        self.assertEqual(before.cut(after).Volume(), 0)
        self.assertEqual(after.cut(before).Volume(), 0)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    unittest.main()
