"""Inspect actual admitted production poses, not manually posed ball copies."""

import argparse
import json
import logging

import cadquery as cq
import matplotlib.pyplot as plt

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.positioning_ball_contact import BALL, BELL, FRAME, COLLAR
from simulation.tools.positioning_ball_ring import RING
from simulation.tools.interference import world_solids, rigid_leaves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True)
    args = parser.parse_args()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    initial = sim.snapshot()
    fig, axes = plt.subplots(1, 5, figsize=(20, 7))
    stages = (
        ('Rest', False, ()),
        ('Bell pushes outward', False, (('crank_rotation', 90, 'completed'),)),
        ('Return retains ball', False, (('crank_rotation', 360, 'completed'),)),
        ('Raised carriage stops crank', True, (('carriage_elevation', 6, 'completed'),
                                             ('crank_rotation', 90, 'blocked'))),
        ('Outward bell stops lift', True, (('crank_rotation', 90, 'completed'),
                                         ('carriage_elevation', 6, 'blocked'))),
    )
    for axis, (label, reset, requests) in zip(axes, stages):
        if reset:
            sim.restore(initial)
        for name, target, expected in requests:
            request = sim.move(name, to=target, duration=.5)
            sim.run(.5)
            assert request.status == expected, (label, name, request.status)
        native = world_solids(sim.node, selected={BALL, BELL, FRAME, RING})
        plane = cq.Plane((0, 0, 0), (1, 0, 0), (0, -1, 0))
        for path, color in ((FRAME, 'gray'), (BELL, 'tab:orange'),
                            (RING, 'tab:purple'), (BALL, 'tab:blue')):
            section = cq.Workplane(plane).add(native[path]).section().val()
            for index, edge in enumerate(section.Edges()):
                points, _ = edge.sample(80)
                axis.plot([p.x for p in points], [p.z for p in points], color=color,
                          label=path.rsplit('.', 1)[-1] if index == 0 else None)
        collar = dict(rigid_leaves(sim.node))[COLLAR].mesh
        section = collar.section(plane_origin=(0, 0, 0), plane_normal=(0, 1, 0))
        if section is not None:
            for index, line in enumerate(section.discrete):
                axis.plot(line[:, 0], line[:, 2], color='tab:green',
                          label='collar (source mesh)' if index == 0 else None)
        angle, lift = sim.state['crank_rotation'], sim.state['carriage_elevation']
        axis.set(xlim=(4, 19), ylim=(24, 42), aspect='equal', xlabel='World X (mm)',
                 ylabel='World Z (mm)', title=f'{label}\ncrank {angle:.6f}°, lift {lift:.6f} mm')
        axis.legend(fontsize=7)
        axis.grid(alpha=.3)
        print(json.dumps(dict(stage=label, bank=dict(sim.state))), flush=True)
    fig.tight_layout()
    fig.savefig(args.image, dpi=160)
    plt.close(fig)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
