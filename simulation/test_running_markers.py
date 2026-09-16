"""Each physical annotation moves independently and cannot pass its neighbour."""

import unittest
from solid_node.motion.ports import Time
from solid_node.simulation import Sim
from simulation.decimal_markers import MarkerBench, LOWER_GAPS, UPPER_GAPS


class RunningMarkerBench(MarkerBench):
    time = Time.running()


class RunningMarkerTest(unittest.TestCase):
    def test_complete_bank_can_circle_the_track_without_a_false_end_stop(self):
        sim = Sim(RunningMarkerBench(), dt=.1)
        for index in range(1, 11):
            sim.move(f'marker_{index}', by=360, duration=1)
        sim.run(1)
        for index in range(1, 11):
            bank = 'lower' if index < 6 else 'upper'
            self.assertAlmostEqual(sim.state[f'{bank}.decimal_marker_{index}.turn'], 360)
        # Contact limits follow the retained angles, not the initial pose.
        sim.move('marker_2', by=1, duration=.1)
        sim.run(.1)
        self.assertAlmostEqual(sim.state['lower.decimal_marker_2.turn'], 360 + LOWER_GAPS[0])

    def test_real_machine_markers_do_not_change_the_registers(self):
        from simulation.running import OperatingCurta, register_reading
        sim = Sim(OperatingCurta(), dt=.1)
        sim.move('marker_1_rotation', by=20, duration=.1)
        sim.move('marker_6_rotation', by=20, duration=.1)
        sim.run(.1)
        self.assertEqual(sim.state['enclosure.decimal_markers.decimal_marker_1.turn'], 20)
        self.assertEqual(sim.state['carriage.registers.clearing_ring.decimal_markers.decimal_marker_6.turn'], 20)
        self.assertEqual(register_reading(sim), 0)
        self.assertEqual(register_reading(sim, True), 0)
        self.assertTrue(all(sim.state[f'digit_{i}'] == 0 for i in range(1, 9)))

    def test_counterclockwise_requests_meet_the_previous_neighbour(self):
        for bank, first, gaps in (('lower', 1, LOWER_GAPS), ('upper', 6, UPPER_GAPS)):
            for offset in range(5):
                index, gap = first + offset, gaps[(offset - 1) % 5]
                with self.subTest(marker=index):
                    sim = Sim(RunningMarkerBench(), dt=.1)
                    sim.move(f'marker_{index}', by=gap + 1, duration=1)
                    sim.run(1)
                    self.assertAlmostEqual(sim.state[f'{bank}.decimal_marker_{index}.turn'], gap)

    def test_every_marker_stops_at_its_next_neighbour_without_moving_it(self):
        for bank, first, gaps in (('lower', 1, LOWER_GAPS), ('upper', 6, UPPER_GAPS)):
            for offset, gap in enumerate(gaps):
                index = first + offset
                with self.subTest(marker=index):
                    sim = Sim(RunningMarkerBench(), dt=.1)
                    sim.move(f'marker_{index}', by=-(gap + 1), duration=1)
                    sim.run(1)
                    self.assertAlmostEqual(sim.state[f'{bank}.decimal_marker_{index}.turn'], -gap)
                    for other in range(1, 11):
                        if other != index:
                            key = f'{"lower" if other < 6 else "upper"}.decimal_marker_{other}.turn'
                            self.assertEqual(sim.state[key], 0)

    def test_moving_a_neighbour_opens_space_and_snapshot_replays(self):
        sim = Sim(RunningMarkerBench(), dt=.1)
        sim.move('marker_5', by=-20, duration=1)
        sim.run(1)
        saved = sim.snapshot()
        sim.move('marker_4', by=-10, duration=1)
        sim.run(1)
        self.assertAlmostEqual(sim.state['lower.decimal_marker_4.turn'], -10)
        expected = sim.snapshot()
        sim.restore(saved)
        sim.move('marker_4', by=-10, duration=1)
        sim.run(1)
        self.assertEqual(sim.snapshot(), expected)
