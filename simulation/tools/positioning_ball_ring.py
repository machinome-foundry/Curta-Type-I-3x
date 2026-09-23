"""Read-only native section of the newly exposed ball/thrust-ring contact."""

import argparse
import json
import logging
from pathlib import Path

import cadquery as cq
import matplotlib.pyplot as plt

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.positioning_ball_profiles import bell_limit, collar_limit
from simulation.tools.positioning_ball_contact import BALL, BELL, COLLAR, FRAME
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.tools.open_run_transitions import bounds
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume

RING = 'Curta.carriage.positioning.thrust_ring'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path, required=True)
    args = parser.parse_args()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    saved = dict(sim.state)
    native = world_solids(sim.node, selected={BALL, BELL, RING, FRAME})
    leaves = dict(rigid_leaves(sim.node))
    facets = {path: mesh_solid(leaves[path].mesh) for path in (BALL, BELL, RING, FRAME, COLLAR)}
    ring = native[RING]
    print(json.dumps(dict(kind='ring-source', bounds_mm=bounds(ring).tolist(),
        volume_mm3=ring.Volume(), planar_faces=[dict(center=f.Center().toTuple(),
        normal=f.normalAt().toTuple(), area_mm2=f.Area()) for f in ring.Faces()
        if f.geomType() == 'PLANE'], circular_edge_radii_mm=sorted({e.radius()
        for e in ring.Edges() if e.geomType() == 'CIRCLE'}))), flush=True)
    fig, axes = plt.subplots(1, 3, figsize=(15, 7))
    for axis, (angle, lift, offset, label) in zip(axes, (
            (0, 0, 0, 'Original rest'), (90, 0, float(bell_limit(-90)), 'Bell outer land'),
            (0, 6, float(collar_limit(6)), 'Raised carriage limit'))):
        ball = native[BALL].translate((offset, 0, 0))
        body = ring.translate((0, 0, lift))
        common = ball.intersect(body)
        assert common.isValid()
        mesh_common = facets[BALL].translate((offset, 0, 0)) ^ facets[RING].translate((0, 0, lift))
        print(json.dumps(dict(kind='contact', label=label, bell_degrees=angle, lift_mm=lift,
            ball_offset_mm=offset, native_mm3=common.Volume(),
            world64_mm3=faceted_common_volume(mesh_common),
            common_bounds_mm=bounds(common).tolist() if common.Vertices() else None)), flush=True)
        plane = cq.Plane((0, 0, 0), (1, 0, 0), (0, -1, 0))
        for shape, name, color in ((ball, 'unchanged ball', 'tab:blue'),
                (body, 'unchanged seated ring', 'tab:orange'),
                (native[BELL].rotate((0, 0, 0), (0, 0, 1), -angle), 'bell', 'gray'),
                (common, 'positive common', 'red')):
            if not shape.Solids():
                continue
            section = cq.Workplane(plane).add(shape).section().val()
            for index, edge in enumerate(section.Edges()):
                points, _ = edge.sample(80)
                axis.plot([p.x for p in points], [p.z for p in points], color=color,
                          label=name if index == 0 else None)
        collar_mesh = leaves[COLLAR].mesh.copy()
        collar_mesh.apply_translation((0, 0, lift))
        section = collar_mesh.section(plane_origin=(0, 0, 0), plane_normal=(0, 1, 0))
        if section is not None:
            for index, line in enumerate(section.discrete):
                axis.plot(line[:, 0], line[:, 2], color='tab:green',
                          label='collar (source mesh)' if index == 0 else None)
        axis.set(xlim=(4, 19), ylim=(25, 42), aspect='equal', xlabel='World X (mm)',
                 ylabel='World Z (mm)', title=label+'\nY=0 section')
        axis.grid(alpha=.3)
        axis.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(args.image, dpi=160)
    plt.close(fig)
    assert dict(sim.state) == saved
    print(json.dumps(dict(kind='finished', bank_unchanged=True,
        acceptance='Read-only interaction finding, no adopted ball law or ring fit')), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
