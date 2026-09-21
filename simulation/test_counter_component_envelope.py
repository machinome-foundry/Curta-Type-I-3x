"""Component curves retain their limited scope and every observed interval."""

import unittest
from unittest.mock import patch

from simulation.tools.counter_component_envelope import component_envelope


class CounterComponentEnvelopeTest(unittest.TestCase):
    def test_keeps_multiple_intervals_and_positive_endpoints_without_an_epsilon(self):
        def volume(angle, kernel='native'):
            self.assertEqual(kernel, 'native')
            return 1e-20 if 90 < angle < 110 or 200 < angle < 210 else 0

        with patch('simulation.tools.counter_component_envelope.pair_reader', return_value=volume) as read:
            row = component_envelope(2, 1, 156, 'carry_tooth', step=5, trial=True)
        self.assertEqual(row['component'], 'carry_tooth')
        self.assertEqual(row['kernel'], 'native')
        self.assertEqual(row['pair'], ['turns_counter_carry_ring', 'transmission_gear_0_6'])
        self.assertEqual(row['station'], 2)
        self.assertTrue(row['trial'])
        self.assertEqual(read.call_args.kwargs['stack_path'],
                         ('shaft', 'p_10220_410003_1_419081'))
        self.assertEqual([b['enters_contact'] for b in row['boundaries']], [True, False, True, False])
        for boundary, expected in zip(row['boundaries'], (90, 110, 200, 210)):
            self.assertLessEqual(boundary['left'], expected)
            self.assertGreaterEqual(boundary['right'], expected)
            self.assertLess(boundary['right']-boundary['left'], .00002)
            self.assertEqual(boundary['right_mm3'] > 0, boundary['enters_contact'])
            self.assertNotEqual(boundary['left_mm3'] > 0, boundary['enters_contact'])

    def test_nonfinite_measurement_is_not_reported_as_clear(self):
        with patch('simulation.tools.counter_component_envelope.pair_reader',
                   return_value=lambda angle: float('nan')):
            with self.assertRaisesRegex(ValueError, 'non-finite'):
                component_envelope(2, 1, 156, 'lower_lock')

    def test_invalid_scope_refuses_before_geometry_is_built(self):
        with patch('simulation.tools.counter_component_envelope.pair_reader') as reader:
            for kwargs in ({'station': 1}, {'carry': 1.1}, {'shaft': float('nan')},
                           {'step': 0}, {'step': 11}, {'component': 'unknown'}):
                args = dict(station=2, carry=1, shaft=156, component='lower_lock')
                args.update(kwargs)
                with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                    component_envelope(**args)
            reader.assert_not_called()


if __name__ == '__main__':
    unittest.main()
