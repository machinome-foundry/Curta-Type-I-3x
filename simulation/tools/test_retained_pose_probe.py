"""Framework-only reduction of the Curta's retained bank/pose disagreement."""

import unittest
from machinome.simulation import Sim
from simulation.tools.retained_pose_probe import NestedPoseProbe


class RetainedPoseBindingTest(unittest.TestCase):
    def test_parent_motion_preserves_independent_child_coordinates(self):
        node = NestedPoseProbe()
        sim = Sim(node, dt=.1)
        sim.move('rotation', to=20)
        self.assertEqual(sim.state['carrier.ring.turn'], 0)
        self.assertEqual(sim.state['carrier.ring.wheel.turn'], -146)
        self.assertEqual(node.carrier.ring.turn.value, 0)
        self.assertEqual(node.carrier.ring.wheel.turn.value, -146)

    def test_child_motion_is_bound_to_its_own_retained_pose(self):
        node = NestedPoseProbe()
        sim = Sim(node, dt=.1)
        sim.move('clearing', to=90)
        self.assertEqual(sim.state['carrier.turn'], 0)
        self.assertEqual(sim.state['carrier.ring.turn'], -90)
        self.assertEqual(node.carrier.ring.turn.value, -90)


if __name__ == '__main__':
    unittest.main()
