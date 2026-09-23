"""The radial trial must clear its actual seated production thrust ring."""

import logging
import unittest

from machinome.simulation import Sim
from simulation.positioning_ball_trial import RadialBallTrial
from simulation.tools.positioning_ball_contact import BALL
from simulation.tools.positioning_ball_ring import RING
from simulation.tools.interference import world_solids
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


class FollowBallRingTest(unittest.TestCase):
    model = RadialBallTrial

    def test_actual_outward_following_clears_the_seated_ring(self):
        sim = Sim(self.model(), dt=.1, meshes=True)
        command = sim.move('crank_rotation', to=90, duration=.5)
        sim.run(.5)
        self.assertEqual(command.status, 'completed')
        native = world_solids(sim.node, selected={BALL, RING})
        common = native[BALL].intersect(native[RING])
        self.assertTrue(common.isValid())
        with self.subTest(kernel='native'):
            self.assertEqual(common.Volume(), 0)
        with self.subTest(kernel='world64'):
            positioning = sim.node.carriage.positioning
            common = (mesh_solid(positioning.p_6mm_ball_419094.mesh) ^
                      mesh_solid(positioning.thrust_ring.mesh))
            self.assertEqual(faceted_common_volume(common), 0)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    unittest.main()
