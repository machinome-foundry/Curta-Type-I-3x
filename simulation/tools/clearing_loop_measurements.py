"""Small source-print cross sections; identify the loop's original clip arcs."""

import json
from collections import Counter
from pathlib import Path
import numpy as np
import trimesh


def circles(points):
    points = points[:-1, :2]
    previous = np.roll(points, 1, axis=0)
    following = np.roll(points, -1, axis=0)
    first, second = points - previous, following - points
    cross = first[:, 0] * second[:, 1] - first[:, 1] * second[:, 0]
    points = points[np.abs(cross) > 1e-5]
    counts = Counter()
    for a, b, c in zip(np.roll(points, 1, axis=0), points, np.roll(points, -1, axis=0)):
        matrix = 2 * np.array((b - a, c - a))
        if abs(np.linalg.det(matrix)) < 1e-5:
            continue
        center = np.linalg.solve(matrix, (b @ b - a @ a, c @ c - a @ a))
        radius = np.linalg.norm(a - center)
        if radius < 50:
            counts[tuple(round(float(v), 2) for v in (*center, radius))] += 1
    return [{'center': [x, y], 'radius': r, 'segments': n}
            for (x, y, r), n in counts.most_common() if n >= 3]


if __name__ == '__main__':
    directory = Path(__file__).resolve().parents[2] / 'STLs' / '37 - Clearing Cover'
    for name in ('clearing ring.stl', 'clearing ring rivet x2.stl'):
        mesh = trimesh.load_mesh(directory / name)
        print(json.dumps({'source': name, 'bounds': mesh.bounds.tolist(),
                          'vertices': len(mesh.vertices), 'watertight': mesh.is_watertight}), flush=True)
        for z in (.2, 1.5, 3, 4.5, 6, 9, 11):
            section = mesh.section(plane_origin=(0, 0, z), plane_normal=(0, 0, 1))
            if section is not None:
                print(json.dumps({'z': z, 'loops': [circles(points) for points in section.discrete]}),
                      flush=True)
