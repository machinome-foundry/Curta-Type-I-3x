"""Small print-only check of radial ball travel in the actual knob bore."""

import json
from pathlib import Path
import manifold3d as manifold
import numpy as np
import trimesh


def solid(mesh):
    body = manifold.Manifold(manifold.Mesh64(
        np.array(mesh.vertices, dtype=np.float64, order='C', copy=True),
        np.array(mesh.faces, dtype=np.uint64, order='C', copy=True)))
    assert body.status() == manifold.Error.NoError, body.status()
    return body


def probe():
    path = Path(__file__).resolve().parents[2] / (
        'STLs/27 - Assemble Reversing Lever/reversing lever knob.stl')
    mesh = trimesh.load_mesh(path)
    parts = mesh.split(only_watertight=False)
    knob, = [part for part in parts if part.bounds[0, 2] < -30]
    assert knob.is_watertight
    body = solid(knob)
    print(json.dumps({'source_components': len(parts), 'knob_triangles': len(knob.faces),
                      'knob_bounds': knob.bounds.tolist(),
                      'frame': 'print local: shaft axis (0,57), ball Z -9.75'}), flush=True)
    for ball_radius in (2.5, 2.7):
        sphere = solid(trimesh.creation.icosphere(subdivisions=4, radius=ball_radius))
        volumes = {}
        for radial in (2.5, 3, 3.5, 3.84, 4.25, 4.48, 5, 5.5310689635676225,
                       6, 6.4, 6.5, 15, 17, 19):
            common = body ^ sphere.translate((0, 57 + radial, -9.75))
            assert common.status() == manifold.Error.NoError, common.status()
            volumes[radial] = common.volume()
            print(json.dumps({'ball_radius': ball_radius, 'ball_center_radius': radial,
                              'overlap_mm3': common.volume()}), flush=True)
        assert any(volumes[radius] > 0 for radius in (15, 17, 19)), 'missing bore-end witness'


if __name__ == '__main__':
    probe()
