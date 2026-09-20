"""The compiled follower must use the same positive phase as the CAD pose."""

import unittest
from machinome.simulation import Sim
from simulation.clearing_stop_motion import following
from simulation.tools.clearing_rest import Bench


class ClearingFollowerRunningTest(unittest.TestCase):
    def test_repeated_positive_and_negative_sweeps_match_the_pose_profile(self):
        sim = Sim(Bench(), dt=.1)
        sim.move('elevation', to=6)
        for sweep in (0, -1, -5, -90, -230, -360, -450, -720,
                      0, 90, 230, 360, 450, 720, 0):
            sim.move('sweep', to=sweep)
            self.assertAlmostEqual(sim.state['carrier.pin.slide'],
                                   following(None, None)(-sweep), places=6)

    def test_each_period_and_each_rest_blocks_both_directions(self):
        sim = Sim(Bench(), dt=.1)
        for base in (-720, -360, 0, 360, 720):
            for rest in (base, base + 230):
                for direction in (-1, 1):
                    sim.move('elevation', to=6)
                    sim.move('sweep', to=rest)
                    sim.move('elevation', to=0)
                    command = sim.move('sweep', to=rest + direction * 90)
                    self.assertEqual(command.status, 'blocked', (rest, direction))
                    self.assertEqual(sim.state['carrier.lift'], 0)
                    self.assertAlmostEqual(sim.state['carrier.pin.slide'], 3.09, places=6)
