"""A valid free crank request must survive observing its actual carry stack.

The constrained case is deliberately red on framework e63700e. Catching the
engine error as success or splitting this request would hide the regression.
"""

import unittest

from machinome.simulation import Sim
from simulation.carry_constraint_repro import CarryConstraintRepro, ConstrainedCarryRepro


class CarryConstraintReproTest(unittest.TestCase):
    def check_turn(self, node_type):
        sim = Sim(node_type(), dt=.1)
        self.assertEqual(sim.move('crank_angle', to=360).status, 'completed')
        self.assertEqual(sim.state['crank_angle'], 360)
        self.assertAlmostEqual(sim.state['ones.turn'], 652, places=8)
        self.assertAlmostEqual(sim.state['wheel_0.turn'], -470, places=8)
        self.assertAlmostEqual(sim.state['tens.turn'], -16, places=8)

    def test_source_carry_laws_complete_without_the_observer(self):
        self.check_turn(CarryConstraintRepro)

    def test_free_constraint_observation_preserves_the_same_request(self):
        self.check_turn(ConstrainedCarryRepro)


if __name__ == '__main__':
    unittest.main()
