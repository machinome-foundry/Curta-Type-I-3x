"""Native reverse-contact angles with the actual pawl seated on its spring."""

import json
import logging
from machinome.test import TestCase
from simulation.pawl import AntiReversal, PawlBench, RELEASE, TOOTH_PITCH, CLOSING_RELEASE, RAMP


class SeatedPawl(AntiReversal):
    pawl_drive = AntiReversal.turn.drives(
        AntiReversal.reverse_rotation_prevention_pawl.turn, ratio=0, offset=RAMP[0][1])


class StopProbe(PawlBench):
    pawl = SeatedPawl()


def probe():
    logging.disable(logging.INFO)
    model = StopProbe()
    model.set_state(crank_turns=0)
    model.assemble()
    model.build_stls()
    checks = TestCase()
    releases = [RELEASE + index * TOOTH_PITCH for index in (0, 1, 20, 60, 97)]
    releases += [CLOSING_RELEASE, CLOSING_RELEASE + TOOTH_PITCH]
    for release in releases:
        def clear(angle):
            model.set_state(crank_turns=angle / 360)
            try:
                checks.assertNotIntersecting(model.disc, model.pawl.reverse_rotation_prevention_pawl)
            except AssertionError:
                return False
            return True
        low, high = release - .5, release + .005
        assert not clear(low)
        assert clear(high)
        for _ in range(20):
            middle = (low + high) / 2
            if clear(middle):
                high = middle
            else:
                low = middle
        print(json.dumps({'release': release, 'last_contact': low, 'first_free': high,
                          'free_offset_from_release': high - release}), flush=True)


if __name__ == '__main__':
    probe()
