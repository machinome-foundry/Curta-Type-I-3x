"""Conservative sphere/mesh clearance over radial, lift and collar-shift domains.

An outward polyhedron encloses the unchanged native sphere and its source mesh.
Convex hulls cover affine movement; an outward face-plane expansion bounds the
curvature of collar-relative angular arcs. No positive-volume epsilon is used.
"""

import json
import logging
from math import cos, radians, sin
import time

import numpy as np
import trimesh
import cadquery as cq

from machinome.simulation import Sim
from machinome.exact import intersect_shapes
from simulation.running import OperatingCurta
from simulation.positioning_ball_profiles import BELL_ENVELOPE, COLLAR_ENVELOPE, collar_limit
from simulation.tools.positioning_ball_contact import BALL, BELL, COLLAR, FRAME
from simulation.tools.positioning_ball_ring import RING
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


def plane_distances(mesh, centre):
    return np.einsum('ij,ij->i', mesh.face_normals, mesh.triangles_center-centre)


def enclose(meshes, padding):
    combined = meshes[0]
    for mesh in meshes[1:]:
        combined = combined + mesh
    hull = combined.convex_hull
    assert hull.is_watertight and hull.is_winding_consistent
    centre = hull.center_mass
    clearance = float(plane_distances(hull, centre).min())
    assert clearance > 0
    # Every supporting plane moves outward by at least padding. The result
    # therefore contains the hull's Euclidean padding-neighbourhood.
    hull.vertices = centre + (hull.vertices-centre)*(1+padding/clearance)
    return mesh_solid(hull)


def main():
    started = time.monotonic()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    saved = dict(sim.state)
    leaves = dict(rigid_leaves(sim.node))
    native = world_solids(sim.node, selected={BALL})[BALL]
    assert native.isValid() and len(native.Faces()) == 1 and native.Faces()[0].geomType() == 'SPHERE'
    native_radius = (native.Volume()*3/(4*np.pi))**(1/3)
    centre = np.asarray(native.Center().toTuple())
    np.testing.assert_allclose(centre, (9.627860318, 0, 30), atol=1e-9, rtol=0)
    actual_radius = float(np.linalg.norm(leaves[BALL].mesh.vertices-centre, axis=1).max())
    assert native_radius < 3.751 and actual_radius < 3.751
    sphere = trimesh.creation.icosphere(subdivisions=3, radius=1)
    sphere.vertices *= 3.751/float(plane_distances(sphere, np.zeros(3)).min()) + .000001
    assert plane_distances(sphere, np.zeros(3)).min() > 3.751
    outer = float(np.linalg.norm(sphere.vertices, axis=1).max())
    assert outer < 3.78

    def placement(radius, lift=0, angle=0):
        mesh = sphere.copy()
        mesh.vertices += (radius, 0, 30-lift)
        theta = radians(angle)
        rotation = np.array(((cos(theta), -sin(theta), 0),
                             (sin(theta), cos(theta), 0), (0, 0, 1)))
        mesh.vertices = mesh.vertices @ rotation.T
        return mesh

    frame = mesh_solid(leaves[FRAME].mesh)
    ring = mesh_solid(leaves[RING].mesh)
    collar = mesh_solid(leaves[COLLAR].mesh)
    bell = mesh_solid(leaves[BELL].mesh)
    radial = (8.332, 11.950)
    frame_enclosure = enclose([placement(r) for r in radial], .000001)
    ring_enclosure = enclose([placement(r, lift) for r in radial for lift in (0, 6)], .000001)
    assert faceted_common_volume(frame_enclosure ^ frame) == 0
    assert faceted_common_volume(ring_enclosure ^ ring) == 0
    native_frame = world_solids(sim.node, selected={FRAME})[FRAME]
    native_sweep = cq.Solid.makeCylinder(3.751, radial[1]-radial[0],
        (radial[0], 0, 30), (1, 0, 0)).fuse(
            cq.Solid.makeSphere(3.751, (radial[0], 0, 30), angleDegrees1=-90),
            cq.Solid.makeSphere(3.751, (radial[1], 0, 30), angleDegrees1=-90)).clean()
    native_common = intersect_shapes(native_frame, native_sweep, FRAME, 'conservative ball sweep')
    assert native_common.isValid() and native_common.Volume() == 0
    print(json.dumps(dict(kind='frame-and-ring', whole_radial_domain=radial,
        ring_lift_domain=[0, 6], sphere_encloser_outer_radius_mm=outer,
        sphere_minimum_support_distance_mm=float(plane_distances(sphere, np.zeros(3)).min()),
        frame_mm3=0, native_frame_mm3=0, ring_mm3=0)), flush=True)

    checks, accepted = 0, 0

    def prove(l0, l1, a0, a1, depth=0):
        nonlocal checks, accepted
        meshes = []
        for lift in (l0, l1):
            upper = float(collar_limit(lift))+9.627860318+.000001
            for radius in (8.332, upper):
                for angle in (a0, a1):
                    meshes.append(placement(radius, lift, -angle))
        # Every endpoint vertex is within radius16 of the Z axis. Its arc
        # lies within this sagitta of the chord joining its two endpoints.
        # Lift and radial bounds interpolate affinely inside each profile
        # knot interval; their intermediate sets are convex combinations.
        padding = 16*(1-cos(radians(a1-a0)/2))+.000001
        hull = enclose(meshes, padding)
        common = faceted_common_volume(hull ^ collar)
        checks += 1
        if common == 0:
            accepted += 1
            return
        assert depth < 12, (l0, l1, a0, a1, common, 'unresolved enclosure')
        mid = (a0+a1)/2
        prove(l0, l1, a0, mid, depth+1)
        prove(l0, l1, mid, a1, depth+1)

    lifts = [float(lift) for lift, _ in COLLAR_ENVELOPE]
    for l0, l1 in zip(lifts, lifts[1:]):
        for a0 in range(0, 100, 5):
            prove(l0, l1, a0, a0+5)
        print(json.dumps(dict(kind='collar-lift-interval', lower=l0, upper=l1,
            checks=checks, certified_intervals=accepted)), flush=True)
    collar_checks, collar_accepted = checks, accepted
    profile = np.asarray(BELL_ENVELOPE)

    def prove_bell(a0, a1, depth=0):
        nonlocal checks, accepted
        lower = [float(np.interp(a, profile[:, 0], profile[:, 1]))-.000001
                 for a in (a0, a1)]
        endpoints = [placement(radius, angle=a)
                     for a, lo in zip((a0, a1), lower) for radius in (lo, 11.950)]
        theta = radians(a1-a0)
        # For a rotated point whose radial coordinate changes affinely,
        # ||p''|| <= theta²*16 + 2*|theta|*|delta_radius|. Its distance from
        # the endpoint chord is bounded by max||p''||/8 on the unit interval.
        # This includes every retained radius between the linear lower
        # envelope and constant upper bound, not only the two boundary paths.
        padding = (theta*theta*16+2*abs(theta)*abs(lower[1]-lower[0]))/8+.000001
        hull = enclose(endpoints, padding)
        common = faceted_common_volume(hull ^ bell)
        checks += 1
        if common == 0:
            accepted += 1
            return
        assert depth < 14, (a0, a1, common, 'unresolved bell enclosure')
        mid = (a0+a1)/2
        prove_bell(a0, mid, depth+1)
        prove_bell(mid, a1, depth+1)

    for a0, a1 in zip(profile[:-1, 0], profile[1:, 0]):
        prove_bell(float(a0), float(a1))
        print(json.dumps(dict(kind='bell-angle-interval', start=float(a0), end=float(a1),
            checks=checks-collar_checks, certified_intervals=accepted-collar_accepted)), flush=True)
    assert dict(sim.state) == saved
    print(json.dumps(dict(kind='finished', checks=checks, certified_intervals=accepted,
        seconds=time.monotonic()-started, bank_unchanged=True,
        collar_checks=collar_checks, bell_checks=checks-collar_checks,
        acceptance='Continuous native frame and sphere/mesh frame, ring, collar and bell interfaces; other neighbours separate')), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
