"""Apply the unchanged production-facing operation contract to the trial."""

import unittest
import numpy as np
from machinome.simulation import Sim
from simulation.test_operating_loop import OperatingLoopTest as _Contract
from simulation.clearing_loop_operating_trial import LoopOperatingTrial
from simulation.running import OperatingCurta, ReverserOperatingCurta
from simulation.tools.interference import rigid_leaves
from simulation.tools.operating_loop_contacts import PARTS
from simulation.test_carry_bank_trial import flexible_meshes
from simulation.test_running import RunningCurtaTest as _ArithmeticContract
from simulation.test_running_interlocks import (
    RunningCarriageIndexTest as _IndexContract,
    RunningClearingInterlockTest as _ClearingContract,
)


class LoopOperatingTrialTest(_Contract):
    model = LoopOperatingTrial


class LoopArithmeticTest(_ArithmeticContract):
    model = LoopOperatingTrial


class LoopIndexTest(_IndexContract):
    model = LoopOperatingTrial


class LoopClearingTest(_ClearingContract):
    model = LoopOperatingTrial


class LoopPreservationTest(unittest.TestCase):
    model = OperatingCurta

    def test_only_the_three_named_occurrences_and_two_new_coordinates_change(self):
        before = Sim(ReverserOperatingCurta(), dt=.1, meshes=True)
        after = Sim(self.model(), dt=.1, meshes=True)
        self.assertEqual(set(after.state)-set(before.state), {
            'loop_deployment', 'carriage.registers.clearing_ring.clearing_ring.swivel'})
        self.assertEqual(len(before.state), 214)
        self.assertEqual(len(after.state), 216)
        self.assertEqual(set(after.node.controls)-set(before.node.controls), {
            'deploy loop (simulation-only mounting)'})
        for request in (None, ('crank_rotation', 90), ('crank_rotation', 360),
                        ('carriage_elevation', 6), ('carriage_rotation', 40),
                        ('clearing_rotation', 230), ('carriage_elevation', 0)):
            if request:
                for sim in (before, after):
                    command = sim.move(request[0], to=request[1], duration=.2)
                    sim.run(.2)
                    self.assertEqual(command.status, 'completed', request)
            self.assertEqual(dict(before.state), {
                key: after.state[key] for key in before.state})
            old, new = dict(rigid_leaves(before.node)), dict(rigid_leaves(after.node))
            self.assertEqual(set(old), set(new))
            self.assertEqual(len(new), 389)
            for path in old.keys()-set(PARTS):
                np.testing.assert_array_equal(old[path].mesh.vertices,
                                              new[path].mesh.vertices, err_msg=path)
                np.testing.assert_array_equal(old[path].mesh.faces,
                                              new[path].mesh.faces, err_msg=path)
            old_flex, new_flex = dict(flexible_meshes(before.node)), dict(flexible_meshes(after.node))
            self.assertEqual(set(old_flex), set(new_flex))
            for path in old_flex:
                np.testing.assert_array_equal(old_flex[path].vertices,
                                              new_flex[path].vertices, err_msg=path)
                np.testing.assert_array_equal(old_flex[path].faces,
                                              new_flex[path].faces, err_msg=path)
