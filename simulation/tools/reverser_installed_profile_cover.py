"""Offline native/mesh covers of complete installed reverser contact prints.

Only independently proved radially or axially separated material is excluded.
The output is investigation data, not an adopted running restraint.
"""

import argparse
from copy import deepcopy
import hashlib
import json
import logging
from math import cos, hypot, isfinite, radians, sin
from pathlib import Path


def probe(source_profiles, *, axial_allowance_mm=None, model=None):
    import cadquery as cq
    import manifold3d as mf
    import numpy as np
    from machinome.simulation import Sim
    from simulation.cover_fits import mesh_solid
    from simulation.running import OperatingCurta
    from simulation.test_reverser_assembly import INPUTS
    from simulation.tools.interference import rigid_leaves, world_solids
    from simulation.tools.reverser_profile_cover import (profile_cover, cover_mesh_arrays,
                                                        checked_native_remainder,
                                                        convex_partition, axial_allowance)
    from simulation.tools.reverser_tooth_envelope import DRUMS

    model = OperatingCurta if model is None else model
    sim = Sim(model(), dt=.1, meshes=True)
    for key in ('FittedCounterPinion', 'ReversingCounterPinion'):
        report = source_profiles[key]
        if convex_partition(report['points'], report['triangles']) != report['polygons']:
            raise ValueError(f'Source profile decomposition changed: {key}')
    paths = [f'Curta.transmission.turns.{name}.{member}' for name, member in INPUTS]
    native = world_solids(sim.node, selected=set(paths) | set(DRUMS))
    leaves = dict(rigid_leaves(sim.node))
    axes = {p: tuple(type(getattr(sim.node.transmission.turns, name)).turn.at)
            for (name, _), p in zip(INPUTS, paths)}
    angles = {p: sim.state[f'transmission.turns.{name}.turn']
              for (name, _), p in zip(INPUTS, paths)}
    minimum_axis = min(hypot(*axis[:2]) for axis in axes.values())
    input_outer, drum_outer = 6.3, 36.62
    input_core, drum_core = 3.86, 34.1
    # The cut at 3.86 simplifies the source; an independent 3.87 cylinder
    # covers the concave cut's faceting remainder, with strictly positive
    # separation from the complete drum envelope. It is not a volume epsilon.
    input_exclusion = 3.87
    if not minimum_axis > max(input_outer+drum_core, drum_outer+input_exclusion):
        raise ValueError('Radial envelopes do not separate the excluded cores')

    # Prove both bounding cylinders on complete native and actual mesh prints.
    for path in (*paths, *DRUMS):
        source = native[path]
        box = source.BoundingBox()
        axis = axes.get(path, (0, 0, 0))
        radius = input_outer if path in axes else drum_outer
        outside = source.copy().cut(cq.Solid.makeCylinder(
            radius, box.zlen+2, (axis[0], axis[1], box.zmin-1)))
        volume = outside.Volume()
        mesh = leaves[path].mesh
        mesh_solid(mesh)
        mesh_radius = max(hypot(float(x)-axis[0], float(y)-axis[1])
                          for x, y, _ in mesh.vertices)
        if not source.isValid() or not outside.isValid() or volume != 0 or mesh_radius > radius:
            raise ValueError(f'Failed complete-print envelope: {path}, {volume}, {mesh_radius}')
        yield dict(kind='radial_envelope', path=path, axis=axis, radius_mm=radius,
                   native_outside_mm3=volume, mesh_radius_mm=mesh_radius)

    # Driver endpoints are checked explicitly; changed controls invalidate the probe.
    if tuple(model.reverser_height.range) != (-6.9425, 3.9075):
        raise ValueError('Reverser driver range changed')
    if tuple(model.crank_elevation.range) != (0, 9):
        raise ValueError('Crank-elevation driver range changed')
    bottom_clip = -72.0
    minimum_z = min(min(native[p].BoundingBox().zmin, float(leaves[p].mesh.bounds[0, 2]))
                    for p in paths) - 6.9425 - sim.state['reverser_height'] - 9
    if not minimum_z > bottom_clip:
        raise ValueError('Lower drum clip is not separated throughout driver ranges')
    yield dict(kind='axial_exclusion', bottom_clip=bottom_clip,
               minimum_input_z_in_drum_frame=minimum_z,
               reverser_range=[-6.9425, 3.9075], crank_elevation_range=[0, 9])

    class Candidate:
        def __init__(self, shape):
            self.value = shape

        def shape(self):
            return self.value

    for path in (*paths, *DRUMS):
        source = native[path]
        box = source.BoundingBox()
        axis = axes.get(path, (0, 0, 0))
        core_radius = input_core if path in axes else drum_core
        outside = source.copy().cut(cq.Solid.makeCylinder(
            core_radius, box.zlen+2, (axis[0], axis[1], box.zmin-1)))
        remainder = mesh_solid(leaves[path].mesh) - mf.Manifold.cylinder(
            box.zlen+2, core_radius, circular_segments=720).translate(
                (axis[0], axis[1], box.zmin-1))
        if path == DRUMS[1]:
            outside = outside.copy().intersect(cq.Solid.makeBox(
                100, 100, 200, (-50, -50, bottom_clip)))
            remainder = remainder - mf.Manifold.cube((100, 100, 200)).translate(
                (-50, -50, bottom_clip-200))
        if not outside.isValid() or remainder.status() != mf.Error.NoError:
            raise ValueError(f'Invalid contact-region decomposition: {path}')
        before = remainder.volume()
        if not isfinite(before) or before <= 0:
            raise ValueError(f'No positive negative-control material: {path}, {before}')
        reports = []
        if path in axes:
            # Use the already checked, conforming full source pinion cover.
            # The trimmed inner arc's candidate triangulation folds, so it
            # is refused rather than repaired or used for the mesh verdict.
            key = 'FittedCounterPinion' if path == paths[0] else 'ReversingCounterPinion'
            c, s = cos(radians(angles[path])), sin(radians(angles[path]))
            bands = sorted({(solid.BoundingBox().zmin, solid.BoundingBox().zmax)
                            for solid in outside.Solids()})
            for low, high in bands:
                report = deepcopy(source_profiles[key])
                report['points'] = [(c*x-s*y+axis[0], s*x+c*y+axis[1])
                                    for x, y in report['points']]
                report['source_height'] = [low, high]
                if axial_allowance_mm is not None:
                    report['axial_allowance_mm'] = axial_allowance_mm
                report.pop('mesh_cover_polygons', None)
                reports.append(report)
        else:
            reports = [profile_cover(Candidate(solid), join='intersection',
                                     axial_allowance_mm=axial_allowance_mm)
                       for solid in outside.Solids()]
        native_remainder = outside
        count = 0
        for index, report in enumerate(reports):
            low, high = report['source_height']
            allowance = axial_allowance(report)
            wire = cq.Wire.makePolygon([(report['points'][i][0], report['points'][i][1],
                                         low-allowance) for i in report['boundary']], close=True)
            native_cover = cq.Solid.extrudeLinear(wire, [], cq.Vector(0, 0, high-low+2*allowance))
            if not native_cover.isValid():
                raise ValueError(f'Invalid placed native cover: {path}, {index}')
            native_remainder = native_remainder.copy().cut(native_cover.copy())
            vertices, faces = cover_mesh_arrays(report)
            cover = mf.Manifold(mf.Mesh64(np.array(vertices, dtype=np.float64),
                                         np.array(faces, dtype=np.uint64)))
            if cover.status() != mf.Error.NoError:
                raise ValueError(f'Invalid constructed mesh cover: {path}, {index}, '
                                 f'{cover.status()}, points={len(report["points"])}, '
                                 f'unique={len(set(map(tuple, report["points"])))}')
            remainder = remainder - cover
            report.update(kind='installed_profile', path=path, component=index,
                          axis=axis, coordinates='Installed initial world XY',
                          reference_shaft_angle=angles.get(path, 0),
                          reference_reverser_height=sim.state['reverser_height'],
                          scope='Placed candidate; complete native/mesh coverage verdict follows')
            yield report
            count += 1
        excluded = (cq.Solid.makeCylinder(input_exclusion, box.zlen+2,
                    (axis[0], axis[1], box.zmin-1)) if path in axes else None)
        native_volume, native_union_volume = checked_native_remainder(native_remainder, excluded)
        volume = remainder.volume()
        if remainder.status() != mf.Error.NoError or not isfinite(volume) or volume < 0:
            raise ValueError(f'Unresolved mesh remainder: {path}, {volume}')
        residual_radius = 0.0
        if not remainder.is_empty():
            residual_radius = max(hypot(float(x)-axis[0], float(y)-axis[1])
                                  for x, y, _ in remainder.to_mesh64().vert_properties)
        other_outer = drum_outer if path in axes else input_outer
        separated = remainder.is_empty() or residual_radius+other_outer < minimum_axis
        yield dict(kind='installed_mesh_verdict', path=path, components=count,
                   native_remainder_mm3=native_volume,
                   native_remainder_after_exclusion_mm3=native_union_volume,
                   uncovered_control_mm3=before, remainder_mm3=volume,
                   remainder_empty=remainder.is_empty(), residual_radius_mm=residual_radius,
                   separated=separated, other_outer_radius_mm=other_outer,
                   minimum_axis_radius_mm=minimum_axis,
                   scope='Profile covers plus proved radial/axial exclusions; no operating adoption')
        if not separated:
            raise ValueError(f'Uncovered mesh material may contact: {path}, {volume}, {residual_radius}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-profiles', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--axial-allowance', type=float,
                        help='Independent positive Z-cover length; default uses the XY allowance')
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f'Preserve existing evidence: {args.output}')
    raw = args.source_profiles.read_bytes()
    source_profiles = {row['part']: row for row in map(json.loads, raw.splitlines())}
    count = 0
    with args.output.open('x') as output:
        for row in probe(source_profiles, axial_allowance_mm=args.axial_allowance):
            row['source_profiles_sha256'] = hashlib.sha256(raw).hexdigest()
            print(json.dumps(row), file=output, flush=True)
            print(json.dumps({key: row[key] for key in
                              ('kind', 'path', 'component', 'separated', 'remainder_mm3')
                              if key in row}), flush=True)
            count += 1
    print(json.dumps(dict(output=str(args.output), rows=count)), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
