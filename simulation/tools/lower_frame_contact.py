"""Measure and section the actual lower shell/frame contact without posing it."""

import argparse
import json
import logging
from math import cos, sin, radians, isfinite
from pathlib import Path

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.running_parts import RunningEnclosure
from simulation.standard.assembly import LowerHousing1
from simulation.standard.parts import BottomHousing
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.cover_fits import mesh_solid as mesh_solid64
from simulation.tools.higher_locking_envelope import faceted_common_volume


SHELL = 'Curta.enclosure.lower_housing_1.bottom_housing'
FRAME = 'Curta.frame.upper_frame.main_body'
BEARING = 'Curta.frame.lower_bearing_plate.bearing_plate'


class FineBottomHousing(BottomHousing):
    linear_deflection = .01
    angular_deflection = .1


class FineLowerHousing(LowerHousing1):
    bottom_housing = FineBottomHousing()


class FineEnclosure(RunningEnclosure):
    lower_housing_1 = FineLowerHousing()


class FineHousingTrial(OperatingCurta):
    enclosure = FineEnclosure()


def bounds(shape):
    box = shape.BoundingBox()
    return [[box.xmin, box.ymin, box.zmin], [box.xmax, box.ymax, box.zmax]]


def mesh_bounds(shape):
    values = shape.bounding_box()
    return values if all(isfinite(value) for value in values) else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--fine', action='store_true', help='Source shell with finer mesh, without seat fits')
    args = parser.parse_args()
    model = FineHousingTrial if args.fine else OperatingCurta
    sim = Sim(model(), dt=.1, meshes=True)
    bank = dict(sim.state)
    paths = (SHELL, FRAME, BEARING)
    native = world_solids(sim.node, selected=set(paths))
    nodes = dict(rigid_leaves(sim.node))
    report = {'model': model.__name__, 'parts': {}, 'contacts': {}}
    for path in paths:
        report['parts'][path] = {'native_bounds': bounds(native[path]),
                                 'mesh_bounds': nodes[path].mesh.bounds.tolist()}
        if path in (SHELL, FRAME):
            faces = []
            for face in native[path].Faces():
                lo, hi = bounds(face)
                if not all(hi[i] >= low and lo[i] <= high for i, (low, high) in
                           enumerate(((47, 50), (39, 42), (-23, -18.5)))):
                    continue
                faces.append({'type': face.geomType(), 'bounds': [lo, hi],
                              'center': face.Center().toTuple(),
                              'normal': face.normalAt().toTuple(),
                              'vertices': [v.Center().toTuple() for v in face.Vertices()]})
            report['parts'][path]['contact_region_faces'] = faces
        if path == SHELL:
            report['parts'][path]['lower_seat_faces'] = [
                {'type': face.geomType(), 'bounds': bounds(face),
                 'center': face.Center().toTuple(), 'normal': face.normalAt().toTuple(),
                 'area': face.Area()}
                for face in native[path].Faces()
                if face.geomType() == 'PLANE'
                and abs(face.Center().z + 138.45) < .000001
            ]
    for other in (FRAME, BEARING):
        common = native[SHELL].intersect(native[other])
        if not common.isValid():
            raise ValueError(f'Invalid native common: {other}')
        mesh_common = mesh_solid(nodes[SHELL].mesh) ^ mesh_solid(nodes[other].mesh)
        mesh_common64 = mesh_solid64(nodes[SHELL].mesh) ^ mesh_solid64(nodes[other].mesh)
        report['contacts'][other] = {
            'native_mm3': common.Volume(),
            'faceted_mm3': faceted_common_volume(mesh_common),
            'world_float32_raw_mm3': mesh_common.volume(),
            'world_float32_bounds': mesh_bounds(mesh_common),
            'world_float64_mm3': faceted_common_volume(mesh_common64),
            'world_float64_raw_mm3': mesh_common64.volume(),
            'world_float64_bounds': mesh_bounds(mesh_common64),
            'native_components': [{'mm3': solid.Volume(), 'bounds': bounds(solid)}
                                  for solid in common.Solids()],
        }
    import matplotlib.pyplot as plt
    figure, grid = plt.subplots(2, 2, figsize=(14, 10))
    axes = grid.ravel()
    for axis, angle in zip(axes[:2], (0, 40)):
        c, s = cos(radians(angle)), sin(radians(angle))
        for color, path in enumerate(paths):
            section = nodes[path].mesh.section(plane_origin=(0, 0, 0),
                                               plane_normal=(-s, c, 0))
            if section is None:
                raise ValueError(f'Missing {angle} degree section: {path}')
            for index, line in enumerate(section.discrete):
                axis.plot(line[:, 0]*c + line[:, 1]*s, line[:, 2], color=f'C{color}',
                          label=path.rsplit('.', 1)[-1] if index == 0 else None)
    axes[0].set(xlim=(-72, 72), ylim=(-165, 68), title='Complete frame section, azimuth 0°')
    axes[1].set(xlim=(59, 70), ylim=(-27, -14), title='Native contact region, azimuth 40°')
    for axis in axes[:2]:
        axis.set(xlabel='Radial section coordinate (mm)', ylabel='World Z (mm)', aspect='equal')
        axis.grid()
        axis.legend()
    for color, path in enumerate((SHELL, FRAME)):
        section = nodes[path].mesh.section(plane_origin=(0, 0, -20), plane_normal=(0, 0, 1))
        if section is None:
            raise ValueError(f'Missing Z=-20 section: {path}')
        for index, line in enumerate(section.discrete):
            axes[2].plot(line[:, 0], line[:, 1], color=f'C{color}',
                         label=path.rsplit('.', 1)[-1] if index == 0 else None)
    axes[2].set(xlim=(42, 56), ylim=(33, 47), title='Contact plan at world Z=-20 mm',
                xlabel='World X (mm)', ylabel='World Y (mm)', aspect='equal')
    axes[2].grid()
    axes[2].legend()
    for color, path in ((0, SHELL), (2, BEARING)):
        section = nodes[path].mesh.section(plane_origin=(0, 0, 0), plane_normal=(0, 1, 0))
        if section is None:
            raise ValueError(f'Missing lower-seat section: {path}')
        for index, line in enumerate(section.discrete):
            axes[3].plot(line[:, 0], line[:, 2], color=f'C{color}',
                         label=path.rsplit('.', 1)[-1] if index == 0 else None)
    axes[3].set(xlim=(62.5, 64.6), ylim=(-138.7, -138.1),
                title='Bearing shoulder seat, azimuth 0°', xlabel='World X (mm)',
                ylabel='World Z (mm)', aspect='equal')
    axes[3].grid()
    axes[3].legend()
    figure.tight_layout()
    figure.savefig(args.output, dpi=160)
    plt.close(figure)
    if dict(sim.state) != bank:
        raise ValueError('Inspection changed the retained bank')
    report.update(coordinates=len(bank), bank_unchanged=True, section=str(args.output))
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
