"""Map native guide lands and contact regions before extending frame passages."""

import argparse
import json
import logging
import math
import time

import numpy as np
from simulation.carry_bank_frame import CarryBankFrameBench, stations
from simulation.standard.parts import MainBody
from simulation.test_frame_fits import registration_lands
from simulation.tools.interference import world_solids
from simulation.tools.moving_seats import world_frames
from simulation.tools.open_run_transitions import bounds


def describe(shape, *, surface=False):
    assert shape.isValid()
    result = dict(area_mm2=shape.Area())
    if not surface:
        result['volume_mm3'] = shape.Volume()
    if shape.Vertices():
        result['bounds_mm'] = bounds(shape).tolist()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drop', type=float, action='append')
    args = parser.parse_args()
    drops = args.drop if args.drop is not None else (0, .084, 1.1630815, 2.562, 4.2)
    if any(not 0 <= drop <= 4.2 for drop in drops):
        parser.error('drops must be within the supported 0..4.2 mm stroke')
    started = time.monotonic()
    model = CarryBankFrameBench()
    model.set_state(drop_mm=0)
    model.assemble()
    source = MainBody().shape()
    frames = world_frames(model, include_assemblies=True)
    first = frames['Curta.result_carries.results_tens_lever_assembly_1.tens_slide_bearing']
    shapes = world_solids(model, include_flexible=True)
    records = {}
    for path, node, slider in stations(model):
        guide = shapes['Curta.'+path+'.tens_slide_bearing']
        relative = frames['Curta.'+path+'.tens_slide_bearing'] @ np.linalg.inv(first)
        angle = math.degrees(math.atan2(relative[1, 0], relative[0, 0]))
        # Inspection-only rotation: retain the full transform and its source
        # residuals instead of claiming exact rotational symmetry.
        nominal = round(angle/10)*10
        lands = list(registration_lands(source, guide))
        assert lands
        record = dict(path=path, relative_guide_frame=relative.tolist(),
                      inspection_rotation_degrees=-nominal,
                      guide_frame_common=describe(source.intersect(guide)),
                      total_registration_area_mm2=sum(face.Area() for face in lands),
                      lands=[describe(face.rotate((0, 0, 0), (0, 0, 1), -nominal), surface=True)
                             for face in lands], contacts=[])
        records[path] = record
        print(json.dumps(dict(kind='supports', **record)), flush=True)
    for drop in drops:
        model.set_state(drop_mm=drop)
        shapes = world_solids(model, include_flexible=True)
        for path, node, slider in stations(model):
            angle = records[path]['inspection_rotation_degrees']
            for suffix in (slider, 'carry_lever_spring.wire'):
                body = shapes['Curta.'+path+'.'+suffix]
                common = body.intersect(source)
                print(json.dumps(dict(kind='contact', path=path, part=suffix, drop_mm=drop,
                    aligned_common=describe(common.rotate((0, 0, 0), (0, 0, 1), angle)),
                    aligned_regions=[describe(piece.rotate((0, 0, 0), (0, 0, 1), angle))
                                     for piece in common.Solids()])), flush=True)
    print(json.dumps(dict(kind='finished', stations=len(records),
                          wall_seconds=time.monotonic()-started,
                          acceptance='Measurement only; no proposed region or fit is certified')),
          flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
