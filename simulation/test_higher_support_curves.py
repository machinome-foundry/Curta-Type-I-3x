"""Measured disconnected mesh contacts must not be turned into false jams."""

import unittest

from simulation.tools.higher_support_curves import combined_boundaries


def interval(start, end):
    return [{'left': start, 'right': start+.0000004, 'enters_contact': True},
            {'left': end-.0000004, 'right': end, 'enters_contact': False}]


class HigherSupportCurvesTest(unittest.TestCase):
    def test_four_actual_mesh_islands_can_be_covered_by_native_contact(self):
        # Observed at shaft 49.1044453125, death edge of the first source flat.
        islands = (interval(158.96805191040045, 159.08097457885742)
                   +interval(159.2521800994873, 159.47291717529296)
                   +interval(159.64374580383299, 159.8663551330567)
                   +interval(160.0379421234131, 160.14808006286617))
        native = interval(147.5, 154.4)+interval(158.96, 160.15)
        self.assertEqual(combined_boundaries(native, islands, 157, 161), native)

    def test_separated_representations_preserve_the_free_interval(self):
        native, mesh = interval(158, 159), interval(159.5, 160)
        self.assertEqual(combined_boundaries(native, mesh, 157, 161), native+mesh)

    def test_mesh_islands_without_native_support_remain_separate(self):
        mesh = interval(158, 158.2)+interval(159, 159.2)
        self.assertEqual(combined_boundaries([], mesh, 157, 161), mesh)

    def test_overlapping_brackets_keep_the_outer_measured_boundaries(self):
        native, mesh = interval(158, 159.5), interval(159, 160)
        self.assertEqual(combined_boundaries(native, mesh, 157, 161),
                         [native[0], mesh[1]])


if __name__ == '__main__':
    unittest.main()
