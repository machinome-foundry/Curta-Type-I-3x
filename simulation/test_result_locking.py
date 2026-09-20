"""A withdrawn selector must not let a retained shaft cross the closing bell.

The two-channel source bench keeps the real complete bell and upper stack.
These tests cover the ones lockout only, not the neighbouring carry restraint.
"""

import unittest

from machinome.simulation import Sim
from simulation.result_locking import ResultLocking as ResultActionOrder, contact_gap, closing_limit
from simulation.cycle import tooth_passage, RESULT_INPUT_END


class ResultLockingTest(unittest.TestCase):
    def test_surface_bound_agrees_with_the_measured_contact_region(self):
        for shaft in range(4, 365, 2):
            for crank in range(-360, 721, 10):
                self.assertEqual(-crank >= closing_limit(-crank, -crank, shaft),
                                 contact_gap(crank, shaft) <= 0, (crank, shaft))

    def test_complete_source_tooth_passages_stay_outside_the_forbidden_region(self):
        # Independent counts, not a calculator result or a selector-derived
        # permission: all eleven lower-drum tooth counts at all five flats.
        for flat in range(5):
            for count in range(11):
                for half_degree in range(721):
                    crank = half_degree/2
                    shaft = 4+72*flat+72*tooth_passage(crank, count, RESULT_INPUT_END)
                    self.assertLessEqual(contact_gap(crank, shaft), 0,
                                         (flat, count, crank, shaft))

    def test_all_five_flats_and_later_revolutions_stop_and_replay(self):
        for turns in range(5):
            with self.subTest(turns=turns):
                sim = Sim(ResultActionOrder(), dt=.1,
                          state={'digit': 3, 'crank_height': 0})
                sim.move('crank_angle', to=360*turns+120)
                sim.move('digit', to=0)
                saved = sim.snapshot()
                held = sim.state['ones.turn']
                request = sim.move('crank_angle', to=360*turns+150)
                self.assertEqual(request.status, 'blocked')
                stopped = sim.snapshot()
                angle = sim.state['crank_angle']
                self.assertGreater(angle-360*turns, 125.1)
                self.assertLess(angle-360*turns, 125.5)
                self.assertEqual(sim.state['ones.turn'], held)
                sim.restore(saved)
                sim.move('crank_angle', to=360*turns+150)
                self.assertEqual(sim.snapshot(), stopped)
                self.assertEqual(sim.move('crank_angle', by=-.05).status, 'completed')
                sim.run(.1)
                self.assertAlmostEqual(sim.state['crank_angle'], angle-.05, places=8)
                self.assertEqual(sim.state['ones.turn'], held)
                self.assertEqual(sim.move('crank_angle', to=360*turns+150).status,
                                 'blocked')
                self.assertAlmostEqual(sim.state['crank_angle'], angle, places=8)

    def test_whole_turns_do_not_acquire_an_artificial_one_turn_limit(self):
        for digit, height, expected in ((0, 0, 4), (3, 0, 652),
                                        (9, 0, 1948), (0, 9, 2164)):
            with self.subTest(digit=digit, height=height):
                sim = Sim(ResultActionOrder(), dt=.1,
                          state={'digit': digit, 'crank_height': height})
                request = sim.move('crank_angle', by=1080)
                self.assertEqual(request.status, 'completed')
                self.assertAlmostEqual(sim.state['ones.turn'], expected, places=7)

    def test_closing_contact_cannot_be_skipped_by_a_long_request(self):
        sim = Sim(ResultActionOrder(), dt=.1,
                  state={'digit': 3, 'crank_height': 0})
        sim.move('crank_angle', to=120)
        sim.move('digit', to=0)
        request = sim.move('crank_angle', to=840)
        self.assertEqual(request.status, 'blocked')
        self.assertGreater(sim.state['crank_angle'], 125.1)
        self.assertLess(sim.state['crank_angle'], 125.5)
        self.assertAlmostEqual(sim.state['ones.turn'], 189.6, places=9)

    def test_distinct_withdrawal_phases_meet_their_measured_closing_flank(self):
        for withdrawal, low, high in ((115, 120.3, 120.8),
                                      (118, 123.1, 123.6),
                                      (120, 125.1, 125.5),
                                      (121, 126.2, 126.8),
                                      (123, 129.5, 130.2)):
            with self.subTest(withdrawal=withdrawal):
                sim = Sim(ResultActionOrder(), dt=.1,
                          state={'digit': 3, 'crank_height': 0})
                sim.move('crank_angle', to=withdrawal)
                sim.move('digit', to=0)
                held = sim.state['ones.turn']
                request = sim.move('crank_angle', to=150)
                self.assertEqual(request.status, 'blocked')
                self.assertGreater(sim.state['crank_angle'], low)
                self.assertLess(sim.state['crank_angle'], high)
                self.assertEqual(sim.state['ones.turn'], held)


if __name__ == '__main__':
    unittest.main()
