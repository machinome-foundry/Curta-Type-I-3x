"""The counter measuring tool brackets contact without a volume tolerance."""

import unittest
from unittest.mock import patch

from simulation.tools.counter_locking_envelope import indexed_bands


class CounterIndexedBandProbeTest(unittest.TestCase):
    def test_each_station_uses_its_actual_five_shaft_indices(self):
        calls = []

        def reader(station, carry, shaft, reference=0, trial=False):
            calls.append((station, carry, shaft, reference, trial))
            base = 134-20*(station-1)
            nearest = base+72*round((shaft-base)/72)

            def volume(crank, kernel):
                self.assertEqual(crank, 180)
                width = .25 if kernel == 'native' else .125
                # Any positive common is contact, however small.
                return 1e-20 if abs(shaft-nearest) > width else 0.0
            return volume

        with patch('simulation.tools.counter_locking_envelope.station_reader', reader):
            rows = list(indexed_bands(3, .5, crank=180, trial=True))
        self.assertEqual(len(rows), 10)
        self.assertEqual({r['index'] for r in rows}, {94+72*i for i in range(5)})
        for row in rows:
            width = .25 if row['kernel'] == 'native' else .125
            for direction, bound in zip((-1, 1), row['bounds']):
                with self.subTest(index=row['index'], kernel=row['kernel'], side=direction):
                    free = direction*(bound['last_free']-row['index'])
                    contact = direction*(bound['first_contact']-row['index'])
                    self.assertLessEqual(free, width)
                    self.assertGreater(contact, width)
                    self.assertLessEqual(contact-free, 5/2**18)
                    self.assertEqual(bound['free_mm3'], 0)
                    self.assertGreater(bound['contact_mm3'], 0)
        self.assertTrue(all(s == 3 and c == .5 and r == 180 and t
                            for s, c, _, r, t in calls))

    def test_a_blocked_index_is_not_reported_as_a_free_band(self):
        with patch('simulation.tools.counter_locking_envelope.station_reader',
                   return_value=lambda crank, kernel: 1e-20):
            with self.assertRaisesRegex(ValueError, 'indexed position.*contact'):
                list(indexed_bands(1, 0, trial=True))

    def test_a_missing_locking_flank_is_not_silently_bracketed(self):
        with patch('simulation.tools.counter_locking_envelope.station_reader',
                   return_value=lambda crank, kernel: 0):
            with self.assertRaisesRegex(ValueError, 'outer bracket.*contact'):
                list(indexed_bands(1, 0, trial=True))


if __name__ == '__main__':
    unittest.main()
