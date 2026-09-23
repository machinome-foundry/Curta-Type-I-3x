"""Native carry/frame contact sections with the original guides still present."""

import argparse
import logging
from pathlib import Path

import cadquery as cq
import matplotlib.pyplot as plt
from simulation.carry_bank_frame import CarryBankFrameBench, FittedCarryBankFrameBench
from simulation.tools.interference import world_solids


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True, type=Path)
    parser.add_argument('--candidate', action='store_true')
    args = parser.parse_args()
    model = FittedCarryBankFrameBench() if args.candidate else CarryBankFrameBench()
    model.set_state(drop_mm=0)
    model.assemble()
    figure, axes = plt.subplots(2, 3, figsize=(17, 11))
    for row, (path, slider, angle, lower_z) in enumerate((
            ('result_carries.results_tens_lever_assembly_3', 'tens_slider_for_results', 40, -16.35),
            ('turns_carries.turns_tens_lever_assembly_1', 'tens_slider_for_turns_counter', -130, -15.6))):
        for col, (drop, z, spring) in enumerate(((0, -21.9, False), (4.2, lower_z, False),
                                                (2.562, -17.5, True))):
            model.set_state(drop_mm=drop)
            shapes = world_solids(model, include_flexible=True)
            prefix = 'Curta.'+path+'.'
            move = 'carry_lever_spring.wire' if spring else slider
            frame = shapes['Curta.frame.main_body'].rotate((0, 0, 0), (0, 0, 1), angle)
            guide = shapes[prefix+'tens_slide_bearing'].rotate((0, 0, 0), (0, 0, 1), angle)
            body = shapes[prefix+move].rotate((0, 0, 0), (0, 0, 1), angle)
            common = body.intersect(frame)
            plane = cq.Plane((0, 0, z), (1, 0, 0), (0, 0, 1))
            axis = axes[row, col]
            for label, shape, color, width in (('frame', frame, 'gray', 1.4),
                    ('guide', guide, 'tab:green', 1.6), ('spring' if spring else 'slider', body, 'tab:blue', 1.5),
                    ('positive common', common, 'tab:red', 2.4)):
                if not shape.Solids():
                    continue
                section = cq.Workplane(plane).add(shape).section().val()
                for index, edge in enumerate(section.Edges()):
                    points, _ = edge.sample(60)
                    axis.plot([p.x for p in points], [p.y for p in points], color=color,
                              linewidth=width, label=label if index == 0 else None)
            axis.set(xlim=(47, 64), ylim=(-13, -5.5), aspect='equal', xlabel='Station X (mm)',
                     ylabel='Station Y (mm)', title=f'{path.split(".")[-1]}\ndrop {drop:g}, Z={z:g} mm')
            axis.grid(alpha=.3)
            axis.legend(fontsize=8)
    label = 'candidate' if args.candidate else 'current'
    figure.suptitle(f'Independent station sections — complete {label} frame, unchanged moving parts and guides')
    figure.tight_layout()
    figure.savefig(args.image, dpi=160)
    plt.close(figure)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
