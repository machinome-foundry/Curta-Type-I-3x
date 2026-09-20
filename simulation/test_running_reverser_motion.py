"""Retained requests must move the actual fork, all six inputs and follower."""

import numpy as np
from machinome.simulation import Sim
from machinome.test import TestCase
from simulation.running_reverser_motion import RunningReverserMotion
from simulation.test_reverser_assembly import INPUTS
from simulation.reverser_following import RADIAL
from simulation.reverser_detent_motion import ball_radius_at, SOURCE_BALL_Z


class RunningReverserMotionTest(TestCase):
    node = RunningReverserMotion

    def test_installed_requests_move_one_connected_bank_and_preserve_mounts(self):
        sim = Sim(self.node, dt=.1, meshes=True)
        lever = self.node.main_drive.reversing_lever.reversing_lever_1
        knob = lever.reversing_lever_knob_1.reversing_lever_knob
        fork = lever.reversing_lever_knob_1.reversing_actuator
        gears = [getattr(getattr(self.node.transmission.turns, name), member)
                 for name, member in INPUTS]
        moving = [knob, fork, *gears]
        original = [part.mesh.vertices.copy() for part in moving]
        fixed = [lever.reversing_shaft, lever.upper_reversing_lever_spacer,
                 lever.lower_reversing_lever_spacer, self.node.frame.upper_frame.main_body]
        seats = [part.mesh.vertices.copy() for part in fixed]
        try:
            self.assertAlmostEqual(lever.reversing_shaft.mesh.bounds[1, 2], -11.7, delta=.001)
            for height in (-4.9425, -5.5, -6.9425, 0, 3.9075):
                sim.move('reverser_height', to=height)
                for part, points in zip(moving, original):
                    np.testing.assert_allclose(part.mesh.vertices,
                                               points+(0, 0, height-3.9075), atol=.00001, rtol=0)
                for part, points in zip(fixed, seats):
                    np.testing.assert_array_equal(part.mesh.vertices, points)
                center = lever.p_5mm_ball.mesh.bounds.mean(axis=0)
                radius = ball_radius_at(SOURCE_BALL_Z+height-1.9)
                expected = np.array((17.613968679, 54.210221429, -53.7575+height))+np.array(RADIAL)*radius
                np.testing.assert_allclose(center, expected, atol=.015, rtol=0)
                self.assertNotIntersecting(knob, self.node.enclosure.lower_housing_1.bottom_housing)
                self.assertNotIntersecting(knob, lever.upper_reversing_lever_spacer)
                for gear in gears:
                    self.assertNotIntersecting(gear, fork)
                    self.assertBlockedBeyond(gear, .3, against=fork, along=(0, 0, 1))
                self.assertNotIntersecting(lever.selector_knob_spring.wire, knob)
                self.assertNotIntersecting(lever.selector_knob_spring.wire, lever.p_5mm_ball)
        finally:
            sim.reset()
