"""Measure a radial exclusion on all six complete installed counter inputs.

This is independent-pose evidence, not a running constraint. All Boolean
operands are copies; neither the source print nor its published mesh changes.
The smaller input cylinder is an explicit negative containment control.
"""

import argparse
from collections import Counter
import json
import logging
from math import hypot, isfinite
from pathlib import Path


def probe():
    import cadquery as cq
    from machinome.simulation import Sim
    from simulation.cover_fits import mesh_solid
    from simulation.running import OperatingCurta
    from simulation.test_reverser_assembly import INPUTS
    from simulation.tools.interference import rigid_leaves, world_solids
    from simulation.tools.reverser_tooth_envelope import DRUMS

    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    paths = [f'Curta.transmission.turns.{name}.{member}' for name, member in INPUTS]
    native = world_solids(sim.node, selected=set(paths) | set(DRUMS))
    leaves = dict(rigid_leaves(sim.node))
    core_radius, input_radius = 34.1, 6.3
    for station, ((name, _), path) in enumerate(zip(INPUTS, paths), 1):
        node = getattr(sim.node.transmission.turns, name)
        axis = tuple(type(node).turn.at)
        source = native[path]
        if not source.isValid():
            raise ValueError(f'Invalid native input: {path}')
        mesh = leaves[path].mesh
        mesh_solid(mesh)  # Independently refuse malformed published geometry.
        radius = max(hypot(float(x)-axis[0], float(y)-axis[1])
                     for x, y, _ in mesh.vertices)
        box = source.BoundingBox()
        checks = []
        for candidate in (6.0, input_radius):
            cylinder = cq.Solid.makeCylinder(candidate, box.zlen+2,
                                              (axis[0], axis[1], box.zmin-1))
            outside = source.copy().cut(cylinder.copy())
            volume = outside.Volume()
            if not outside.isValid() or not isfinite(volume) or volume < 0:
                raise ValueError(f'Unresolved radial difference: {path}, {candidate}, {volume}')
            contained = volume == 0 and radius <= candidate
            if contained != (candidate == input_radius):
                raise ValueError(f'Unexpected radial control result: {path}, {candidate}')
            checks.append(dict(radius_mm=candidate, native_valid=True,
                               native_outside_mm3=volume, mesh_inside=radius <= candidate))
        gap = hypot(*axis[:2])-core_radius-input_radius
        if not gap > 0:
            raise ValueError(f'Core exclusion not established: {path}')
        yield dict(kind='installed_input', station=station, path=path, axis=axis,
                   shaft_angle=sim.state[f'transmission.turns.{name}.turn'],
                   reverser_height=sim.state['reverser_height'],
                   native_z=[box.zmin, box.zmax], mesh_z=list(map(float, mesh.bounds[:, 2])),
                   mesh_radius_mm=radius, core_radius_mm=core_radius,
                   radial_gap_mm=gap, checks=checks,
                   scope='Radial exclusion under axial translation and own-axis rotation only')

    for path in DRUMS:
        source = native[path]
        box = source.BoundingBox()
        core = cq.Solid.makeCylinder(core_radius, box.zlen+2, (0, 0, box.zmin-1))
        outside = source.copy().cut(core.copy())
        if not source.isValid() or not outside.isValid():
            raise ValueError(f'Invalid drum radial decomposition: {path}')
        solids = []
        for solid in outside.Solids():
            bounds = solid.BoundingBox()
            volume = solid.Volume()
            if not isfinite(volume) or volume <= 0:
                raise ValueError(f'Unresolved outer drum component: {path}, {volume}')
            solids.append(dict(z=[bounds.zmin, bounds.zmax], volume_mm3=volume,
                               face_types=dict(Counter(f.geomType() for f in solid.Faces()))))
        yield dict(kind='native_outer_drum', path=path, core_radius_mm=core_radius,
                   source_z=[box.zmin, box.zmax], solids=solids,
                   scope='Native radial decomposition only; mesh and axial-profile covers unproved')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f'Preserve existing evidence: {args.output}')
    count = 0
    with args.output.open('x') as output:
        for row in probe():
            print(json.dumps(row), file=output, flush=True)
            print(json.dumps(dict(kind=row['kind'], path=row['path'],
                                  solids=len(row.get('solids', ())))), flush=True)
            count += 1
    print(json.dumps(dict(output=str(args.output), rows=count)), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
