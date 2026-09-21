"""Contact labels must refer to the material of the complete measured prints."""

import unittest

from simulation.higher_lockout_trial import HigherLockoutFitBench
from simulation.tools.counter_lockout_probe import STATIONS, station_bench
from simulation.tools.higher_locking_envelope import component_shapes
from simulation.tools.interference import world_solids


class CounterComponentProbeTest(unittest.TestCase):
    def test_counter_ingredients_cover_exactly_the_complete_prints(self):
        upper_name = STATIONS[1][1]
        node_type = station_bench(2, trial=True)
        for carry in (0, .5, 1):
            bell_parts, upper_parts = component_shapes(
                carry, 200, 156, node_type, stack_path=('shaft', upper_name))
            node = node_type()
            node.set_state(shaft_angle=156, crank_angle=200, carry_position=carry, time=0)
            node.assemble()
            complete = world_solids(node, selected={'Curta.bell', 'Curta.shaft.'+upper_name})
            for path, pieces in (('Curta.bell', bell_parts),
                                 ('Curta.shaft.'+upper_name, upper_parts)):
                with self.subTest(carry=carry, body=path):
                    missing = complete[path]
                    self.assertTrue(pieces)
                    for name, part in pieces.items():
                        self.assertTrue(part.isValid(), name)
                        extra = part.cut(complete[path])
                        self.assertTrue(extra.isValid(), name)
                        self.assertEqual(extra.Volume(), 0, name)
                        missing = missing.cut(part)
                    self.assertTrue(missing.isValid())
                    self.assertEqual(missing.Volume(), 0)

    def test_default_result_path_keeps_its_existing_material(self):
        default = component_shapes(0, 140, 169.6, HigherLockoutFitBench)
        explicit = component_shapes(0, 140, 169.6, HigherLockoutFitBench,
                                    stack_path=('tens', 'p_10220_410003_1_419227'))
        for before, after in zip(default, explicit):
            self.assertEqual(before.keys(), after.keys())
            for name in before:
                with self.subTest(part=name):
                    self.assertEqual(before[name].cut(after[name]).Volume(), 0)
                    self.assertEqual(after[name].cut(before[name]).Volume(), 0)


if __name__ == '__main__':
    unittest.main()
