"""Production adoption must add a real independent retained loop control."""

import unittest
from machinome.simulation import Sim
from simulation.running import OperatingCurta


LOOP_INPUT = 'loop_deployment'
LOOP_JOINT = 'carriage.registers.clearing_ring.clearing_ring.swivel'
LOOP_CONTROL = 'deploy loop (simulation-only mounting)'


class OperatingLoopTest(unittest.TestCase):
    model = OperatingCurta

    def test_replacement_is_labeled_on_its_own_visible_control(self):
        self.assertIn(LOOP_CONTROL, self.model.controls)
        self.assertIn('clear registers', self.model.controls)

    def test_partial_stop_retry_relief_and_replay_change_only_the_loop(self):
        sim = Sim(self.model(), dt=.1)
        initial = sim.snapshot()
        before = dict(sim.state)

        def sequence():
            outcomes = []
            for target, expected, status in ((30, 30, 'completed'),
                    (200, 90.4, 'blocked'), (200, 90.4, 'blocked'),
                    (45, 45, 'completed'), (-100, -.4, 'blocked'),
                    (0, 0, 'completed')):
                command = sim.move(LOOP_INPUT, to=target, duration=.2)
                sim.run(.2)
                self.assertEqual(command.status, status)
                self.assertAlmostEqual(sim.state[LOOP_INPUT], expected)
                self.assertAlmostEqual(sim.state[LOOP_JOINT], -expected)
                for key, value in before.items():
                    if key not in (LOOP_INPUT, LOOP_JOINT):
                        self.assertEqual(sim.state[key], value, key)
                outcomes.append((command.status, dict(sim.state)))
            return outcomes

        first = sequence()
        finished = sim.snapshot()
        sim.restore(initial)
        self.assertEqual(sequence(), first)
        self.assertEqual(sim.snapshot(), finished)
