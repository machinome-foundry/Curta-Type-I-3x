"""The actual operating crank must meet the measured ones locking flank."""

import unittest
import manifold3d as manifold

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.ancestor_lockout_contact import (
    prepare, SHAFT, BELL, LOCKOUT, contact_shapes, mesh_solid)
from simulation.tools.interference import rigid_leaves


class RunningLockoutTest(unittest.TestCase):
    def test_short_and_long_requests_stop_the_operating_crank(self):
        sim = Sim(OperatingCurta(), dt=.1, meshes=True, record=8)
        prepare(sim)
        saved = sim.snapshot()
        for target in (150, 840):
            with self.subTest(target=target):
                sim.restore(saved)
                request = sim.move('crank_rotation', to=target)
                self.assertEqual(request.status, 'blocked')
                self.assertAlmostEqual(sim.state['crank_rotation'], 125.22323837227304, places=7)
                self.assertAlmostEqual(sim.state['main_drive.crank.turn'], -125.22323837227304, places=7)
                self.assertAlmostEqual(sim.state[SHAFT], 189.6, places=9)
                self.assertTrue(any(stop.coordinate == 'main_drive.crank.turn'
                                    for stop in sim.stops))
                print(f'PASS actual operating crank: target={target}, '
                      f'stop={sim.state["crank_rotation"]}', flush=True)
                stopped = sim.snapshot()
                sim.restore(saved)
                self.assertEqual(sim.move('crank_rotation', to=target).status, 'blocked')
                self.assertEqual(sim.snapshot(), stopped)
                self.assertEqual(sim.move('crank_rotation', by=-.05).status, 'completed')
                sim.run(.1)
                self.assertAlmostEqual(sim.state['crank_rotation'],
                                       125.22323837227304-.05, places=7)
                self.assertEqual(sim.move('crank_rotation', to=target).status, 'blocked')

        # Judge the installed complete solids and the exact published meshes.
        # A posed .2-degree overtravel is a negative geometry control, not an
        # admitted command or an override of the running bank.
        bell, lockout = contact_shapes(sim.node)
        leaves = dict(rigid_leaves(sim.node))
        bell_mesh = mesh_solid(leaves[BELL].mesh)
        lockout_mesh = mesh_solid(leaves[LOCKOUT].mesh)
        for overtravel in (0, .2):
            native = lockout.intersect(bell.rotate((0, 0, 0), (0, 0, 1), -overtravel))
            faceted = lockout_mesh ^ bell_mesh.rotate((0, 0, -overtravel))
            self.assertTrue(native.isValid())
            self.assertEqual(faceted.status(), manifold.Error.NoError)
            for kernel, volume in (('native', native.Volume()), ('faceted', faceted.volume())):
                with self.subTest(kernel=kernel, overtravel=overtravel):
                    if overtravel:
                        self.assertGreater(volume, 0)
                    else:
                        self.assertLessEqual(volume, 0)
                    print(f'PASS installed {kernel}: overtravel={overtravel}, '
                          f'overlap_mm3={volume}', flush=True)

        reverse = sim.move('crank_rotation', by=-10)
        self.assertEqual(reverse.status, 'blocked')
        self.assertTrue(any(stop.coordinate == 'main_drive.crank.turn' and stop.bound == 'high'
                            for stop in sim.stops))


if __name__ == '__main__':
    unittest.main()
