"""Operating clearing-pin lower-end fit, leaving the entire cam follower intact."""

import cadquery as cq
from machinome.parameters import Length
from simulation.standard.parts import ClearingPin

# Source pin tip Z21.6 minus rest cam depression 3.089172 is Z18.510828.
# The frame land is Z21. Face 2.54 mm off only the bottom tip, leaving a
# .050828 mm gap at rest without moving the proven head, shoulder or sleeve.
PIN_TIP_FACING = 2.54
FRAME_GAP = .05
FREE_PIN_DROP = 21.6 + PIN_TIP_FACING - 21 - FRAME_GAP


class FittedClearingPin(ClearingPin):
    bottom_facing = Length(PIN_TIP_FACING, min=0)

    def adjust(self, shape):
        box = shape.BoundingBox()
        tool = cq.Solid.makeBox(box.xlen + 2, box.ylen + 2, self.bottom_facing + 1,
                                cq.Vector(box.xmin - 1, box.ymin - 1, box.zmin - 1))
        return shape.cut(tool)
