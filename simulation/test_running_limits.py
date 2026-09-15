"""Physical stroke limits stop Python requests, not just viewer sliders."""

import unittest

from solid_node.node import AssemblyNode
from solid_node.motion.ports import Time
from solid_node.simulation import Driver, Sim
from simulation.running_parts import RunningMainDrive


class CrankLiftBench(AssemblyNode):
    time = Time.running()
    crank_elevation = Driver(default=0, unit='mm')
    crank_rotation = Driver(default=0, unit='deg')
    drive = RunningMainDrive()
    crank_elevation.drives(drive.subtract, ratio=1 / 9)
    crank_rotation.drives(drive.turn)


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
