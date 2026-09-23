"""Local experiment only: full angular/bank acceptance remains outstanding."""

import simulation.test_running_reverser_wrong_order as contracts
from simulation.reverser_contact_trial import LocalReverserContactTrial


class LocalReverserContactTrialTest(contracts.RunningReverserWrongOrderTest):
    model = LocalReverserContactTrial

    def test_long_request_cannot_cross_contact_into_a_later_clear_band(self):
        sim = contracts.prepare(self.model)
        saved = sim.snapshot()
        original = dict(sim.state)
        request = sim.move('reverser_height', to=-3)
        self.assertEqual(request.status, 'blocked')
        self.assertGreaterEqual(sim.state['reverser_height'], contracts.FIRST_CONTACT)
        self.assertLess(sim.state['reverser_height'], 3.9075)
        self.assertEqual(contracts.commons(sim), (0, 0))
        expected = sim.snapshot()
        request = sim.move('reverser_height', to=-3)
        self.assertEqual(request.status, 'blocked')
        self.assertEqual(sim.snapshot(), expected)
        sim.restore(saved)
        sim.move('reverser_height', to=-3)
        self.assertEqual(sim.snapshot(), expected)
        self.assertEqual(sim.state['crank_rotation'], original['crank_rotation'])
        self.assertEqual(sim.state['transmission.turns.ones.turn'],
                         original['transmission.turns.ones.turn'])
        # Relief is an explicit user request, not scheduled completion.
        self.assertEqual(sim.move('reverser_height', to=3.9075).status, 'completed')
        self.assertEqual(sim.snapshot(), saved)
