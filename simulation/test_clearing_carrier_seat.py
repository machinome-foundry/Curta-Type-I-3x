"""The rotating clearing cover must clear the stationary counter-body rim."""

import hashlib
import json

import cadquery as cq

from machinome.simulation import Sim
from machinome.test import TestCase
from simulation.carriage_frame_fit import FittedCounterBody
from simulation.clearing_carrier_seat import ClearingCarrierSeatBench
from simulation.contracts import assert_connected_material


class ClearingCarrierSeatTest(TestCase):
    node = ClearingCarrierSeatBench

    def test_initial_bank_retains_the_measured_pre_fit_witness(self):
        sim = Sim(self.node, dt=.1)
        bank = dict(sim.state)
        self.assertEqual(len(bank), 214)
        self.assertEqual(bank.pop('carriage.positioning.p_6mm_ball_419094.slide'), 0)
        self.assertEqual(len(bank), 213)
        encoded = json.dumps(bank, sort_keys=True, separators=(',', ':')).encode()
        self.assertEqual(hashlib.sha256(encoded).hexdigest(),
                         'ea39d95d50f06580db66c894f5b3f700ab6ed930cee113b2b9ffe4689935f5b7')

    def test_only_the_measured_outer_top_land_is_relieved(self):
        original = FittedCounterBody().shape()
        body = self.node.carriage.registers.carrier.upper_carriage_body_1.counter_body
        fitted = body.shape()
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        assert_connected_material(body.mesh)
        self.assertEqual(fitted.cut(original).Volume(), 0)
        removed = original.cut(fitted)
        self.assertGreater(removed.Volume(), 0)
        # The measured intersection is the R46.8..48.75, Z0..0.8 annulus.
        # A .05 mm axial/radial seating gap must not reach any inner bearing,
        # indexing pocket, bore, pin seat, or the remaining outer flange.
        zone = cq.Solid.makeCylinder(48.8, .85).cut(
            cq.Solid.makeCylinder(46.75, .85))
        self.assertEqual(removed.cut(zone).Volume(), 0)
        protected = cq.Solid.makeCylinder(46.75, 22, cq.Vector(0, 0, -1))
        self.assertEqual(removed.intersect(protected).Volume(), 0)
        for bound in ('xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax'):
            self.assertAlmostEqual(getattr(fitted.BoundingBox(), bound),
                                   getattr(original.BoundingBox(), bound), places=7)

    def test_clearing_sweep_preserves_clearance_and_axial_capture(self):
        sim = Sim(self.node, dt=.1, meshes=True)
        registers = self.node.carriage.registers
        body = registers.carrier.upper_carriage_body_1.counter_body
        cover = registers.clearing_ring.clearing_cover
        try:
            self.assertNotIntersecting(body, cover)
            self.assertEqual(sim.move('carriage_elevation', to=6).status, 'completed')
            for shift in (0, 20, 40, 60, 80, 100):
                self.assertEqual(sim.move('carriage_rotation', to=shift).status, 'completed')
                for angle in (0, 45, 90, 135, 180, 230, 270, 315, 360):
                    self.assertEqual(sim.move('clearing_rotation', to=angle).status, 'completed')
                    self.assertNotIntersecting(body, cover)
                    # Perturbations use the part frame: the source cover is
                    # turned upside down, so local +Z presses world-down.
                    self.assertFreeWithin(cover, .04, against=body,
                                          along=(0, 0, 1), directions='forward')
                    self.assertBlockedBeyond(cover, .1, against=body,
                                             along=(0, 0, 1), directions='forward')
        finally:
            sim.reset()
