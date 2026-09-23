"""Face only the grip's lower seat, keeping its bore and retaining-screw end."""

import cadquery as cq
from simulation.standard.parts import CrankHandle

GRIP_SEAT_GAP = .05


class SeatedCrankGrip(CrankHandle):
    """A .05 mm lower-face gap avoids a numerically crossed flush seat."""

    def adjust(self, shape):
        box = shape.BoundingBox()
        # The source bottom plane is Z=0; a BRep bounding box includes its
        # tolerance padding and is not the machining datum.
        seat = cq.Solid.makeBox(box.xlen + 2, box.ylen + 2, .1,
                               cq.Vector(box.xmin - 1, box.ymin - 1,
                                         GRIP_SEAT_GAP - .1))
        return shape.cut(seat).clean()
