"""Acceptance for a physical reversing input, independent of crank mode."""

import unittest
from machinome.simulation import Sim
from simulation.running import OperatingCurta, register_reading

LOWER = -4.9425
UPPER = 3.9075


class RunningReverserTest(unittest.TestCase):
    def test_unseated_lever_produces_its_actual_unwanted_counter_entry(self):
        sim = Sim(OperatingCurta(), dt=.2)
        sim.move('reverser_height', to=-3)
        sim.move('crank_rotation', by=360, duration=2)
        sim.run(2)
        # The native/faceted contact bench independently proves one driving
        # tooth at each of these six heights. Do not replace this by +/-1.
        self.assertEqual(register_reading(sim), 0)
        self.assertEqual(register_reading(sim, True), 111111)
        self.assertAlmostEqual(sim.state['reverser_height'], -3)
        self.assertEqual(sim.state['crank_elevation'], 0)

    def test_detent_is_not_an_invented_hard_stop(self):
        sim = Sim(OperatingCurta(), dt=.1)
        key = 'main_drive.reversing_lever.reversing_lever_1.reversing_lever_knob_1.lift'
        sim.move('reverser_height', to=LOWER)
        command = sim.move('reverser_height', to=-5.5)
        self.assertEqual(command.status, 'completed')
        self.assertAlmostEqual(sim.state[key], -5.5)
        self.assertEqual(register_reading(sim, True), 0)
        command = sim.move('reverser_height', to=-8)
        self.assertEqual(command.status, 'blocked')
        self.assertAlmostEqual(sim.state[key], -6.9425)
        command = sim.move('reverser_height', to=6)
        self.assertEqual(command.status, 'blocked')
        self.assertAlmostEqual(sim.state[key], UPPER)

    def test_counter_direction_changes_without_recomputing_result_or_history(self):
        sim = Sim(OperatingCurta(), dt=.1)
        sim.move('digit_1', to=3)
        sim.move('crank_rotation', by=360, duration=2)
        sim.run(2)
        self.assertEqual((register_reading(sim), register_reading(sim, True)), (3, 1))
        sim.move('reverser_height', to=LOWER)
        self.assertEqual((register_reading(sim), register_reading(sim, True)), (3, 1))
        sim.move('crank_rotation', by=360, duration=2)
        sim.run(2)
        self.assertEqual((register_reading(sim), register_reading(sim, True)), (6, 0))
        sim.move('crank_elevation', to=9)
        sim.move('crank_rotation', by=360, duration=2)
        sim.run(2)
        self.assertEqual((register_reading(sim), register_reading(sim, True)), (3, 1))
        sim.move('reverser_height', to=UPPER)
        sim.move('crank_rotation', by=360, duration=2)
        sim.run(2)
        self.assertEqual((register_reading(sim), register_reading(sim, True)), (0, 0))

    def test_both_counter_directions_at_every_carriage_shift_and_crank_mode(self):
        # A second tick size also checks that tooth/carry event subdivision,
        # not coincidental alignment with the .1 s history test, controls totals.
        sim = Sim(OperatingCurta(), dt=.2)
        empty = sim.snapshot()
        for shift in range(6):
            for subtract in (False, True):
                for reversed_counter in (False, True):
                    with self.subTest(shift=shift, subtract=subtract, reversed_counter=reversed_counter):
                        # Fixture isolation only: restore the untouched initial
                        # run, never seed a result or synthesize operation history.
                        sim.restore(empty)
                        sim.move('digit_1', to=3)
                        sim.move('carriage_elevation', to=6)
                        sim.move('carriage_rotation', to=20*shift)
                        sim.move('carriage_elevation', to=0)
                        sim.move('crank_elevation', to=9*subtract)
                        sim.move('reverser_height', to=LOWER if reversed_counter else UPPER)
                        sim.move('crank_rotation', by=360, duration=2)
                        sim.run(2)
                        self.assertEqual(register_reading(sim),
                            ((-1 if subtract else 1)*3*10**shift) % 10**11)
                        self.assertEqual(register_reading(sim, True),
                            ((-1 if subtract != reversed_counter else 1)*10**shift) % 10**6)
                        print(f'PASS shift={shift}, subtract={subtract}, reverse={reversed_counter}: '
                              f'result={register_reading(sim)}, counter={register_reading(sim, True)}',
                              flush=True)

    def test_partial_lever_request_keeps_other_controls_and_replays(self):
        sim = Sim(OperatingCurta(), dt=.1)
        sim.move('digit_1', to=7)
        sim.move('reverser_height', to=0, duration=.4)
        sim.run(.4)
        saved = sim.snapshot()
        self.assertEqual(register_reading(sim), 0)
        self.assertEqual(register_reading(sim, True), 0)
        self.assertEqual(sim.state['main_drive.crank.turn'], 0)
        self.assertEqual(sim.state['main_drive.crank.lift'], 0)
        self.assertEqual(sim.state['carriage.registers.lift'], 0)
        sim.move('reverser_height', to=LOWER, duration=.4)
        sim.run(.4)
        expected = sim.snapshot()
        sim.restore(saved)
        sim.move('reverser_height', to=LOWER, duration=.4)
        sim.run(.4)
        self.assertEqual(sim.snapshot(), expected)
