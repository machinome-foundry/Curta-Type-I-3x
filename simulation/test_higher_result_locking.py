"""The next result station must meet its own sliding-stack locking surface.

The complete operating probe finds positive contact at 170 degrees after
withdrawing digit 2 at 140: native .308686 mm³, published mesh .213925 mm³.
This focused two-channel regression does not substitute the ones profile.
"""

import unittest

from machinome.simulation import Sim
from simulation.higher_result_locking import HigherResultLocking


class HigherResultLockingTest(unittest.TestCase):
    def test_tens_cannot_pass_its_closing_bell_after_withdrawal(self):
        sim = Sim(HigherResultLocking(), dt=.1,
                  state={'digit': 3, 'crank_height': 0})
        self.assertEqual(sim.move('crank_angle', to=140).status, 'completed')
        self.assertEqual(sim.move('digit', to=0).status, 'completed')
        self.assertAlmostEqual(sim.state['tens.turn'], 169.6, places=8)
        self.assertAlmostEqual(sim.state['tens.p_10220_410003_1_419227.travel'], -4.2)
        request = sim.move('crank_angle', to=170)
        self.assertEqual(request.status, 'blocked')
        self.assertLess(sim.state['crank_angle'], 170)
        self.assertAlmostEqual(sim.state['tens.turn'], 169.6, places=8)


class HigherTrialActionOrderTest(unittest.TestCase):
    def test_all_five_source_flats_stop_on_later_revolutions(self):
        for carry in (0, 4.2):
            for turns in range(5):
                with self.subTest(carry=carry, turns=turns):
                    sim = Sim(HigherResultLocking(), dt=.1,
                              state={'carry_latch': carry})
                    for turn in range(1, turns+1):
                        self.assertEqual(sim.move('crank_angle', to=360*turn).status,
                                         'completed')
                    self.assertEqual(sim.move('crank_angle', to=360*turns+140).status,
                                     'completed')
                    self.assertEqual(sim.move('digit', to=0).status, 'completed')
                    shaft = sim.state['tens.turn']
                    self.assertAlmostEqual(shaft, 169.6+72*turns*(4 if carry else 3),
                                           places=7)
                    saved = sim.snapshot()
                    self.assertEqual(sim.move('crank_angle', to=360*turns+170).status,
                                     'blocked')
                    angle = sim.state['crank_angle']
                    self.assertGreater(angle-360*turns, 140)
                    self.assertLess(angle-360*turns, 146)
                    self.assertAlmostEqual(sim.state['tens.turn'], shaft, places=7)
                    sim.restore(saved)
                    self.assertEqual(sim.move('crank_angle', to=360*turns+860).status,
                                     'blocked')
                    self.assertAlmostEqual(sim.state['crank_angle'], angle, places=7)

    def test_complete_prints_are_clear_at_the_stop_and_contact_beyond_it(self):
        import manifold3d as manifold
        from simulation.tools.ancestor_lockout_contact import mesh_solid
        from simulation.tools.interference import world_solids, rigid_leaves
        for carry in (0, 4.2):
            with self.subTest(carry=carry):
                sim = Sim(HigherResultLocking(), dt=.1,
                          state={'carry_latch': carry}, meshes=True)
                sim.move('crank_angle', to=140)
                sim.move('digit', to=0)
                self.assertEqual(sim.move('crank_angle', to=170).status, 'blocked')
                bell = 'Curta.bell'
                stack = 'Curta.tens.p_10220_410003_1_419227'
                solids = world_solids(sim.node, selected={bell, stack})
                leaves = dict(rigid_leaves(sim.node))
                meshes = {p: mesh_solid(leaves[p].mesh) for p in (bell, stack)}
                for extra in (0, .2):
                    native = solids[stack].intersect(solids[bell].rotate(
                        (0, 0, 0), (0, 0, 1), -extra))
                    faceted = meshes[stack] ^ meshes[bell].rotate((0, 0, -extra))
                    self.assertTrue(native.isValid())
                    self.assertEqual(faceted.status(), manifold.Error.NoError)
                    for volume in (native.Volume(), faceted.volume()):
                        if extra:
                            self.assertGreater(volume, 0)
                        else:
                            self.assertLessEqual(volume, 0)

    def test_lowering_a_retained_stack_cannot_push_it_into_the_carry_tooth(self):
        sim = Sim(HigherResultLocking(), dt=.1)
        sim.move('crank_angle', to=140)
        sim.move('digit', to=0)
        self.assertEqual(sim.move('crank_angle', to=145.1).status, 'completed')
        request = sim.move('carry_latch', to=4.2)
        self.assertEqual(request.status, 'blocked')
        self.assertAlmostEqual(sim.state['carry_latch'], 2.1, places=7)
        self.assertAlmostEqual(sim.state['crank_angle'], 145.1, places=7)
        self.assertAlmostEqual(sim.state['tens.turn'], 169.6, places=7)
        self.assertEqual(sim.move('carry_latch', by=-.05).status, 'completed')

    def test_ordinary_multi_turn_requests_keep_their_tooth_counts(self):
        for carry in (0, 4.2):
            for digit, height, count in ((0, 0, 0), (3, 0, 3), (9, 0, 9), (0, 9, 9)):
                with self.subTest(carry=carry, digit=digit, height=height):
                    sim = Sim(HigherResultLocking(), dt=.1, state={
                        'digit': digit, 'crank_height': height, 'carry_latch': carry})
                    request = sim.move('crank_angle', by=1080)
                    self.assertEqual(request.status, 'completed')
                    expected = -16+3*72*(count+(1 if carry else 0))
                    self.assertAlmostEqual(sim.state['tens.turn'], expected, places=7)

    def test_both_axial_seats_must_stop_after_selector_withdrawal(self):
        for carry in (0, 4.2):
            with self.subTest(carry=carry):
                sim = Sim(HigherResultLocking(), dt=.1,
                          state={'carry_latch': carry})
                self.assertEqual(sim.move('crank_angle', to=140).status, 'completed')
                self.assertEqual(sim.move('digit', to=0).status, 'completed')
                self.assertAlmostEqual(sim.state['tens.turn'], 169.6, places=8)
                self.assertAlmostEqual(sim.state['tens.p_10220_410003_1_419227.travel'],
                                       carry-4.2, places=8)
                saved = sim.snapshot()
                request = sim.move('crank_angle', to=170)
                self.assertEqual(request.status, 'blocked')
                self.assertGreater(sim.state['crank_angle'], 140)
                self.assertLess(sim.state['crank_angle'], 146)
                stopped_angle = sim.state['crank_angle']
                stopped = sim.snapshot()
                held = sim.state['tens.turn']
                sim.restore(saved)
                self.assertEqual(sim.move('crank_angle', to=170).status, 'blocked')
                self.assertEqual(sim.snapshot(), stopped)
                self.assertEqual(sim.move('crank_angle', by=-.05).status, 'completed')
                sim.run(.1)
                self.assertAlmostEqual(sim.state['crank_angle'], stopped_angle-.05,
                                       places=7)
                self.assertAlmostEqual(sim.state['tens.turn'], held, places=7)
                self.assertEqual(sim.move('crank_angle', to=170).status, 'blocked')
                self.assertAlmostEqual(sim.state['crank_angle'], stopped_angle,
                                       places=7)
                sim.restore(saved)
                self.assertEqual(sim.move('crank_angle', to=860).status, 'blocked')
                self.assertAlmostEqual(sim.state['crank_angle'], stopped_angle,
                                       places=7)


if __name__ == '__main__':
    unittest.main()
