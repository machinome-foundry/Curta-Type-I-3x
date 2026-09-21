"""Challenge the complete result carry graph with the unchanged bulk request.

These CAD-free cases are diagnostic regressions, not whole-machine acceptance.
They preserve all result shafts/dials/levers but omit the independent counter,
pawl, enclosure and other physical interfaces.
"""

import unittest

from machinome.simulation import Sim
from simulation.result_carry_graph_repro import (
    ResultCarryGraphRepro, ConstrainedResultCarryGraphRepro)


class ResultCarryGraphReproTest(unittest.TestCase):
    def check_preparation(self, model):
        sim = Sim(model(), dt=.1, record=64)
        for name, value in (('digit', 0), ('height', 9), ('crank_angle', 90)):
            self.assertEqual(sim.move(name, to=value).status, 'completed', (name, value))
        self.assertAlmostEqual(sim.state['ones.turn'], 501.6, places=8)
        self.assertAlmostEqual(sim.state['tens.turn'], 281.6, places=8)
        self.assertAlmostEqual(sim.state['lever.travel'], -4.2, places=8)
        command = sim.move('crank_angle', to=180)
        self.assertEqual(command.status, 'completed', dict(sim.state))
        self.assertEqual(sim.state['crank_angle'], 180)
        self.assertAlmostEqual(sim.state['ones.turn'], 724, places=8)
        self.assertAlmostEqual(sim.state['tens.turn'], 704, places=8, msg=dict(sim.state))
        self.assertAlmostEqual(sim.state['lever.travel'], 0, places=8)

    def test_full_result_graph_without_contact_observation(self):
        self.check_preparation(ResultCarryGraphRepro)

    def test_full_result_graph_with_ones_and_tens_contact_observation(self):
        self.check_preparation(ConstrainedResultCarryGraphRepro)


if __name__ == '__main__':
    unittest.main()
