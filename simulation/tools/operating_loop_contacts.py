"""Inventory replacement mounting contacts on the complete retained root.

Every positive common is reported without a volume epsilon. This sampled
diagnostic is not a continuous clearance certificate or whole-machine proof.
"""

import argparse
import json
import logging
from pathlib import Path

import manifold3d as manifold
import numpy as np

from machinome.simulation import Sim
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.tools.clearing_loop_sweep import mesh_solid


PREFIX = 'Curta.carriage.registers.clearing_ring.'
PARTS = tuple(PREFIX + name for name in (
    'clearing_ring', 'clearing_ring_rivet_1', 'clearing_ring_rivet_2'))


def mounting_contacts(root, *, native=False):
    meshes = {path: part.mesh.copy() for path, part in rigid_leaves(root)}
    bounds = {path: mesh.bounds for path, mesh in meshes.items()}
    exact = world_solids(root) if native else {}
    solids = {}
    examined = set()
    result = {'rigid_occurrences': len(meshes), 'tested_pairs': 0,
              'positive_commons_mm3': {}, 'refusals': {},
              'nonpositive_signed_sums_mm3': {}}

    def solid(path):
        if path not in solids:
            solids[path] = mesh_solid(meshes[path])
        return solids[path]

    for first in PARTS:
        for second in meshes:
            pair = tuple(sorted((first, second)))
            if first == second or pair in examined:
                continue
            examined.add(pair)
            a, b = bounds[first], bounds[second]
            if not np.all(np.minimum(a[1], b[1]) > np.maximum(a[0], b[0])):
                continue
            result['tested_pairs'] += 1
            key = ' / '.join(pair)
            try:
                if first in exact and second in exact:
                    common = exact[first].intersect(exact[second])
                    if not common.isValid():
                        raise ValueError('Invalid native common')
                    volume = common.Volume()
                else:
                    common = solid(first) ^ solid(second)
                    if common.status() != manifold.Error.NoError:
                        raise ValueError(str(common.status()))
                    volume = common.volume()
                if volume > 0:
                    result['positive_commons_mm3'][key] = volume
                elif volume < 0:
                    result['nonpositive_signed_sums_mm3'][key] = volume
            except Exception as error:
                result['refusals'][key] = f'{type(error).__name__}: {error}'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', action='store_true')
    parser.add_argument('--transport', action='store_true',
                        help='Also sample independent crank, carriage and clearing requests')
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists():
        raise FileExistsError('Preserve earlier contact evidence')
    logging.disable(logging.INFO)
    from simulation.clearing_loop_operating_trial import LoopOperatingTrial
    report = {'validation': 'pending', 'native_with_stl_fallback': args.native,
              'coverage': 'sampled three adapted leaves versus all rigid leaves',
              'samples': []}
    try:
        sim = Sim(LoopOperatingTrial(), dt=.1, meshes=True)
        nodes = dict(rigid_leaves(sim.node))
        originals = {path: nodes[path].mesh.vertices.copy() for path in PARTS}
        requests = [('loop_deployment', value) for value in (0, 30, 60, 90, 90.4, -.4, 0)]
        if args.transport:
            requests += [('loop_deployment', 90), ('crank_elevation', 9),
                         ('crank_rotation', 90), ('loop_deployment', 45),
                         ('crank_rotation', 360), ('carriage_elevation', 6)]
            requests += [('carriage_rotation', value) for value in (20, 40, 60, 80, 100)]
            requests += [('clearing_rotation', value) for value in (90, 180, 230, 360)]
            requests += [('carriage_elevation', 0), ('loop_deployment', 0)]

        def rotated(vertices, angle, pivot=(0, 0, 0)):
            theta = np.radians(angle)
            matrix = np.array(((np.cos(theta), -np.sin(theta), 0),
                               (np.sin(theta), np.cos(theta), 0), (0, 0, 1)))
            return (vertices-pivot) @ matrix.T + pivot

        for name, target in requests:
            command = sim.move(name, to=target, duration=.2)
            sim.run(.2)
            if command.status != 'completed':
                raise AssertionError(('requested motion', name, target, command.status))
            for path, original in originals.items():
                expected = original
                if path == PARTS[0]:
                    expected = rotated(expected, -sim.state['loop_deployment'],
                                       (39.372124643, 10.943003894, 0))
                expected = rotated(expected, sim.state['carriage_rotation']-
                                   sim.state['clearing_rotation'])
                expected = expected + (0, 0, sim.state['carriage_elevation'])
                np.testing.assert_allclose(nodes[path].mesh.vertices, expected,
                                           rtol=0, atol=1e-7, err_msg=path)
            sample = {'request': [name, target],
                      'deployment': sim.state['loop_deployment'],
                      'bank': dict(sim.state),
                      'transport_vertex_equivalence': True,
                      'contacts': mounting_contacts(
                sim.node, native=args.native)}
            report['samples'].append(sample)
            print(json.dumps({key: value for key, value in sample.items() if key != 'bank'}), flush=True)
        report['validation'] = ('failed' if any(
            row['contacts']['positive_commons_mm3'] or row['contacts']['refusals']
            for row in report['samples']) else 'passed')
        if report['validation'] != 'passed':
            raise AssertionError('Installed mounting has positive commons or refusals')
    except Exception as error:
        report['validation'] = 'failed'
        report['failure'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        args.report.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
