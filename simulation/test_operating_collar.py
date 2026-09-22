"""Collar fitting must survive carriage travel without losing its retainers."""

from machinome.simulation import Sim
from machinome.test import TestCase
from simulation.operating_collar import OperatingCollarBench


class OperatingCollarTest(TestCase):
    node = OperatingCollarBench

    def test_initial_bank_matches_the_unchanged_default_root(self):
        from simulation.running import OperatingCurta

        trial = Sim(self.node, dt=.1)
        original = Sim(OperatingCurta(), dt=.1)
        self.assertEqual(dict(trial.state), dict(original.state))

    def test_operating_parts_match_the_independent_seating_bench(self):
        import numpy as np
        from scipy.spatial import cKDTree
        from simulation.collar_pin_seat import FittedCollarPinSeat

        bench = FittedCollarPinSeat()
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
            for changed in (carrier.crank_collar, carrier.crank_collar_nut):
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
        spider = registers.dial_detents.spider_spring.mount
        pins = (carrier.upper_carriage_body_1.counter_body_pin_1,
                carrier.upper_carriage_body_1.counter_body_pin_2)

        def check():
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
                for clearing in (0, 180):
                    self.assertEqual(sim.move('clearing_rotation', to=clearing).status,
                                     'completed')
                    check()
                    self.assertEqual(sim.move('carriage_elevation', to=0).status,
                                     'completed')
                    check()
                    self.assertEqual(sim.move('carriage_elevation', to=6).status,
                                     'completed')
        finally:
            sim.reset()
