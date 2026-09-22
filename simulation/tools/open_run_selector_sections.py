"""Localize selector findings and measure working contacts; never fit a part."""

import hashlib
import json
import logging
from math import pi
from pathlib import Path

import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from simulation.curta import Curta
from simulation.tools.carry_frame_sections import plot_section
from simulation.tools.interference import world_solids
from simulation.tools.open_run_selector import SELECTOR, INPUT_GROUP, MOVERS, move_shape, retained_state
from simulation.tools.open_run_transitions import bounds


def probe():
    root = Curta()
    root.set_state(initial_result=99, initial_turns=0, operand=1, crank_turns=0,
                   subtract=0, carriage_position=0, carriage_lift=0, clear=0)
    root.assemble()
    frozen = retained_state(root)
    housing = 'Curta.enclosure.lower_housing_1.bottom_housing'
    native = world_solids(root, selected=set(MOVERS) | {housing})
    assert set(native) == set(MOVERS) | {housing}
    posed = {path: move_shape(path, shape, 0, 1) if path in MOVERS else shape
             for path, shape in native.items()}
    prefix = SELECTOR+'.selector_knob_1_419057.'
    names = dict(knob=prefix+'selector_knob', ball=prefix+'p_5mm_ball',
                 spring=prefix+'selector_knob_spring', screw=prefix+'digit_selector_screw',
                 shaft=SELECTOR+'.selector_shaft_bottom',
                 top=SELECTOR+'.selector_shaft_top_1_419054.selector_shaft_top',
                 roll=SELECTOR+'.selector_shaft_top_1_419054.number_roll',
                 group=INPUT_GROUP, housing=housing)
    bodies = {name: posed[path] for name, path in names.items()}
    result = dict(kind='selector-contact-localization', setting=0, frozen_state=frozen,
                  parts={name: dict(path=names[name], volume_mm3=shape.Volume(),
                                   bounds_mm=bounds(shape).tolist(), valid=shape.isValid(),
                                   solids=len(shape.Solids()),
                                   face_types=sorted(set(f.geomType() for f in shape.Faces())))
                         for name, shape in bodies.items()}, contact_probes=[])
    ball = bodies['ball']
    nominal_ball = cq.Solid.makeSphere(2.5, ball.Center(), angleDegrees1=-90,
                                      angleDegrees2=90, angleDegrees3=360)
    differences = (ball.cut(nominal_ball), nominal_ball.cut(ball))
    assert all(shape.isValid() for shape in differences)
    result['five_mm_ball_comparison'] = dict(source_volume_mm3=ball.Volume(),
        nominal_sphere_volume_mm3=4*pi*2.5**3/3,
        source_outside_nominal_mm3=differences[0].Volume(),
        nominal_outside_source_mm3=differences[1].Volume(),
        note='Comparison witness only; no source or operating ball is replaced')

    for motion, moving, against, deltas in (
        ('input-group axial offset', 'group', 'knob', (0, -.01, .01, -.05, .05, -.1, .1, -.25, .25, -.5, .5, -1, 1)),
        ('selector-shaft angular offset', 'shaft', 'screw', (0, -.1, .1, -1, 1, -2, 2, -5, 5)),
    ):
        for delta in deltas:
            shape = (bodies[moving].translate((0, 0, delta)) if moving == 'group'
                     else bodies[moving].rotate((58.5, 0, 0), (58.5, 0, 1), delta))
            common = shape.intersect(bodies[against])
            assert common.isValid() and common.Volume() >= 0
            result['contact_probes'].append(dict(motion=motion, delta=delta,
                unit='mm' if moving == 'group' else 'deg', moving=names[moving],
                against=names[against], overlap_mm3=common.Volume()))

    figure, axes = plt.subplots(2, 3, figsize=(17, 11))
    configurations = (
        ('Knob / housing slot', 'knob', 'housing',
         cq.Plane((0, 0, -63), (1, 0, 0), (0, 0, 1)), (60, 71), (-4.5, 4.5), 'X', 'Y'),
        ('Number roll / housing', 'roll', 'housing',
         cq.Plane((0, 0, -43.8), (1, 0, 0), (0, 0, 1)), (48, 69), (-11, 10), 'X', 'Y'),
        ('Ball / helical shaft', 'ball', 'shaft',
         cq.Plane((0, -.58, 0), (1, 0, 0), (0, -1, 0)), (57, 67), (-60, -52), 'X', 'Z'),
        ('Spring / ball, source assembled pose', 'spring', 'ball',
         cq.Plane((0, 0, 0), (1, 0, 0), (0, -1, 0)), (60, 76), (-60, -52), 'X', 'Z'),
        ('Spring / knob back seat', 'spring', 'knob',
         cq.Plane((0, 0, 0), (1, 0, 0), (0, -1, 0)), (70, 77), (-60, -52), 'X', 'Z'),
        ('Shaft joint, 0.025 mm overlap', 'shaft', 'top',
         cq.Plane((0, 0, 0), (1, 0, 0), (0, -1, 0)), (53.5, 63.5), (-45, -41), 'X', 'Z'),
    )
    for ax, (title, first, second, plane, xlim, ylim, xlabel, ylabel) in zip(axes.flat, configurations):
        a, b = bodies[first], bodies[second]
        common = a.intersect(b)
        assert common.isValid() and common.Volume() > 0
        for shape, name, color, width in ((b, second, 'gray', 1.5), (a, first, 'tab:blue', 1.6),
                                         (common, 'Native overlap', 'tab:red', 3)):
            plot_section(ax, plane, shape, name, color, width)
        ax.set(title=f'{title}\nNative overlap {common.Volume():.9f} mm³',
               xlim=xlim, ylim=ylim, xlabel=xlabel+' (mm)', ylabel=ylabel+' (mm)')
        ax.set_aspect('equal')
        ax.grid(alpha=.3)
        ax.legend(fontsize=8)
    figure.suptitle('Selected Curta input, setting zero — existing installed contacts, not proposed fits\n'
                    'Native sections, equal axis scales; complete 428-body sweeps are recorded separately')
    figure.tight_layout()
    output = Path('_build_evidence/open-run-selector-sections.png')
    figure.savefig(output, dpi=170)
    plt.close(figure)
    assert retained_state(root) == frozen
    result.update(image=str(output), image_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                  retained_state_unchanged=True)
    record = Path('_build_evidence/open-run-selector-sections.json')
    record.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(record), image=str(output),
                          ball_comparison=result['five_mm_ball_comparison'])), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    probe()
