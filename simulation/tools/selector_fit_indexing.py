"""Independent detent-index witness and read-only guide-alignment alternative.

Neither the alternate guide nor a flexible spring is installed by this probe.
The proposed center is derived from the native cone, not a prescribed pose
selected to hide an intersection. Material/support changes need a new decision.
"""

import hashlib
import json
import logging
from math import sin
from pathlib import Path

import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from OCP.BRepAdaptor import BRepAdaptor_Surface

from simulation.selector_fit import SelectorFitBench
from simulation.tools.carry_frame_sections import plot_section
from simulation.tools.interference import world_solids
from simulation.tools.selector_fit_contacts import BALL_Z, closest, radial_support
from simulation.tools.selector_fit_measurements import PATHS


def sphere(center):
    return cq.Solid.makeSphere(2.5, center, angleDegrees1=-90, angleDegrees2=90, angleDegrees3=360)


def measure():
    trace_path = Path('_build_evidence/selector-fit-contacts.json')
    trace = json.loads(trace_path.read_text())
    bench = SelectorFitBench()
    bench.set_state(setting=0, postcarry=0)
    bench.assemble()
    native = world_solids(bench, selected=set(PATHS.values()))
    bodies = {name: native[path] for name, path in PATHS.items()}
    zero_cone = BRepAdaptor_Surface(bodies['shaft'].Faces()[4].wrapped).Cone()
    axis = np.array(zero_cone.Axis().Direction().Coord())
    apex = np.array(zero_cone.Apex().Coord())
    # A sphere tangent to a cone all around its seat has its center on the
    # cone axis, radius/sin(semi-angle) from the apex.
    centered = apex + axis*(2.5/sin(zero_cone.SemiAngle()))
    centered_ball = sphere(tuple(centered))
    result = dict(kind='selector-detent-indexing-conflict',
        scope='Measured conflict and uninstalled alternative, not a ratified fit',
        contact_trace_sha256=hashlib.sha256(trace_path.read_bytes()).hexdigest(),
        source_cone_axis=axis.tolist(), source_cone_apex_mm=apex.tolist(),
        source_cone_center_height_mm=float(apex[2]), source_guide_height_mm=BALL_Z,
        source_guide_radius_mm=2.6185, nominal_ball_radius_mm=2.5,
        unmodified_guide_radial_play_mm=2.6185-2.5,
        nominal_center_on_cone_axis_mm=centered.tolist(),
        alignment_shift_yz_mm=[float(centered[1]), float(centered[2]-BALL_Z)],
        centered_trial_overlaps_mm3={}, numbered_state_witnesses=[],
        limitations=['No guide or spring-seat modification authorized by this measurement',
                     'No continuous clearance or force/friction/strength claim',
                     'Dense sampled trough location is approximate, not a minimum certificate'])
    for name in ('shaft', 'knob'):
        common = centered_ball.intersect(bodies[name])
        assert common.isValid() and common.Volume() >= 0
        result['centered_trial_overlaps_mm3'][name] = common.Volume()
    for setting in (1-.025, 1, 1+.025):
        shaft = bodies['shaft'].rotate((58.5, 0, 0), (58.5, 0, 1), setting*36)
        support = radial_support(shaft, BALL_Z-6*setting)
        current_ball = sphere((support['center_x_bracket_mm'][1], 0, BALL_Z-6*setting))
        knob = bodies['knob'].translate((0, 0, -6*setting))
        overlaps = {}
        for name, against in (('shaft', shaft), ('knob', knob)):
            common = current_ball.intersect(against)
            assert common.isValid() and common.Volume() >= 0
            overlaps[name] = common.Volume()
        row = dict(setting=setting, **support, overlaps_mm3=overlaps)
        result['numbered_state_witnesses'].append(row)
        print(json.dumps(row), flush=True)
    low, seated, high = result['numbered_state_witnesses']
    result['seated_has_lower_adjacent_compression'] = (
        low['center_x_bracket_mm'][1] < seated['center_x_bracket_mm'][0])
    assert result['seated_has_lower_adjacent_compression']
    result['inward_drop_over_0_15_mm_knob_travel_mm'] = (
        seated['center_x_bracket_mm'][0]-low['center_x_bracket_mm'][1])
    result['all_ten_numbered_inward_drops_mm'] = []
    sample_map = {item['setting']: item for item in trace['samples']}
    for digit in range(10):
        at, toward = sample_map[digit], sample_map[digit-.025]
        drop = at['center_x_bracket_mm'][0]-toward['center_x_bracket_mm'][1]
        assert drop > .12
        result['all_ten_numbered_inward_drops_mm'].append(drop)
    # Setting below zero is diagnostic extrapolation of the source law only;
    # the other nine counterexamples lie strictly inside the approved stroke.
    result['zero_negative_setting_is_extrapolation_only'] = True
    first_pitch = [item for item in trace['samples'] if 0 <= item['setting'] <= 1]
    trough = min(first_pitch, key=lambda item: item['center_x_bracket_mm'][1])
    result['sampled_trough'] = trough

    figure, axes = plt.subplots(1, 3, figsize=(17, 6))
    axes[0].plot([item['setting'] for item in first_pitch],
                 [item['center_x_bracket_mm'][1] for item in first_pitch], color='tab:blue')
    axes[0].scatter([0, 1], [sample_map[0]['center_x_bracket_mm'][1],
                            sample_map[1]['center_x_bracket_mm'][1]], color='tab:red',
                    label='Numbered positions')
    axes[0].scatter([trough['setting']], [trough['center_x_bracket_mm'][1]],
                    color='tab:green', label='Sampled trough')
    axes[0].set(xlabel='Source setting (one pitch)', ylabel='Required ball center X (mm)',
                title='Nominal 5 mm ball, unmodified guide\nNumbered positions are on the ramp')
    axes[0].legend()
    plane = cq.Plane((0, 0, 0), (1, 0, 0), (0, -1, 0))
    seated_ball = sphere((sample_map[0]['center_x_bracket_mm'][1], 0, BALL_Z))
    for shape, name, color, width in ((bodies['shaft'], 'Shaft', 'gray', 1.5),
                                     (bodies['knob'], 'Source knob', 'black', 1),
                                     (seated_ball, 'Guided 5 mm ball', 'tab:blue', 1.8)):
        plot_section(axes[1], plane, shape, name, color, width)
    axes[1].axhline(apex[2], color='tab:green', linestyle=':', label='Detent center height')
    axes[1].axhline(BALL_Z, color='tab:blue', linestyle=':', label='Guide center height')
    axes[1].set(xlim=(58, 74), ylim=(-60, -51), xlabel='X (mm)', ylabel='Z (mm)',
                title='Setting zero: actual native section\n5 mm ball touches a flank, not a centered seat')
    axes[1].set_aspect('equal')
    axes[1].legend(fontsize=8)
    alternate_plane = cq.Plane((0, float(centered[1]), 0), (1, 0, 0), (0, -1, 0))
    common = centered_ball.intersect(bodies['knob'])
    for shape, name, color, width in ((bodies['shaft'], 'Unmodified shaft', 'gray', 1.5),
                                     (bodies['knob'], 'Unmodified knob', 'black', 1),
                                     (centered_ball, 'Uninstalled centered ball', 'tab:green', 1.8),
                                     (common, 'Ball / source guide overlap', 'tab:red', 3)):
        plot_section(axes[2], alternate_plane, shape, name, color, width)
    axes[2].set(xlim=(58, 74), ylim=(-60, -51), xlabel='X (mm)', ylabel='Z (mm)',
                title='Read-only alternative: center on source cone\nGuide interference; not an accepted correction')
    axes[2].set_aspect('equal')
    axes[2].legend(fontsize=8)
    for ax in axes:
        ax.grid(alpha=.25)
    figure.suptitle('Selected Curta detent — indexing conflict before any production cut\n'
                    'Native localized witnesses; the complete frozen fixtures are retained separately')
    figure.tight_layout()
    output = Path('_build_evidence/selector-fit-indexing.png')
    figure.savefig(output, dpi=170)
    plt.close(figure)
    result.update(image=str(output), image_sha256=hashlib.sha256(output.read_bytes()).hexdigest())
    record = Path('_build_evidence/selector-fit-indexing.json')
    record.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(record), image=str(output),
                          centered_trial_overlaps_mm3=result['centered_trial_overlaps_mm3'],
                          centered=centered.tolist(), drop=result['inward_drop_over_0_15_mm_knob_travel_mm'])),
          flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    measure()
