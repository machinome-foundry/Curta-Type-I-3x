"""Localize the open-run frame contacts; evidence only, no geometry changes."""

import json
import logging

import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from simulation.carry import CarryBench
from simulation.curta import Curta
from simulation.tools.interference import world_solids
from simulation.tools.open_run_transitions import SecondCarryBench, bounds


def probe():
    root = Curta()
    root.set_state(initial_result=99, initial_turns=0, operand=1,
                   crank_turns=0, subtract=0, carriage_position=0,
                   carriage_lift=0, clear=0)
    root.assemble()
    frame_path = 'Curta.frame.upper_frame.main_body'
    frame = world_solids(root, selected={frame_path})[frame_path]
    preload = 4.2*root.carry_mechanism.result_carries.results_tens_lever_assembly_1.engage.value
    records, selected_shapes = [], {}
    for stage, model_class in ((1, CarryBench), (2, SecondCarryBench)):
        model = model_class()
        for drop in (0, preload, 2.562, 4.2, 2.35):
            model.set_state(engaged=drop/4.2)
            model.assemble()
            shapes = world_solids(model, include_flexible=True)
            for name, suffix in (('slider', 'tens_slider_for_results'),
                                 ('spring', 'carry_lever_spring.wire')):
                shape = shapes['Curta.'+suffix]
                overlap = shape.intersect(frame)
                row = dict(stage=stage, part=name, drop_mm=drop,
                           valid=overlap.isValid(), volume_mm3=overlap.Volume())
                if row['volume_mm3'] > 0:
                    row['bounds_mm'] = bounds(overlap).tolist()
                    row['regions'] = [dict(volume_mm3=s.Volume(), center_mm=s.Center().toTuple())
                                      for s in overlap.Solids()]
                records.append(row)
                if stage == 1:
                    if name == 'spring' and drop == 2.562:
                        selected_shapes['spring'] = (shape, overlap)
                    elif name == 'slider' and drop in (0, 4.2):
                        selected_shapes['slider-up' if drop == 0 else 'slider-down'] = (shape, overlap)

    figure, axes = plt.subplots(1, 3, figsize=(16, 6))
    configurations = (
        ('spring', cq.Plane((54, 0, 0), (0, 1, 0), (1, 0, 0)),
         (-13, -9), (-21, -14), 'World Y (mm)', 'World Z (mm)',
         'Spring at trip threshold: X = 54 mm'),
        ('slider-down', cq.Plane((0, 0, -16.35), (1, 0, 0), (0, 0, 1)),
         (52.5, 53.1), (-8.3, -6), 'World X (mm)', 'World Y (mm)',
         'Lowered slider: Z = -16.35 mm'),
        ('slider-up', cq.Plane((0, 0, -21.9), (1, 0, 0), (0, 0, 1)),
         (47, 54), (-11, -4), 'World X (mm)', 'World Y (mm)',
         'Raised slider: Z = -21.9 mm'),
    )
    for ax, (name, plane, xlim, ylim, xlabel, ylabel, title) in zip(axes, configurations):
        shape, overlap = selected_shapes[name]
        for label, part, color, width in (
                ('Upper frame', frame, 'gray', 1.3),
                (name.capitalize(), shape, 'tab:blue', 1.8),
                ('Native overlap', overlap, 'tab:red', 3)):
            section = cq.Workplane(plane).add(part).section().val()
            for index, edge in enumerate(section.Edges()):
                points, _ = edge.sample(60)
                local = [plane.toLocalCoords(p) for p in points]
                ax.plot([p.x for p in local], [p.y for p in local], color=color,
                        linewidth=width, label=label if index == 0 else None)
        ax.set(xlim=xlim, ylim=ylim, xlabel=xlabel, ylabel=ylabel, title=title)
        ax.set_aspect('equal')
        ax.grid(alpha=.3)
        ax.legend()
    figure.suptitle('Curta first result carry — measured frame intersections, not proposed reliefs')
    figure.tight_layout()
    output = '_build_evidence/open-run-frame-sections.png'
    figure.savefig(output, dpi=180)
    plt.close(figure)
    print(json.dumps(dict(kind='frame-contact-localization', frame=frame_path,
                          preload_mm=preload, records=records, image=output),
                     sort_keys=True), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    probe()
