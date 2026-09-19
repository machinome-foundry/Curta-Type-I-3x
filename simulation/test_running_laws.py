"""Contact-law probes: prescribed inputs, not an alternate calculator."""

import unittest

from machinome.node import AssemblyNode
from machinome.motion.joints import Prismatic
from machinome.motion.ports import Time
from machinome.math import piecewise
from machinome.simulation import Driver, Sim
from simulation.carry_profiles import PIN_DROP
from simulation.running_laws import lever_motion
from simulation.running_pawl import ContinuousPawlBench


class RunningPawlBench(ContinuousPawlBench):
    time = Time.running()


class Lever(AssemblyNode):
    travel = Prismatic(axis=(0, 0, 1))

    def simulate(self):
        if self.travel.value is None:
            self.travel = -4.2


class PinAndReset(AssemblyNode):
    time = Time.running()
    crank = Driver(default=0)
    carriage = Driver(default=0)
    lift = Driver(default=0)
    wheel = Driver(default=-146)
    lever = Lever()
    (crank & carriage & lift & lever.travel & wheel).drives(
        lever.travel, law=lever_motion(1, -4.2))


class RunningContactTest(unittest.TestCase):
    def test_lifting_the_carriage_releases_unlatched_pin_preload(self):
        sim = Sim(PinAndReset(), dt=.1)
        sim.move('wheel', by=-9 * 36, duration=1)
        sim.run(1)
        sim.move('lift', to=6, duration=1)
        sim.run(1)
        self.assertAlmostEqual(sim.state['lever.travel'], -4.2, places=7)

    def test_pawl_returns_after_each_revolution(self):
        sim = Sim(RunningPawlBench(), dt=.1)
        key = 'pawl.reverse_rotation_prevention_pawl.turn'
        initial = sim.state[key]
        sim.move('crank_turns', by=1, duration=1)
        sim.run(1)
        self.assertAlmostEqual(sim.state[key], initial, places=7)

    def test_reset_does_not_push_through_a_parked_nine_pin(self):
        sim = Sim(PinAndReset(), dt=.1)
        sim.move('wheel', by=-9 * 36, duration=1)
        sim.run(1)
        expected = -4.2 + piecewise(9, PIN_DROP)
        self.assertAlmostEqual(sim.state['lever.travel'], expected, places=7)
        sim.move('crank', by=-360, duration=1)
        sim.run(1)
        self.assertAlmostEqual(sim.state['lever.travel'], expected, places=7)

    def test_pin_latches_and_reset_releases_the_actual_slider(self):
        sim = Sim(PinAndReset(), dt=.1)
        sim.move('wheel', by=-10 * 36, duration=1)
        sim.run(1)
        self.assertAlmostEqual(sim.state['lever.travel'], 0, places=7)
        sim.move('crank', by=-360, duration=1)
        sim.run(1)
        self.assertAlmostEqual(sim.state['lever.travel'], -4.2, places=7)
