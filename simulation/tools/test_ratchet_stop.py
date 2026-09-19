"""Geometry evidence for the open running anti-reversal diagnostic."""

from machinome.test import TestCase
from simulation.pawl import RELEASE, TOOTH_PITCH, CLOSING_RELEASE
from simulation.tools.ratchet_stop import StopProbe


class SeatedStopTest(TestCase):
    node = StopProbe

    def test_seated_pawl_meets_the_measured_backstop(self):
        releases = [RELEASE + index * TOOTH_PITCH for index in (0, 1, 20, 60, 97)]
        releases += [CLOSING_RELEASE, CLOSING_RELEASE + TOOTH_PITCH]
        for release in releases:
            self.node.set_state(crank_turns=(release - .2) / 360)
            pawl = self.node.pawl.reverse_rotation_prevention_pawl
            self.assertNotIntersecting(self.node.disc, pawl)
            self.assertBlockedBeyond(self.node.disc, .001, against=pawl,
                                     axis=(0, 0, -1), directions='forward')
