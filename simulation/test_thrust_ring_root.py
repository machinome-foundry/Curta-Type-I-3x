"""Compare the static-ball production candidate without silently adopting Follow."""

import unittest

import numpy as np
from machinome.simulation import Sim
from simulation.thrust_ring_trial import (FittedRingOperatingTrial, OriginalRingOperatingReference,
                                         OriginalRingRadialOperatingReference)
from simulation.thrust_ring_regions import permitted_local
from simulation.test_carry_bank_trial import flexible_meshes
from simulation.tools.interference import rigid_leaves
from simulation.tools.positioning_ball_ring import RING
from simulation.running import OperatingCurta


class ThrustRingRootTest(unittest.TestCase):
    model = FittedRingOperatingTrial
    before_model = OriginalRingOperatingReference
    coordinates = 213

    def test_all_other_meshes_and_complete_bank_are_unchanged(self):
        before = Sim(self.before_model(), dt=.1, meshes=True)
        after = Sim(self.model(), dt=.1, meshes=True)
        stages = ((), (('crank_rotation', 180),),
                  (('crank_rotation', 360), ('carriage_elevation', 6), ('carriage_rotation', 40)))
        for commands in stages:
            for sim in (before, after):
                for name, value in commands:
                    request = sim.move(name, to=value, duration=.5)
                    sim.run(.5)
                    self.assertEqual(request.status, 'completed')
            self.assertEqual(dict(before.state), dict(after.state))
            self.assertEqual(len(after.state), self.coordinates)
            a, b = dict(rigid_leaves(before.node)), dict(rigid_leaves(after.node))
            self.assertEqual(set(a), set(b))
            for path in a:
                if path == RING:
                    old, new = a[path].shape(), b[path].shape()
                    self.assertTrue(old.isValid() and new.isValid())
                    self.assertEqual(new.cut(old).Volume(), 0)
                    self.assertGreater(old.cut(new).Volume(), 0)
                    self.assertEqual(old.cut(new).cut(permitted_local()).Volume(), 0)
                else:
                    np.testing.assert_array_equal(a[path].mesh.vertices, b[path].mesh.vertices, err_msg=path)
                    np.testing.assert_array_equal(a[path].mesh.faces, b[path].mesh.faces, err_msg=path)
            a, b = dict(flexible_meshes(before.node)), dict(flexible_meshes(after.node))
            self.assertEqual(set(a), set(b))
            for path in a:
                np.testing.assert_array_equal(a[path].vertices, b[path].vertices, err_msg=path)
                np.testing.assert_array_equal(a[path].faces, b[path].faces, err_msg=path)


class ThrustRingProductionRootTest(ThrustRingRootTest):
    model = OperatingCurta
    before_model = OriginalRingRadialOperatingReference
    coordinates = 216


if __name__ == '__main__':
    import logging
    logging.disable(logging.INFO)
    unittest.main()
