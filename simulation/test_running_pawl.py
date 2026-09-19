"""The finite return must stay in the real ratchet's released clearance."""

from simulation.test_pawl import PawlTest
from simulation.pawl import RELEASE, TOOTH_PITCH, CLOSING_RELEASE
from simulation.running_pawl import ContinuousPawlBench, RETURN_SPAN
from simulation.running_pawl import RetainedPawlBench
from machinome.test import TestCase
from machinome.simulation import Sim


class ContinuousPawlTest(PawlTest):
    node = ContinuousPawlBench

    def test_complete_finite_release_path_clears_the_disc(self):
        releases = [RELEASE + tooth * TOOTH_PITCH for tooth in (0, 1, 20, 60, 97)]
        releases += [CLOSING_RELEASE, CLOSING_RELEASE + TOOTH_PITCH]
        for release in releases:
            for index in range(11):
                self.node.set_state(crank_turns=(release + RETURN_SPAN * index / 10) / 360)
                self.assertNotIntersecting(self.node.disc,
                                           self.node.pawl.reverse_rotation_prevention_pawl)


class RetainedPawlGeometryTest(TestCase):
    node = RetainedPawlBench

    def test_forward_return_and_reverse_seating_clear_the_actual_disc(self):
        sim = Sim(self.node, dt=.1, meshes=True)
        releases = [RELEASE + tooth * TOOTH_PITCH for tooth in (0, 1, 20, 60, 97)]
        releases += [CLOSING_RELEASE, CLOSING_RELEASE + TOOTH_PITCH]
        for release in releases:
            for offset in (-.3, 0, .001, .003, .005, .2):
                sim.move('crank_turns', to=(release + offset) / 360)
                self.assertNotIntersecting(self.node.disc,
                                           self.node.pawl.reverse_rotation_prevention_pawl)
            sim.move('crank_turns', by=-1 / 360)
            self.assertNotIntersecting(self.node.disc,
                                       self.node.pawl.reverse_rotation_prevention_pawl)
            try:
                self.assertBlockedBeyond(self.node.disc, .001,
                    against=self.node.pawl.reverse_rotation_prevention_pawl,
                    axis=(0, 0, -1), directions='forward')
            except AssertionError as error:
                error.add_note(f'release={release}; crank={sim.state["disc.turn"]}; '
                               f'pawl={sim.state["pawl.reverse_rotation_prevention_pawl.turn"]}')
                raise
