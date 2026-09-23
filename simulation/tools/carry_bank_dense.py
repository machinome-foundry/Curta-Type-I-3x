"""Independent native/world64 dense proof of all installed carry passages."""

import argparse
import json
import logging
from time import monotonic

import numpy as np

from simulation.carry_bank_frame import FittedCarryBankFrameBench, stations
from simulation.cover_fits import mesh_solid
from simulation.detents import RESULTS, TURNS
from simulation.tools.higher_locking_envelope import faceted_common_volume
from simulation.tools.interference import world_solids


def require_frame(frame):
    if not frame.isValid() or len(frame.Solids()) != 1 or frame.Volume() <= 0:
        raise ValueError('The complete positive-volume frame must be present')


def require_stroke(raised_vertices, current_vertices, drop):
    np.testing.assert_allclose(current_vertices, raised_vertices-(0, 0, drop),
                               atol=1e-8, rtol=0,
                               err_msg='Actual slider travel differs from the required stroke')


def main():
    started = monotonic()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bank', choices=('result', 'counter', 'both'), default='both')
    args = parser.parse_args()
    model = FittedCarryBankFrameBench()
    model.set_state(drop_mm=0)
    model.assemble()
    model.build_stls()
    chosen = [(path, node, slider) for path, node, slider in stations(model)
              if args.bank == 'both' or path.startswith('result' if args.bank == 'result' else 'turns')]
    initial = {path: getattr(node, slider).mesh.vertices.copy() for path, node, slider in chosen}
    frame = model.frame.main_body.shape()
    require_frame(frame)
    frame_mesh = mesh_solid(model.frame.main_body.mesh)
    paths = {'Curta.'+path+'.'+suffix for path, _, slider in chosen
             for suffix in (slider, 'carry_lever_spring.wire')}
    drops = sorted({4.2*i/40 for i in range(41)} |
                   {4.2*x for x, _ in (*RESULTS, *TURNS)} | {1.1630815})
    rows, failures = 0, []
    for drop in drops:
        model.set_state(drop_mm=drop)
        native = world_solids(model, include_flexible=True, selected=paths)
        assert set(native) == paths
        for path, node, slider in chosen:
            require_stroke(initial[path], getattr(node, slider).mesh.vertices, drop)
            for suffix, part in ((slider, getattr(node, slider)),
                                 ('carry_lever_spring.wire', node.carry_lever_spring.wire)):
                common = native['Curta.'+path+'.'+suffix].intersect(frame)
                if not common.isValid() or common.Volume() < 0:
                    raise ValueError('Invalid/signed-negative native contact')
                values = (common.Volume(), faceted_common_volume(mesh_solid(part.mesh) ^ frame_mesh))
                row = dict(station=path, part=suffix, drop_mm=drop,
                           native_mm3=values[0], world64_mm3=values[1])
                rows += 1
                print(json.dumps(row), flush=True)
                if values != (0, 0):
                    failures.append(row)
    print(json.dumps(dict(kind='finished', poses=len(drops), stations=len(chosen), rows=rows,
                          failures=failures, wall_seconds=monotonic()-started)), flush=True)
    assert not failures, failures


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
