"""Trial radial contact following must retain slack and block incompatible motion."""

import unittest

from machinome.simulation import Sim
from simulation.running import register_reading
from simulation.positioning_ball_trial import RadialBallTrial


BALL = 'carriage.positioning.p_6mm_ball_419094.slide'


class RadialPositioningBallTest(unittest.TestCase):
    def test_bell_pushes_outward_and_return_does_not_pull_the_free_ball_back(self):
        sim = Sim(RadialBallTrial(), dt=.1)
        self.assertEqual(sim.state[BALL], 0)
        command = sim.move('crank_rotation', by=90, duration=.5)
        sim.run(.5)
        self.assertEqual(command.status, 'completed')
        self.assertGreater(sim.state[BALL], 2.2)
        outward = sim.state[BALL]
        command = sim.move('crank_rotation', to=360, duration=1.5)
        sim.run(1.5)
        self.assertEqual(command.status, 'completed')
        self.assertEqual(sim.state[BALL], outward)
        self.assertEqual((register_reading(sim), register_reading(sim, True)), (0, 1))

    def test_raised_carriage_presses_the_ball_inward_and_blocks_the_crank(self):
        sim = Sim(RadialBallTrial(), dt=.1)
        command = sim.move('carriage_elevation', to=6)
        self.assertEqual(command.status, 'completed')
        self.assertLess(sim.state[BALL], -1.2)
        saved = sim.snapshot()

        def blocked_turn():
            request = sim.move('crank_rotation', to=90, duration=.5)
            sim.run(.5)
            self.assertEqual(request.status, 'blocked')
            self.assertGreater(sim.state['crank_rotation'], 0)
            self.assertLess(sim.state['crank_rotation'], 1)
            self.assertEqual(sim.state['carriage_elevation'], 6)

        blocked_turn()
        stopped = sim.snapshot()
        sim.restore(saved)
        blocked_turn()
        self.assertEqual(sim.snapshot(), stopped)
        self.assertEqual(sim.move('carriage_elevation', to=0).status, 'completed')
        command = sim.move('crank_rotation', to=90, duration=.5)
        sim.run(.5)
        self.assertEqual(command.status, 'completed')
        self.assertGreater(sim.state[BALL], 2.2)


if __name__ == '__main__':
    unittest.main()
