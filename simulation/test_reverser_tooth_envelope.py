"""An independent phase survey must reproduce the actual retained fixture."""

import unittest

import numpy as np
from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.test_running_reverser_wrong_order import DRUM, commons, prepare
from simulation.tools.reverser_tooth_envelope import ToothEnvelopeReader
from simulation.tools.interference import rigid_leaves, world_solids


class ReverserToothEnvelopeTest(unittest.TestCase):
    def test_transformed_complete_prints_match_admitted_contact_and_clearance(self):
        reader = ToothEnvelopeReader()
        sim = prepare()
        prepared = sim.snapshot()
        for height in (1.0675, 1.0475, 0, -4.9425):
            with self.subTest(height=height):
                sim.restore(prepared)
                sim.move('reverser_height', to=height)
                actual = commons(sim)
                measured = tuple(reader.volumes(
                    sim.state['crank_rotation'],
                    sim.state['transmission.turns.ones.turn'],
                    sim.state['reverser_height'],
                    sim.state['crank_elevation'], kernel=kernel)[DRUM]
                    for kernel in ('native', 'world64'))
                for expected, observed in zip(actual, measured):
                    # Pose-transform rounding may perturb a positive volume's
                    # final bits, but never turn any positive common into zero.
                    self.assertEqual(observed > 0, expected > 0)
                    if expected == 0:
                        self.assertEqual(observed, 0)
                    else:
                        self.assertAlmostEqual(observed, expected, places=10)
        self.assertEqual(len(reader.bank), 214)
        self.assertEqual(reader.bank['crank_rotation'], 0)
        self.assertEqual(reader.bank['reverser_height'], 3.9075)

    def test_nonzero_retained_shaft_phase_and_drum_lift_match_world_placement(self):
        reader = ToothEnvelopeReader()
        sim = Sim(OperatingCurta(), dt=.1, meshes=True)
        empty = sim.snapshot()
        for lift, crank in ((0, 171.25), (9, 90)):
            with self.subTest(lift=lift, crank=crank):
                sim.restore(empty)
                command = sim.move('crank_elevation', to=lift)
                self.assertEqual(command.status, 'completed')
                command = sim.move('crank_rotation', to=crank, duration=.5)
                sim.run(.5)
                self.assertEqual(command.status, 'completed')
                self.assertNotEqual(sim.state['transmission.turns.ones.turn'], reader.shaft)
                coordinates = (sim.state['crank_rotation'],
                               sim.state['transmission.turns.ones.turn'],
                               sim.state['reverser_height'],
                               sim.state['crank_elevation'])
                native = world_solids(sim.node, selected=set(reader.paths))
                measured = reader.posed(*coordinates, kernel='native')
                leaves = dict(rigid_leaves(sim.node))
                faceted = reader.posed(*coordinates, kernel='world64')
                for path in reader.paths:
                    a, b = native[path].BoundingBox(), measured[path].BoundingBox()
                    np.testing.assert_allclose(
                        (a.xmin, a.ymin, a.zmin, a.xmax, a.ymax, a.zmax),
                        (b.xmin, b.ymin, b.zmin, b.xmax, b.ymax, b.zmax),
                        rtol=0, atol=1e-10, err_msg=path)
                    np.testing.assert_allclose(leaves[path].mesh.bounds.ravel(),
                                               faceted[path].bounding_box(),
                                               rtol=0, atol=1e-10, err_msg=path)
                for kernel, volume in zip(('native', 'world64'), commons(sim)):
                    measured_volume = reader.volumes(*coordinates, kernel=kernel)[DRUM]
                    self.assertEqual(measured_volume > 0, volume > 0)
                    if volume == 0:
                        self.assertEqual(measured_volume, 0)
                    else:
                        self.assertAlmostEqual(measured_volume, volume, places=10)


if __name__ == '__main__':
    unittest.main()
