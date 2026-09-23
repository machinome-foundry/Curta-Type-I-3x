"""Native sections of the source and isolated counter-shoulder candidate."""

import argparse
import logging
from pathlib import Path

import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from simulation.carry_bank_frame import FittedCarryBankFrameBench
from simulation.counter_guide_trial import CounterShoulderTrial
from simulation.tools.carry_frame_sections import plot_section
from simulation.tools.interference import world_solids


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path, required=True)
    args = parser.parse_args()
    figure, axes = plt.subplots(2, 2, figsize=(12, 10))
    prefix = 'Curta.turns_carries.turns_tens_lever_assembly_1.'
    names = (prefix+'tens_slider_for_turns_counter', prefix+'tens_slide_bearing')
    plane = cq.Plane((0, -7.2, 0), (1, 0, 0), (0, -1, 0))
    for column, (title, model_type) in enumerate((
            ('Original', FittedCarryBankFrameBench), ('Isolated .35 mm relief', CounterShoulderTrial))):
        model = model_type()
        model.set_state(drop_mm=4.2)
        model.assemble()
        shapes = world_solids(model, selected=set(names))
        body, guide = (shapes[name].rotate((0, 0, 0), (0, 0, 1), -130) for name in names)
        for row, (xlim, ylim) in enumerate((((53, 63), (-28, 0)),
                                           ((60, 62), (-17.6, -16)))):
            axis = axes[row, column]
            for shape, name, color in ((body, 'Counter slider', 'tab:blue'),
                                       (guide, 'Unchanged guide', 'tab:green')):
                plot_section(axis, plane, shape, name, color, 1.8)
            axis.set(xlim=xlim, ylim=ylim, aspect='equal', xlabel='Station X (mm)',
                     ylabel='Station Z (mm)', title=title+' — full 4.2 mm drop')
            axis.grid(alpha=.3)
            axis.legend(fontsize=8)
    figure.suptitle('Native counter shoulder sections, Y=-7.2 mm\n'
                   'Scoped shoulder fit; whole-guide contact and capture remain separate')
    figure.tight_layout()
    figure.savefig(args.image, dpi=160)
    plt.close(figure)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
