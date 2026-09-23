"""Whole-root identity and retained arithmetic with the isolated frame fit."""

import logging
import unittest

import numpy as np

from machinome.simulation import Sim
from simulation.carry_bank_trial import CarryBankOperatingTrial, FirstPairOperatingReference
from simulation.carry_bank_regions import forbidden_removal
from simulation.test_operating_demonstrations import OperatingDemonstrationReplayTest
from simulation.tools.interference import rigid_leaves


def flexible_meshes(root, path='Curta'):
    for child in root.children:
        name = path+'.'+child.name
        if child.children:
            yield from flexible_meshes(child, name)
        elif not child.rigid and getattr(child, 'mesh', None) is not None:
            yield name, child.mesh


class CarryBankOperatingIdentityTest(unittest.TestCase):
    def test_every_other_mesh_and_original_bank_match_at_rest_and_half_turn(self):
        before = Sim(FirstPairOperatingReference(), dt=.1, meshes=True)
        after = Sim(CarryBankOperatingTrial(), dt=.1, meshes=True)
        for angle in (0, 180):
            if angle:
                for sim in (before, after):
                    command = sim.move('crank_rotation', to=angle, duration=1)
                    sim.run(1)
                    self.assertEqual(command.status, 'completed')
            self.assertEqual(dict(before.state), dict(after.state))
            # Comparing the complete banks above forbids any coordinate
            # change by the frame fit, without pinning unrelated future joints.
            self.assertGreaterEqual(len(after.state), 213)
            a, b = dict(rigid_leaves(before.node)), dict(rigid_leaves(after.node))
            self.assertEqual(set(a), set(b))
            unchanged = 0
            for path in a:
                if path == 'Curta.frame.upper_frame.main_body':
                    old, new = a[path].shape(), b[path].shape()
                    self.assertEqual(new.cut(old).Volume(), 0)
                    self.assertEqual(forbidden_removal(old, new).Volume(), 0)
                    self.assertGreater(old.cut(new).Volume(), 0)
                    continue
                np.testing.assert_array_equal(a[path].mesh.vertices, b[path].mesh.vertices, err_msg=path)
                np.testing.assert_array_equal(a[path].mesh.faces, b[path].mesh.faces, err_msg=path)
                unchanged += 1
            self.assertGreater(unchanged, 380)
            flex_a, flex_b = dict(flexible_meshes(before.node)), dict(flexible_meshes(after.node))
            self.assertEqual(set(flex_a), set(flex_b))
            self.assertGreater(len(flex_a), 30)
            for path in flex_a:
                np.testing.assert_array_equal(flex_a[path].vertices, flex_b[path].vertices, err_msg=path)
                np.testing.assert_array_equal(flex_a[path].faces, flex_b[path].faces, err_msg=path)


class CarryBankOperatingReplayTest(OperatingDemonstrationReplayTest):
    model = CarryBankOperatingTrial


if __name__ == '__main__':
    logging.disable(logging.INFO)
    unittest.main()
