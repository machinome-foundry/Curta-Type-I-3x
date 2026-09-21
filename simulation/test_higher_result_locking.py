"""The next result station must meet its own sliding-stack locking surface.

The complete operating probe finds positive contact at 170 degrees after
withdrawing digit 2 at 140: native .308686 mm³, published mesh .213925 mm³.
This focused two-channel regression does not substitute the ones profile.
"""

import unittest

from machinome.simulation import Sim
from simulation.result_locking import ResultLocking
from simulation.higher_result_action_order import HigherResultActionOrder


class HigherResultLockingTest(unittest.TestCase):
    def test_tens_cannot_pass_its_closing_bell_after_withdrawal(self):
        sim = Sim(ResultLocking(), dt=.1,
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
    def test_both_axial_seats_must_stop_after_selector_withdrawal(self):
        for carry in (0, 4.2):
            with self.subTest(carry=carry):
                sim = Sim(HigherResultActionOrder(), dt=.1,
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
                sim.restore(saved)
                self.assertEqual(sim.move('crank_angle', to=860).status, 'blocked')
                self.assertAlmostEqual(sim.state['crank_angle'], stopped_angle,
                                       places=7)


if __name__ == '__main__':
    unittest.main()
