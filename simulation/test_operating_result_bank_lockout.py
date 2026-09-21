"""Higher result inputs must not leave an unrestrained partial shaft behind."""

import json
import os
from pathlib import Path
import unittest

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.running_parts import CHANNEL_NAMES
from simulation.tools.result_bank_lockout_probe import STATIONS
from simulation.tools.interference import world_solids, rigid_leaves
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


BELL = 'Curta.carry_mechanism.tens_bell.tens_bell_1'


class OperatingResultBankLockoutTest(unittest.TestCase):
    model = OperatingCurta

    @classmethod
    def setUpClass(cls):
        cls.acceptance = []

    @classmethod
    def tearDownClass(cls):
        output = os.environ.get('CURTA_RESULT_ACCEPTANCE_REPORT')
        if output:
            Path(output).write_text(json.dumps(cls.acceptance, indent=2)+'\n')

    def check_withdrawal(self, station):
        shift = 20*(station-2)
        channel = CHANNEL_NAMES[station-1]
        shaft = f'transmission.result.{channel}.turn'
        upper = f'Curta.transmission.result.{channel}.{STATIONS[station-2][1]}'
        sim = Sim(self.model(), dt=.1, meshes=True)
        for name, value in ((f'digit_{station}', 3),
                            ('crank_rotation', 140+shift), (f'digit_{station}', 0)):
            self.assertEqual(sim.move(name, to=value).status, 'completed', (name, value))
        self.assertAlmostEqual(sim.state[shaft], 169.6-shift, places=7)

        def volumes(overtravel=0):
            native = world_solids(sim.node, selected={upper, BELL})
            leaves = dict(rigid_leaves(sim.node))
            common = native[upper].intersect(native[BELL].rotate(
                (0, 0, 0), (0, 0, 1), -overtravel))
            self.assertTrue(common.isValid())
            faceted = (mesh_solid(leaves[upper].mesh)
                       ^ mesh_solid(leaves[BELL].mesh).rotate((0, 0, -overtravel)))
            return {'native': common.Volume(), 'faceted': faceted_common_volume(faceted)}

        for kernel, volume in volumes().items():
            self.assertLessEqual(volume, 0, ('prepared', station, kernel))
        prepared = sim.snapshot()
        first_angle = None
        for target in (170+shift, 860+shift):
            sim.restore(prepared)
            command = sim.move('crank_rotation', to=target)
            actual = volumes()
            print(json.dumps({'station': station, 'target': target,
                              'status': command.status, 'crank': sim.state['crank_rotation'],
                              'common_mm3': actual}), flush=True)
            self.assertEqual(command.status, 'blocked')
            angle = sim.state['crank_rotation']
            self.assertGreater(angle, 140+shift)
            self.assertLess(angle, 146+shift)
            self.assertAlmostEqual(sim.state[shaft], 169.6-shift, places=7)
            for kernel, volume in actual.items():
                self.assertLessEqual(volume, 0, ('stop', station, kernel))
            for kernel, volume in volumes(.2).items():
                self.assertGreater(volume, 0, ('overtravel', station, kernel))
            if first_angle is not None:
                self.assertAlmostEqual(angle, first_angle, places=7)
            first_angle = angle
            stopped = sim.snapshot()
            stopped_state = dict(sim.state)
            sim.restore(prepared)
            self.assertEqual(sim.move('crank_rotation', to=target).status, 'blocked')
            self.assertEqual(sim.snapshot(), stopped)
            self.assertEqual(sim.move('crank_rotation', by=-.05).status, 'completed')
            relieved_state = dict(sim.state)
            self.assertEqual(sim.move('crank_rotation', to=target).status, 'blocked')
            self.assertAlmostEqual(sim.state['crank_rotation'], angle, places=7)
            self.acceptance.append({'station': station, 'target': target,
                                    'stopped': stopped_state, 'relieved': relieved_state,
                                    'replay': True})

    def test_hundreds_withdrawal_stops_short_and_long_requests(self):
        self.check_withdrawal(3)

    def test_eighth_input_withdrawal_stops_short_and_long_requests(self):
        self.check_withdrawal(8)


if __name__ == '__main__':
    unittest.main()
