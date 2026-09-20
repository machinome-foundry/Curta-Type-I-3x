"""Measure the unmodified loop against its actual mounted neighbours."""

import json
import logging
import manifold3d as manifold
from simulation.clearing_loop import LoopMountBench
from simulation.tools.interference import world_solids, rigid_leaves
from simulation.tools.carry_phase import solid


def probe():
    logging.disable(logging.INFO)
    bench = LoopMountBench()
    bench.set_state(deployment=0, release_height=0)
    bench.assemble()
    bench.build_stls()
    paths = dict(rigid_leaves(bench))
    moving_path = 'Curta.loop.clearing_ring'
    selected = {moving_path, 'Curta.loop.clearing_ring_rivet_1',
                'Curta.loop.clearing_ring_rivet_2', 'Curta.loop.clearing_cover',
                'Curta.carrier.crank_collar', 'Curta.carrier.crank_collar_washer',
                'Curta.carrier.crank_collar_nut', 'Curta.covers.upper_housing',
                'Curta.covers.digits_cover'}
    selected.update(path for path in paths if path.startswith('Curta.crank.'))
    native = world_solids(bench, selected=selected)
    for path in sorted(selected):
        if path not in paths:
            raise ValueError(f'Missing mounted neighbour: {path}')
        print(json.dumps({'part': path, 'bounds': paths[path].mesh.bounds.tolist(),
                          'kernel': 'exact' if path in native else 'source STL'}), flush=True)
    for height in (0, .05, .5, 3, 8):
        for angle in range(-180, 181, 15):
            bench.set_state(deployment=angle, release_height=height)
            moving = world_solids(bench, selected={moving_path})[moving_path]
            mesh = solid(paths[moving_path].mesh)
            overlaps = {}
            for path in sorted(selected - {moving_path}):
                if path in native:
                    common = moving.intersect(native[path])
                    if not common.isValid():
                        raise ValueError((height, angle, path, 'invalid native intersection'))
                    volume = common.Volume()
                else:
                    common = mesh ^ solid(paths[path].mesh)
                    if common.status() != manifold.Error.NoError:
                        raise ValueError((height, angle, path, str(common.status())))
                    volume = common.volume()
                if volume > 0:
                    overlaps[path] = volume
            print(json.dumps({'height': height, 'swivel': angle,
                              'overlap_mm3': overlaps}), flush=True)


if __name__ == '__main__':
    probe()
