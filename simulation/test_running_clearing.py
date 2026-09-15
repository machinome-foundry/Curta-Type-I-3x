"""Production rack law: real station timing, retained zero, selective sweeps."""

import unittest

from solid_node.node import AssemblyNode
from solid_node.motion.joints import Revolute
from solid_node.motion.ports import Time
from solid_node.simulation import Driver, Sim
from simulation.running_laws import clearing_travel
from simulation.running_parts import RESULT_DIALS, TURNS_DIALS


def fixture(place, digit, counter=False, lifted=True):
    zero = (TURNS_DIALS if counter else RESULT_DIALS)[place][1]

    class Wheel(AssemblyNode):
        turn = Revolute(axis=(1, 0, 0))

        def simulate(self):
            if self.turn.value is None:
                self.turn = zero - 36 * digit

    class Rack(AssemblyNode):
        time = Time.running()
        ring = Driver(default=0)
        lift = Driver(default=6 if lifted else 0)
        wheel = Wheel()
        (ring & lift & wheel.turn).drives(wheel.turn,
            law=lambda sources, target: lambda ring, lift, own:
            clearing_travel(ring, lift, own, zero, place, counter))

    return Rack()


class RunningClearingTest(unittest.TestCase):
    def test_all_digits_at_every_station_clear_in_either_direction(self):
        for counter, table in ((False, RESULT_DIALS), (True, TURNS_DIALS)):
            for place, (_, zero) in enumerate(table):
                for digit in range(10):
                    for direction in (-1, 1):
                        with self.subTest(counter=counter, place=place, digit=digit,
                                          direction=direction):
                            sim = Sim(fixture(place, digit, counter), dt=1)
                            sim.move('ring', by=direction * 360, duration=1)
                            sim.run(1)
                            error = (sim.state['wheel.turn'] - zero + 180) % 360 - 180
                            self.assertLessEqual(abs(error), .500000001)
                            held = sim.state['wheel.turn']
                            saved = sim.snapshot()
                            sim.move('ring', by=direction * 360, duration=1)
                            sim.run(1)
                            self.assertEqual(sim.state['wheel.turn'], held)
                            expected = sim.snapshot()
                            sim.restore(saved)
                            sim.move('ring', by=direction * 360, duration=1)
                            sim.run(1)
                            self.assertEqual(sim.snapshot(), expected)

    def test_opposite_half_sweeps_reach_different_registers(self):
        for direction in (-1, 1):
            for counter in (False, True):
                sim = Sim(fixture(0, 5, counter), dt=.1)
                initial = sim.state['wheel.turn']
                sim.move('ring', by=direction * 180, duration=1)
                sim.run(1)
                reached = (direction < 0) != counter
                self.assertEqual(sim.state['wheel.turn'] != initial, reached)

    def test_seated_carriage_does_not_clear(self):
        sim = Sim(fixture(0, 5, lifted=False), dt=.1)
        initial = sim.state['wheel.turn']
        sim.move('ring', by=-360, duration=1)
        sim.run(1)
        self.assertEqual(sim.state['wheel.turn'], initial)
