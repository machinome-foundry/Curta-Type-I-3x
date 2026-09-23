"""Bounded lower-face seating fit; all upstream source files stay untouched."""

import cadquery as cq
from simulation.standard.parts import ReverseNosePlate

SEAT_GAP = .05
DRUM_LAND_RADIUS = 9


class SeatedReverseNosePlate(ReverseNosePlate):
    """Relieve the lower mating sector, retaining the upper axial stop."""
    linear_deflection = .01
    angular_deflection = .1

    def adjust(self, shape):
        # Source coordinates: local +Z faces the drum below the plate.
        seat = cq.Solid.makeCylinder(DRUM_LAND_RADIUS + SEAT_GAP, .15,
                                     cq.Vector(-14.4, 0, 3 - SEAT_GAP))
        return shape.cut(seat).clean()
