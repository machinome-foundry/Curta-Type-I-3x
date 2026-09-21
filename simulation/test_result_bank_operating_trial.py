"""The whole-bank trial must install each measured print in its own frame."""

import unittest

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.running_parts import CHANNEL_NAMES, RESULT_RESTS
from simulation.result_bank_operating_trial import ResultBankOperatingTrial
from simulation.tools.interference import world_solids
from simulation.tools.result_bank_lockout_probe import STATIONS, station_bench
from simulation import test_operating_result_bank_lockout as operating_tests


class ResultBankOperatingTrialTest(operating_tests.OperatingResultBankLockoutTest):
    model = ResultBankOperatingTrial


class ResultBankOperatingFixtureTest(unittest.TestCase):
    def test_installed_bank_matches_measured_prints_and_preserves_initial_state(self):
        sim = Sim(ResultBankOperatingTrial(), dt=.1, meshes=True)
        original = Sim(OperatingCurta(), dt=.1)
        self.assertEqual(dict(sim.state), dict(original.state))
        paths = {f'Curta.transmission.result.{CHANNEL_NAMES[station-1]}.{upper}'
                 for station, (_, upper) in enumerate(STATIONS, 2)}
        actual = world_solids(sim.node, selected=paths)
        self.assertEqual(set(actual), paths)
        for station, (_, upper) in enumerate(STATIONS, 2):
            prefix = f'transmission.result.{CHANNEL_NAMES[station-1]}'
            carry = (sim.state[prefix+'.'+upper+'.travel']-RESULT_RESTS[station-2])/4.2
            bench = station_bench(station, trial=True)()
            bench.set_state(shaft_angle=0, crank_angle=0, carry_position=0, time=0)
            bench.assemble()
            self.assertEqual(getattr(bench.shaft, upper).travel.value, RESULT_RESTS[station-2])
            bench.set_state(shaft_angle=sim.state[prefix+'.turn'], crank_angle=0,
                            carry_position=carry, time=0)
            bench.assemble()
            measured = world_solids(bench, selected={'Curta.shaft.'+upper})
            expected = measured['Curta.shaft.'+upper]
            installed = actual['Curta.'+prefix+'.'+upper]
            with self.subTest(station=station):
                self.assertTrue(installed.isValid())
                self.assertEqual(installed.cut(expected).Volume(), 0)
                self.assertEqual(expected.cut(installed).Volume(), 0)


if __name__ == '__main__':
    unittest.main()
