"""Open red diagnostics: reverse operation is not yet accepted.

Run separately from the established forward-operation regression. These tests
must become green before the development root can replace the pose model.
"""

import unittest
from machinome.simulation import Sim
from simulation.pawl import RELEASE, RAMP, TOOTH_PITCH
from simulation.running_pawl import RETURN_SPAN
from simulation.test_running_laws import RunningPawlBench
from simulation.test_running_limits import CrankLiftBench


class RunningRatchetTest(unittest.TestCase):
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
