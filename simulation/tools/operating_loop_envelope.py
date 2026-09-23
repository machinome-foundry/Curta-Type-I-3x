"""Conservative installed-loop clearance from the central upper mechanism.

The permitted loop lift is 0..6 mm. Central neighbours rotate only about Z;
crank/drum lift by 0..9 mm, and carriage neighbours by 0..6 mm. Crop each
neighbour to the entire potentially relevant height range, then prove that
crop lies inside an R28.6 cylinder. A full deployment certificate against
that cylinder covers every relative Z-axis phase and permitted lift of those
named neighbours, not just the sampled crank angles. Other neighbours and
mounting-seat contacts have separate installed and isolated gates.
"""

import argparse
import json
import logging
from math import cos, pi
from pathlib import Path

import cadquery as cq
import manifold3d as manifold
import numpy as np

from machinome.simulation import Sim
from simulation.tools.interference import world_solids, rigid_leaves
from simulation.tools.clearing_loop_sweep import mesh_solid, certify_rotation


CENTRAL = (
    'Curta.frame.upper_frame.main_body',
    'Curta.main_drive.crank.crank_handle_1.main_crank',
    'Curta.main_drive.stepped_drum.main_axle_step_drum_1.main_axle_step_drum_top_1',
    'Curta.carry_mechanism.tens_bell.tens_bell_1',
    'Curta.carry_mechanism.tens_bell.tens_bell_c_clip',
    'Curta.carry_mechanism.tens_bell.retaining_ring_for_tens_bell',
    'Curta.carriage.positioning.carriage_spring_sleeve',
    'Curta.carriage.positioning.spring_sleeve_c_clip',
    'Curta.carriage.registers.carrier.crank_collar',
    'Curta.carriage.registers.carrier.crank_collar_washer',
)
LOOP = 'Curta.carriage.registers.clearing_ring.clearing_ring'
PIVOT = (39.372124643, 10.943003894, 0.)
RADIUS = 28.6


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists():
        raise FileExistsError('Preserve earlier envelope evidence')
    logging.disable(logging.INFO)
    from simulation.clearing_loop_operating_trial import LoopOperatingTrial
    report = {'validation': 'pending', 'radius_mm': RADIUS,
              'deployment_degrees': [-.4, 90.4], 'neighbours': [], 'paths': {}}
    try:
        root = LoopOperatingTrial()
        sim = Sim(root, dt=.1, meshes=True)
        nodes = dict(rigid_leaves(root))
        solids = world_solids(root, selected={*CENTRAL, LOOP})
        initial_vertices = nodes[LOOP].mesh.vertices.copy()
        base_loop = mesh_solid(nodes[LOOP].mesh)
        box = solids[LOOP].BoundingBox()
        # World height is unchanged by deployment; carriage adds 0..6 mm.
        low_loop, high_loop = box.zmin, box.zmax + 6
        report['loop_height_envelope_mm'] = [low_loop, high_loop]
        for path in CENTRAL:
            rise = (9 if path.startswith('Curta.main_drive.') else
                    6 if path.startswith('Curta.carriage.') else 0)
            low, high = low_loop-rise, high_loop
            slab = cq.Solid.makeBox(400, 400, high-low, cq.Vector(-200, -200, low))
            cylinder = cq.Solid.makeCylinder(RADIUS, high-low, cq.Vector(0, 0, low))
            row = {'part': path, 'permitted_rise_mm': [0, rise],
                   'source_height_interval_mm': [low, high]}
            if path in solids:
                outside = solids[path].intersect(slab).cut(cylinder)
                assert outside.isValid(), path
                row['native_outside_volume_mm3'] = outside.Volume()
                assert outside.Volume() == 0, row
            else:
                row['native'] = 'source-STL; published mesh only'
            crop = mesh_solid(nodes[path].mesh) ^ manifold.Manifold.cube(
                (400, 400, high-low)).translate((-200, -200, low))
            assert crop.status() == manifold.Error.NoError, path
            vertices = np.asarray(crop.to_mesh64().vert_properties)[:, :3]
            radial = (float(np.linalg.norm(vertices[:, :2], axis=1).max())
                      if len(vertices) else 0.)
            row['mesh_maximum_radius_mm'] = radial
            # The cylinder is convex: containing every triangle vertex also
            # contains its face interior, not merely a point sample.
            assert radial < RADIUS, row
            report['neighbours'].append(row)
            print(json.dumps(row), flush=True)

        radius = max(np.hypot(x-PIVOT[0], y-PIVOT[1])
                     for x in (box.xmin, box.xmax) for y in (box.ymin, box.ymax))
        radius = max(radius, np.linalg.norm(initial_vertices[:, :2]-PIVOT[:2], axis=1).max())
        for deployment in (-.4, 45, 90.4):
            request = sim.move('loop_deployment', to=deployment)
            assert request.status == 'completed'
            angle = np.radians(-deployment)
            rotation = np.array(((np.cos(angle), -np.sin(angle), 0),
                                 (np.sin(angle), np.cos(angle), 0), (0, 0, 1)))
            expected = (initial_vertices-PIVOT) @ rotation.T + PIVOT
            np.testing.assert_allclose(nodes[LOOP].mesh.vertices, expected, rtol=0, atol=1e-7)
        # An explicitly circumscribed prism contains the analytic cylinder.
        # The additional .001 mm avoids resting on floating-point tangency.
        mesh_cylinder = manifold.Manifold.cylinder(
            100, (RADIUS+.001)/cos(pi/128), circular_segments=128)
        native_cylinder = cq.Solid.makeCylinder(RADIUS, 100)
        for kernel in ('native', 'mesh64'):
            if kernel == 'native':
                common = solids[LOOP].intersect(native_cylinder)
                assert common.isValid() and common.Volume() == 0

                def gap_at(angle, cap):
                    return solids[LOOP].rotate(PIVOT, (*PIVOT[:2], 1), angle).distance(
                        native_cylinder.copy())
            else:
                common = base_loop ^ mesh_cylinder
                assert common.status() == manifold.Error.NoError and common.volume() == 0

                def gap_at(angle, cap):
                    moved = base_loop.translate(tuple(-v for v in PIVOT)).rotate(
                        (0, 0, angle)).translate(PIVOT)
                    return moved.min_gap(mesh_cylinder, cap)
            rows = certify_rotation(gap_at, float(radius), low=-90.4, high=.4)
            report['paths'][kernel] = rows
            print(json.dumps({'kernel': kernel, 'certified_intervals': len(rows)}), flush=True)
        report['validation'] = 'passed'
    except Exception as error:
        report['validation'] = 'failed'
        report['failure'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        args.report.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
