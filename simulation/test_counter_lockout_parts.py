"""Production counter-ones parts must equal the independently admitted trial."""

import unittest

from simulation.counter_lockout_parts import ContactCounterOnesUpper
from simulation.counter_operating_trial import TrialCounterOnesUpper


class CounterOnesPartsTest(unittest.TestCase):
    def test_complete_print_matches_the_measured_candidate(self):
        reference = TrialCounterOnesUpper()
        candidate = ContactCounterOnesUpper()
        reference.assemble()
        candidate.assemble()
        expected = reference.shape()
        actual = candidate.shape()
        for shape in (expected, actual):
            self.assertTrue(shape.isValid())
            self.assertEqual(len(shape.Solids()), 1)
        self.assertEqual(actual.cut(expected).Volume(), 0)
        self.assertEqual(expected.cut(actual).Volume(), 0)


if __name__ == '__main__':
    unittest.main()
