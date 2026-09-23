"""The whole-bank trial must install each measured print in its own frame."""

import hashlib
import json
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
    model = ResultBankOperatingTrial

    def test_installed_bank_matches_measured_prints_and_preserves_initial_state(self):
        sim = Sim(self.model(), dt=.1, meshes=True)
        # Fixed pre-adoption witness, not two aliases of the fitted default.
        bank = dict(sim.state)
        self.assertEqual(len(bank), 214)
        self.assertEqual(bank.pop('carriage.positioning.p_6mm_ball_419094.slide'), 0)
        self.assertEqual(len(bank), 213)
        encoded = json.dumps(bank, sort_keys=True, separators=(',', ':')).encode()
        self.assertEqual(hashlib.sha256(encoded).hexdigest(),
                         'ea39d95d50f06580db66c894f5b3f700ab6ed930cee113b2b9ffe4689935f5b7')
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


class OperatingResultBankFixtureTest(ResultBankOperatingFixtureTest):
    model = OperatingCurta


if __name__ == '__main__':
    unittest.main()
