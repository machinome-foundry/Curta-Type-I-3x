"""A withdrawn, partly driven counter-tens input must hold the actual crank.

The production case stays red until the independently verified trial is
adopted. This is one raised-stack action order, not complete counter coverage.
"""

import unittest

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.higher_counter_wrong_order import (
    PARTIAL_INPUT_REQUESTS, SHAFT, UPPER, BELL, pair_contacts)
from simulation.tools.interference import world_solids, rigid_leaves
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


class OperatingCounterTensLockoutTest(unittest.TestCase):
    model = OperatingCurta

    def test_partial_input_withdrawal_stops_before_complete_print_contact(self):
        sim = Sim(self.model(), dt=.1, meshes=True, record=64)
        for name, value in PARTIAL_INPUT_REQUESTS[:-1]:
            self.assertEqual(sim.move(name, to=value).status, 'completed', (name, value))
        self.assertAlmostEqual(sim.state[SHAFT], 147.6, places=8)
        self.assertEqual(pair_contacts(sim), {'native': 0, 'faceted': 0})
        prepared = sim.snapshot()
        for target in (200, 920):
            sim.restore(prepared)
            self.assertEqual(sim.move('crank_rotation', to=target).status, 'blocked')
            angle = sim.state['crank_rotation']
            self.assertGreater(angle, 190)
            self.assertLess(angle, 200)
            self.assertAlmostEqual(sim.state[SHAFT], 147.6, places=8)
            self.assertEqual(pair_contacts(sim), {'native': 0, 'faceted': 0})
            shapes = world_solids(sim.node, selected={UPPER, BELL})
            leaves = dict(rigid_leaves(sim.node))
            common = shapes[UPPER].intersect(shapes[BELL].rotate(
                (0, 0, 0), (0, 0, 1), -.2))
            self.assertTrue(common.isValid())
            self.assertGreater(common.Volume(), 0)
            self.assertGreater(faceted_common_volume(
                mesh_solid(leaves[UPPER].mesh)
                ^ mesh_solid(leaves[BELL].mesh).rotate((0, 0, -.2))), 0)
            stopped = sim.snapshot()
            sim.restore(prepared)
            self.assertEqual(sim.move('crank_rotation', to=target).status, 'blocked')
            self.assertEqual(sim.snapshot(), stopped)
            self.assertEqual(sim.move('crank_rotation', by=-.05).status, 'completed')
            self.assertAlmostEqual(sim.state['crank_rotation'], angle-.05, places=7)
            self.assertEqual(sim.move('crank_rotation', to=target).status, 'blocked')
            self.assertAlmostEqual(sim.state['crank_rotation'], angle, places=7)
            print(f'PASS counter tens withdrawal: target={target}, stop={angle}', flush=True)


if __name__ == '__main__':
    unittest.main()
