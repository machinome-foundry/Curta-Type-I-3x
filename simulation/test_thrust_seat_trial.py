"""The washer and spring must be supported by real seats over carriage travel."""

import numpy as np
from machinome.test import TestCase
from simulation.thrust_seat_trial import ThrustSeatBench, SeatedThrustBench


class ThrustSeatTest(TestCase):
    node = SeatedThrustBench

    def test_ring_clears_the_collar_and_is_supported_by_its_inner_ledge(self):
        for lift in (0, 1.5, 3, 4.5, 6):
            for angle in range(-100, 101, 20):
                self.node.set_state(travel=lift, shift=angle)
                self.assertNotIntersecting(self.node.thrust_ring, self.node.collar)
                self.assertFreeWithin(self.node.thrust_ring, .04,
                                      against=self.node.collar, along=(0, 0, 1))
                self.assertBlockedBeyond(self.node.thrust_ring, .1,
                                         against=self.node.collar, along=(0, 0, -1),
                                         directions='forward')

    def test_spring_clears_both_seats_but_is_captured_between_them(self):
        for lift in (0, 1.5, 3, 4.5, 6):
            self.node.set_state(travel=lift, shift=0)
            wire = self.node.carriage_spring.wire
            for part in (self.node.collar, self.node.thrust_ring,
                         self.node.carriage_spring_sleeve):
                self.assertNotIntersecting(wire, part)
            for seat in (self.node.thrust_ring, self.node.carriage_spring_sleeve):
                self.assertFreeWithin(wire, .04, against=seat, along=(0, 0, 1))
            self.assertBlockedBeyond(wire, .2, against=self.node.thrust_ring,
                                     along=(0, 0, -1), directions='forward')
            self.assertBlockedBeyond(wire, .2, against=self.node.carriage_spring_sleeve,
                                     along=(0, 0, 1), directions='forward')

    def test_endpoints_follow_the_measured_seats_not_the_old_free_pose(self):
        self.node.set_state(travel=0, shift=0)
        sleeve = self.node.carriage_spring_sleeve.mesh.vertices.copy()
        for lift in (0, 1.5, 3, 4.5, 6):
            self.node.set_state(travel=lift, shift=80)
            caps = self.node.carriage_spring.wire.mesh.vertices[-2:]
            self.assertAlmostEqual(caps[0, 2], 35.5 + lift, places=6)
            self.assertAlmostEqual(caps[1, 2], 53.35, places=6)
            np.testing.assert_array_equal(
                self.node.carriage_spring_sleeve.mesh.vertices, sleeve)

    def test_source_sized_wire_stays_connected_through_full_compression(self):
        from simulation.contracts import assert_connected_material
        for lift in (0, 1.5, 3, 4.5, 6):
            self.node.set_state(travel=lift, shift=0)
            wire = self.node.carriage_spring.wire
            assert_connected_material(wire.mesh)
            radius = np.linalg.norm(wire.mesh.vertices[:, :2], axis=1)
            self.assertGreaterEqual(radius.min(), 12.29)
            self.assertLessEqual(radius.max(), 14.11)
            if wire.exact:
                self.assertTrue(wire.shape().isValid())
                self.assertEqual(len(wire.shape().Solids()), 1)

    def test_original_placement_still_reproduces_both_source_contacts(self):
        original = ThrustSeatBench()
        original.set_state(travel=0, shift=0)
        original.assemble()
        original.build_stls()
        self.assertIntersecting(original.thrust_ring, original.collar)
        self.assertIntersecting(original.carriage_spring.wire, original.thrust_ring)
