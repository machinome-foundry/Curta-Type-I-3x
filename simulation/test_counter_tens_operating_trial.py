"""Scoped full-machine check of the unadopted counter-tens restraint."""

import unittest

from machinome.simulation import Sim
from simulation import test_operating_counter_tens_lockout as operating_tests
from simulation.counter_tens_operating_trial import CounterTensOperatingTrial
from simulation.running import OperatingCurta
from simulation.tools.counter_lockout_probe import station_bench
from simulation.tools.higher_counter_wrong_order import SHAFT, UPPER, BELL
from simulation.tools.interference import world_solids


class CounterTensOperatingTrialTest(operating_tests.OperatingCounterTensLockoutTest):
    model = CounterTensOperatingTrial


class CounterTensOperatingFixtureTest(unittest.TestCase):
    def test_measured_complete_prints_and_entire_initial_bank_match(self):
        sim = Sim(CounterTensOperatingTrial(), dt=.1, meshes=True)
        baseline = Sim(OperatingCurta(), dt=.1)
        self.assertEqual(dict(sim.state), dict(baseline.state))
        actual = world_solids(sim.node, selected={UPPER, BELL})
        node = station_bench(2, trial=True)()
        node.set_state(shaft_angle=sim.state[SHAFT], crank_angle=0,
                       carry_position=0, time=0)
        node.assemble()
        upper = 'Curta.shaft.p_10220_410003_1_419081'
        measured = world_solids(node, selected={upper, 'Curta.bell'})
        for installed, reference in ((UPPER, upper), (BELL, 'Curta.bell')):
            with self.subTest(part=installed):
                self.assertTrue(actual[installed].isValid())
                self.assertEqual(actual[installed].cut(measured[reference]).Volume(), 0)
                self.assertEqual(measured[reference].cut(actual[installed]).Volume(), 0)


if __name__ == '__main__':
    unittest.main()
