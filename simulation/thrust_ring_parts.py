"""Local underside passage; the complete upper and outer ring seats remain."""

import cadquery as cq
from machinome.parameters import Length
from simulation.standard.parts import ThrustRing


# Independent measured ball-centre range and source ring installation, not
# imports from a trial motion law or acceptance-region module.
CENTRE_INNER = 8.332135134696959
CENTRE_OUTER = 11.949090957641602
BALL_Z_IN_RING = -3.05
RING_PHASE = 35.717779468


def radial_passage(gap):
    radius = 3.75 + gap
    start = (CENTRE_INNER, 0, BALL_Z_IN_RING)
    end = (CENTRE_OUTER, 0, BALL_Z_IN_RING)
    cylinder = cq.Solid.makeCylinder(radius, CENTRE_OUTER-CENTRE_INNER,
                                    start, (1, 0, 0))
    first = cq.Solid.makeSphere(radius, start, angleDegrees1=-90)
    last = cq.Solid.makeSphere(radius, end, angleDegrees1=-90)
    return cylinder.fuse(first, last).clean().rotate(
        (0, 0, 0), (0, 0, 1), -RING_PHASE)


class BallPassageThrustRing(ThrustRing):
    running_gap = Length(.05, min=.04, max=.06)
    linear_deflection = .005
    angular_deflection = .1

    def adjust(self, shape):
        return shape.cut(radial_passage(self.running_gap)).clean()
