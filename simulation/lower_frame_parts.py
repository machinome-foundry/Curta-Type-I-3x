"""Bounded upper key-seat fit for the concentric operating lower shell.

The source shell flank is u=11.4 and the installed frame flank u=11.01,
where u points at -40 degrees. Relieve only their upper seating band to
u=10.96, preserving the original deeper key and all external shell datums.
The lower bearing shoulder is faced .05 mm below its formerly flush seat;
its STL otherwise overlaps the bearing's rounded 20.1 mm source face.
"""

import cadquery as cq
from simulation.standard.parts import BottomHousing
from simulation.standard.assembly import LowerHousing1


class SeatedBottomHousing(BottomHousing):
    linear_deflection = .01
    angular_deflection = .1

    def adjust(self, shape):
        key = cq.Solid.makeBox(.49, 4, 3.9, cq.Vector(10.96, 61, 128.2)).rotate(
            (0, 0, 0), (0, 0, 1), -40)
        # Do not extend the key relief into the outer wall beyond the frame's
        # R64.4305 circular extent plus the declared .05 mm radial gap.
        key = key.intersect(cq.Solid.makeCylinder(64.4805, 4, cq.Vector(0, 0, 128.2)))
        shoulder = cq.Solid.makeCylinder(64.111, .1, cq.Vector(0, 0, 11.95))
        return shape.cut(key).cut(shoulder).clean()


class SeatedLowerHousing(LowerHousing1):
    bottom_housing = SeatedBottomHousing()
