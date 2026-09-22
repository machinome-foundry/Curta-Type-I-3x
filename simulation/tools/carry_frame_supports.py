"""Read-only native support map for the ratified frame-fit feasibility gate.

No relief cutter or fitted geometry is created. Nearby faces are an inventory,
not automatically a set of safe-to-remove material.
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
from simulation.tools.moving_seats import world_frames
from simulation.tools.open_run_transitions import bounds


def describe(shape):
    result = dict(valid=shape.isValid(), volume_mm3=shape.Volume())
    if shape.Vertices():
        result.update(bounds_mm=bounds(shape).tolist(), center_mm=shape.Center().toTuple())
    return result


def probe():
    model = CarryFrameBench()
    model.set_state(drop_mm=0)
    model.assemble()
    shapes = world_solids(model, include_flexible=True)
    # This historical feasibility probe always measures the original frame,
    # even after the operating bench has adopted the fitted adapter.
    frame = MainBody().shape()
    records = dict(kind='native-frame-support-map', frame=describe(frame),
                   rigid_world_frames={k: v.tolist() for k, v in world_frames(model).items()},
                   stations={})
    first_shapes = {}
    for station in ('first', 'second'):
        prefix = 'Curta.'+station+'.'
        bearing = shapes[prefix+'tens_slide_bearing']
        seat = frame.intersect(bearing)
        record = dict(bearing=describe(bearing), frame_bearing_common=describe(seat),
                      frame_to_bearing_distance_mm=frame.distance(bearing), contacts=[])
        # Express second-station inspection bounds in the first station's
        # radial/tangential frame, without moving anything in the model.
        angle = 0 if station == 'first' else 20
        aligned_frame = frame.rotate((0, 0, 0), (0, 0, 1), angle)
        aligned_bearing = bearing.rotate((0, 0, 0), (0, 0, 1), angle)
        nearby = []
        for owner, shape in (('frame', aligned_frame), ('bearing', aligned_bearing)):
            for index, face in enumerate(shape.Faces()):
                box = bounds(face)
                if not np.all(np.minimum(box[1], (64, -5, 7)) >=
                              np.maximum(box[0], (46, -19, -24))):
                    continue
                item = dict(owner=owner, index=index, type=face.geomType(),
                            area_mm2=face.Area(), center_mm=face.Center().toTuple(),
                            bounds_mm=box.tolist())
                if face.geomType() == 'PLANE':
                    item['normal'] = face.normalAt().toTuple()
                nearby.append(item)
        record['nearby_faces_aligned_to_station_1'] = nearby
        for drop in (0, 1.1630815, 2.562, 4.2):
            model.set_state(drop_mm=drop)
            model.assemble()
            moving = world_solids(model, include_flexible=True,
                                  selected={prefix+'tens_slider_for_results',
                                            prefix+'carry_lever_spring.wire'})
            for label, suffix in (('slider', 'tens_slider_for_results'),
                                  ('spring', 'carry_lever_spring.wire')):
                body = moving[prefix+suffix]
                common = body.intersect(frame)
                item = dict(part=label, drop_mm=drop, overlap=describe(common))
                if common.Volume() > 0:
                    item['overlap_to_bearing_distance_mm'] = common.distance(bearing)
                    item['regions'] = [describe(solid) for solid in common.Solids()]
                record['contacts'].append(item)
                if station == 'first':
                    first_shapes[(label, drop)] = (body, common)
        records['stations'][station] = record

    figure, axes = plt.subplots(2, 3, figsize=(18, 11))
    bearing = shapes['Curta.first.tens_slide_bearing']
    configurations = (
        ('spring', 2.562, cq.Plane((54, 0, 0), (0, 1, 0), (1, 0, 0)),
         (-18, -5), (-24, 7), 'World Y', 'World Z', 'Spring leg; X = 54'),
        ('slider', 4.2, cq.Plane((0, 0, -16.35), (1, 0, 0), (0, 0, 1)),
         (47, 64), (-18, -4), 'World X', 'World Y', 'Lower edge; Z = -16.35'),
        ('slider', 0, cq.Plane((0, 0, -21.9), (1, 0, 0), (0, 0, 1)),
         (47, 64), (-18, -4), 'World X', 'World Y', 'Raised shoulder; Z = -21.9'),
        ('spring', 2.562, cq.Plane((0, -11.1, 0), (1, 0, 0), (0, 1, 0)),
         (47, 64), (-7, 24), 'World X', 'Minus world Z', 'Spring/frame contact; Y = -11.1'),
        ('slider', 4.2, cq.Plane((52.8, 0, 0), (0, 1, 0), (1, 0, 0)),
         (-18, -4), (-24, 7), 'World Y', 'World Z', 'Guide side; X = 52.8'),
        ('slider', 0, cq.Plane((0, -7.2, 0), (1, 0, 0), (0, 1, 0)),
         (47, 64), (-7, 24), 'World X', 'Minus world Z', 'Slider passage; Y = -7.2'),
    )
    for ax, (label, drop, plane, xlim, ylim, xlabel, ylabel, title) in zip(axes.flat, configurations):
        body, common = first_shapes[(label, drop)]
        for name, part, color, width in (
                ('Frame', frame, 'gray', 1.3), ('Fixed guide / spring seat', bearing, 'tab:green', 1.8),
                (label, body, 'tab:blue', 1.8), ('Native overlap', common, 'tab:red', 3)):
            section = cq.Workplane(plane).add(part).section().val()
            for index, edge in enumerate(section.Edges()):
                points, _ = edge.sample(60)
                local = [plane.toLocalCoords(point) for point in points]
                ax.plot([point.x for point in local], [point.y for point in local],
                        color=color, linewidth=width, label=name if index == 0 else None)
        ax.set(xlim=xlim, ylim=ylim, xlabel=xlabel+' (mm)', ylabel=ylabel+' (mm)', title=title)
        ax.set_aspect('equal')
        ax.grid(alpha=.3)
        ax.legend(fontsize=8)
    figure.suptitle('First result carry: unchanged source frame and fitted fixed guide — feasibility evidence')
    figure.tight_layout()
    image = Path('_build_evidence/carry-frame-supports.png')
    image.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(image, dpi=160)
    plt.close(figure)
    records['image'] = str(image)
    output = Path('_build_evidence/carry-frame-supports.json')
    output.write_text(json.dumps(records, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(output), image=str(image), stations={
        key: {name: value for name, value in record.items()
              if name != 'nearby_faces_aligned_to_station_1'}
        for key, record in records['stations'].items()})), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    probe()
