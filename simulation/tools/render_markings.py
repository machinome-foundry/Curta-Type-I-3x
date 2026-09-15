"""Orthographic evidence from the built solid and decal triangles.

This is a finite diagnostic, not a viewer implementation. It neither modifies
the meshes nor claims that the browser/OpenSCAD renderer supports decals.
"""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import numpy as np
import trimesh

from simulation.tools.check_markings import entries


def project(ax, mesh, angle, color, up=1, limits=None):
    normal = np.array([np.cos(angle), np.sin(angle), 0])
    right = up * np.array([-np.sin(angle), np.cos(angle), 0])
    triangles = mesh.triangles
    depth = triangles @ normal
    visible = (depth > 0).all(axis=1)
    triangles, depth = triangles[visible], depth[visible]
    points = np.stack((triangles @ right, up * triangles[:, :, 2]), axis=2)
    if limits is not None:
        xmin, xmax, ymin, ymax = limits
        inside = ((points[:, :, 0].max(axis=1) >= xmin) &
                  (points[:, :, 0].min(axis=1) <= xmax) &
                  (points[:, :, 1].max(axis=1) >= ymin) &
                  (points[:, :, 1].min(axis=1) <= ymax))
        points, depth = points[inside], depth[inside]
    ax.add_collection(PolyCollection(points[np.argsort(depth.mean(axis=1))],
                                     facecolors=color, edgecolors='none', antialiaseds=False))


def render(document, directory, output):
    chosen = {}
    for _, node in entries(document['root']):
        if node.get('markings'):
            chosen.setdefault(node['model'], node)
    bands = [n for n in chosen.values() if n['markings'][0]['name'] == 'digits']
    fig, axes = plt.subplots(len(bands), 10, figsize=(16, 7), squeeze=False)
    for row, node in enumerate(bands):
        body = trimesh.load_mesh(directory / node['model'])
        decal = trimesh.load_mesh(directory / node['markings'][0]['model'])
        is_input = node['name'] == 'number_roll'
        zero, up = (-175.6, -1) if is_input else (-124, 1)
        limits = (-2.9, 2.9, -15, 0) if is_input else (-2.9, 2.9, .9, 11.4)
        for digit, ax in enumerate(axes[row]):
            angle = np.radians(zero + 36 * digit)
            project(ax, body, angle, node['color'], up, limits)
            project(ax, decal, angle, node['markings'][0]['color'], up, limits)
            ax.set(xlim=limits[:2], ylim=limits[2:], aspect='equal', title=str(digit))
            ax.set_xticks([]); ax.set_yticks([])
            if digit == 0:
                ax.set_ylabel('Input' if is_input else node['name'].replace('_', ' '))
    fig.suptitle('Built solid + decal triangles, 0–9 viewing positions (diagnostic, not browser rendering)')
    fig.tight_layout()
    fig.savefig(output / 'markings-digits.png', dpi=160)
    plt.close(fig)

    cases = [('lower_housing', -142, (-80, 80, 25, 51)),
             ('upper_outer_sleeve', -70, (-74, 74, 0, 65)),
             ('bottom_housing', 80.4135, (-15, 15, 78, 114))]
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    for ax, (name, angle, limits) in zip(axes, cases):
        node = next(n for n in chosen.values() if n['name'] == name)
        project(ax, trimesh.load_mesh(directory / node['model']), np.radians(angle),
                node['color'], limits=limits)
        mark = node['markings'][0]
        project(ax, trimesh.load_mesh(directory / mark['model']), np.radians(angle),
                mark['color'], limits=limits)
        ax.set(xlim=limits[:2], ylim=limits[2:], aspect='equal', title=name)
        ax.set_xlabel('Local tangential projection (mm)'); ax.set_ylabel('Local z (mm)')
    fig.suptitle('Housing decals on their built solids — orthographic diagnostic')
    fig.tight_layout()
    fig.savefig(output / 'markings-housings.png', dpi=160)
    plt.close(fig)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path, nargs='?', default=Path('_build/viewer.json'))
    parser.add_argument('-o', type=Path, default=Path('_build_evidence'))
    args = parser.parse_args()
    args.o.mkdir(parents=True, exist_ok=True)
    render(json.loads(args.manifest.read_text()), args.manifest.parent, args.o)
