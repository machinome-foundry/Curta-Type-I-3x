"""Collar/spider shoulder-facing fit and its independent measuring bench.

The source underside is local Z39 (world 46.8); the installed source spider
mount reaches world 47.47. The trial measures an additional .05 mm seating
gap without moving either part. The separate operating-collar trial combines
this fit with measured collar/nut clocking; the default root is unchanged.
Thread, bore, carrier-pin and full-neighbour contracts are separate from this
shoulder bench. Upstream print files stay untouched.
"""

import manifold3d as manifold

from machinome.node import AssemblyNode
from machinome.parameters import Length
from simulation.cover_fits import mesh_solid, fitted_mesh
from simulation.print_parts import CrankCollar
from simulation.spider import SpiderMount, SEAT_GAP


class TrialShoulderCollar(CrankCollar):
    shoulder_facing = Length(.72, min=0, max=.72)

    def adjust(self, mesh):
        if not self.shoulder_facing:
            return mesh
        # Continue the source stem's actual faceted outer surface through
        # the faced band. A round R17.95 tool left a colliding annular lip;
        # an R17.941 tool crossed source facets and left STL-encoding slivers.
        # Slice the unchanged straight stem at local Z38 instead. The R17
        # disc fills that section's R16.559 bore without changing its outside.
        body = mesh_solid(mesh)
        stem = body.slice(38) + manifold.CrossSection.circle(17, 128)
        retained = stem.extrude(self.shoulder_facing)
        outer = manifold.Manifold.cylinder(self.shoulder_facing, 24.05,
                                            circular_segments=720)
        tool = (outer - retained).translate((0, 0, 39))
        return fitted_mesh(body - tool)


class CollarShoulderBench(AssemblyNode):
    collar = TrialShoulderCollar()
    spider = SpiderMount()

    def render(self):
        self.collar.rotate(-144.282220532, (0, 0, 1)).translate((0, 0, 7.8))
        # The operating carriage's recentering cancels the spider's source
        # XY/clocking transform; its named carrier gap remains independent.
        self.spider.translate((0, 0, 45.2 + SEAT_GAP))


class UnfittedCollarShoulderBench(CollarShoulderBench):
    """Placement witness and zero-facing negative control."""
    collar = TrialShoulderCollar(shoulder_facing=0)
