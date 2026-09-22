"""Operating outer-rim seat for the counter body below the clearing cover.

The native common is exactly the R46.8..48.75 annulus, .8 mm deep at the
source top face. Relieve that land with a named .05 mm radial/axial gap;
keep the body datum and every inner bearing, indexing pocket and bore.
"""

import cadquery as cq
from machinome.parameters import Length
from simulation.carriage_frame_fit import FittedCounterBody


class ClearingSeatCounterBody(FittedCounterBody):
    clearing_seat_depth = Length(.85, min=0)
    clearing_seat_radius = Length(46.75, min=0)

    def adjust(self, shape):
        shape = super().adjust(shape)
        origin = cq.Vector(0, 0, -1)
        outer = cq.Solid.makeCylinder(48.8, 1+self.clearing_seat_depth, origin)
        inner = cq.Solid.makeCylinder(self.clearing_seat_radius,
                                      1+self.clearing_seat_depth, origin)
        return shape.cut(outer.cut(inner)).clean()
