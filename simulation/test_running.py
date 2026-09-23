"""Retained motion comes from the actual Curta, not the calculator page."""

import unittest

from machinome.simulation import Sim
from machinome.test import TestCase
from simulation.running import OperatingCurta, register_reading
from simulation.contracts import assert_connected_material


class OperatingCurtaIntegrityTest(TestCase):
    node = OperatingCurta

    def test_solid_integrity(self):
        def check(node):
            if node.rigid or not node.children:
                assert_connected_material(node.mesh)
                if node.exact:
                    self.assertEqual(len(node.shape().Solids()), 1, node.name)
            else:
                for child in node.children:
                    check(child)
        check(self.node)

    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)


class RunningCurtaTest(unittest.TestCase):
    model = OperatingCurta

    def test_every_selector_moves_independently_without_driving_a_register(self):
        sim = Sim(self.model(), dt=.1)
        settings = [0] * 8
        for index in (8, 1, 5, 2, 7, 3, 6, 4):
            settings[index - 1] = index
            sim.move(f'digit_{index}', to=index)
            for place, digit in enumerate(settings, 1):
                key = (f'input_selectors.selectors.digit_selector_axle_{place}'
                       '.selector_shaft_bottom.turn')
                self.assertAlmostEqual(sim.state[key], 36 * digit)
            self.assertEqual(register_reading(sim), 0)
            self.assertEqual(register_reading(sim, True), 0)

    def test_subtraction_borrows_through_both_registers_and_addition_undoes_it(self):
        sim = Sim(self.model(), dt=.1)
        sim.move('digit_1', to=1)
        sim.move('crank_elevation', to=9)
        sim.move('crank_rotation', by=360, duration=2)
        sim.run(2)
        self.assertEqual(register_reading(sim), 10 ** 11 - 1)
        self.assertEqual(register_reading(sim, True), 10 ** 6 - 1)
        sim.move('crank_elevation', to=0)
        sim.move('crank_rotation', by=360, duration=2)
        sim.run(2)
        self.assertEqual(register_reading(sim), 0)
        self.assertEqual(register_reading(sim, True), 0)

    def test_shift_reassociates_actual_dials_without_changing_retained_values(self):
        sim = Sim(self.model(), dt=.1)
        sim.move('digit_1', to=9)
        sim.move('crank_rotation', by=360, duration=2)
        sim.run(2)
        sim.move('carriage_elevation', to=6)
        sim.move('carriage_rotation', to=40)
        self.assertEqual(register_reading(sim), 9)
        self.assertEqual(register_reading(sim, True), 1)
        sim.move('carriage_elevation', to=0)
        sim.move('digit_1', to=3)
        sim.move('crank_rotation', by=360, duration=2)
        sim.run(2)
        self.assertEqual(register_reading(sim), 309)
        self.assertEqual(register_reading(sim, True), 101)

    def test_independent_inputs_and_two_successive_additions(self):
        machine = self.model()
        sim = Sim(machine, dt=.1)
        self.assertTrue(sim.running)
        self.assertEqual(register_reading(sim), 0)
        self.assertEqual(register_reading(sim, True), 0)
        sim.move('digit_1', to=3)
        sim.move('crank_rotation', by=360, duration=2)
        sim.run(2)
        self.assertEqual(register_reading(sim), 3)
        self.assertEqual(register_reading(sim, True), 1)
        sim.move('digit_1', to=2)
        self.assertEqual(register_reading(sim), 3)
        sim.move('crank_rotation', by=360, duration=2)
        sim.run(2)
        self.assertEqual(register_reading(sim), 5)
        self.assertEqual(register_reading(sim, True), 2)
        sim.move('carriage_elevation', to=6, duration=.2)
        sim.run(.2)
        self.assertEqual(register_reading(sim), 5)
        sim.move('clearing_rotation', by=180, duration=.2)
        sim.run(.2)
        self.assertEqual(register_reading(sim), 0)
        self.assertEqual(register_reading(sim, True), 2)
        sim.move('clearing_rotation', by=180, duration=.2)
        sim.run(.2)
        self.assertEqual(register_reading(sim, True), 0)
        cleared = sim.snapshot()
        sim.move('clearing_rotation', by=-360, duration=.2)
        sim.run(.2)
        self.assertEqual(register_reading(sim), 0)
        self.assertEqual(register_reading(sim, True), 0)
        expected = sim.snapshot()
        sim.restore(cleared)
        sim.move('clearing_rotation', by=-360, duration=.2)
        sim.run(.2)
        self.assertEqual(sim.snapshot(), expected)

    def test_manual_calibration_carries(self):
        machine = self.model()
        sim = Sim(machine, dt=.1)
        for turns, (units, tens, expected) in enumerate(
                ((0, 0, 0), (1, 0, 1), (9, 0, 10), (0, 9, 100)), 1):
            sim.move('digit_1', to=units)
            sim.move('digit_2', to=tens)
            command = sim.move('crank_rotation', by=360, duration=2)
            sim.run(2)
            self.assertEqual(command.status, 'completed')
            self.assertEqual(register_reading(sim), expected)
            self.assertEqual(register_reading(sim, True), turns)

    def test_partial_crank_release_and_snapshot_replay(self):
        machine = self.model()
        sim = Sim(machine, dt=.1)
        sim.move('digit_1', to=9)
        sim.move('crank_rotation', by=90, duration=.5)
        sim.run(.5)
        saved = sim.snapshot()
        sim.move('crank_rotation', by=270, duration=1.5)
        sim.run(1.5)
        expected = sim.snapshot()
        self.assertEqual(register_reading(sim), 9)
        sim.restore(saved)
        sim.move('crank_rotation', by=270, duration=1.5)
        sim.run(1.5)
        self.assertEqual(sim.snapshot(), expected)
