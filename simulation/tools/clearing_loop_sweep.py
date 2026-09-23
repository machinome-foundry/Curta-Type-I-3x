"""Conservative rotational-clearance check for the isolated replacement mount.

At every accepted interval, the midpoint separation exceeds the maximum
displacement of ANY loop point to either endpoint, plus a positive numerical
guard. This closes the gaps between sampled poses without waiving an overlap.
The native mode explicitly uses published Mesh64 for source-STL neighbours.
"""

import argparse
import json
import logging
from math import ceil, isfinite, radians, sin
from pathlib import Path
import manifold3d as manifold
import numpy as np

from simulation.tools.interference import rigid_leaves, world_solids


def certify_rotation(gap_at, radius, *, low=-90., high=0., guard=1e-5, max_depth=18):
    if not (isfinite(radius) and radius > 0 and guard > 0 and low < high):
        raise ValueError('Invalid separation proof bounds')
    # A small initial angular span gives the mesh distance query a tight
    # search cap. Far-away finger-loop triangles then need no pairwise search.
    divisions = ceil(high-low)
    pending = [(low+(high-low)*i/divisions, low+(high-low)*(i+1)/divisions, 0)
               for i in range(divisions)]
    accepted = []
    while pending:
        left, right, depth = pending.pop()
        middle = (left + right) / 2
        displacement = 2 * radius * sin(radians(right - left) / 4)
        gap = float(gap_at(middle, displacement + 2*guard))
        if not isfinite(gap) or gap <= guard:
            raise AssertionError(('no strict separation', middle, gap))
        if gap > displacement + guard:
            accepted.append({'from': left, 'to': right, 'gap': gap,
                             'displacement_bound': displacement})
        elif depth >= max_depth:
            raise AssertionError(('unproved interval', left, right, gap, displacement))
        else:
            pending.extend(((middle, right, depth + 1), (left, middle, depth + 1)))
    return accepted


def mesh_solid(mesh):
    result = manifold.Manifold(manifold.Mesh64(
        np.asarray(mesh.vertices, dtype=np.float64),
        np.asarray(mesh.faces, dtype=np.uint64)))
    if result.status() != manifold.Error.NoError:
        raise AssertionError(str(result.status()))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel', choices=('native', 'mesh64'), required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--source-trial', action='store_true')
    parser.add_argument('--low', type=float, default=-90.)
    parser.add_argument('--high', type=float, default=0.)
    args = parser.parse_args()
    if args.report.exists():
        raise FileExistsError('Preserve earlier sweep evidence')
    logging.disable(logging.INFO)
    if args.source_trial:
        from simulation.clearing_loop_seat import LoopSeatTrial
        root = LoopSeatTrial()
    else:
        from simulation.clearing_loop_mounting import ReplacementLoopBench
        root = ReplacementLoopBench()
    root.set_state(deployment=0, release_height=0)
    root.assemble()
    root.build_stls()
    nodes = dict(rigid_leaves(root))
    moving_path = 'Curta.loop.clearing_ring'
    selected = ['Curta.loop.clearing_ring_rivet_2', 'Curta.loop.clearing_ring_rivet_1',
                 'Curta.loop.clearing_cover', 'Curta.carrier.crank_collar',
                 'Curta.carrier.crank_collar_washer', 'Curta.carrier.crank_collar_nut',
                 'Curta.covers.upper_housing', 'Curta.covers.digits_cover']
    selected += [path for path in nodes if path.startswith('Curta.crank.')]
    natives = world_solids(root, selected={moving_path, *selected})
    meshes = {path: node.mesh.copy() for path, node in nodes.items()
              if path in {moving_path, *selected}}
    pivot = (39.372124643, 10.943003894, 0.)
    moving_mesh = mesh_solid(meshes[moving_path])
    moving_native = natives[moving_path]
    # A native bounding box encloses curved faces, not only their mesh vertices.
    box = moving_native.BoundingBox()
    radius = max(np.hypot(x-pivot[0], y-pivot[1])
                 for x in (box.xmin, box.xmax) for y in (box.ymin, box.ymax))
    radius = max(radius, np.linalg.norm(
        meshes[moving_path].vertices[:, :2] - pivot[:2], axis=1).max())
    # Independently calibrate the rotation against actual public node poses.
    for angle in (-90, -45, 0):
        root.set_state(deployment=angle, release_height=0)
        theta = radians(angle)
        matrix = np.array(((np.cos(theta), -np.sin(theta), 0),
                           (np.sin(theta), np.cos(theta), 0), (0, 0, 1)))
        expected = (meshes[moving_path].vertices - pivot) @ matrix.T + pivot
        np.testing.assert_allclose(nodes[moving_path].mesh.vertices, expected,
                                   rtol=0, atol=1e-7)
    report = {'validation': 'pending', 'kernel': args.kernel,
              'source_trial': args.source_trial, 'radius_bound_mm': float(radius),
              'range_degrees': [args.low, args.high],
              'numerical_separation_guard_mm': 1e-5, 'pairs': []}
    try:
        for path in selected:
            other_mesh = mesh_solid(meshes[path])
            native = args.kernel == 'native' and path in natives
            other = natives[path] if native else other_mesh
            initial = (moving_native.intersect(other) if native else moving_mesh ^ other)
            if native:
                if not initial.isValid() or initial.Volume() != 0:
                    raise AssertionError((path, 'initial native common', initial.Volume()))
            elif initial.status() != manifold.Error.NoError or initial.volume() != 0:
                raise AssertionError((path, 'initial mesh common', initial.volume()))
            if native:
                other_box = other.BoundingBox()
                z_gap = max(other_box.zmin-box.zmax, box.zmin-other_box.zmax)
            else:
                moving_bounds, other_bounds = meshes[moving_path].bounds, meshes[path].bounds
                z_gap = max(other_bounds[0, 2]-moving_bounds[1, 2],
                            moving_bounds[0, 2]-other_bounds[1, 2])
            if z_gap > 1e-5:
                row = {'part': path, 'kernel': 'native' if native else 'published-mesh64',
                       'invariant_z_gap_mm': float(z_gap), 'from': args.low, 'to': args.high}
                report['pairs'].append(row)
                print(json.dumps(row), flush=True)
                continue
            if native:
                def gap_at(angle, search_cap):
                    moved = moving_native.rotate(pivot, (pivot[0], pivot[1], 1), angle)
                    return moved.copy().distance(other.copy())
            else:
                def gap_at(angle, search_cap):
                    moved = (moving_mesh.translate(tuple(-v for v in pivot))
                             .rotate((0, 0, angle)).translate(pivot))
                    return moved.min_gap(other, search_cap)
            intervals = certify_rotation(gap_at, float(radius), low=args.low, high=args.high)
            row = {'part': path, 'kernel': 'native' if native else 'published-mesh64',
                   'intervals': intervals}
            report['pairs'].append(row)
            print(json.dumps({'part': path, 'kernel': row['kernel'],
                              'certified_intervals': len(intervals)}), flush=True)
        report['validation'] = 'passed'
    except Exception as error:
        report['validation'] = 'failed'
        report['failure'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        args.report.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
