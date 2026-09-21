"""Actual carry-lever/shaft orders, not a diagnostic carry-height instrument."""

import unittest
import json
import os
from pathlib import Path

from machinome.simulation import Sim
from simulation.higher_operating_trial import HigherOperatingTrial


class HigherOperatingTrialTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.acceptance = []

    @classmethod
    def tearDownClass(cls):
        output = os.environ.get('CURTA_ACCEPTANCE_REPORT')
        if output:
            Path(output).write_text(json.dumps(cls.acceptance, indent=2)+'\n')

    def check_withdrawal(self, carried):
        sim = Sim(HigherOperatingTrial(), dt=.1)
        if carried:
            for name, value in (('digit_1', 9), ('crank_rotation', 360), ('digit_1', 1)):
                self.assertEqual(sim.move(name, to=value).status, 'completed')
        withdrawal = 500 if carried else 140
        for name, value in (('digit_2', 3), ('crank_rotation', withdrawal), ('digit_2', 0)):
            self.assertEqual(sim.move(name, to=value).status, 'completed')
        shaft = 'transmission.result.tens.turn'
        travel = 'transmission.result.tens.p_10220_410003_1_419227.travel'
        self.assertAlmostEqual(sim.state[shaft], 169.6, places=7)
        self.assertAlmostEqual(sim.state[travel], 0 if carried else -4.2, places=7)
        saved = sim.snapshot()
        request = sim.move('crank_rotation', to=withdrawal+30)
        self.assertEqual(request.status, 'blocked')
        stopped = sim.snapshot()
        angle = sim.state['crank_rotation']
        stopped_state = dict(sim.state)
        self.assertGreater(angle, withdrawal)
        self.assertLess(angle, withdrawal+6)
        self.assertAlmostEqual(sim.state[shaft], 169.6, places=7)
        sim.restore(saved)
        self.assertEqual(sim.move('crank_rotation', to=withdrawal+30).status, 'blocked')
        self.assertEqual(sim.snapshot(), stopped)
        sim.restore(saved)
        self.assertEqual(sim.move('crank_rotation', to=withdrawal+720).status, 'blocked')
        self.assertAlmostEqual(sim.state['crank_rotation'], angle, places=7)
        self.assertEqual(sim.move('crank_rotation', by=-.05).status, 'completed')
        sim.run(.1)
        self.assertAlmostEqual(sim.state['crank_rotation'], angle-.05, places=7)
        self.acceptance.append({'carried': carried, 'stopped': stopped_state,
                                'idle': dict(sim.state), 'replay': True})

    def test_raised_tens_withdrawal_stops_the_actual_crank(self):
        self.check_withdrawal(False)

    def test_real_carry_then_withdrawal_stops_the_actual_crank(self):
        self.check_withdrawal(True)


if __name__ == '__main__':
    unittest.main()
