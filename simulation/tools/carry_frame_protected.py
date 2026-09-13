"""Named installed supports around the independently bounded frame removal.

The complete original-minus-fitted native difference is the preservation
contract. Distances below locate the protected hardware and non-selected
guides relative to that difference; they are not a mass-budget substitute.
"""

import hashlib
import json
import logging
from pathlib import Path

from simulation.curta import Curta
from simulation.standard.parts import MainBody
from simulation.test_frame_fits import forbidden_removal
from simulation.tools.interference import world_solids
from simulation.tools.open_run_transitions import bounds, physical_nodes


def report():
    root = Curta()
    root.set_state(initial_result=99, initial_turns=0, operand=1, crank_turns=0,
                   subtract=0, carriage_position=0, carriage_lift=0, clear=0)
    root.assemble()
    nodes = dict(physical_nodes(root))
    frame_path = 'Curta.frame.upper_frame.main_body'
    groups = {}
    for path in nodes:
        if path == frame_path:
            continue
        name = path.rsplit('.', 1)[-1]
        if name == 'tens_slide_bearing':
            if any(f'results_tens_lever_assembly_{i}.' in path for i in (1, 2)):
                continue  # Their approved edge exception has its own face map.
            groups[path] = 'non-selected carry guide'
        elif 'frame_support_' in name or name.startswith('m4_nut_'):
            groups[path] = 'frame support / nut'
        elif name.startswith('m4'):
            groups[path] = 'M4 fastening'
        elif path.startswith('Curta.frame.'):
            groups[path] = 'fixed bearing / frame neighbour'
        elif name in ('main_crank', 'upper_outer_sleeve') or 'main_axle_step_drum_' in name:
            groups[path] = 'main shaft / drum support'
    native = world_solids(root, selected=set(groups) | {frame_path})
    if set(native) != set(groups) | {frame_path}:
        raise ValueError('A named protection reference is missing native geometry')
    original, fitted = MainBody().shape(), native[frame_path]
    removed = original.cut(fitted)
    outside = forbidden_removal(original, fitted)
    assert removed.isValid() and removed.Volume() > 0
    assert outside.isValid() and outside.Volume() == 0
    references = []
    for path, group in sorted(groups.items()):
        distance = removed.distance(native[path])
        if distance <= 0:
            raise ValueError(f'Frame relief reaches a protected installed body: {path}')
        references.append(dict(path=path, group=group, bounds_mm=bounds(native[path]).tolist(),
                               removal_distance_mm=distance))
    # The complete source cylinder inventory includes fastener bores, shaft
    # passages and the large frame wall. Report changed surfaces honestly;
    # the latter may meet the approved local shoulder at its bottom rim.
    cylinders = []
    for index, face in enumerate(original.Faces()):
        if face.geomType() != 'CYLINDER':
            continue
        lost = face.cut(fitted)
        assert lost.isValid()
        cylinders.append(dict(source_face=index, bounds_mm=bounds(face).tolist(),
                              original_area_mm2=face.Area(), removed_area_mm2=lost.Area()))
    protected_sources = ('standard/carry.py', 'carry_spring.py', 'carry_seat.py',
                         'detents.py', 'carry_heads.py', 'carry_fits.py', 'carry_profiles.py')
    result = dict(kind='carry-frame-protected-features', references=references,
                  source_cylinders=cylinders, outside_permitted_removal_mm3=outside.Volume(),
                  unchanged_source_sha256={name: hashlib.sha256(
                      (Path('simulation')/name).read_bytes()).hexdigest() for name in protected_sources})
    output = Path('_build_evidence/carry-frame-protected.json')
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(output), named_references=len(references),
                         minimum_reference_distance_mm=min(p['removal_distance_mm'] for p in references),
                         changed_cylinder_faces=[c for c in cylinders if c['removed_area_mm2'] > 1e-7])),
          flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    report()
