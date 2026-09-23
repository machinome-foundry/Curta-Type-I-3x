"""Dense independent sphere/ring checks and source/fit section inspection."""

import argparse
import json
import logging
import time

import cadquery as cq
import matplotlib.pyplot as plt
import numpy as np

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.thrust_ring_parts import BallPassageThrustRing
from simulation.standard.parts import ThrustRing
from simulation.thrust_ring_trial import FittedThrustBench
from simulation.tools.positioning_ball_contact import BALL
from simulation.tools.positioning_ball_ring import RING
from simulation.tools.interference import world_solids, rigid_leaves
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True)
    args = parser.parse_args()
    started = time.monotonic()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    saved = dict(sim.state)
    source = world_solids(sim.node, selected={BALL, RING})
    leaves = dict(rigid_leaves(sim.node))
    part = BallPassageThrustRing()
    part.assemble()
    part.build_stls()
    fitted = part.shape().rotate((0, 0, 0), (0, 0, 1), 35.717779468).translate((0, 0, 33.05))
    mesh = mesh_solid(part.mesh).rotate((0, 0, 35.717779468)).translate((0, 0, 33.05))
    ball_mesh = mesh_solid(leaves[BALL].mesh)
    total = 0
    for lift in np.linspace(0, 6, 61):
        ring = fitted.translate((0, 0, float(lift)))
        ring_mesh = mesh.translate((0, 0, float(lift)))
        for radius in np.linspace(8.332, 11.950, 41):
            offset = float(radius)-9.627860318
            common = ring.intersect(source[BALL].translate((offset, 0, 0)))
            assert common.isValid()
            native_volume = common.Volume()
            mesh_volume = faceted_common_volume(ring_mesh ^ ball_mesh.translate((offset, 0, 0)))
            assert native_volume == mesh_volume == 0, (lift, radius, native_volume, mesh_volume)
            total += 1
        print(json.dumps(dict(kind='lift', lift_mm=float(lift), radii=41,
                             native_and_world64_clear=True)), flush=True)
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    bench = FittedThrustBench()
    bench.set_state(travel=0, shift=0)
    bench.assemble()
    bench.build_stls()
    for axis, (x, lift) in zip(axes, ((9.627860318, 0), (11.949090957641602, 0), (8.402658462524414, 6))):
        shapes = ((source[RING].translate((0, 0, lift)), 'source ring', 'tab:orange'),
                  (fitted.translate((0, 0, lift)), 'fitted ring', 'tab:green'),
                  (source[BALL].translate((x-9.627860318, 0, 0)), 'unchanged ball', 'tab:blue'))
        for shape, label, color in shapes:
            section = cq.Workplane(cq.Plane((0, 0, 0), (1, 0, 0), (0, -1, 0))).add(shape).section().val()
            for i, edge in enumerate(section.Edges()):
                points, _ = edge.sample(80)
                axis.plot([p.x for p in points], [p.z for p in points], color=color,
                          label=label if i == 0 else None)
        bench.set_state(travel=lift, shift=0)
        for support, label, color in ((bench.collar.mesh, 'installed collar mesh', 'tab:purple'),
                (bench.carriage_spring.wire.mesh, 'spring wire mesh', 'gray')):
            section = support.section(plane_origin=(0, 0, 0), plane_normal=(0, 1, 0))
            if section is not None:
                for i, line in enumerate(section.discrete):
                    axis.plot(line[:, 0], line[:, 2], color=color, label=label if i == 0 else None)
        axis.set(xlim=(7, 17), ylim=(26, 42), aspect='equal', xlabel='World X (mm)',
                 ylabel='World Z (mm)', title=f'Centre X{x:.4f}, lift {lift} mm')
        axis.legend(fontsize=8)
        axis.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(args.image, dpi=160)
    plt.close(fig)
    removed = ThrustRing().shape().cut(part.shape())
    assert dict(sim.state) == saved
    print(json.dumps(dict(kind='finished', poses=total, seconds=time.monotonic()-started,
        removed_mm3=removed.Volume(), retained_mm3=part.shape().Volume(),
        bank_unchanged=True, acceptance='Ring interface only; other ball contacts not certified')), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
