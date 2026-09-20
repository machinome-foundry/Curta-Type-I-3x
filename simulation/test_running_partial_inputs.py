"""Characterize admitted partial settings without pretending they are detents.

This does not certify missing whole-machine interlocks. It prevents an
admitted partial input from acting through fictional fractional teeth.
"""

import unittest
from machinome.simulation import Sim
from simulation.running import OperatingCurta, register_reading


class RunningPartialInputTest(unittest.TestCase):
    def test_partial_selector_uses_actual_teeth_and_keeps_its_history(self):
        sim = Sim(OperatingCurta(), dt=.2)
        sim.move('digit_1', to=.25)
        self.assertEqual(register_reading(sim), 0)
        sim.move('crank_rotation', by=360, duration=2)
        sim.run(2)
        # The lower source row at this height has ten teeth. The geometric
        # bench proves each passage, independently of this retained result.
        self.assertEqual(register_reading(sim), 10)
        self.assertAlmostEqual(sim.state['digit_1'], .25)
        saved = sim.snapshot()

        def resume():
            sim.move('digit_1', to=0)
            self.assertEqual(register_reading(sim), 10)
            sim.move('crank_rotation', by=360, duration=2)
            sim.run(2)
            self.assertEqual(register_reading(sim), 10)
            self.assertEqual(register_reading(sim, True), 2)

        resume()
        expected = sim.snapshot()
        sim.restore(saved)
        resume()
        self.assertEqual(sim.snapshot(), expected)
