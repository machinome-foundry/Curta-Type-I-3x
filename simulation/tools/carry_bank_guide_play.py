"""Measure unchanged guide play; positive source contacts remain findings."""

import json
import logging
from math import cos, sin, radians
from time import monotonic

import numpy as np

from simulation.carry_bank_frame import FittedCarryBankFrameBench, stations
from simulation.carry_bank_regions import RESULT_ANGLES, COUNTER_ANGLES
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume
from simulation.tools.interference import world_solids


def main():
    started = monotonic()
    model = FittedCarryBankFrameBench()
    model.set_state(drop_mm=0)
    model.assemble()
    model.build_stls()
    rows = []
    selected = {'Curta.'+path+'.'+suffix for path, _, slider in stations(model)
                for suffix in (slider, 'tens_slide_bearing')}
    for drop in (0, 2.1, 4.2):
        model.set_state(drop_mm=drop)
        shapes = world_solids(model, selected=selected)
        for path, node, slider in stations(model):
            index = int(path.rsplit('_', 1)[-1])-1
            angle = radians((COUNTER_ANGLES if path.startswith('turns') else RESULT_ANGLES)[index])
            guide = shapes['Curta.'+path+'.tens_slide_bearing']
            native = shapes['Curta.'+path+'.'+slider]
            mesh = getattr(node, slider).mesh
            guide_mesh = mesh_solid(node.tens_slide_bearing.mesh)
            for axis, direction in (('radial', (cos(angle), sin(angle), 0)),
                                    ('tangential', (-sin(angle), cos(angle), 0))):
                for offset in (-.2, -.01, 0, .01, .2):
                    vector = np.array(direction)*offset
                    common = native.translate(tuple(vector)).intersect(guide)
                    moved = mesh.copy()
                    moved.apply_translation(vector)
                    row = dict(station=path, drop_mm=drop, axis=axis, offset_mm=offset,
                               native_valid=common.isValid(), native_mm3=common.Volume(),
                               world64_mm3=faceted_common_volume(mesh_solid(moved) ^ guide_mesh))
                    rows.append(row)
                    print(json.dumps(row), flush=True)
    print(json.dumps(dict(kind='finished', rows=len(rows),
                          invalid_native=sum(not row['native_valid'] for row in rows),
                          unshifted_positive=sum(row['offset_mm'] == 0 and
                              (row['native_mm3'] > 0 or row['world64_mm3'] > 0) for row in rows),
                          wall_seconds=monotonic()-started,
                          acceptance='Unchanged source-interface measurement; no overlap waiver')),
          flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
