"""Actual operating crank/shaft evidence for ancestor-joint-constraints."""

import unittest
import manifold3d as manifold

from machinome.simulation import Sim
from simulation.ancestor_lockout import AncestorLockoutCurta, LAST_FREE
from simulation.tools.ancestor_lockout_contact import (
    prepare, SHAFT, BELL, LOCKOUT, contact_shapes, mesh_solid)
from simulation.tools.interference import rigid_leaves


class AncestorLockoutTest(unittest.TestCase):
    def test_wrong_order_request_stops_the_actual_crank(self):
        # OperatingCurta now contributes the independently measured five-flat
        # restraint. Its .1-degree stand-off is stricter than the historical
        # local diagnostic, so both must intersect rather than replace it.
        expected_stop = 125.22323837227304
        self.assertLess(expected_stop, LAST_FREE)
        sim = Sim(AncestorLockoutCurta(), dt=.1, meshes=True, record=8)
        prepare(sim)
        prepared = sim.snapshot()
        request = sim.move('crank_rotation', to=150)
        self.assertEqual(request.status, 'blocked')
        self.assertAlmostEqual(sim.state['crank_rotation'], expected_stop, places=7)
        self.assertAlmostEqual(sim.state['main_drive.crank.turn'], -expected_stop, places=7)
        self.assertAlmostEqual(sim.state[SHAFT], 189.6, places=10)
        self.assertTrue(any(stop.coordinate == 'main_drive.crank.turn'
                            for stop in sim.stops))
        stopped = sim.snapshot()
        bell, lockout = contact_shapes(sim.node)
        common = bell.intersect(lockout)
        self.assertTrue(common.isValid())
        self.assertEqual(common.Volume(), 0)
        leaves = dict(rigid_leaves(sim.node))
        common_mesh = mesh_solid(leaves[BELL].mesh) ^ mesh_solid(leaves[LOCKOUT].mesh)
        self.assertEqual(common_mesh.status(), manifold.Error.NoError)
        self.assertLessEqual(common_mesh.volume(), 0)

        sim.restore(prepared)
        sim.move('crank_rotation', to=150)
        self.assertEqual(sim.snapshot(), stopped)
        relief = sim.move('crank_rotation', to=expected_stop-.05)
        self.assertEqual(relief.status, 'completed')
        self.assertAlmostEqual(sim.state[SHAFT], 189.6, places=10)
        sim.run(.1)
        self.assertAlmostEqual(sim.state['crank_rotation'], expected_stop-.05, places=7)
        self.assertEqual(sim.move('crank_rotation', to=150).status, 'blocked')
        self.assertAlmostEqual(sim.state['crank_rotation'], expected_stop, places=7)
