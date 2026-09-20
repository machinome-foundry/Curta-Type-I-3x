"""Physical stroke limits stop Python requests, not just viewer sliders."""

import unittest

from machinome.node import AssemblyNode
from machinome.motion.ports import Time
from machinome.simulation import Driver, Sim
from simulation.running_parts import RunningMainDrive, RunningReverser


class CrankLiftBench(AssemblyNode):
    time = Time.running()
    crank_elevation = Driver(default=0, unit='mm')
    crank_rotation = Driver(default=0, unit='deg')
    drive = RunningMainDrive()
    crank_elevation.drives(drive.subtract, ratio=1 / 9)
    crank_rotation.drives(drive.turn)


class ReverserLiftBench(AssemblyNode):
    time = Time.running()
    height = Driver(default=3.9075, unit='mm')
    lever = RunningReverser()
    height.drives(lever.displacement)


class ReverserLiftTest(unittest.TestCase):
    def test_window_and_spacer_bound_motion_but_the_lower_pocket_does_not(self):
        sim = Sim(ReverserLiftBench(), dt=.1)
        key = 'lever.reversing_lever_knob_1.lift'
        for target in (-4.9425, -5.5):
            command = sim.move('height', to=target)
            self.assertEqual(command.status, 'completed')
            self.assertAlmostEqual(sim.state[key], target)
        for target, admitted in ((-8, -6.9425), (6, 3.9075)):
            command = sim.move('height', to=target)
            self.assertEqual(command.status, 'blocked')
            self.assertAlmostEqual(sim.state[key], admitted)
            self.assertAlmostEqual(sim.state['lever.p_5mm_ball.lift'], admitted)
            self.assertAlmostEqual(sim.state['lever.selector_knob_spring.lift'], admitted)


class CrankLiftTest(unittest.TestCase):
    def test_crank_cannot_lift_past_subtraction_stroke(self):
        sim = Sim(CrankLiftBench(), dt=.1)
        sim.move('crank_elevation', to=12, duration=1)
        sim.run(1)
        self.assertAlmostEqual(sim.state['drive.crank.lift'], 9)
        self.assertAlmostEqual(sim.state['drive.stepped_drum.lift'], 9)
        sim.move('crank_elevation', to=0, duration=1)
        sim.run(1)
        self.assertAlmostEqual(sim.state['drive.crank.lift'], 0)

    def test_crank_cannot_sink_below_addition_seat(self):
        sim = Sim(CrankLiftBench(), dt=.1)
        sim.move('crank_elevation', to=-3, duration=1)
        sim.run(1)
        self.assertAlmostEqual(sim.state['drive.crank.lift'], 0)
        self.assertAlmostEqual(sim.state['drive.stepped_drum.lift'], 0)
