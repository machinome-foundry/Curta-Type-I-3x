"""Collar fitting must survive carriage travel without losing its retainers."""

import hashlib
import json

from machinome.simulation import Sim
from machinome.test import TestCase
from simulation.operating_collar import OperatingCollarBench


class OperatingCollarTest(TestCase):
    node = OperatingCollarBench

    def test_initial_bank_matches_the_pre_adoption_default_root(self):
        trial = Sim(self.node, dt=.1)
        # Captured before adoption at project 5f101ae / framework c81a585.
        # A fixed witness keeps this meaningful once the default adopts the
        # same parts; comparing two aliases of the fitted root would not.
        bank = dict(trial.state)
        self.assertEqual(len(bank), 216)
        # The separately proved loop adds only these two zero-at-rest entries;
        # retain the entire original bank hash below, not a new fitted witness.
        self.assertEqual(bank.pop('loop_deployment'), 0)
        self.assertEqual(bank.pop('carriage.registers.clearing_ring.clearing_ring.swivel'), 0)
        self.assertEqual(len(bank), 214)
        self.assertEqual(bank.pop('carriage.positioning.p_6mm_ball_419094.slide'), 0)
        self.assertEqual(len(bank), 213)
        encoded = json.dumps(bank, sort_keys=True, separators=(',', ':')).encode()
        self.assertEqual(hashlib.sha256(encoded).hexdigest(),
                         'ea39d95d50f06580db66c894f5b3f700ab6ed930cee113b2b9ffe4689935f5b7')

    def test_operating_parts_match_the_independent_seating_bench(self):
        import numpy as np
        from scipy.spatial import cKDTree
        from simulation.collar_pin_seat import SeatedCollarPinSeat

        bench = SeatedCollarPinSeat()
        bench.assemble()
        bench.build_stls()
        carrier = self.node.carriage.registers.carrier
        for name, actual in (
                ('collar', carrier.crank_collar),
                ('nut', carrier.crank_collar_nut),
                ('pin_left', carrier.upper_carriage_body_1.counter_body_pin_1),
                ('pin_right', carrier.upper_carriage_body_1.counter_body_pin_2)):
            expected = getattr(bench, name).mesh
            actual = actual.mesh
            a = np.concatenate((actual.vertices, actual.triangles_center))
            b = np.concatenate((expected.vertices, expected.triangles_center))
            with self.subTest(part=name):
                self.assertLess(cKDTree(a).query(b)[0].max(), .00001)
                self.assertLess(cKDTree(b).query(a)[0].max(), .00001)

    def test_collar_and_nut_clear_all_rigid_neighbours_at_rest(self):
        from simulation.tools.interference import rigid_leaves

        sim = Sim(self.node, dt=.1, meshes=True)
        try:
            carrier = self.node.carriage.registers.carrier
            for changed in (carrier.crank_collar, carrier.crank_collar_nut,
                            carrier.crank_collar_washer):
                for path, other in rigid_leaves(self.node):
                    if changed is not other:
                        with self.subTest(changed=changed.name, neighbour=path):
                            self.assertNotIntersecting(changed, other)
        finally:
            sim.reset()

    def test_collar_seats_and_retention_follow_lift_shift_and_clearing(self):
        sim = Sim(self.node, dt=.1, meshes=True)
        registers = self.node.carriage.registers
        carrier = registers.carrier
        collar, nut = carrier.crank_collar, carrier.crank_collar_nut
        washer = carrier.crank_collar_washer
        cover = registers.clearing_ring.clearing_cover
        spider = registers.dial_detents.spider_spring.mount
        pins = (carrier.upper_carriage_body_1.counter_body_pin_1,
                carrier.upper_carriage_body_1.counter_body_pin_2)

        def check():
            self.assertNotIntersecting(washer, collar)
            self.assertNotIntersecting(washer, cover)
            for neighbour, direction in ((collar, (0, 0, -1)), (cover, (0, 0, 1))):
                self.assertFreeWithin(washer, .04, against=neighbour,
                                      along=direction, directions='forward')
                self.assertBlockedBeyond(washer, .1, against=neighbour,
                                         along=direction, directions='forward')
            self.assertNotIntersecting(collar, spider)
            self.assertFreeWithin(spider, .04, against=collar, along=(0, 0, 1))
            self.assertBlockedBeyond(spider, .1, against=collar,
                                     along=(0, 0, 1), directions='forward')
            self.assertNotIntersecting(collar, nut)
            self.assertFreeWithin(nut, .1, against=collar, along=(0, 0, 1))
            self.assertBlockedBeyond(nut, .4, against=collar, along=(0, 0, 1))
            for pin in pins:
                self.assertNotIntersecting(collar, pin)
                self.assertFreeWithin(collar, 1, against=pin)
                self.assertBlockedBeyond(collar, 2, against=pin)
            for changed in (collar, nut):
                self.assertNotIntersecting(changed, registers.clearing_ring.clearing_cover)
                self.assertNotIntersecting(changed, carrier.crank_collar_washer)
                self.assertNotIntersecting(changed, self.node.carriage.positioning.thrust_ring)

        try:
            check()
            for lift in (1.5, 3, 4.5, 6):
                self.assertEqual(sim.move('carriage_elevation', to=lift).status, 'completed')
                check()
            for shift in (0, 20, 40, 60, 80, 100):
                self.assertEqual(sim.move('carriage_rotation', to=shift).status, 'completed')
                # The printed clearing cam has its two rest pockets at 0
                # and 230 degrees. Half a turn is intentionally not a seat.
                for clearing in (0, 230):
                    self.assertEqual(sim.move('clearing_rotation', to=clearing).status,
                                     'completed')
                    check()
                    self.assertEqual(sim.move('carriage_elevation', to=0).status,
                                     'completed')
                    check()
                    self.assertEqual(sim.move('carriage_elevation', to=6).status,
                                     'completed')
            self.assertEqual(sim.move('clearing_rotation', to=180).status, 'completed')
            self.assertEqual(sim.move('carriage_elevation', to=0).status, 'blocked')
            self.assertAlmostEqual(sim.state['carriage.registers.lift'], 4.810085)
            check()
        finally:
            sim.reset()
