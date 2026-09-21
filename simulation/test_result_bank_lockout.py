"""Every result station needs its own complete-print contact evidence."""

import unittest
import cadquery as cq
import manifold3d as manifold

from simulation.contracts import assert_connected_material
from simulation.higher_lockout_trial import HigherLockoutFitBench
from simulation.tools.higher_locking_envelope import contact_reader, faceted_common_volume
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.result_bank_lockout_probe import STATIONS, station_bench, station_reader


class ResultBankFixtureTest(unittest.TestCase):
    def test_positive_spatial_volume_is_retained_even_below_roundoff_of_a_plane(self):
        common = manifold.Manifold.cube((1e-6, 1e-6, 1e-6))
        self.assertGreater(common.volume(), 0)
        self.assertLess(common.volume(), 1e-15)
        self.assertEqual(faceted_common_volume(common), common.volume())

    def test_planar_contact_is_zero_volume_without_a_volume_tolerance(self):
        node = station_bench(3, trial=True)()
        node.set_state(shaft_angle=-37.999, crank_angle=160, carry_position=.5, time=0)
        node.assemble()
        node.build_stls()
        stack = getattr(node.shaft, STATIONS[1][1])
        common = mesh_solid(stack.mesh) ^ mesh_solid(node.bell.mesh).rotate((0, 0, -10))
        self.assertEqual(common.status(), manifold.Error.NoError)
        bounds = common.bounding_box()
        self.assertEqual(bounds[2], -31.5)
        self.assertEqual(bounds[5], -31.5)
        # An exactly planar set has no spatial volume, irrespective of the
        # floating signed-tetrahedron sum returned by the Boolean library.
        read = station_reader(3, .5, -17.999, trial=True)
        self.assertEqual(read(150, 'faceted'), 0)

    def test_trial_keeps_each_source_upper_in_its_own_local_frame(self):
        # Each source fusion contains absolute station-local placements. A
        # shared cached artifact would put another station's print on this
        # shaft even though its enclosing assembly uses the correct pivot.
        for station, (_, upper_name) in enumerate(STATIONS, 2):
            before_node = station_bench(station)()
            after_node = station_bench(station, trial=True)()
            for node in (before_node, after_node):
                node.set_state(shaft_angle=0, crank_angle=0, carry_position=0, time=0)
                node.assemble()
                node.build_stls()
            original = getattr(before_node.shaft, upper_name)
            before = original.shape()
            upper = getattr(after_node.shaft, upper_name)
            after = upper.shape()
            with self.subTest(station=station):
                self.assertTrue(after.isValid())
                self.assertEqual(len(after.Solids()), 1)
                assert_connected_material(upper.mesh)
                self.assertEqual(after.cut(before).Volume(), 0)
                removed = before.cut(after)
                lockout = original.pentagonal_lockout.shape()
                self.assertGreater(removed.Volume(), 0)
                self.assertLessEqual(removed.Volume(), lockout.Area()*.01)
                box = lockout.BoundingBox()
                core = cq.Solid.makeCylinder(4, box.zlen+2,
                                             cq.Vector(0, 0, box.zmin-1))
                for operation in original.pentagonal_lockout.operations:
                    if hasattr(operation, 'angle'):
                        lockout = lockout.rotate((0, 0, 0), operation.axis, operation.angle)
                        core = core.rotate((0, 0, 0), operation.axis, operation.angle)
                    else:
                        lockout = lockout.translate(operation.translation)
                        core = core.translate(operation.translation)
                self.assertEqual(removed.cut(lockout).Volume(), 0)
                self.assertEqual(removed.intersect(core).Volume(), 0)
                for bound in ('xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax'):
                    self.assertAlmostEqual(getattr(before.BoundingBox(), bound),
                                           getattr(after.BoundingBox(), bound), delta=.02)


class ResultBankContactTest(unittest.TestCase):
    # Deliberately red handoff fixture: .15 mm simulation fit has measured
    # indexed overlaps. Do not hide them or select the .16 mm trial until
    # its whole-bank material/engagement/admission checks justify adoption.
    trial = False

    def test_all_indexed_flats_clear_at_both_actual_carry_seats(self):
        for station in range(2, 12):
            for carry in (0, 1):
                for flat in range(5):
                    read = station_reader(station, carry, -16+72*flat, self.trial)
                    for kernel in ('native', 'faceted'):
                        with self.subTest(station=station, carry=carry, flat=flat, kernel=kernel):
                            self.assertLessEqual(read(180, kernel), 0)

    def test_both_locking_flanks_remain_present_at_every_station(self):
        for station in range(2, 12):
            for carry in (0, .25, .5, .75, 1):
                for flat in range(5):
                    for side in (-4, 4):
                        read = station_reader(station, carry, -16+72*flat+side, self.trial)
                        for kernel in ('native', 'faceted'):
                            with self.subTest(station=station, carry=carry, flat=flat,
                                              side=side, kernel=kernel):
                                self.assertGreater(read(180, kernel), 0)

    def test_generalized_tens_fixture_matches_the_original_trial(self):
        for carry, shaft in ((0, 169.6), (1, 169.6), (1, 22.22), (1, 49.08)):
            old = contact_reader(carry, shaft=shaft, node_type=HigherLockoutFitBench)
            new = station_reader(2, carry, shaft, trial=True)
            for crank in (145, 146.5, 159.5, 180):
                for kernel in ('native', 'faceted'):
                    with self.subTest(carry=carry, shaft=shaft, crank=crank, kernel=kernel):
                        self.assertEqual(new(crank, kernel), old(crank, kernel))


if __name__ == '__main__':
    unittest.main()
