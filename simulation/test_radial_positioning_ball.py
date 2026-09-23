"""Trial radial contact following must retain slack and block incompatible motion."""

import unittest
import math

from machinome.simulation import Sim
from simulation.running import register_reading
from simulation.positioning_ball_trial import RadialBallTrial
from simulation.positioning_ball_profiles import bell_limit, collar_limit


BALL = 'carriage.positioning.p_6mm_ball_419094.slide'


class RadialPositioningBallTest(unittest.TestCase):
    model = RadialBallTrial

    def test_bell_pushes_outward_and_return_does_not_pull_the_free_ball_back(self):
        sim = Sim(self.model(), dt=.1)
        self.assertEqual(sim.state[BALL], 0)
        command = sim.move('crank_rotation', by=90, duration=.5)
        sim.run(.5)
        self.assertEqual(command.status, 'completed')
        self.assertGreater(sim.state[BALL], 2.2)
        outward = sim.state[BALL]
        command = sim.move('crank_rotation', to=360, duration=1.5)
        sim.run(1.5)
        self.assertEqual(command.status, 'completed')
        self.assertEqual(sim.state[BALL], outward)
        self.assertEqual((register_reading(sim), register_reading(sim, True)), (0, 1))

    def test_raised_carriage_presses_the_ball_inward_and_blocks_the_crank(self):
        sim = Sim(self.model(), dt=.1)
        command = sim.move('carriage_elevation', to=6)
        self.assertEqual(command.status, 'completed')
        self.assertLess(sim.state[BALL], -1.2)
        saved = sim.snapshot()

        def blocked_turn():
            request = sim.move('crank_rotation', to=90, duration=.5)
            sim.run(.5)
            self.assertEqual(request.status, 'blocked')
            self.assertGreater(sim.state['crank_rotation'], 0)
            self.assertLess(sim.state['crank_rotation'], 1)
            self.assertEqual(sim.state['carriage_elevation'], 6)

        blocked_turn()
        stopped = sim.snapshot()
        sim.restore(saved)
        blocked_turn()
        self.assertEqual(sim.snapshot(), stopped)
        self.assertEqual(sim.move('carriage_elevation', to=0).status, 'completed')
        command = sim.move('crank_rotation', to=90, duration=.5)
        sim.run(.5)
        self.assertEqual(command.status, 'completed')
        self.assertGreater(sim.state[BALL], 2.2)

    def test_outward_bell_blocks_lift_without_turning_it_and_relief_is_explicit(self):
        sim = Sim(self.model(), dt=.1)
        turn = sim.move('crank_rotation', to=90, duration=.5)
        sim.run(.5)
        self.assertEqual(turn.status, 'completed')
        before_lift = sim.snapshot()

        def blocked_lift():
            request = sim.move('carriage_elevation', to=6, duration=.5)
            sim.run(.5)
            self.assertEqual(request.status, 'blocked')
            self.assertEqual(sim.state['crank_rotation'], 90)
            self.assertGreater(sim.state['carriage_elevation'], 1)
            self.assertLess(sim.state['carriage_elevation'], 1.3)

        blocked_lift()
        stopped = sim.snapshot()
        bank = dict(sim.state)
        sim.run(.5)
        self.assertEqual(dict(sim.state), bank)
        self.assertEqual(sim.move('carriage_elevation', to=6).status, 'blocked')
        self.assertEqual(dict(sim.state), bank)
        sim.restore(before_lift)
        blocked_lift()
        self.assertEqual(sim.snapshot(), stopped)
        self.assertEqual(sim.move('carriage_elevation', to=0).status, 'completed')
        self.assertEqual(sim.state['crank_rotation'], 90)
        turn = sim.move('crank_rotation', to=360, duration=1.5)
        sim.run(1.5)
        self.assertEqual(turn.status, 'completed')
        self.assertEqual(sim.move('carriage_elevation', to=6).status, 'completed')

    def test_long_and_short_requests_stop_at_the_same_contact(self):
        for outward in (False, True):
            banks = []
            for duration in (.1, .5):
                sim = Sim(self.model(), dt=.1)
                if outward:
                    request = sim.move('crank_rotation', to=90, duration=.5)
                    sim.run(.5)
                    self.assertEqual(request.status, 'completed')
                    name, target = 'carriage_elevation', 6
                else:
                    self.assertEqual(sim.move('carriage_elevation', to=6).status, 'completed')
                    name, target = 'crank_rotation', 90
                request = sim.move(name, to=target, duration=duration)
                sim.run(duration)
                self.assertEqual(request.status, 'blocked')
                self.assertLessEqual(bell_limit(sim.state['carry_mechanism.tens_bell.turn']),
                                     collar_limit(sim.state['carriage.registers.lift']))
                banks.append(dict(sim.state))
            # Different per-tick deltas meet the same contact within the
            # running-bound contract's existing 1e-9 agreement window.
            # Same-command snapshot replay remains bit-exact in tests above.
            dependent = ({'carriage_elevation', 'carriage.registers.lift',
                          'carriage.positioning.carriage_spring.slide',
                          'carriage.positioning.thrust_ring.slide'} if outward else
                         {'crank_rotation', 'carry_mechanism.tens_bell.turn',
                          'main_drive.crank.turn', 'main_drive.stepped_drum.turn',
                          'main_drive.zero_positioning.zero_positioning_disc.turn',
                          'main_drive.zero_positioning.zero_positioning_disc_pin.turn',
                          'main_drive.anti_reversal.reverse_rotation_prevention_pawl.turn',
                          'main_drive.zero_positioning.follower.turn'})
            self.assertEqual(set(banks[0]), set(banks[1]))
            for name in banks[0]:
                if name in dependent:
                    self.assertTrue(math.isclose(banks[0][name], banks[1][name],
                                                rel_tol=1e-9, abs_tol=1e-9), name)
                else:
                    self.assertEqual(banks[0][name], banks[1][name], name)


if __name__ == '__main__':
    unittest.main()
