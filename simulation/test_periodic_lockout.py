"""A long request must meet the same first closing surface as a short one."""

import unittest

from machinome.simulation import Sim
from simulation.periodic_lockout import PeriodicLockoutBench, FixedLockoutBench


class PeriodicLockoutTest(unittest.TestCase):
    def check_request(self, model, target, duration=None):
        sim = Sim(model(), dt=.1, state={'digit': 3, 'crank_height': 0})
        sim.move('crank_angle', to=120)
        sim.move('digit', to=0)
        self.assertAlmostEqual(sim.state['ones.turn'], 189.6, places=8)
        request = sim.move('crank_angle', to=target, **(
            {} if duration is None else {'duration': duration}))
        if duration is not None:
            sim.run(duration)
        self.assertEqual(request.status, 'blocked')
        self.assertAlmostEqual(sim.state['crank_angle'], 125.22, places=7)
        self.assertAlmostEqual(sim.state['ones.turn'], 189.6, places=8)

    def test_fixed_local_surface_stops_long_request(self):
        self.check_request(FixedLockoutBench, 840)

    def test_periodic_surface_stops_short_request(self):
        self.check_request(PeriodicLockoutBench, 150)

    def test_periodic_surface_stops_long_request(self):
        self.check_request(PeriodicLockoutBench, 840)

    def test_periodic_surface_stops_timed_long_request(self):
        self.check_request(PeriodicLockoutBench, 840, duration=2)
