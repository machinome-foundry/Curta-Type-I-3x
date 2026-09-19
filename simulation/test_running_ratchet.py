"""Measured ratchet backlash and retained pawl seating."""

import unittest
from machinome.simulation import Sim
from simulation.pawl import RELEASE, RAMP, TOOTH_PITCH, CLOSING_RELEASE
from simulation.running_pawl import RETURN_SPAN, RetainedPawlBench
from simulation.test_running_laws import RunningPawlBench
from simulation.test_running_limits import CrankLiftBench


class RunningRatchetTest(unittest.TestCase):
    def test_all_teeth_hold_after_reverse_and_snapshot_replay(self):
        sim = Sim(RetainedPawlBench(), dt=.1)
        releases = [RELEASE + index * TOOTH_PITCH for index in range(98)]
        releases += [CLOSING_RELEASE + index * TOOTH_PITCH for index in range(19)]
        for cycle in (0, 1):
            for release in releases:
                with self.subTest(cycle=cycle, release=release):
                    angle = 360 * cycle + release
                    sim.move('crank_turns', to=(angle + .2) / 360)
                    saved = sim.snapshot()
                    command = sim.move('crank_turns', by=-1 / 360)
                    self.assertEqual(command.status, 'blocked')
                    self.assertAlmostEqual(sim.state['disc.turn'], -(angle - .2), places=7)
                    self.assertAlmostEqual(sim.state['pawl.reverse_rotation_prevention_pawl.turn'],
                                           1.006, places=7)
                    expected = sim.snapshot()
                    sim.move('crank_turns', by=-1 / 360)
                    self.assertAlmostEqual(sim.state['disc.turn'], -(angle - .2), places=7)
                    sim.restore(saved)
                    sim.move('crank_turns', by=-1 / 360)
                    self.assertEqual(sim.snapshot(), expected)

    def test_unreleased_tooth_does_not_capture_the_crank_early(self):
        sim = Sim(RetainedPawlBench(), dt=.1)
        sim.move('crank_turns', to=(RELEASE + TOOTH_PITCH - .1) / 360)
        command = sim.move('crank_turns', by=-1 / 360)
        self.assertEqual(command.status, 'completed')
        self.assertAlmostEqual(sim.state['disc.turn'], -(RELEASE + TOOTH_PITCH - 1.1))

    def test_reverse_play_does_not_reopen_the_seated_pawl(self):
        sim = Sim(RunningPawlBench(), dt=.1)
        sim.move('crank_turns', to=(RELEASE + RETURN_SPAN + .2) / 360, duration=.1)
        sim.run(.1)
        sim.move('crank_turns', to=(RELEASE - .1) / 360, duration=.1)
        sim.run(.1)
        self.assertAlmostEqual(sim.state['pawl.reverse_rotation_prevention_pawl.turn'],
                               RAMP[0][1], places=6)

    def test_repeated_reverse_requests_cannot_walk_back_through_teeth(self):
        sim = Sim(CrankLiftBench(), dt=.1)
        sim.move('crank_rotation', to=-10, duration=1)
        sim.run(1)
        # Native seated-pawl contact lies .20005--.20008 degrees before
        # each release. Use its rounded-inward free-side angle here.
        seat = RELEASE - .2 + 3 * TOOTH_PITCH
        for request in range(3):
            with self.subTest(request=request):
                sim.move('crank_rotation', to=0, duration=1)
                sim.run(1)
                self.assertAlmostEqual(sim.state['drive.crank.turn'], -seat)
                self.assertGreater(sim.state['drive.crank.turn'], -10)
