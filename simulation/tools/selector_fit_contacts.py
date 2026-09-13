"""Measure nominal-ball support and source follower constraints, without fitting.

The radial contact bracket is a localization measurement, not a continuous
certificate or an implemented ball law. Numerical bracket widths are retained;
no positive overlap is waived.
"""

import hashlib
import json
import logging
from math import pi
from pathlib import Path

import cadquery as cq
import numpy as np
from OCP.BRepExtrema import BRepExtrema_DistShapeShape

from simulation.selector_fit import SelectorFitBench
from simulation.tools.interference import world_solids
from simulation.tools.open_run_transitions import bounds
from simulation.tools.selector_fit_measurements import PATHS, body_measurements


BALL_Z = -55.785999642


def closest(first, second):
    query = BRepExtrema_DistShapeShape()
    query.SetMultiThread(False)
    query.LoadS1(first.wrapped)
    query.LoadS2(second.wrapped)
    assert query.Perform() and query.IsDone()
    return query.Value(), query.PointOnShape1(1).Coord(), query.PointOnShape2(1).Coord()


def radial_support(shaft, z, y=0):
    low, high = 62.2, 66.
    def distance(x):
        return closest(shaft, cq.Vertex.makeVertex(x, y, z))[0]
    assert distance(low) < 2.5 < distance(high)
    while high-low > 1e-8:
        middle = (low+high)/2
        if distance(middle) < 2.5:
            low = middle
        else:
            high = middle
    distance, on_shaft, _ = closest(shaft, cq.Vertex.makeVertex(high, y, z))
    return dict(center_x_bracket_mm=[low, high], center_y_mm=y, center_z_mm=z,
                distance_mm=distance, on_shaft_mm=on_shaft)


def measure():
    bench = SelectorFitBench()
    bench.set_state(setting=0, postcarry=0)
    bench.assemble()
    native = world_solids(bench, selected=set(PATHS.values()))
    source = {name: native[path] for name, path in PATHS.items()}
    result = dict(kind='selector-fit-contact-measurements',
                  scope='Read-only localized witnesses, not continuous-path acceptance',
                  selected_parts={name: body_measurements(source[name])
                                  for name in ('spring', 'shaft')}, samples=[])
    spring = source['spring']
    seam = next(edge for edge in spring.Edges() if edge.geomType() == 'BSPLINE')
    points = np.array([point.toTuple() for point in seam.sample(1301)[0]])
    angles = np.unwrap(np.arctan2(points[:, 2]-BALL_Z, points[:, 1]))
    ordered = np.argsort(points[:, 0])
    points, angles = points[ordered], angles[ordered]
    radius = np.linalg.norm(points[:, 1:]-(0, BALL_Z), axis=1)
    slope, intercept = np.polyfit(points[:, 0], angles, 1)
    residual = angles-(slope*points[:, 0]+intercept)
    result['spring_helix_measurement'] = dict(
        wire_diameter_mm=.51, centerline_radius_mm=[float(radius.min()), float(radius.max())],
        source_end_centers_mm=[edge.arcCenter().toTuple() for edge in spring.Edges()
                               if edge.geomType() == 'CIRCLE'],
        signed_turns_in_increasing_x=float((angles[-1]-angles[0])/(2*pi)),
        pitch_mm=float(2*pi/abs(slope)), axial_seam_span_mm=float(np.ptp(points[:, 0])),
        sampled_linear_phase_residual_rad=float(abs(residual).max()),
        end_forms='Plain cut ends, circular planar caps; no separate end coils in source',
        note='Sampled seam fit measures winding/hand; not a bound on B-spline approximation')
    print(json.dumps(dict(phase='spring', **result['spring_helix_measurement'])), flush=True)

    settings = sorted(set([i/40 for i in range(-10, 41)] +
                          [i/4 for i in range(4, 37)] +
                          [i+offset for i in range(1, 10) for offset in (-.2, -.175, -.15, -.025)]))
    for setting in settings:
        shaft = source['shaft'].rotate((58.5, 0, 0), (58.5, 0, 1), 36*setting)
        support = radial_support(shaft, BALL_Z-6*setting)
        row = dict(setting=setting, shaft_phase_deg=36*setting, **support)
        if setting in (0, .5, 1, 5, 9):
            ball = cq.Solid.makeSphere(2.5, (support['center_x_bracket_mm'][1], 0, BALL_Z-6*setting),
                                      angleDegrees1=-90, angleDegrees2=90, angleDegrees3=360)
            knob = source['knob'].translate((0, 0, -6*setting))
            screw = source['screw'].translate((0, 0, -6*setting))
            row['native_overlaps_mm3'] = {}
            for name, a, b in (('nominal_ball_knob', ball, knob), ('nominal_ball_shaft', ball, shaft),
                               ('source_screw_shaft', screw, shaft)):
                common = a.intersect(b)
                assert common.isValid() and common.Volume() >= 0
                row['native_overlaps_mm3'][name] = common.Volume()
            row['nearest_shaft_faces'] = sorted(
                [dict(index=index, type=face.geomType(), distance_mm=closest(
                    face, cq.Vertex.makeVertex(support['center_x_bracket_mm'][1], 0, BALL_Z-6*setting))[0])
                 for index, face in enumerate(shaft.Faces())], key=lambda item: item['distance_mm'])[:3]
        result['samples'].append(row)
        if setting in (0, .5, 1, 5, 9):
            print(json.dumps(row), flush=True)
    result['fixed_joint_regions'] = {}
    for first, second in (('screw', 'knob'), ('shaft', 'top')):
        common = source[first].intersect(source[second])
        assert common.isValid() and common.Volume() > 0
        result['fixed_joint_regions'][first+'/'+second] = dict(
            volume_mm3=common.Volume(), bounds_mm=bounds(common).tolist(), solids=len(common.Solids()),
            note='Source region only; full canonical-inventory proof remains open')
    output = Path('_build_evidence/selector-fit-contacts.json')
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(output), sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                          samples=len(result['samples']), fixed_joint_regions=result['fixed_joint_regions'])), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    measure()
