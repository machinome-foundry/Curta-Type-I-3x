"""Measure whether the requested gap reaches an existing guide seating land.

The 0.025 mm translated slider copies below are witness geometry only: each
lies within the requested 0.05 mm clearance neighbourhood. They are neither
new operating poses nor a production cutter. No installed part is changed.
"""

import json
import logging
from pathlib import Path

import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from simulation.carry_frame import CarryFrameBench
from simulation.standard.parts import MainBody
from simulation.tools.interference import world_solids
from simulation.tools.open_run_transitions import bounds


def side_face(shape, *, frame):
    matches = []
    for face in shape.Faces():
        box = bounds(face)
        if (face.geomType() == 'PLANE' and
                np.allclose(box[:, 0], 52.8, atol=1e-5, rtol=0) and
                abs(box[0, 2] - (-22.2 if frame else -21.6)) < 1e-5 and
                abs(box[1, 2] - (-15.9 if frame else -4.2)) < 1e-5):
            matches.append(face)
    if len(matches) != 1:
        raise ValueError(f'Expected one measured side face, got {len(matches)}')
    return matches[0]


def face_record(shape):
    result = dict(valid=shape.isValid(), area_mm2=shape.Area(), faces=len(shape.Faces()))
    if shape.Vertices():
        result['bounds_mm'] = bounds(shape).tolist()
    return result


def draw(ax, shape, label, color, width):
    for index, edge in enumerate(shape.Edges()):
        points, _ = edge.sample(60)
        ax.plot([point.y for point in points], [point.z for point in points],
                color=color, linewidth=width, label=label if index == 0 else None)


def probe():
    model = CarryFrameBench()
    model.set_state(drop_mm=0)
    model.assemble()
    fixed = world_solids(model, selected={'Curta.frame.main_body',
        'Curta.first.tens_slide_bearing', 'Curta.second.tens_slide_bearing'})
    # The approval gate concerns the source land, not its subsequent fit.
    frame = MainBody().shape()
    result = dict(kind='protected-guide-seat-clearance-gate', requested_gap_mm=.05,
                  witness_offset_mm=.025, stations={})
    figure, axes = plt.subplots(1, 2, figsize=(13, 7))
    for station, angle in (('first', 0), ('second', 20)):
        prefix = 'Curta.'+station+'.'
        frame_aligned = frame.rotate((0, 0, 0), (0, 0, 1), angle)
        bearing = fixed[prefix+'tens_slide_bearing'].rotate((0, 0, 0), (0, 0, 1), angle)
        frame_side = side_face(frame_aligned, frame=True)
        guide_side = side_face(bearing, frame=False)
        seat = frame_side.intersect(guide_side)
        if not seat.isValid() or seat.Area() <= 0:
            raise ValueError('No valid native guide/frame seating patch')
        record = dict(frame_face=face_record(frame_side), guide_face=face_record(guide_side),
                      common_seating_land=face_record(seat), endpoints=[])
        for index, (name, drop, offset) in enumerate((('raised', 0, .025), ('lowered', 4.2, -.025))):
            model.set_state(drop_mm=drop)
            model.assemble()
            slider = world_solids(model, selected={prefix+'tens_slider_for_results'})[
                prefix+'tens_slider_for_results'].rotate((0, 0, 0), (0, 0, 1), angle)
            touch = seat.intersect(slider)
            # Every point in this translated copy is only 0.025 mm from a
            # point of the actual slider, strictly inside the requested gap.
            witness = slider.translate((0, 0, offset))
            invaded_seat = seat.intersect(witness)
            # A 0.01 mm native frame layer behind the independently identified
            # registration face establishes that this is existing material.
            behind = cq.Solid.makeBox(.01, 1.47, .025, cq.Vector(
                52.79, -7.89, -21.6 if name == 'raised' else -16.825))
            material = witness.intersect(frame_aligned).intersect(behind)
            record['endpoints'].append(dict(endpoint=name, drop_mm=drop,
                slider_to_seat_distance_mm=slider.distance(seat),
                actual_slider_on_seat=face_record(touch),
                gap_witness_on_seat=face_record(invaded_seat),
                witness_in_frame_skin=dict(valid=material.isValid(), volume_mm3=material.Volume())))
            if station == 'first':
                ax = axes[index]
                draw(ax, frame_side, 'Frame registration face', 'gray', 1.3)
                draw(ax, seat, 'Existing guide/frame seating land', 'tab:green', 1.8)
                draw(ax, invaded_seat, 'Seat inside 0.025 mm gap witness', 'tab:red', 3)
                ax.set(xlim=(-8.3, -6.2),
                       ylim=(-21.7, -21.45) if name == 'raised' else (-16.95, -16.7),
                       xlabel='World Y (mm)', ylabel='World Z (mm)',
                       title=name.capitalize()+' slider — X = 52.8 mm')
                ax.grid(alpha=.3)
                ax.legend(fontsize=8)
        result['stations'][station] = record
    figure.suptitle('Protected guide-seat edge lies inside the requested 0.05 mm clearance\n'
                   'Native source contact faces; axes enlarged vertically to inspect 0.025 mm strips')
    figure.tight_layout()
    image = Path('_build_evidence/carry-frame-seat-gate.png')
    image.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(image, dpi=170)
    plt.close(figure)
    result['image'] = str(image)
    output = Path('_build_evidence/carry-frame-seat-gate.json')
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    probe()
