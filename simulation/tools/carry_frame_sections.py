"""Before/after native sections; identical moving parts and guides in both."""

import hashlib
import json
import logging
from pathlib import Path

import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from simulation.carry_frame import CarryFrameBench
from simulation.standard.parts import MainBody
from simulation.tools.interference import world_solids


def plot_section(ax, plane, shape, name, color, width):
    if not shape.Vertices():
        return
    edges = []
    for section in cq.Workplane(plane).add(shape).section().vals():
        if hasattr(section, 'Edges'):
            edges.extend(section.Edges())
    for index, edge in enumerate(edges):
        points, _ = edge.sample(60)
        points = [plane.toLocalCoords(point) for point in points]
        ax.plot([point.x for point in points], [point.y for point in points],
                color=color, linewidth=width, label=name if index == 0 else None)


def render():
    model = CarryFrameBench()
    model.set_state(drop_mm=0)
    model.assemble()
    source, fitted = MainBody().shape(), model.frame.main_body.shape()
    records = []
    for station, angle in (('first', 0), ('second', 20)):
        figure, axes = plt.subplots(3, 2, figsize=(13, 15))
        configurations = (
            ('Spring lower leg', 2.562, 'carry_lever_spring.wire',
             cq.Plane((54, 0, 0), (0, 1, 0), (1, 0, 0)),
             (-11.55, -10.15), (-20.2, -15.5), 'Y', 'Z'),
            ('Lowered slider edge', 4.2, 'tens_slider_for_results',
             cq.Plane((0, 0, -16.35), (1, 0, 0), (0, 0, 1)),
             (52.6, 53), (-8.4, -6.2), 'X', 'Y'),
            ('Raised slider shoulder / guide-seat edge', 0, 'tens_slider_for_results',
             cq.Plane((0, -7.2, 0), (1, 0, 0), (0, 1, 0)),
             (48, 53.2), (21.3, 22.5), 'X', 'minus Z'),
        )
        for row, (title, drop, suffix, plane, xlim, ylim, xlabel, ylabel) in enumerate(configurations):
            model.set_state(drop_mm=drop)
            model.assemble()
            prefix = 'Curta.'+station+'.'
            bodies = world_solids(model, include_flexible=True,
                                  selected={prefix+suffix, prefix+'tens_slide_bearing'})
            moving = bodies[prefix+suffix].rotate((0, 0, 0), (0, 0, 1), angle)
            guide = bodies[prefix+'tens_slide_bearing'].rotate((0, 0, 0), (0, 0, 1), angle)
            for column, (label, frame) in enumerate((('Before', source), ('After', fitted))):
                frame = frame.rotate((0, 0, 0), (0, 0, 1), angle)
                common = frame.intersect(moving)
                if not common.isValid():
                    raise ValueError('Invalid section contact geometry')
                ax = axes[row, column]
                for shape, name, color, width in ((frame, 'Frame', 'gray', 1.5),
                        (guide, 'Unchanged guide', 'tab:green', 1.5),
                        (moving, 'Unchanged moving part', 'tab:blue', 1.8),
                        (common, 'Native overlap', 'tab:red', 3)):
                    plot_section(ax, plane, shape, name, color, width)
                ax.set(xlim=xlim, ylim=ylim, xlabel=xlabel+' (mm)', ylabel=ylabel+' (mm)',
                       title=f'{label}: {title}\nNative overlap {common.Volume():.9f} mm³')
                ax.set_aspect('equal')
                ax.grid(alpha=.3)
                ax.legend(fontsize=8)
        figure.suptitle(f'{station.capitalize()} result-carry frame fit — native sections\n'
                       'Station-local axes coincide with station one; no part is relocated')
        figure.tight_layout()
        output = Path('_build_evidence/carry-frame-sections-'+station+'.png')
        figure.savefig(output, dpi=170)
        plt.close(figure)
        records.append(dict(station=station, image=str(output),
                            sha256=hashlib.sha256(output.read_bytes()).hexdigest()))
    print(json.dumps(records), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    render()
