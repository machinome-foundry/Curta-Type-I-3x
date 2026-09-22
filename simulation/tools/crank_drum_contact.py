"""Inspect the actual main-crank/drum connection without altering its state."""

import argparse
import json
import logging
from pathlib import Path

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


CRANK = 'Curta.main_drive.crank.crank_handle_1.main_crank'
DRUM = 'Curta.main_drive.stepped_drum.main_axle_step_drum_1.main_axle_step_drum_top_1'
PIN = 'Curta.main_drive.crank.crank_handle_pin'


def bounds(shape):
    box = shape.BoundingBox()
    return [[box.xmin, box.ymin, box.zmin], [box.xmax, box.ymax, box.zmax]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--perturbations', action='store_true',
                        help='Also measure the ten native vertical offsets at each pin seat')
    args = parser.parse_args()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    bank = dict(sim.state)
    native = world_solids(sim.node, selected={CRANK, DRUM, PIN})
    leaves = dict(rigid_leaves(sim.node))
    common = native[CRANK].intersect(native[DRUM])
    if not common.isValid():
        raise ValueError('Invalid native crank/drum common')
    mesh_common = mesh_solid(leaves[CRANK].mesh) ^ mesh_solid(leaves[DRUM].mesh)
    report = {
        'native_mm3': common.Volume(), 'world64_mm3': faceted_common_volume(mesh_common),
        'components': [{'volume': part.Volume(), 'bounds': bounds(part)} for part in common.Solids()],
        'parts': {name: {'bounds': bounds(shape)} for name, shape in native.items()},
    }
    for name, shape in native.items():
        circles = []
        for edge in shape.Edges():
            if edge.geomType() != 'CIRCLE' or edge.radius() > 6:
                continue
            center = edge.arcCenter()
            if 55 < center.z < 100:
                direction = edge._geomAdaptor().Circle().Axis().Direction()
                circles.append({'radius': edge.radius(), 'center': center.toTuple(),
                                'normal': [direction.X(), direction.Y(), direction.Z()]})
        report['parts'][name]['coupling_circles'] = circles
    report['crank_local_circles'] = [
        {'radius': edge.radius(), 'center': edge.arcCenter().toTuple()}
        for edge in leaves[CRANK].shape().Edges()
        if edge.geomType() == 'CIRCLE' and edge.radius() < 6
        and abs(edge.arcCenter().x) < 6 and abs(edge.arcCenter().y) < 6
    ]
    if args.perturbations:
        report['pin_vertical_perturbations_native_mm3'] = {
            name: {str(delta): native[name].translate((0, 0, delta)).intersect(native[PIN]).Volume()
                   for delta in (-1, -.75, -.5, -.3, -.02, .02, .3, .5, .75, 1)}
            for name in (CRANK, DRUM)
        }
    import matplotlib.pyplot as plt
    figure, axes = plt.subplots(1, 3, figsize=(17, 7))
    lo, hi = ((-5, -5, 68), (5, 5, 90))
    if common.Solids():
        lo, hi = bounds(common)
    for color, path in enumerate((CRANK, DRUM, PIN)):
        section = leaves[path].mesh.section(plane_origin=(0, 0, 0), plane_normal=(0, 1, 0))
        if section is None:
            raise ValueError(f'Missing Y=0 section: {path}')
        for axis in axes:
            for index, line in enumerate(section.discrete):
                axis.plot(line[:, 0], line[:, 2], color=f'C{color}',
                          label=path.rsplit('.', 1)[-1] if index == 0 else None)
    axes[1].set(xlim=(lo[0]-2, hi[0]+2), ylim=(lo[2]-2, hi[2]+2),
                title='Pinned connection, enlarged')
    axes[0].set_title('Complete crank/drum section')
    for axis in axes:
        axis.set(xlabel='World X (mm)', ylabel='World Z (mm)', aspect='equal')
        axis.grid()
        axis.legend()
    axes[2].set(xlim=(-5, 5), ylim=(88.7, 89.2), aspect='auto',
                title='Roof gap: expanded vertical scale')
    figure.tight_layout()
    figure.savefig(args.output, dpi=160)
    plt.close(figure)
    if dict(sim.state) != bank:
        raise ValueError('Inspection changed retained state')
    report.update(coordinates=len(bank), bank_unchanged=True, image=str(args.output))
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
