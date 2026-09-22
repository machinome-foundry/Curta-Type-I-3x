"""Production higher-result parts must equal each independently measured print."""

import unittest

from simulation.result_bank_lockout_parts import contact_result_channel
from simulation.tools.result_bank_lockout_probe import STATIONS, station_channel


class ResultBankPartsTest(unittest.TestCase):
    def test_selection_does_not_wrap_or_replace_existing_ones_and_tens(self):
        for station in (-1, 0, 1, 2, 12):
            with self.subTest(station=station), self.assertRaises(ValueError):
                contact_result_channel(station)

    def test_source_specific_artifact_identities_are_distinct(self):
        self.assertEqual(len({contact_result_channel(station)().uniq_id
                              for station in range(3, 12)}), 9)

    def test_each_complete_upper_equals_its_independent_trial(self):
        for station in range(3, 12):
            upper = STATIONS[station-2][1]
            reference = getattr(station_channel(station, trial=True)(), upper)
            candidate = getattr(contact_result_channel(station)(), upper)
            reference.assemble()
            candidate.assemble()
            expected = reference.shape()
            actual = candidate.shape()
            with self.subTest(station=station):
                self.assertTrue(actual.isValid())
                self.assertEqual(len(actual.Solids()), 1)
                self.assertEqual(actual.cut(expected).Volume(), 0)
                self.assertEqual(expected.cut(actual).Volume(), 0)


if __name__ == '__main__':
    unittest.main()
