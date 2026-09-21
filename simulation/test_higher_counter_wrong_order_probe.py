"""The higher-counter diagnostic uses only physical operating requests."""

import unittest
import sys
from types import SimpleNamespace
from unittest.mock import Mock, patch

from simulation.tools.higher_counter_wrong_order import withdrawal_trace, SHAFT, main


class HigherCounterWrongOrderProbeTest(unittest.TestCase):
    def test_real_entry_point_enables_bounded_stop_recording(self):
        factory = Mock(side_effect=RuntimeError('construction intercepted'))
        model = object()
        with patch.dict(sys.modules, {
                'machinome.simulation': SimpleNamespace(Sim=factory),
                'simulation.running': SimpleNamespace(OperatingCurta=lambda: model)}):
            with self.assertRaisesRegex(RuntimeError, 'construction intercepted'):
                main()
        factory.assert_called_once_with(model, dt=.1, meshes=True, record=64)

    def test_trace_requests_actual_controls_and_reads_the_retained_shaft(self):
        class Machine:
            state = {'crank_rotation': 0, SHAFT: 114}
            stops = ()

            def __init__(self):
                self.calls = []

            def move(self, name, *, to):
                self.calls.append((name, to))
                if name == 'crank_rotation':
                    self.state = dict(self.state, crank_rotation=to)
                return SimpleNamespace(status='completed')

        sim = Machine()
        reads = []

        def contacts(machine):
            self.assertIs(machine, sim)
            reads.append(len(machine.calls))
            return {'native': 0, 'faceted': 0}

        rows = list(withdrawal_trace(sim, contacts=contacts))
        self.assertEqual(sim.calls, [
            ('crank_elevation', 9), ('reverser_height', -4.9425),
            ('crank_rotation', 90), ('crank_rotation', 180),
            ('crank_rotation', 190), ('reverser_height', -6.9425),
            ('crank_rotation', 200)])
        self.assertEqual(reads, list(range(1, 8)))
        self.assertEqual([row['crank'] for row in rows], [0, 0, 90, 180, 190, 190, 200])
        self.assertTrue(all(row['shaft'] == 114 for row in rows))
        self.assertTrue(all(row['common_mm3'] == {'native': 0, 'faceted': 0} for row in rows))

    def test_an_unexpected_preparation_stop_is_reported_without_repair(self):
        class Machine:
            state = {'crank_rotation': 12, SHAFT: 123}
            stops = (SimpleNamespace(coordinate='main_drive.crank.turn', bound='low'),)

            def move(self, name, *, to):
                return SimpleNamespace(status='blocked')

        rows = list(withdrawal_trace(Machine(), contacts=lambda sim: {'native': 0, 'faceted': 0}))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['status'], 'blocked')
        self.assertEqual(rows[0]['crank'], 12)
        self.assertEqual(rows[0]['shaft'], 123)
        self.assertEqual(rows[0]['stops'], [{'coordinate': 'main_drive.crank.turn', 'bound': 'low'}])


if __name__ == '__main__':
    unittest.main()
