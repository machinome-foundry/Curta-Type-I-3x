"""A phase candidate must preserve the stricter kernel and every source sector."""

import unittest

from simulation.tools.compile_reverser_phase import common_boundary, free_windows, chart_windows


def boundary(left, right, enters):
    return dict(left={'shaft': left}, right={'shaft': right}, enters_contact=enters)


class ReverserPhaseCompilerTest(unittest.TestCase):
    def test_contact_union_uses_the_stricter_kernel_on_both_edges(self):
        world = boundary(152.22, 152.23, False)
        native = dict(boundary(152.235, 152.236, False), world64_seed=world)
        self.assertEqual(common_boundary(world, native),
                         dict(left=152.235, right=152.236, enters_contact=False))
        world = boundary(174.07217, 174.07220, True)
        native = dict(boundary(174.07214, 174.07216, True), world64_seed=world)
        self.assertEqual(common_boundary(world, native),
                         dict(left=174.07214, right=174.07216, enters_contact=True))

    def test_free_interval_crosses_the_period_seam_without_a_fake_wall(self):
        self.assertEqual(free_windows([
            dict(left=171, right=171.01, enters_contact=True),
            dict(left=190, right=190.01, enters_contact=False)]), ((190.01, 531),))

    def test_missing_transitions_and_empty_data_are_not_certified(self):
        for values in ([], [dict(left=1, right=2, enters_contact=True)],
                       [dict(left=1, right=2, enters_contact=True),
                        dict(left=3, right=4, enters_contact=True)]):
            with self.subTest(values=values), self.assertRaises(ValueError):
                free_windows(values)

    def test_chart_preserves_five_unequal_source_windows(self):
        windows = [(152.3+72*i+.001*i, 174+72*i-.002*i) for i in range(5)]
        chart = chart_windows(windows, 90)
        self.assertEqual({entry['source_window'] for entry in chart}, set(range(5)))
        for entry in chart:
            original = windows[entry['source_window']]
            self.assertAlmostEqual(entry['upper']-entry['lower'], original[1]-original[0])
        self.assertEqual(len({round(row['upper']-row['lower'], 8) for row in chart}), 5)

    def test_duplicate_or_missing_source_windows_are_refused(self):
        for windows in ([(152, 174)]*5, [(152+72*i, 174+72*i) for i in range(4)]):
            with self.subTest(windows=windows), self.assertRaises(ValueError):
                chart_windows(windows, 90)


if __name__ == '__main__':
    unittest.main()
