"""Measured carriage-cover fits; no upstream print or STEP file is edited.

The covers keep their corrected datum and dial windows. Bounded thread/seat
lapping now clears their source overlap while retaining axial capture. The
clearing ring, axle bearings and carrier keep their already-tested placements.
See docs/measurements.md for the rejected axle translations and local contacts.
"""

import cadquery as cq
import manifold3d as manifold
import numpy as np
import trimesh
from machinome.parameters import Length
from simulation.print_parts import DigitsCover, UpperHousing
from simulation.standard.parts import DigitsAxle
from simulation.clearing_stop_spring import ClearingPinCarrier

SEAT_GAP = .05
# Measured in the recentered carriage, from the seventeen source axle axes.
AXLE_ANGLES = (*range(0, -181, -20), 160, *range(130, 29, -20))


def mesh_solid(mesh):
    # Keep source coordinates in double precision until the final STL write.
    body = manifold.Manifold(manifold.Mesh64(
        np.array(mesh.vertices, dtype=np.float64, order='C', copy=True),
        np.array(mesh.faces, dtype=np.uint64, order='C', copy=True)))
    if body.status() != manifold.Error.NoError:
        raise ValueError(f'Invalid source cover: {body.status()}')
    return body


def fitted_mesh(body):
    if body.status() != manifold.Error.NoError:
        raise ValueError(f'Invalid cover fit: {body.status()}')
    mesh = body.to_mesh64()
    return trimesh.Trimesh(vertices=mesh.vert_properties[:, :3], faces=mesh.tri_verts, process=False)


class FittedDigitsCover(DigitsCover):
    """Face .10 mm off the inner top land, leaving .05 mm below the ring."""
    rim_relief = Length(.1, min=0)

    def adjust(self, mesh):
        # Local -Z is upward. The ring's R61.5 underside is world Z43.6;
        # this land starts at 43.65. Neither clearing groove nor window moves.
        tool = manifold.Manifold.cylinder(self.rim_relief + SEAT_GAP, 61.5 + SEAT_GAP,
                                          circular_segments=360).translate((0, 0, -12-SEAT_GAP))
        return fitted_mesh(mesh_solid(mesh) - tool)


class FittedUpperHousing(UpperHousing):
    """Seventeen axle-end pockets and a bounded fit of the mating thread/seat."""
    seat_gap = Length(SEAT_GAP, min=0)
    thread_gap = Length(.05, min=0)
    thread_radial_gap = Length(.02, min=0)
    thread_mesh_precision = Length(.000008, min=0)

    def adjust(self, mesh):
        body = self.fitted_body(mesh)
        if self.thread_gap:
            # Reset only the generated Boolean's face provenance so coplanar
            # triangles from different cutters can be collapsed together.
            # Keeping those artificial seams leaves edges that collapse on a
            # binary-STL round trip. No source mesh is repaired or welded.
            body = body.as_original().simplify(self.thread_mesh_precision)
        return fitted_mesh(body)

    def fitted_body(self, mesh):
        body = mesh_solid(mesh)
        # Axles are R2.945 at world Z33.9, outer ends on R73.574057463.
        # Housing local Z = world Z + 4.35 and its installed clocking is 160°.
        # The 2 mm tools span R71.65..73.65, not the outer threaded wall.
        pocket = manifold.Manifold.cylinder(2, 2.945+self.seat_gap, circular_segments=128)
        # Half a facet avoids a cutter edge coincident with an original radial
        # seam, which otherwise leaves zero-thickness fins on STL conversion.
        pocket = pocket.rotate((0, 0, 180/128)).rotate((0, 90, 0)).translate((71.65, 0, 38.25))
        for angle in AXLE_ANGLES:
            body = body - pocket.rotate((0, 0, angle-160))
        if self.thread_gap:
            # The source threads interfere at the window-aligned placement.
            # Lap only this mating thread/seat zone against the unchanged
            # male print, with an explicit axial assembly allowance. Relative
            # placement is transcribed from standard.layers.CarriageCovers;
            # the later common carriage recentering cancels out here.
            mate = trimesh.load_mesh(DigitsCover.stl_source)
            mate.apply_transform(trimesh.transformations.rotation_matrix(
                np.radians(-180), (.168920173, .985629735, 0)))
            mate.apply_transform(trimesh.transformations.rotation_matrix(
                np.radians(-160.549916905), (0, 0, 1)))
            mate.apply_translation((0, 0, 36))
            male = mesh_solid(mate)
            # A sampled union or a scaled male leaves slivers at thread-root
            # edges. Dilate the actual mating surface continuously instead:
            # +/- .02 mm in X/Y and +/- .05 mm axially, bounded below to the
            # measured thread/seat zone. Neither printed part is scaled.
            slab = manifold.Manifold.cube((152, 152, 7)).translate((-76, -76, 35.65))
            allowance = manifold.Manifold.cube((2*self.thread_radial_gap,
                2*self.thread_radial_gap, 2*self.thread_gap), center=True)
            tool = (male ^ slab).minkowski_sum(allowance)
            outside = manifold.Manifold.cylinder(6.5, 75, circular_segments=720)
            inside = manifold.Manifold.cylinder(6.5, 71.9, circular_segments=720)
            zone = (outside - inside).translate((0, 0, 35.9))
            body = body - (tool ^ zone)
        return body


class FittedDigitsAxle(DigitsAxle):
    """Extend the outer retaining flat .15 mm; keep the entire 54 mm bearing."""
    flat_extension = Length(.15, min=0)

    def adjust(self, shape):
        tool = cq.Solid.makeBox(3.1, 6, 1.8+self.flat_extension, cq.Vector(-4, -3, 0))
        return shape.cut(tool)


class FittedAxleCarrier(ClearingPinCarrier):
    digits_axle_1 = FittedDigitsAxle()
    digits_axle_2 = FittedDigitsAxle()
    digits_axle_3 = FittedDigitsAxle()
    digits_axle_4 = FittedDigitsAxle()
    digits_axle_5 = FittedDigitsAxle()
    digits_axle_6 = FittedDigitsAxle()
    digits_axle_7 = FittedDigitsAxle()
    digits_axle_8 = FittedDigitsAxle()
    digits_axle_9 = FittedDigitsAxle()
    digits_axle_10 = FittedDigitsAxle()
    digits_axle_11 = FittedDigitsAxle()
    digits_axle_12 = FittedDigitsAxle()
    digits_axle_13 = FittedDigitsAxle()
    digits_axle_14 = FittedDigitsAxle()
    digits_axle_15 = FittedDigitsAxle()
    digits_axle_16 = FittedDigitsAxle()
    digits_axle_17 = FittedDigitsAxle()
