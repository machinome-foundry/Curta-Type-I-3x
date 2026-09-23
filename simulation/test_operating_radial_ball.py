"""Production-facing radial-ball adoption gates, initially red on the static root."""

import logging
import unittest
import numpy as np
import cadquery as cq

from machinome.simulation import Sim
from machinome.exact import intersect_shapes
from simulation.running import OperatingCurta, StaticBallOperatingCurta
from simulation.positioning_ball_trial import RadialBallTrial, ReversedRadialBallTrial, PullingBallTrial
from simulation.test_radial_positioning_ball import RadialPositioningBallTest as _RetainedContract
from simulation.tools.positioning_ball_contact import BALL, BELL, FRAME, COLLAR
from simulation.tools.positioning_ball_ring import RING
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume
from simulation.test_carry_bank_trial import flexible_meshes
from simulation.counter_shoulder_operating_trial import ShoulderFittedStaticBallReference


class OperatingRadialBallGeometryTest(unittest.TestCase):
    model = OperatingCurta

    def test_default_adds_only_the_named_coordinate_and_no_ball_control(self):
        sim = Sim(self.model(), dt=.1)
        self.assertIn('carriage.positioning.p_6mm_ball_419094.slide', sim.state)
        self.assertEqual(sim.state['carriage.positioning.p_6mm_ball_419094.slide'], 0)
        self.assertEqual(len(sim.state), 214)
        self.assertEqual(set(self.model.controls), set(StaticBallOperatingCurta.controls))
        self.assertFalse(any('ball' in name for name in self.model.controls))

    def test_actual_source_sphere_moves_radially_and_clears_its_neighbours(self):
        sim = Sim(self.model(), dt=.1, meshes=True)
        original = world_solids(sim.node, selected={BALL})[BALL]
        command = sim.move('crank_rotation', to=90, duration=.5)
        sim.run(.5)
        self.assertEqual(command.status, 'completed')
        native = world_solids(sim.node, selected={BALL, BELL, FRAME, RING})
        centre = native[BALL].Center()
        self.assertGreater(centre.x, 11.8)
        self.assertAlmostEqual(centre.y, 0, places=9)
        self.assertAlmostEqual(centre.z, 30, places=9)
        self.assertAlmostEqual(native[BALL].Volume(), original.Volume(), places=9)
        for path in (BELL, FRAME, RING):
            common = intersect_shapes(native[BALL], native[path], BALL, path)
            self.assertTrue(common.isValid(), path)
            self.assertEqual(common.Volume(), 0, path)
        leaves = dict(rigid_leaves(sim.node))
        sphere = mesh_solid(leaves[BALL].mesh)
        for path in (BELL, FRAME, RING, COLLAR):
            self.assertEqual(faceted_common_volume(sphere ^ mesh_solid(leaves[path].mesh)), 0, path)

    def test_source_guide_captures_transverse_motion_without_closing_the_free_gap(self):
        sim = Sim(self.model(), dt=.1, meshes=True)
        native = world_solids(sim.node, selected={BALL, FRAME})
        leaves = dict(rigid_leaves(sim.node))
        sphere, frame = mesh_solid(leaves[BALL].mesh), mesh_solid(leaves[FRAME].mesh)
        saved = sim.snapshot()
        for radial in (-1.2252018554755857, 0, 2.213142830078919):
            for axis in (1, 2):
                for sign in (-1, 1):
                    for travel, blocked in ((.01, False), (.2, True)):
                        shift = [radial, 0, 0]
                        shift[axis] = sign * travel
                        moved = native[BALL].translate(tuple(shift))
                        common = moved.intersect(native[FRAME])
                        self.assertTrue(common.isValid())
                        volumes = (common.Volume(), faceted_common_volume(sphere.translate(tuple(shift)) ^ frame))
                        if blocked and radial > 2 and axis == 2:
                            # The raw OCCT common falsely reports empty here.
                            # Independently measured strict interior witnesses
                            # prove native capture without inventing a volume or
                            # relaxing a tolerance. The separate framework fix
                            # must refuse the inconsistent common.
                            witness = ({-1: (11.93431004745964, .4477315369512816, 26.088069310162098),
                                         1: (11.541571853564232, 3.0652117978127276, 32.321879856111245)})[sign]
                            vertex = cq.Vertex.makeVertex(*witness)
                            for solid in (moved, native[FRAME]):
                                self.assertTrue(solid.isInside(witness, 0))
                                self.assertGreater(min(vertex.distance(face) for face in solid.Faces()), 0)
                            self.assertGreater(volumes[1], 0)
                            continue
                        for volume in volumes:
                            if blocked:
                                self.assertGreater(volume, 0, (radial, axis, sign, travel))
                            else:
                                self.assertEqual(volume, 0, (radial, axis, sign, travel))
        self.assertEqual(sim.snapshot(), saved)


class OperatingRadialBallHistoryTest(_RetainedContract):
    model = OperatingCurta


class OperatingRadialBallPreservationTest(unittest.TestCase):
    def test_shared_bank_and_every_other_mesh_are_unchanged(self):
        # Compare the ball-only change with the same accepted shoulder fit
        # on both sides. The explicit original-shoulder reference has its own
        # all-other-geometry/214-bank preservation contract.
        before = Sim(ShoulderFittedStaticBallReference(), dt=.1, meshes=True)
        after = Sim(OperatingCurta(), dt=.1, meshes=True)
        for commands in ((), (('crank_rotation', 90),), (('crank_rotation', 360),),
                         (('carriage_elevation', 6), ('carriage_rotation', 40))):
            for sim in (before, after):
                for name, value in commands:
                    request = sim.move(name, to=value, duration=.5)
                    sim.run(.5)
                    self.assertEqual(request.status, 'completed')
            bank = dict(after.state)
            bank.pop('carriage.positioning.p_6mm_ball_419094.slide')
            self.assertEqual(bank, dict(before.state))
            a, b = dict(rigid_leaves(before.node)), dict(rigid_leaves(after.node))
            self.assertEqual(set(a), set(b))
            for path in a:
                # The ball's source material stays identical even as its placement changes.
                if path == BALL:
                    self.assertEqual(a[path].shape().cut(b[path].shape()).Volume(), 0)
                    self.assertEqual(b[path].shape().cut(a[path].shape()).Volume(), 0)
                else:
                    np.testing.assert_array_equal(a[path].mesh.vertices, b[path].mesh.vertices, err_msg=path)
                    np.testing.assert_array_equal(a[path].mesh.faces, b[path].mesh.faces, err_msg=path)
            a, b = dict(flexible_meshes(before.node)), dict(flexible_meshes(after.node))
            self.assertEqual(set(a), set(b))
            for path in a:
                np.testing.assert_array_equal(a[path].vertices, b[path].vertices, err_msg=path)
                np.testing.assert_array_equal(a[path].faces, b[path].faces, err_msg=path)

    def test_static_and_reversed_axis_have_actual_geometric_counterexamples(self):
        for model in (StaticBallOperatingCurta, ReversedRadialBallTrial):
            sim = Sim(model(), dt=.1, meshes=True)
            request = sim.move('crank_rotation', to=90, duration=.5)
            sim.run(.5)
            self.assertEqual(request.status, 'completed')
            native = world_solids(sim.node, selected={BALL, BELL})
            common = native[BALL].intersect(native[BELL])
            self.assertTrue(common.isValid())
            self.assertGreater(common.Volume(), 0)
            leaves = dict(rigid_leaves(sim.node))
            self.assertGreater(faceted_common_volume(
                mesh_solid(leaves[BALL].mesh) ^ mesh_solid(leaves[BELL].mesh)), 0)

    def test_endpoint_difference_law_does_not_satisfy_retention(self):
        sim = Sim(PullingBallTrial(), dt=.1)
        request = sim.move('crank_rotation', to=90, duration=.5)
        sim.run(.5)
        self.assertEqual(request.status, 'completed')
        outward = sim.state['carriage.positioning.p_6mm_ball_419094.slide']
        self.assertGreater(outward, 2.2)
        request = sim.move('crank_rotation', to=360, duration=1.5)
        sim.run(1.5)
        self.assertEqual(request.status, 'completed')
        self.assertNotEqual(sim.state['carriage.positioning.p_6mm_ball_419094.slide'], outward)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    unittest.main()
