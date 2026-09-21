"""The actual crank must stop when a withdrawn counter input leaves a flank."""

import unittest

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.counter_wrong_order import prepare_partial_turn, SHAFT, UPPER, BELL
from simulation.tools.interference import world_solids, rigid_leaves
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


class OperatingCounterLockoutTest(unittest.TestCase):
    def test_withdrawn_counter_stops_short_and_long_crank_requests(self):
        sim = Sim(OperatingCurta(), dt=.1, meshes=True, record=16)
        prepare_partial_turn(sim)
        self.assertAlmostEqual(sim.state[SHAFT], 167.6, places=9)
        self.assertEqual(sim.move('reverser_height', to=-6.9425).status, 'completed')
        self.assertAlmostEqual(sim.state[SHAFT], 167.6, places=9)
        prepared = sim.snapshot()
        for target in (180, 900):
            sim.restore(prepared)
            request = sim.move('crank_rotation', to=target)
            # Intentionally fails on the installed model until adoption.
            self.assertEqual(request.status, 'blocked')
            stop_angle = sim.state['crank_rotation']
            self.assertGreater(stop_angle, 170)
            self.assertLess(stop_angle, 175)
            self.assertAlmostEqual(sim.state['main_drive.crank.turn'], -stop_angle, places=9)
            self.assertAlmostEqual(sim.state[SHAFT], 167.6, places=9)
            self.assertTrue(any(stop.coordinate == 'main_drive.crank.turn'
                                and stop.bound == 'low' for stop in sim.stops))
            stopped = sim.snapshot()
            shapes = world_solids(sim.node, selected={UPPER, BELL})
            leaves = dict(rigid_leaves(sim.node))
            meshes = {path: mesh_solid(leaves[path].mesh) for path in (UPPER, BELL)}
            for overtravel in (0, .2):
                common = shapes[UPPER].intersect(shapes[BELL].rotate(
                    (0, 0, 0), (0, 0, 1), -overtravel))
                self.assertTrue(common.isValid())
                volumes = (common.Volume(), faceted_common_volume(
                    meshes[UPPER] ^ meshes[BELL].rotate((0, 0, -overtravel))))
                for volume in volumes:
                    if overtravel:
                        self.assertGreater(volume, 0)
                    else:
                        self.assertLessEqual(volume, 0)
            sim.restore(prepared)
            self.assertEqual(sim.move('crank_rotation', to=target).status, 'blocked')
            self.assertEqual(sim.snapshot(), stopped)
            self.assertEqual(sim.move('crank_rotation', by=-.05).status, 'completed')
            self.assertEqual(sim.move('crank_rotation', to=target).status, 'blocked')
            print(f'PASS counter withdrawal: target={target}, stop={stop_angle}', flush=True)


if __name__ == '__main__':
    unittest.main()
