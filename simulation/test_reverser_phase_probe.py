"""Interpolation probes must not bridge unmeasured regions or erase a sector."""

import unittest

from simulation.tools.probe_reverser_phase import interpolated_edges


def row(crank, offset=0):
    return dict(crank=crank, height=0, lift=0,
                chart=[dict(lower=10+72*i+offset, upper=20+72*i+offset)
                       for i in range(5)])


class ReverserPhaseProbeTest(unittest.TestCase):
    def test_uses_requested_measured_sector_and_free_side_guard(self):
        result = interpolated_edges([row(0), row(2, 2)], 1, 0, 0, 3, .01)
        self.assertEqual(result['bracket'], (0, 2))
        self.assertAlmostEqual(result['lower'], 233.41)
        self.assertAlmostEqual(result['upper'], 243.39)

    def test_unmeasured_intermediate_row_cannot_be_skipped(self):
        rows = [row(0), dict(row(1), chart=None), row(2)]
        with self.assertRaises(ValueError):
            interpolated_edges(rows, .5, 0, 0, 0, .01)

    def test_no_extrapolation_or_collapsed_interval(self):
        for crank, guard in ((-1, .01), (3, .01), (1, 6)):
            with self.subTest(crank=crank, guard=guard), self.assertRaises(ValueError):
                interpolated_edges([row(0), row(2)], crank, 0, 0, 0, guard)


if __name__ == '__main__':
    unittest.main()
