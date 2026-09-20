"""Try shaft-depth calibration against native seats AND unchanged print files.

The manual (p29) tells the builder to push the shaft upward after engaging
the counter gears, then secure its M4 nut. Test whether further insertion
from the imported final seating can close the measured lower-row gap.
No print fitting, deformation or geometry change is performed.
"""

import hashlib
import json
import logging
from pathlib import Path

import numpy as np
import manifold3d as manifold
import trimesh
from simulation.tools.carry_phase import solid
from simulation.tools.interference import world_solids
from simulation.tools.reverser_shaft_seat import ShaftSeatBench


def probe():
    logging.disable(logging.INFO)
    bench = ShaftSeatBench()
    bench.set_state(knob_height=-6.8425, gear_height=-6.6575,
                    crank_angle=101.25, subtract=0, reversed_counter=1)
    bench.assemble()
    selected = {'Curta.lever.reversing_shaft', 'Curta.upper_frame',
                'Curta.lower_frame', 'Curta.fasteners.m4_nut_2'}
    shapes = world_solids(bench, selected=selected)
    shaft = shapes.pop('Curta.lever.reversing_shaft')
    root = Path(__file__).resolve().parents[2]
    printed = {}
    files = {
        'shaft': 'STLs/27 - Assemble Reversing Lever/reversing shaft.stl',
        'upper_frame': 'STLs/9 - Tens Bell & Main Body/main body.stl',
        'lower_frame': 'STLs/12 - Step Drum & Bearing Plate/bearing plate.stl',
    }
    for name, filename in files.items():
        path = root / filename
        mesh = trimesh.load_mesh(path)
        assert mesh.is_watertight, filename
        print(json.dumps({'source': filename, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                          'bounds': mesh.bounds.tolist(), 'watertight': True}), flush=True)
        if name == 'shaft':
            mesh.apply_transform(trimesh.transformations.rotation_matrix(np.radians(70), (0, 0, 1)))
            mesh.apply_translation((17.613968679, 54.210221429, -139.2))
        elif name == 'lower_frame':
            mesh.apply_transform(trimesh.transformations.rotation_matrix(np.pi, (1, 0, 0)))
            mesh.apply_translation((0, 0, -118.35))
        printed[name] = solid(mesh)

    # Positive insertion raises the fixed pockets and, if seated in them,
    # the knob/yoke/input stack. .3075 only reaches edge contact; 1.8075
    # aligns the full 1.5 mm tooth band. Negative insertion goes the wrong way.
    for rise in (-1, -.1, 0, .05, .3075, .5, 1, 1.8075):
        native = {}
        for name, other in shapes.items():
            common = shaft.translate((0, 0, rise)).intersect(other)
            assert common.isValid(), (rise, name, 'invalid native common')
            native[name] = common.Volume()
        raw = {}
        for name in ('upper_frame', 'lower_frame'):
            common = printed['shaft'].translate((0, 0, rise)) ^ printed[name]
            assert common.status() == manifold.Error.NoError, (rise, name, common.status())
            raw[name] = {'status': str(common.status()), 'overlap_mm3': common.volume()}
        print(json.dumps({'shaft_insertion_mm': rise,
                          'predicted_lower_row_gap_mm': .3075 - rise,
                          'native_overlap_mm3': native, 'source_print_contact': raw}), flush=True)


if __name__ == '__main__':
    probe()
