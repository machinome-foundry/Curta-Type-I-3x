"""Bounded seat facings for the measured collar trial, not upstream edits.

The collar's local Z0 end stands at world Z7.8, flush with the fixed
frame floor. The washer's local Z0 face stands upside down at world Z60.3,
flush with the collar's retaining lip. Its other face, local Z3.2, lies
on the clearing cover at world Z57.1. A .05 mm axial facing at each seat
gives a real locational gap without translating any installed part.
The independent shoulder fit and pin/thread clocking remain separate.
"""

import cadquery as cq
import manifold3d as manifold

from simulation.collar_seat_trial import TrialShoulderCollar
from simulation.cover_fits import mesh_solid, fitted_mesh
from simulation.standard.parts import CrankCollarWasher


class SeatedCollar(TrialShoulderCollar):
    def adjust(self, mesh):
        shoulder = super().adjust(mesh)
        end_skin = manifold.Manifold.cube((100, 100, 1.05)).translate((-50, -50, -1))
        return fitted_mesh(mesh_solid(shoulder) - end_skin)


class SeatedCollarWasher(CrankCollarWasher):
    def adjust(self, shape):
        end_skin = cq.Solid.makeBox(100, 100, 1.05, cq.Vector(-50, -50, -1))
        cover_skin = cq.Solid.makeBox(100, 100, 1.05, cq.Vector(-50, -50, 3.15))
        return shape.cut(end_skin).cut(cover_skin).clean()
