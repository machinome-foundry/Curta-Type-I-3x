"""Retained-root acceptance using committed model data, not diagnostic files."""

import unittest

from machinome.simulation import Sim
from simulation import test_reverser_contact_trial as contact_contracts
from simulation import test_running_reverser_contact_path as path_contracts
from simulation.reverser_compiled_trial import CompiledReverserTrial


class CompiledReverserTrialTest(contact_contracts.LocalReverserContactTrialTest):
    model = CompiledReverserTrial


class CompiledReverserPathTest(path_contracts.ReverserContactPathTest):
    model = CompiledReverserTrial


class CompiledReverserStrokeTest(unittest.TestCase):
    def test_all_four_prepared_modes_complete_a_full_crank_stroke(self):
        for lever, lift in ((-4.9425, 0), (3.9075, 9), (3.9075, 0), (-4.9425, 9)):
            with self.subTest(lever=lever, lift=lift):
                sim = Sim(CompiledReverserTrial(), dt=.1, meshes=False)
                self.assertEqual(sim.move('reverser_height', to=lever).status, 'completed')
                self.assertEqual(sim.move('crank_elevation', to=lift).status, 'completed')
                request = sim.move('crank_rotation', to=360, duration=2)
                sim.run(2)
                self.assertEqual(request.status, 'completed')
                self.assertEqual(sim.state['crank_rotation'], 360)
