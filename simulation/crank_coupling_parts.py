"""Coaxial crank seat with a bounded internal roof relief.

The R4.56 source bore is about .349 mm off the R4.4425 drum shaft. Move the
whole handle assembly onto the unchanged shaft/pin datum. The shaft tip is
world Z88.95 while the source internal roof starts at Z88.35; extend that
pocket to Z89.00 for .05 mm clearance without touching its transverse bore.
"""

import cadquery as cq
from simulation.standard.parts import MainCrank
from simulation.standard.assembly import CrankHandle1
from simulation.standard.layers import CrankAssembly
from simulation.crank_grip_parts import SeatedCrankGrip


class SeatedMainCrank(MainCrank):
    linear_deflection = .01
    angular_deflection = .1

    def adjust(self, shape):
        pocket = cq.Solid.makeCylinder(4.56, .70, cq.Vector(0, 0, 28.45))
        return shape.cut(pocket).clean()


class SeatedCrankHandle(CrankHandle1):
    main_crank = SeatedMainCrank()
    crank_handle = SeatedCrankGrip()

    def render(self):
        super().render()
        self.translate((-.091031728, .337283020, 0))


class SeatedCrankAssembly(CrankAssembly):
    crank_handle_1 = SeatedCrankHandle()
