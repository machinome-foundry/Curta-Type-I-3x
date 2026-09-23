"""Keep the rejected orbit candidate and its whole-machine counterexample."""

import math
import unittest

import numpy as np

from machinome.simulation import Sim
from simulation.running import OperatingCurta, register_reading
from simulation.positioning_ball_trial import OrbitingBallTrial
from simulation.tools.interference import world_solids
from simulation.tools.positioning_ball_contact import BALL, BELL, DRUM
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


class OperatingPositioningBallTest(unittest.TestCase):
    def test_rejected_orbit_clears_bell_but_penetrates_the_stationary_frame(self):
        sim = Sim(OrbitingBallTrial(), dt=.1, meshes=True)
        ball = sim.node.carriage.positioning.p_6mm_ball_419094
        bell = sim.node.carry_mechanism.tens_bell.tens_bell_1
        drum = sim.node.main_drive.stepped_drum.main_axle_step_drum_1.main_axle_step_drum_top_1

        def check(angle):
            native = world_solids(sim.node, selected={BALL, BELL, DRUM})
            for name, part in ((BELL, bell), (DRUM, drum)):
                common = native[BALL].intersect(native[name])
                self.assertTrue(common.isValid(), name)
                self.assertEqual(common.Volume(), 0, name)
                self.assertEqual(faceted_common_volume(mesh_solid(ball.mesh) ^ mesh_solid(part.mesh)),
                                 0, name)
            # The ball's native spherical centre, independent of its mesh bounds
            # and the new joint declaration; source radius/height are unchanged.
            center = native[BALL].Center().toTuple()
            phase = math.radians(-angle)
            np.testing.assert_allclose(center, (9.627860318*math.cos(phase),
                                               9.627860318*math.sin(phase), 30),
                                       rtol=0, atol=1e-8)
            self.assertAlmostEqual(native[BALL].Volume(), 220.89323345553234, places=8)

        check(0)
        for angle in (90, 180, 270, 360):
            command = sim.move('crank_rotation', to=angle, duration=.5)
            sim.run(.5)
            self.assertEqual(command.status, 'completed')
            check(angle)
            if angle == 90:
                frame = sim.node.frame.upper_frame.main_body
                self.assertGreater(faceted_common_volume(mesh_solid(ball.mesh) ^ mesh_solid(frame.mesh)), 100)
        self.assertEqual(register_reading(sim), 0)
        self.assertEqual(register_reading(sim, True), 1)
        self.assertEqual(sim.move('crank_elevation', to=9).status, 'completed')
        check(360)
        saved = sim.snapshot()
        sim.move('crank_rotation', by=90, duration=.5)
        sim.run(.5)
        check(450)
        final = sim.snapshot()
        vertices = ball.mesh.vertices.copy()
        sim.restore(saved)
        sim.move('crank_rotation', by=90, duration=.5)
        sim.run(.5)
        self.assertEqual(sim.snapshot(), final)
        np.testing.assert_array_equal(ball.mesh.vertices, vertices)

    def test_default_model_has_not_adopted_the_rejected_orbit(self):
        sim = Sim(OperatingCurta(), dt=.1)
        self.assertEqual(len(sim.state), 214)
        self.assertEqual(sim.state['carriage.positioning.p_6mm_ball_419094.slide'], 0)
        self.assertNotIn('carriage.positioning.p_6mm_ball_419094.turn', sim.state)


if __name__ == '__main__':
    unittest.main()
