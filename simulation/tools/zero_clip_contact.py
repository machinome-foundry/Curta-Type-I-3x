"""Inspect the installed zero-cam spring clip without assuming a fitting fix."""

import argparse
import json
import logging
from pathlib import Path
from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.tools.crank_drum_contact import bounds
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume

CAM = 'Curta.main_drive.zero_positioning.zero_positioning_disc'
CLIP = 'Curta.main_drive.zero_positioning.zero_positioning_disc_securing_spring'
BEARING = 'Curta.frame.lower_bearing_plate.bearing_plate'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--axial-shift', type=float, action='append',
                        help='Read-only unchanged-clip shift against cam and bearing')
    args = parser.parse_args()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    bank = dict(sim.state)
    shapes = world_solids(sim.node, selected={CAM, CLIP, BEARING})
    leaves = dict(rigid_leaves(sim.node))
    common = shapes[CAM].intersect(shapes[CLIP])
    if not common.isValid():
        raise ValueError('Invalid native zero-cam/clip common')
    report = {
        'native_mm3': common.Volume(),
        'world64_mm3': faceted_common_volume(mesh_solid(leaves[CAM].mesh) ^ mesh_solid(leaves[CLIP].mesh)),
        'parts': {name: {'bounds': bounds(shape), 'circles': [
            {'radius': edge.radius(), 'center': edge.arcCenter().toTuple()}
            for edge in shape.Edges() if edge.geomType() == 'CIRCLE']}
            for name, shape in shapes.items()},
        'components': [{'volume': part.Volume(), 'bounds': bounds(part)} for part in common.Solids()],
    }
    if args.axial_shift:
        meshes = {name: mesh_solid(leaves[name].mesh) for name in (CAM, CLIP, BEARING)}
        report['axial_shift_contacts_mm3'] = []
        for shift in args.axial_shift:
            moved = shapes[CLIP].translate((0, 0, shift))
            row = {'shift': shift, 'contacts': {}}
            for other in (CAM, BEARING):
                contact = moved.intersect(shapes[other])
                if not contact.isValid():
                    raise ValueError(f'Invalid shifted clip common: {shift}, {other}')
                row['contacts'][other] = {
                    'native': contact.Volume(),
                    'world64': faceted_common_volume(meshes[CLIP].translate((0, 0, shift)) ^ meshes[other]),
                }
            report['axial_shift_contacts_mm3'].append(row)
    import matplotlib.pyplot as plt
    figure, axes = plt.subplots(1, 3, figsize=(16, 6))
    lo, hi = bounds(common)
    z = (lo[2]+hi[2])/2
    sections = (((0, 0, z), (0, 0, 1), (0, 1)),
                ((0, 0, 0), (1, 0, 0), (1, 2)),
                ((0, 0, 0), (0, 1, 0), (0, 2)))
    for axis, (origin, normal, indices) in zip(axes, sections):
        for color, name in enumerate((CAM, CLIP, BEARING)):
            section = leaves[name].mesh.section(plane_origin=origin, plane_normal=normal)
            if section is not None:
                for index, line in enumerate(section.discrete):
                    axis.plot(line[:, indices[0]], line[:, indices[1]], color=f'C{color}',
                              label=name.rsplit('.', 1)[-1] if index == 0 else None)
        axis.set(xlabel='World '+ 'XYZ'[indices[0]]+' (mm)',
                 ylabel='World '+ 'XYZ'[indices[1]]+' (mm)', aspect='equal')
        axis.grid()
        axis.legend()
    axes[0].set_title(f'XY at common mid-Z {z:.6f}')
    axes[1].set_title('YZ at X=0')
    axes[2].set_title('XZ at Y=0')
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
