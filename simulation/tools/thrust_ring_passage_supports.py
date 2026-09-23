"""Measure protected ring seats before cutting any passage. No model edits."""

import json
import logging
import time

import numpy as np

from machinome.simulation import Sim
from simulation.positioning_ball_trial import RadialBallTrial
from simulation.thrust_ring_trial import InstalledThrustBench
from simulation.thrust_ring_regions import permitted_world, permitted_faceted
from simulation.tools.positioning_ball_contact import BALL, COLLAR
from simulation.tools.positioning_ball_ring import RING
from simulation.tools.interference import world_solids, rigid_leaves
from simulation.tools.open_run_transitions import bounds
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


def main():
    started = time.monotonic()
    sim = Sim(RadialBallTrial(), dt=.1, meshes=True)
    native = world_solids(sim.node, selected={BALL, RING})
    ball, ring = native[BALL], native[RING]
    assert ball.isValid() and len(ball.Solids()) == 1
    assert len(ball.Faces()) == 1 and ball.Faces()[0].geomType() == 'SPHERE'
    centre = np.asarray(ball.Center().toTuple())
    np.testing.assert_allclose(centre, (9.627860318, 0, 30), atol=1e-9, rtol=0)
    radius = (ball.Volume()*3/(4*np.pi))**(1/3)
    assert abs(radius-3.75) < 1e-9
    leaves = dict(rigid_leaves(sim.node))
    max_mesh_radius = float(np.linalg.norm(leaves[BALL].mesh.vertices-centre, axis=1).max())
    assert max_mesh_radius < 3.751  # Recorded source STL approximation, not a clearance waiver.
    for face in ring.Faces():
        if face.geomType() == 'PLANE' and abs(face.Center().z-34.55) < 1e-8:
            assert face.intersect(permitted_world()).Area() == 0
    print(json.dumps(dict(kind='source', sphere_radius_mm=radius,
        max_mesh_radius_mm=max_mesh_radius, ring_bounds_mm=bounds(ring).tolist(),
        upper_plane_area_mm2=sum(f.Area() for f in ring.Faces()
            if f.geomType() == 'PLANE' and abs(f.Center().z-34.55) < 1e-8))), flush=True)

    fixture = InstalledThrustBench()
    fixture.set_state(travel=0, shift=0)
    fixture.assemble()
    fixture.build_stls()
    np.testing.assert_array_equal(fixture.thrust_ring.mesh.vertices, leaves[RING].mesh.vertices)
    np.testing.assert_allclose(fixture.collar.mesh.vertices, leaves[COLLAR].mesh.vertices,
                               atol=1e-9, rtol=0)
    region = permitted_faceted()
    rows = 0
    for lift in (0, 1.5, 3, 4.5, 6):
        for shift in range(-100, 101, 5):
            fixture.set_state(travel=lift, shift=shift)
            body = mesh_solid(fixture.thrust_ring.mesh)
            collar = mesh_solid(fixture.collar.mesh)
            support = body.translate((0, 0, -.1)) ^ collar
            support_volume = faceted_common_volume(support)
            assert support_volume > 0
            threatened = faceted_common_volume(support ^ region.translate((0, 0, lift-.1)))
            assert threatened == 0
            wire = mesh_solid(fixture.carriage_spring.wire.mesh).translate((0, 0, -.2))
            capture = body ^ wire
            capture_volume = faceted_common_volume(capture)
            assert capture_volume > 0
            assert faceted_common_volume(capture ^ region.translate((0, 0, lift))) == 0
            print(json.dumps(dict(kind='protected-seats', lift_mm=lift, shift_degrees=shift,
                collar_capture_mm3=support_volume, spring_capture_mm3=capture_volume,
                collar_bounds_mm=list(support.bounding_box()),
                spring_bounds_mm=list(capture.bounding_box()), threatened_mm3=threatened)), flush=True)
            rows += 1
    original_ring = leaves[RING].mesh.vertices.copy()
    original_ball = leaves[BALL].mesh.vertices.copy()
    assert sim.move('carriage_elevation', to=6).status == 'completed'
    moved = dict(rigid_leaves(sim.node))
    np.testing.assert_allclose(moved[RING].mesh.vertices, original_ring+(0, 0, 6), atol=1e-9, rtol=0)
    offset = sim.state['carriage.positioning.p_6mm_ball_419094.slide']
    np.testing.assert_allclose(moved[BALL].mesh.vertices, original_ball+(offset, 0, 0), atol=1e-9, rtol=0)
    raised_ring = moved[RING].mesh.vertices.copy()
    raised_ball = moved[BALL].mesh.vertices.copy()
    for shift in (20, 50, 100):
        assert sim.move('carriage_rotation', to=shift).status == 'completed'
        np.testing.assert_array_equal(moved[RING].mesh.vertices, raised_ring)
        np.testing.assert_array_equal(moved[BALL].mesh.vertices, raised_ball)
    print(json.dumps(dict(kind='finished', protected_rows=rows,
        actual_parent_frame_motion=True, ring_and_ball_do_not_follow_carriage_shift=True,
        seconds=time.monotonic()-started, acceptance='Independent region only; no fitted ring yet')), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
