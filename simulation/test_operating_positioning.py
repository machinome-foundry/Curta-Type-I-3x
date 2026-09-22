"""The operating carriage spring must sit between its physical support faces.

These checks use admitted requests on the actual default root. The independent
source-seat numbers are from the collar/sleeve measurements, not the spring's
placement formula. They certify this interface, not whole-machine clearance.
"""

import numpy as np

from machinome.simulation import Sim
from machinome.test import TestCase
from simulation.operating_positioning import OperatingPositioningBench
from simulation.running import register_reading


class OperatingPositioningTest(TestCase):
    node = OperatingPositioningBench

    def test_ring_and_wire_are_seated_after_lift_shift_and_replay(self):
        sim = Sim(self.node, dt=.1, meshes=True)
        positioning = self.node.carriage.positioning
        ring = positioning.thrust_ring
        wire = positioning.carriage_spring.wire
        sleeve = positioning.carriage_spring_sleeve
        collar = self.node.carriage.registers.carrier.crank_collar
        sleeve_vertices = sleeve.mesh.vertices.copy()

        def check():
            lift = sim.state['carriage.registers.lift']
            self.assertAlmostEqual(ring.mesh.bounds[0, 2], 33.05 + lift, places=5)
            caps = wire.mesh.vertices[-2:]
            self.assertAlmostEqual(caps[0, 2], 35.5 + lift, places=5)
            self.assertAlmostEqual(caps[1, 2], 53.35, places=5)
            np.testing.assert_array_equal(sleeve.mesh.vertices, sleeve_vertices)
            self.assertNotIntersecting(ring, collar)
            for part in (ring, collar, sleeve, positioning.p_6mm_ball_419094):
                self.assertNotIntersecting(wire, part)
            self.assertFreeWithin(ring, .04, against=collar, along=(0, 0, 1))
            self.assertBlockedBeyond(ring, .1, against=collar,
                                     along=(0, 0, -1), directions='forward')
            self.assertBlockedBeyond(wire, .2, against=ring,
                                     along=(0, 0, -1), directions='forward')
            self.assertBlockedBeyond(wire, .2, against=sleeve,
                                     along=(0, 0, 1), directions='forward')
            self.assertEqual(register_reading(sim), 0)
            self.assertEqual(register_reading(sim, True), 0)

        try:
            check()
            for lift in (1.5, 3, 4.5, 6):
                self.assertEqual(sim.move('carriage_elevation', to=lift).status,
                                 'completed')
                check()
            saved = sim.snapshot()
            for shift in (20, 40, 60, 80, 100):
                self.assertEqual(sim.move('carriage_rotation', to=shift).status,
                                 'completed')
                check()
                self.assertEqual(sim.move('carriage_elevation', to=0).status,
                                 'completed')
                check()
                self.assertEqual(sim.move('carriage_elevation', to=6).status,
                                 'completed')
            final = dict(sim.state)
            final_caps = wire.mesh.vertices[-2:].copy()
            sim.restore(saved)
            for shift in (20, 40, 60, 80, 100):
                sim.move('carriage_rotation', to=shift)
                sim.move('carriage_elevation', to=0)
                sim.move('carriage_elevation', to=6)
            self.assertEqual(dict(sim.state), final)
            np.testing.assert_array_equal(wire.mesh.vertices[-2:], final_caps)
        finally:
            sim.reset()

    def test_changed_ring_and_wire_clear_every_rigid_neighbour_at_rest(self):
        from simulation.tools.interference import rigid_leaves

        sim = Sim(self.node, dt=.1, meshes=True)
        try:
            positioning = self.node.carriage.positioning
            ring, wire = positioning.thrust_ring, positioning.carriage_spring.wire
            for path, other in rigid_leaves(self.node):
                for changed in (ring, wire):
                    if changed is other:
                        continue
                    with self.subTest(changed=changed.name, neighbour=path):
                        self.assertNotIntersecting(changed, other)
        finally:
            sim.reset()
