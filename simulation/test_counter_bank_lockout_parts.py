"""Production candidates must equal the independently accepted trial prints."""

import unittest

from simulation.counter_bank_lockout_parts import contact_counter_channel
from simulation.counter_bank_operating_trial import trial_counter_channel, COUNTER_TRIAL_STATIONS


class CounterBankPartsTest(unittest.TestCase):
    def test_selection_does_not_wrap_or_replace_the_ones_station(self):
        for station in (-1, 0, 1, 7):
            with self.subTest(station=station), self.assertRaises(ValueError):
                contact_counter_channel(station)

    def test_source_specific_artifact_identities_are_distinct(self):
        self.assertEqual(len({contact_counter_channel(station)().uniq_id
                              for station in range(2, 7)}), 5)

    def test_each_complete_upper_equals_the_independent_operating_trial(self):
        for station, (_, upper_name) in enumerate(COUNTER_TRIAL_STATIONS, 2):
            reference = getattr(trial_counter_channel(station)(), upper_name)
            candidate = getattr(contact_counter_channel(station)(), upper_name)
            reference.assemble()
            candidate.assemble()
            expected, actual = reference.shape(), candidate.shape()
            with self.subTest(station=station):
                self.assertTrue(actual.isValid())
                self.assertEqual(len(actual.Solids()), 1)
                self.assertEqual(actual.cut(expected).Volume(), 0)
                self.assertEqual(expected.cut(actual).Volume(), 0)
