"""Read-only source/operating frame contact comparison for the repair proposal.

No print alignment, part repair, source edit or fitted geometry change is made.
The STL stays in its supplied coordinates. Trimesh's default duplicate-vertex
processing is used for STL connectivity, not hole filling or winding repair.
This is a discrete source diagnostic, not a clearance or shape-equivalence proof.
"""

import hashlib
import json
import logging
from pathlib import Path

import trimesh

from simulation.carry import CarryBench
from simulation.standard.parts import MainBody
from simulation.tools.carry_phase import solid
from simulation.tools.carry_spring import SourceCarryBench
from simulation.tools.interference import world_solids


def probe():
    path = Path('STLs/9 - Tens Bell & Main Body/main body.stl')
    printed = trimesh.load(path)
    assert printed.is_volume
    printed_solid = solid(printed)
    frame = MainBody()
    frame.assemble()
    exact = frame.shape()
    assert exact.isValid()
    frame.build_stls()
    records = []
    for version, model_class in (('source', SourceCarryBench), ('fitted', CarryBench)):
        model = model_class()
        for drop in (0, 1.1630815, 2.562, 4.2):
            model.set_state(engaged=drop/4.2)
            model.assemble()
            parts = world_solids(model, include_flexible=True)
            model.build_stls()
            spring_path = 'carry_lever_spring' + ('.wire' if version == 'fitted' else '')
            spring_node = (model.carry_lever_spring.wire if version == 'fitted'
                           else model.carry_lever_spring)
            for name, suffix, node in (
                    ('slider', 'tens_slider_for_results', model.tens_slider_for_results),
                    ('spring', spring_path, spring_node)):
                overlap = parts['Curta.'+suffix].intersect(exact)
                mesh_overlap = solid(node.mesh) ^ printed_solid
                row = dict(version=version, part=name, drop_mm=drop,
                           native_valid=overlap.isValid(), native_mm3=overlap.Volume(),
                           source_STL_status=str(mesh_overlap.status()),
                           source_STL_mm3=mesh_overlap.volume())
                assert row['native_valid']
                records.append(row)
    result = dict(
        kind='frame-source-comparison',
        source_stl=str(path), source_stl_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        source_stl_bounds_mm=printed.bounds.tolist(),
        source_stl_volume_mm3=printed.volume, source_stl_triangles=len(printed.faces),
        source_stl_watertight=printed.is_watertight,
        source_stl_winding_consistent=printed.is_winding_consistent,
        native_volume_mm3=exact.Volume(),
        native_mesh_bounds_mm=frame.mesh.bounds.tolist(),
        native_mesh_volume_mm3=frame.mesh.volume,
        registration='Identity; supplied source coordinates, no best fit or recentering',
        source_spring_limitation='Original source wire is static, not an alternative moving spring law',
        records=records,
    )
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    probe()
