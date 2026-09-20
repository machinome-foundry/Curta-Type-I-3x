"""Native closing-disc contact with a retained, partly rotated ones shaft.

No running stop is adopted from these samples alone. The complete retained
probe independently identifies this disc/lockout pair before it is isolated.
"""

import json
import logging
from simulation.standard.parts import ResultsLockingDisc
from simulation.fit import FittedCarryLockout


def main():
    logging.disable(logging.INFO)
    disc = ResultsLockingDisc().shape().translate((0, 0, -23.1))
    pentagon = FittedCarryLockout().shape()
    for edge in disc.Edges():
        box = edge.BoundingBox()
        if abs(box.zmax-box.zmin) < 1e-7 and abs(box.zmin+23.1) < 1e-7:
            print(json.dumps({'disc_edge': edge.geomType(),
                              'ends': [edge.positionAt(t).toTuple() for t in (0, 1)],
                              'radius': edge.radius() if edge.geomType() == 'CIRCLE' else None}), flush=True)
    for phase in sorted(set([4+2*i for i in range(37)]+[45.6])):
        lockout = pentagon.rotate((0, 0, 0), (0, 0, 1), phase).translate((40.5, 0, -22.65))

        def volume(crank):
            common = lockout.intersect(disc.rotate((0, 0, 0), (0, 0, 1), -crank))
            assert common.isValid()
            return common.Volume()

        assert volume(100) == 0, (phase, 'not free at probe start')
        if volume(180) == 0:
            print(json.dumps({'shaft_phase': phase, 'closed_disc_clear': True}), flush=True)
            continue
        free, blocked = 100, 150
        assert volume(blocked) > 0
        for _ in range(20):
            middle = (free+blocked)/2
            if volume(middle) > 0:
                blocked = middle
            else:
                free = middle
        print(json.dumps({'shaft_phase': phase, 'last_free': free,
                          'first_contact': blocked, 'closed_overlap_mm3': volume(180)}), flush=True)


if __name__ == '__main__':
    main()
