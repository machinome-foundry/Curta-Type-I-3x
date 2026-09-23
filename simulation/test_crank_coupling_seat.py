"""The pinned crank must fit the actual complete axle without overlap."""

from machinome.test import TestCase
from simulation.crank_coupling_seat import CrankCouplingSeatBench
from simulation.standard.parts import MainCrank
from simulation.tools.interference import world_solids
from simulation.tools.crank_drum_contact import CRANK, DRUM
from simulation.contracts import assert_connected_material
import cadquery as cq
import hashlib
import json
from machinome.simulation import Sim


class CrankCouplingSeatTest(TestCase):
    node = CrankCouplingSeatBench

    def test_crank_clears_complete_drum(self):
        self.assertNotIntersecting(self.node.main_drive.crank.crank_handle_1.main_crank,
            self.node.main_drive.stepped_drum.main_axle_step_drum_1.main_axle_step_drum_top_1)

    def test_retaining_pin_clears_both_mating_parts(self):
        pin = self.node.main_drive.crank.crank_handle_pin
        self.assertNotIntersecting(pin, self.node.main_drive.crank.crank_handle_1.main_crank)
        self.assertNotIntersecting(pin,
            self.node.main_drive.stepped_drum.main_axle_step_drum_1.main_axle_step_drum_top_1)

    def test_crank_bore_is_coaxial_with_unchanged_axle(self):
        shapes = world_solids(self.node, selected={CRANK, DRUM})
        for path, radius in ((CRANK, 4.56), (DRUM, 4.4425)):
            circles = [edge for edge in shapes[path].Edges()
                       if edge.geomType() == 'CIRCLE' and abs(edge.radius()-radius) < 1e-9
                       and edge.arcCenter().z > 68]
            self.assertGreater(len(circles), 0)
            for edge in circles:
                center = edge.arcCenter()
                self.assertAlmostEqual(center.x, -.009541016, places=8)
                self.assertAlmostEqual(center.y, .073549841, places=8)

    def test_only_internal_pocket_roof_has_bounded_relief(self):
        part = self.node.main_drive.crank.crank_handle_1.main_crank
        source, fitted = MainCrank().shape(), part.shape()
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        assert_connected_material(part.mesh)
        self.assertEqual(fitted.cut(source).Volume(), 0)
        removed = source.cut(fitted)
        self.assertGreater(removed.Volume(), 0)
        pocket = cq.Solid.makeCylinder(4.56, .70, cq.Vector(0, 0, 28.45))
        self.assertEqual(removed.cut(pocket).Volume(), 0)
        for bound in ('xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax'):
            self.assertAlmostEqual(getattr(fitted.BoundingBox(), bound),
                                   getattr(source.BoundingBox(), bound), places=7)

    def test_transverse_pin_keeps_vertical_capture(self):
        pin = self.node.main_drive.crank.crank_handle_pin
        for part in (self.node.main_drive.crank.crank_handle_1.main_crank,
                     self.node.main_drive.stepped_drum.main_axle_step_drum_1.main_axle_step_drum_top_1):
            self.assertFreeWithin(part, .02, against=pin, along=(0, 0, 1))
            # Measured source hole clearances exceed .3 mm. The unchanged
            # crank and shaft are both captured at .75 mm in either direction.
            self.assertBlockedBeyond(part, .75, against=pin, along=(0, 0, 1))

    def test_initial_bank_retains_pre_fit_witness(self):
        bank = dict(Sim(self.node, dt=.1).state)
        self.assertEqual(len(bank), 214)
        self.assertEqual(bank.pop('carriage.positioning.p_6mm_ball_419094.slide'), 0)
        self.assertEqual(len(bank), 213)
        self.assertEqual(hashlib.sha256(json.dumps(bank, sort_keys=True,
            separators=(',', ':')).encode()).hexdigest(),
            'ea39d95d50f06580db66c894f5b3f700ab6ed930cee113b2b9ffe4689935f5b7')

    def test_coupling_follows_actual_crank_turn_and_lift(self):
        sim = Sim(self.node, dt=.1, meshes=True)
        crank = self.node.main_drive.crank.crank_handle_1.main_crank
        drum = self.node.main_drive.stepped_drum.main_axle_step_drum_1.main_axle_step_drum_top_1
        pin = self.node.main_drive.crank.crank_handle_pin
        try:
            initial = sim.snapshot()
            for lift in (0, 9):
                # Two independently initialized legal crank modes, not a
                # mid-cycle mode switch (which can meet a locking restraint).
                sim.restore(initial)
                self.assertEqual(sim.move('crank_elevation', to=lift).status, 'completed')
                for angle in (90, 270):
                    result = sim.move('crank_rotation', to=angle)
                    self.assertEqual(result.status, 'completed', (lift, angle))
                    self.assertNotIntersecting(crank, drum)
                    self.assertNotIntersecting(crank, pin)
                    self.assertNotIntersecting(drum, pin)
        finally:
            sim.reset()
