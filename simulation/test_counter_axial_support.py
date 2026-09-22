"""Axial contact brackets must preserve tiny positive commons and both sides."""

import unittest
from unittest.mock import patch

from simulation.tools.counter_axial_support import axial_boundary


class CounterAxialSupportTest(unittest.TestCase):
    def test_entry_and_exit_keep_free_and_contact_endpoint_measurements(self):
        for entering in (False, True):
            def reader(station, carry, shaft, reference=0, trial=False, *, world_precision):
                self.assertEqual((station, shaft, reference, trial), (2, 156, 94, True))
                self.assertEqual(world_precision, 64)
                def volume(crank, kernel):
                    self.assertEqual(crank, 94)
                    boundary = .3 if kernel == 'native' else .3001
                    contact = carry > boundary if entering else carry < boundary
                    return 1e-20 if contact else 0
                return volume
            with patch('simulation.tools.counter_axial_support.station_reader', reader):
                rows = list(axial_boundary(2, 156, 94, trial=True))
            self.assertEqual(len(rows), 2)
            for row in rows:
                self.assertEqual(row['world_precision_bits'], 64)
                boundary = .3 if row['kernel'] == 'native' else .3001
                with self.subTest(kernel=row['kernel'], entering=entering):
                    self.assertEqual(row['enters_contact'], entering)
                    self.assertLessEqual(row['left'], boundary)
                    self.assertGreaterEqual(row['right'], boundary)
                    self.assertLessEqual(row['right']-row['left'], 2**-20)
                    self.assertEqual(row['right_mm3'] > 0, entering)
                    self.assertEqual(row['left_mm3'] > 0, not entering)
                    self.assertEqual(row['travel_bracket'],
                                     [-1.8+4.2*row['left'], -1.8+4.2*row['right']])

    def test_does_not_invent_a_transition_or_move_the_fixed_ones_stack(self):
        for volume in (0, 1e-20, float('nan')):
            with patch('simulation.tools.counter_axial_support.station_reader',
                       return_value=lambda crank, kernel: volume):
                with self.subTest(volume=volume), self.assertRaises(ValueError):
                    list(axial_boundary(2, 156, 94, trial=True))
        with self.assertRaises(ValueError):
            list(axial_boundary(1, 134, 94, trial=True))

    def test_rejects_multiple_sampled_transitions(self):
        def reader(station, carry, shaft, reference=0, trial=False, *, world_precision):
            self.assertEqual(world_precision, 64)
            return lambda crank, kernel: 1e-20 if .2 < carry < .4 or carry > .8 else 0
        with patch('simulation.tools.counter_axial_support.station_reader', reader):
            with self.assertRaisesRegex(ValueError, 'got 3'):
                list(axial_boundary(2, 156, 94, trial=True))


if __name__ == '__main__':
    unittest.main()
