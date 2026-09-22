"""A withdrawn, partly driven counter-tens input must hold the actual crank.

The production case stays red until the independently verified trial is
adopted. This is one raised-stack action order, not complete counter coverage.
"""

import unittest
import json
import os
from pathlib import Path

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.higher_counter_wrong_order import (
    PARTIAL_INPUT_REQUESTS, BELL)
from simulation.tools.interference import world_solids, rigid_leaves
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


class OperatingCounterTensLockoutTest(unittest.TestCase):
    model = OperatingCurta
    station = 2

    @classmethod
    def setUpClass(cls):
        cls.acceptance = []

    @classmethod
    def tearDownClass(cls):
        output = os.environ.get('CURTA_COUNTER_TENS_ACCEPTANCE_REPORT')
        if output:
            Path(output).write_text(json.dumps(cls.acceptance, indent=2)+'\n')

    def test_partial_input_withdrawal_stops_before_complete_print_contact(self):
        from simulation.running_parts import CHANNEL_NAMES
        from simulation.tools.counter_lockout_probe import STATIONS
        shift = 20*(self.station-2)
        channel = CHANNEL_NAMES[self.station-1]
        shaft = f'transmission.turns.{channel}.turn'
        upper = f'Curta.transmission.turns.{channel}.{STATIONS[self.station-1][1]}'
        shaft_angle = 147.6-shift

        def contacts():
            shapes = world_solids(sim.node, selected={upper, BELL})
            leaves = dict(rigid_leaves(sim.node))
            common = shapes[upper].intersect(shapes[BELL])
            self.assertTrue(common.isValid())
            return {'native': common.Volume(), 'faceted': faceted_common_volume(
                mesh_solid(leaves[upper].mesh, world_precision=64)
                ^ mesh_solid(leaves[BELL].mesh, world_precision=64))}

        sim = Sim(self.model(), dt=.1, meshes=True, record=64)
        for name, value in PARTIAL_INPUT_REQUESTS[:-1]:
            if name == 'crank_rotation':
                value += shift
            self.assertEqual(sim.move(name, to=value).status, 'completed', (name, value))
        self.assertAlmostEqual(sim.state[shaft], shaft_angle, places=8)
        self.assertEqual(contacts(), {'native': 0, 'faceted': 0})
        prepared = sim.snapshot()
        for target in (200+shift, 920+shift):
            sim.restore(prepared)
            request = sim.move('crank_rotation', to=target)
            endpoint_contacts = contacts()
            self.assertEqual(request.status, 'blocked', (target, endpoint_contacts))
            angle = sim.state['crank_rotation']
            self.assertGreater(angle, 190+shift)
            self.assertLess(angle, 200+shift)
            self.assertAlmostEqual(sim.state[shaft], shaft_angle, places=8)
            self.assertEqual(endpoint_contacts, {'native': 0, 'faceted': 0})
            shapes = world_solids(sim.node, selected={upper, BELL})
            leaves = dict(rigid_leaves(sim.node))
            common = shapes[upper].intersect(shapes[BELL].rotate(
                (0, 0, 0), (0, 0, 1), -.2))
            self.assertTrue(common.isValid())
            self.assertGreater(common.Volume(), 0)
            self.assertGreater(faceted_common_volume(
                mesh_solid(leaves[upper].mesh, world_precision=64)
                ^ mesh_solid(leaves[BELL].mesh, world_precision=64).rotate((0, 0, -.2))), 0)
            stopped = sim.snapshot()
            stopped_state = dict(sim.state)
            sim.restore(prepared)
            self.assertEqual(sim.move('crank_rotation', to=target).status, 'blocked')
            self.assertEqual(sim.snapshot(), stopped)
            self.assertEqual(sim.move('crank_rotation', by=-.05).status, 'completed')
            sim.run(.1)
            self.assertAlmostEqual(sim.state['crank_rotation'], angle-.05, places=7)
            idle_state = dict(sim.state)
            self.assertEqual(sim.move('crank_rotation', to=target).status, 'blocked')
            self.assertAlmostEqual(sim.state['crank_rotation'], angle, places=7)
            self.acceptance.append({'station': self.station, 'target': target, 'stopped': stopped_state,
                                    'idle': idle_state, 'replay': True})
            print(f'PASS counter {self.station} withdrawal: target={target}, stop={angle}', flush=True)


if __name__ == '__main__':
    unittest.main()
