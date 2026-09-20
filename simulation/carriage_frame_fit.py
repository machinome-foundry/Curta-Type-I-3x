"""Bounded underside fits; keep the carriage's indexing keys and all axes.

The source frame's seventeen bearing bosses meet the carriage's annular land
between Z24.9 and Z25.8. Their entire native intersection lies outside R31.75
and inside R34.2. Relieve only that annulus, plus a .05 mm facing of the bottom
to leave actual clearance when the indexing keys disengage at the 6 mm lift.
"""

import cadquery as cq
from machinome.parameters import Length
from simulation.standard.parts import CounterBody

BOSS_INNER_RADIUS = 31.7
BOSS_OUTER_RADIUS = 34.25
KEY_ROOF_Z = 14.1
KEY_ROOF_INNER_RADIUS = 21.9


class FittedCounterBody(CounterBody):
    bottom_facing = Length(.05, min=0)
    boss_facing = Length(.95, min=0)
    roof_facing = Length(.05, min=0)
    linear_deflection = .01
    angular_deflection = .1

    def adjust(self, shape):
        box = shape.BoundingBox()
        bottom = cq.Solid.makeBox(box.xlen + 2, box.ylen + 2, self.bottom_facing + 1,
                                  cq.Vector(box.xmin - 1, box.ymin - 1,
                                            box.zmax - self.bottom_facing))
        origin = cq.Vector(0, 0, box.zmax - self.boss_facing)
        outer = cq.Solid.makeCylinder(BOSS_OUTER_RADIUS, self.boss_facing + 1, origin)
        inner = cq.Solid.makeCylinder(BOSS_INNER_RADIUS, self.boss_facing + 1, origin)
        # The source pocket roofs touch the frame's two indexing-key tops at
        # world Z30.9 (local Z14.1). Deepen their existing ceilings, not their
        # vertical flanks: a thin source-derived skin cannot cut through a key.
        roof_origin = cq.Vector(0, 0, KEY_ROOF_Z - self.roof_facing)
        roof_outer = cq.Solid.makeCylinder(BOSS_OUTER_RADIUS, self.roof_facing, roof_origin)
        roof_inner = cq.Solid.makeCylinder(KEY_ROOF_INNER_RADIUS, self.roof_facing, roof_origin)
        roof_faces = [face for face in shape.Faces()
                      if face.geomType() == 'PLANE'
                      and abs(face.Center().z - KEY_ROOF_Z) < 1e-6
                      and face.normalAt().z > .999]
        if len(roof_faces) != 1:
            raise ValueError('Expected the single source indexing-pocket ceiling at Z14.1')
        roof_skin = cq.Solid.extrudeLinear(roof_faces[0], (0, 0, -self.roof_facing))
        roof_skin = roof_skin.intersect(roof_outer.cut(roof_inner))
        return shape.cut(bottom).cut(outer.cut(inner)).cut(roof_skin)
