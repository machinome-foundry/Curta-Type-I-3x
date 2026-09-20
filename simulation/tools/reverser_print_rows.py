"""Count actual printable upper-drum tooth rows, independently of STEP labels."""

import hashlib
import json
from pathlib import Path
import numpy as np
import trimesh


def probe():
    root = Path(__file__).resolve().parents[2]
    path = root / 'STLs/11 - Assemble Step Drum/main axle and step drum top.stl'
    mesh = trimesh.load_mesh(path)
    print(json.dumps({'file': str(path.relative_to(root)),
                      'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'bounds': mesh.bounds.tolist(), 'watertight': mesh.is_watertight}), flush=True)
    for lower in (12.1, 13.6, 15.1, 16.6, 18.1, 19.6, 21.1):
        z = lower + .75
        lines = trimesh.intersections.mesh_plane(mesh, (0, 0, 1), (0, 0, z))
        points = lines.reshape(-1, 3)
        outside = points[np.linalg.norm(points[:, :2], axis=1) > 35]
        angles = np.sort(np.unique(np.degrees(np.arctan2(outside[:, 1], outside[:, 0])) % 360))
        gaps = np.diff(np.r_[angles, angles[0] + 360])
        print(json.dumps({'print_local_row': [lower, lower + 1.5],
                          'step_datum_row': [lower - 66.3, lower + 1.5 - 66.3],
                          'outside_R35_sections': int(np.sum(gaps > 5)),
                          'outside_angles': angles.tolist()}), flush=True)
    for name in ('STLs/22 - Transmission Shaft 10216/10218.stl',
                 'STLs/23 - Transmission Shaft 10207/10230 - 410008 x15.stl'):
        path = root / name
        mesh = trimesh.load_mesh(path)
        print(json.dumps({'file': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                          'bounds': mesh.bounds.tolist(),
                          'watertight': mesh.is_watertight}), flush=True)


if __name__ == '__main__':
    probe()
