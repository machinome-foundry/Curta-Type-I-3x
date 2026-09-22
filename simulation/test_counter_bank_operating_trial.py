"""Actual-root and independent complete-print gates for the unadopted bank."""

import unittest

from machinome.simulation import Sim
from simulation import test_operating_counter_tens_lockout as counter_tests
from simulation import test_operating_counter_lockout as counter_ones_tests
from simulation import test_operating_result_bank_lockout as result_tests
from simulation.counter_bank_operating_trial import CounterBankOperatingTrial, COUNTER_TRIAL_STATIONS
from simulation.running import OperatingCurta
from simulation.running_parts import CHANNEL_NAMES
from simulation.tools.counter_lockout_probe import station_bench
from simulation.tools.interference import world_solids


class CounterBankTensTrialTest(counter_tests.OperatingCounterTensLockoutTest):
    model = CounterBankOperatingTrial


class CounterBankHundredsTrialTest(CounterBankTensTrialTest):
    station = 3


class CounterBankFourthTrialTest(CounterBankTensTrialTest):
    station = 4


class CounterBankFifthTrialTest(CounterBankTensTrialTest):
    station = 5


class CounterBankSixthTrialTest(CounterBankTensTrialTest):
    station = 6


class CounterBankPreservesOnesTest(counter_ones_tests.OperatingCounterLockoutTest):
    """Adding higher stops must preserve the previously adopted ones stop."""

    model = CounterBankOperatingTrial


class CounterBankPreservesResultsTest(result_tests.OperatingResultBankLockoutTest):
    """Both existing result withdrawal scenarios run on the combined bank."""

    model = CounterBankOperatingTrial


class CounterBankFixtureTest(unittest.TestCase):
    def test_every_complete_upper_matches_its_independently_measured_source_bench(self):
        sim = Sim(CounterBankOperatingTrial(), dt=.1, meshes=True)
        baseline = Sim(OperatingCurta(), dt=.1)
        self.assertEqual(dict(sim.state), dict(baseline.state))
        bell = 'Curta.carry_mechanism.tens_bell.tens_bell_1'
        paths = [f'Curta.transmission.turns.{CHANNEL_NAMES[n-1]}.{upper}'
                 for n, (_, upper) in enumerate(COUNTER_TRIAL_STATIONS, 2)]
        actual = world_solids(sim.node, selected={bell, *paths})
        for station, ((_, upper_name), path) in enumerate(zip(COUNTER_TRIAL_STATIONS, paths), 2):
            node = station_bench(station, trial=True)()
            node.set_state(shaft_angle=sim.state[f'transmission.turns.{CHANNEL_NAMES[station-1]}.turn'],
                           crank_angle=0, carry_position=0, time=0)
            node.assemble()
            upper = f'Curta.shaft.{upper_name}'
            measured = world_solids(node, selected={upper, 'Curta.bell'})
            for installed, reference in ((path, upper), (bell, 'Curta.bell')):
                with self.subTest(station=station, part=installed):
                    self.assertTrue(actual[installed].isValid())
                    self.assertEqual(actual[installed].cut(measured[reference]).Volume(), 0)
                    self.assertEqual(measured[reference].cut(actual[installed]).Volume(), 0)
