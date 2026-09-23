"""Installed source fork/sleeve capture must survive the fixed-frame change."""

import logging
import unittest

import numpy as np

from machinome.simulation import Sim
from simulation.carry_bank_trial import CarryBankOperatingTrial
from simulation.running_parts import CHANNEL_NAMES
from simulation.result_bank_lockout_parts import RESULT_CONTACT_STATIONS
from simulation.counter_bank_lockout_parts import COUNTER_CONTACT_STATIONS
from simulation.tools.interference import world_solids, rigid_leaves
from simulation.tools.moving_seats import world_frames
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


class CarryBankForkCaptureTest(unittest.TestCase):
    def test_every_installed_fork_retains_its_coupled_sleeve(self):
        sim = Sim(CarryBankOperatingTrial(), dt=.1, meshes=True)
        saved = dict(sim.state)
        mappings = []
        for counter, uppers in ((False, ['p_10220_410003_1_419227']+
                                 [name for _, name in RESULT_CONTACT_STATIONS]),
                                (True, [name for _, name in COUNTER_CONTACT_STATIONS])):
            for index, upper in enumerate(uppers, 1):
                bank = 'turns' if counter else 'result'
                group = 'turns' if counter else 'results'
                suffix = 'tens_slider_for_turns_counter' if counter else 'tens_slider_for_results'
                slider = f'Curta.carry_mechanism.{bank}_carries.{group}_tens_lever_assembly_{index}.{suffix}'
                sleeve = f'Curta.transmission.{bank}.{CHANNEL_NAMES[index]}.{upper}'
                mappings.append((slider, sleeve))
        self.assertEqual(len(mappings), 15)
        shapes = world_solids(sim.node, selected={name for pair in mappings for name in pair})
        leaves = dict(rigid_leaves(sim.node))
        frames = world_frames(sim.node)
        for slider, sleeve in mappings:
            direction = frames[slider][:3, :3] @ np.array((1, 0, 0))
            fixed = mesh_solid(leaves[sleeve].mesh)
            for amount in (-.2, -.01, .01, .2):
                displacement = direction*amount
                common = shapes[slider].translate(tuple(displacement)).intersect(shapes[sleeve])
                self.assertTrue(common.isValid(), (slider, amount))
                moving = leaves[slider].mesh.copy()
                moving.apply_translation(displacement)
                faceted = faceted_common_volume(mesh_solid(moving) ^ fixed)
                for kernel, volume in (('native', common.Volume()), ('world64', faceted)):
                    with self.subTest(slider=slider, amount=amount, kernel=kernel):
                        if abs(amount) == .01:
                            self.assertEqual(volume, 0)
                        else:
                            self.assertGreater(volume, 0)
        self.assertEqual(dict(sim.state), saved)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    unittest.main()
