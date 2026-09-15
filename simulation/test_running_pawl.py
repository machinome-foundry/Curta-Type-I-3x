"""The finite return must stay in the real ratchet's released clearance."""

from simulation.test_pawl import PawlTest
from simulation.pawl import RELEASE, TOOTH_PITCH, CLOSING_RELEASE
from simulation.running_pawl import ContinuousPawlBench, RETURN_SPAN


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
