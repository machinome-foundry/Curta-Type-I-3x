"""An isolated retained counter trial must use the measured complete prints."""

import unittest

from machinome.simulation import Sim
from simulation import test_operating_counter_lockout as operating_tests
from simulation.counter_operating_trial import CounterOperatingTrial
from simulation.running import OperatingCurta
from simulation.tools.counter_lockout_probe import station_bench
from simulation.tools.counter_wrong_order import SHAFT, UPPER, BELL
from simulation.tools.interference import world_solids


class CounterOperatingTrialTest(operating_tests.OperatingCounterLockoutTest):
    model = CounterOperatingTrial


class CounterOperatingFixtureTest(unittest.TestCase):
    def test_installed_trial_matches_measured_parts_and_preserves_initial_bank(self):
        sim = Sim(CounterOperatingTrial(), dt=.1, meshes=True)
        baseline = Sim(OperatingCurta(), dt=.1)
        self.assertEqual(dict(sim.state), dict(baseline.state))
        actual = world_solids(sim.node, selected={UPPER, BELL})
        node = station_bench(1, trial=True)()
        node.set_state(shaft_angle=sim.state[SHAFT], crank_angle=0,
                       carry_position=0, time=0)
        node.assemble()
        measured = world_solids(node, selected={'Curta.shaft.p_10222_1', 'Curta.bell'})
        for installed, bench in ((UPPER, 'Curta.shaft.p_10222_1'), (BELL, 'Curta.bell')):
            with self.subTest(part=installed):
                self.assertTrue(actual[installed].isValid())
                self.assertEqual(actual[installed].cut(measured[bench]).Volume(), 0)
                self.assertEqual(measured[bench].cut(actual[installed]).Volume(), 0)


if __name__ == '__main__':
    unittest.main()
