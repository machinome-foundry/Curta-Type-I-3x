"""Counter contact instruments must retain the operating root's own frames."""

import unittest
import cadquery as cq

from machinome.simulation import Sim
from simulation.contracts import assert_connected_material
from simulation.tools.interference import world_solids
from simulation.tools.counter_lockout_probe import STATIONS, station_bench


class CounterLockoutFixtureTest(unittest.TestCase):
    def test_station_exports_have_distinct_artifact_identities(self):
        self.assertEqual(len({station_bench(station)().uniq_id
                              for station in range(1, 7)}), 6)
        self.assertEqual(len({station_bench(station, trial)().uniq_id
                              for station in range(1, 7) for trial in (False, True)}), 12)
        self.assertEqual(len({station_bench(station, True)().shaft.uniq_id
                              for station in range(1, 7)}), 6)

    def test_trial_removes_only_the_bounded_outer_skin_of_each_source_lockout(self):
        for station, (_, upper_name) in enumerate(STATIONS, 1):
            nodes = [station_bench(station, trial)() for trial in (False, True)]
            for node in nodes:
                node.set_state(shaft_angle=0, crank_angle=0, carry_position=0, time=0)
                node.assemble()
                node.build_stls()
            original, fitted = [getattr(node.shaft, upper_name) for node in nodes]
            before, after = original.shape(), fitted.shape()
            with self.subTest(station=station):
                self.assertTrue(after.isValid())
                self.assertEqual(len(after.Solids()), 1)
                assert_connected_material(fitted.mesh)
                self.assertEqual(after.cut(before).Volume(), 0)
                removed = before.cut(after)
                lockout = original.pentagonal_lockout.shape()
                self.assertGreater(removed.Volume(), 0)
                self.assertLessEqual(removed.Volume(), lockout.Area()*.01)
                box = lockout.BoundingBox()
                core = cq.Solid.makeCylinder(4, box.zlen+2, cq.Vector(0, 0, box.zmin-1))
                for operation in original.pentagonal_lockout.operations:
                    if hasattr(operation, 'angle'):
                        lockout = lockout.rotate((0, 0, 0), operation.axis, operation.angle)
                        core = core.rotate((0, 0, 0), operation.axis, operation.angle)
                    else:
                        lockout = lockout.translate(operation.translation)
                        core = core.translate(operation.translation)
                self.assertEqual(removed.cut(lockout).Volume(), 0)
                self.assertEqual(removed.intersect(core).Volume(), 0)
                for bound in ('zmin', 'zmax'):
                    self.assertAlmostEqual(getattr(before.BoundingBox(), bound),
                                           getattr(after.BoundingBox(), bound), places=7)

    def test_counter_station_selection_does_not_wrap(self):
        for station in (0, 7):
            with self.subTest(station=station), self.assertRaises(ValueError):
                station_bench(station)

    def test_higher_stroke_moves_only_its_own_upper_print_downward(self):
        for station, (_, upper) in enumerate(STATIONS, 1):
            node = station_bench(station)()
            path = f'Curta.shaft.{upper}'
            node.set_state(shaft_angle=134-20*(station-1), crank_angle=0,
                           carry_position=0, time=0)
            node.assemble()
            before = world_solids(node, selected={path})[path]
            for carry in (.5, 1):
                node.set_state(carry_position=carry)
                node.assemble()
                after = world_solids(node, selected={path})[path]
                expected = before.translate((0, 0, -4.2*carry if station > 1 else 0))
                with self.subTest(station=station, carry=carry):
                    self.assertEqual(after.cut(expected).Volume(), 0)
                    self.assertEqual(expected.cut(after).Volume(), 0)

    def test_every_normal_seat_matches_the_actual_retained_root(self):
        from simulation.running import OperatingCurta
        from simulation.running_parts import CHANNEL_NAMES

        sim = Sim(OperatingCurta(), dt=.1, meshes=True)
        paths = {
            f'Curta.transmission.turns.{CHANNEL_NAMES[index]}.{upper}'
            for index, (_, upper) in enumerate(STATIONS)
        }
        bell_path = 'Curta.carry_mechanism.tens_bell.tens_bell_1'
        paths.add(bell_path)
        actual = world_solids(sim.node, selected=paths)
        self.assertEqual(set(actual), paths)
        for station, (_, upper) in enumerate(STATIONS, 1):
            name = CHANNEL_NAMES[station-1]
            shaft = sim.state[f'transmission.turns.{name}.turn']
            node = station_bench(station)()
            node.set_state(shaft_angle=shaft, crank_angle=0, carry_position=0, time=0)
            node.assemble()
            measured = world_solids(node, selected={f'Curta.shaft.{upper}', 'Curta.bell'})
            source = actual[f'Curta.transmission.turns.{name}.{upper}']
            candidate = measured[f'Curta.shaft.{upper}']
            with self.subTest(station=station):
                self.assertTrue(candidate.isValid())
                self.assertEqual(source.cut(candidate).Volume(), 0)
                self.assertEqual(candidate.cut(source).Volume(), 0)
                self.assertEqual(actual[bell_path].cut(measured['Curta.bell']).Volume(), 0)
                self.assertEqual(measured['Curta.bell'].cut(actual[bell_path]).Volume(), 0)


if __name__ == '__main__':
    unittest.main()
