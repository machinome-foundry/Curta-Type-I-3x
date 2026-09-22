"""Conservative native full-stroke proof for the rigid slider.

Partition its native source bounding box. A cell is excluded only by a valid
zero-volume native intersection with the slider. For every occupied cell its
entire translated 4.2 mm interval is an exact box; that box must clear the
frame or be subdivided. No mesh, pose grid or endpoint union proves the path.
"""

import argparse
import json
import logging
from pathlib import Path
from time import monotonic

import cadquery as cq
import numpy as np

from simulation.carry_frame import CarryFrameBench
from simulation.tools.interference import world_solids
from simulation.tools.open_run_transitions import bounds, paths_for


def prism(box):
    return cq.Solid.makeBox(*(box[1]-box[0]), cq.Vector(*box[0]))


def certify(station, max_depth=36, part='slider'):
    start = monotonic()
    model = CarryFrameBench()
    model.set_state(drop_mm=0)
    model.assemble()
    path = 'Curta.'+station+'.tens_slider_for_results'
    shapes = world_solids(model, selected={path, 'Curta.frame.main_body'})
    slider, frame = shapes[path], shapes['Curta.frame.main_body']
    if part == 'sleeve':
        from simulation.curta import Curta
        root = Curta()
        root.set_state(initial_result=99, initial_turns=0, operand=1, crank_turns=0,
                       subtract=0, carriage_position=0, carriage_lift=0, clear=0)
        root.assemble()
        stage = 1 if station == 'first' else 2
        sleeve_path = paths_for(stage)[1]
        carry = getattr(root.carry_mechanism.result_carries,
                        'results_tens_lever_assembly_'+str(stage))
        installed = world_solids(root, selected={sleeve_path})[sleeve_path]
        # The coupled sleeve has the same vertical travel as its slider.
        # Undo the actual installed preload before enclosing the whole stroke.
        slider = installed.translate((0, 0, 4.2*carry.engage.value))
    # A common rigid rotation preserves every contact and the vertical travel.
    # Work in station-local axes so boxes follow the measured slider profile;
    # retaining world-axis boxes at station two wastes many empty subdivisions.
    angle = 0 if station == 'first' else 20
    slider = slider.rotate((0, 0, 0), (0, 0, 1), angle)
    frame = frame.rotate((0, 0, 0), (0, 0, 1), angle)
    source_bounds = bounds(slider)
    swept_bounds = source_bounds.copy()
    swept_bounds[0, 2] -= 4.2
    stack = [(bounds(slider), 0, slider, frame)]
    checks, empty, clear, unresolved = 0, 0, 0, []
    smallest = float('inf')
    while stack:
        box, depth, source_parent, frame_parent = stack.pop()
        sweep = box.copy()
        sweep[0, 2] -= 4.2
        # Additional nonzero guard beyond the native source-box tolerance.
        sweep += np.array([[-1e-6]*3, [1e-6]*3])
        # Child source/swept boxes lie inside their parents. Carry exact
        # native clips down the tree so later tests avoid irrelevant faces.
        contact = prism(sweep).intersect(frame_parent)
        checks += 1
        if not contact.isValid() or contact.Volume() < 0:
            raise ValueError('Invalid/signed-negative swept-box/frame Boolean')
        if contact.Volume() == 0:
            clear += 1
            smallest = min(smallest, float(min(box[1]-box[0])))
            continue
        occupied = prism(box).intersect(source_parent)
        if not occupied.isValid() or occupied.Volume() < 0:
            raise ValueError('Invalid/signed-negative source occupancy Boolean')
        if occupied.Volume() == 0:
            empty += 1
        elif depth >= max_depth:
            unresolved.append(dict(box_mm=box.tolist(), source_volume_mm3=occupied.Volume(),
                                   sweep_frame_volume_mm3=contact.Volume()))
        else:
            axis = int(np.argmax(box[1]-box[0]))
            middle = float(box[:, axis].mean())
            left, right = box.copy(), box.copy()
            left[1, axis], right[0, axis] = middle, middle
            stack.extend(((left, depth+1, occupied, contact),
                          (right, depth+1, occupied, contact)))
        if checks % 100 == 0:
            print(json.dumps(dict(phase='native-swept-cells', station=station,
                                 checked=checks, queued=len(stack), unresolved=len(unresolved))), flush=True)
        if len(unresolved) >= 4:
            break
    result = dict(kind=f'continuous-native-{part}-frame-enclosure', station=station,
                  raised_source_bounds_in_certificate_axes_mm=source_bounds.tolist(),
                  full_stroke_bounds_in_certificate_axes_mm=swept_bounds.tolist(),
                  common_coordinate_rotation_degrees=angle,
                  travel_mm=4.2, guard_mm=1e-6, max_depth=max_depth, native_frame_checks=checks,
                  clear_cells=clear, excluded_empty_cells=empty,
                  smallest_clear_cell_width_mm=smallest, unresolved=unresolved,
                  queued=len(stack), passed=not unresolved and not stack,
                  elapsed_seconds=monotonic()-start)
    suffix = '' if part == 'slider' else '-'+part
    path = Path('_build_evidence/carry-frame-swept-'+station+suffix+'.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)
    return result['passed']


if __name__ == '__main__':
    logging.disable(logging.INFO)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--station', choices=('first', 'second'), default='first')
    parser.add_argument('--part', choices=('slider', 'sleeve'), default='slider')
    args = parser.parse_args()
    raise SystemExit(0 if certify(args.station, part=args.part) else 1)
