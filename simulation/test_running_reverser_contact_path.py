"""An endpoint-clear reversed-counter stroke must also clear its path."""

import unittest

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.test_running_reverser_wrong_order import commons


class ReverserContactPathTest(unittest.TestCase):
    model = OperatingCurta

    def test_reversed_counter_passage_clears_both_geometry_representations(self):
        sim = Sim(self.model(), dt=.1, meshes=True)
        self.assertEqual(sim.move('reverser_height', to=-4.9425).status, 'completed')
        request = sim.move('crank_rotation', to=82.43237719286117, duration=.5)
        sim.run(.5)
        self.assertEqual(request.status, 'completed')
        self.assertAlmostEqual(sim.state['transmission.turns.ones.turn'], 183.16721403431148)
        for kernel, volume in zip(('native', 'world64'), commons(sim)):
            with self.subTest(kernel=kernel):
                self.assertEqual(volume, 0)


if __name__ == '__main__':
    unittest.main()
