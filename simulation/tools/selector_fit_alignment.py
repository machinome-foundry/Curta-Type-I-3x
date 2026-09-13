"""Pre-reconstruction native guide, wall and spring-end measurements.

This probe does not install or construct a fitted knob. Missing material in
independently specified support witnesses is compared with the ratified old
cavity restoration region. That is a feasibility gate, not a finished fit.
"""

import hashlib
import json
import logging
from math import pi, sin
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
from simulation.tools.open_run_transitions import bounds
from simulation.tools.selector_fit_contacts import closest
from simulation.tools.selector_fit_indexing import sphere
from simulation.tools.selector_fit_measurements import PATHS


def native_source():
    bench = SelectorFitBench()
    bench.set_state(setting=0, postcarry=0)
    bench.assemble()
    native = world_solids(bench, selected=set(PATHS.values()))
    return {name: native[path] for name, path in PATHS.items()}


def cylinder(radius, x0, x1, y, z):
    return cq.Solid.makeCylinder(radius, x1-x0, (x0, y, z), (1, 0, 0))


def measured_guide(knob, shaft):
    # Surface identities are the retained source face inventory, not faces
    # chosen from a constructed fit. Assert their types before using them.
    guide_face, support_face = knob.Faces()[28], knob.Faces()[25]
    assert guide_face.geomType() == support_face.geomType() == 'CYLINDER'
    guide = BRepAdaptor_Surface(guide_face.wrapped).Cylinder()
    support = BRepAdaptor_Surface(support_face.wrapped).Cylinder()
    zero_cone = BRepAdaptor_Surface(shaft.Faces()[4].wrapped).Cone()
    center = np.array(zero_cone.Apex().Coord()) + np.array(
        zero_cone.Axis().Direction().Coord()) * (2.5/sin(zero_cone.SemiAngle()))
    return guide, support, center


def numbered_seats(shaft, center):
    rows = []
    for index, face in enumerate(shaft.Faces()):
        if face.geomType() != 'CONE':
            continue
        cone = BRepAdaptor_Surface(face.wrapped).Cone()
        # Radial pocket cones only. The two axial bottom-tip chamfers are
        # conical too, but neither is a numbered detent surface.
        if abs(cone.Axis().Direction().Z()) > 1e-8:
            continue
        digit = round((center[2]-cone.Apex().Z())/6)
        turned = face.rotate((58.5, 0, 0), (58.5, 0, 1), 36*digit)
        actual_cone = BRepAdaptor_Surface(turned.wrapped).Cone()
        actual_center = np.array(actual_cone.Apex().Coord()) + np.array(
            actual_cone.Axis().Direction().Coord())*(2.5/sin(actual_cone.SemiAngle()))
        expected = center-(0, 0, 6*digit)
        native_shaft = shaft.rotate((58.5, 0, 0), (58.5, 0, 1), 36*digit)
        ball = sphere(tuple(actual_center))
        common = native_shaft.intersect(ball)
        assert common.isValid() and common.Volume() >= 0
        distance = closest(native_shaft, cq.Vertex.makeVertex(*actual_center))[0]
        row = dict(digit=digit, source_face=index,
                   cone_axis=actual_cone.Axis().Direction().Coord(),
                   center_mm=actual_center.tolist(),
                   alignment_error_mm=float(np.linalg.norm(actual_center-expected)),
                   center_to_shaft_mm=distance, ball_shaft_overlap_mm3=common.Volume())
        rows.append(row)
        print(json.dumps(dict(phase='numbered_seat', **row)), flush=True)
    assert sorted(row['digit'] for row in rows) == list(range(10))
    return sorted(rows, key=lambda row: row['digit'])


def spring_ends(spring, source_axis):
    seam = next(edge for edge in spring.Edges() if edge.geomType() == 'BSPLINE')
    points, parameters = seam.sample(1301)
    points = np.array([point.toTuple() for point in points])
    angles = np.unwrap(np.arctan2(points[:, 2]-source_axis[2], points[:, 1]-source_axis[1]))
    order = np.argsort(points[:, 0])
    points, angles = points[order], angles[order]
    parameters = np.array(parameters)[order]
    theta = angles-angles[0]
    caps = sorted([face for face in spring.Faces() if face.geomType() == 'PLANE'],
                  key=lambda face: face.Center().x)
    end_centers = [face.Center().toTuple() for face in caps]
    # This seam is the +X pole of the circular source section, not the wire
    # centerline: its first X is cap-center X + 0.255. Retain that distinction.
    seam_offset = float(points[0, 0]-end_centers[0][0])
    centerline_x = points[:, 0]-seam_offset
    linear_x = centerline_x[0] + (centerline_x[-1]-centerline_x[0])*theta/(13*pi)
    tangents = [seam.tangentAt(float(parameters[i]), mode='parameter').toTuple()
                for i in (0, 1, 2, 10, 100, 650, 1200, 1290, 1298, 1299, 1300)]
    tangent_points = [points[i].tolist() for i in (0, 1, 2, 10, 100, 650, 1200, 1290, 1298, 1299, 1300)]
    # Source endpoint tangents/cap normals establish whether flat-ended lead
    # transitions are present; no constant-pitch reconstruction is inferred.
    return dict(end_centers_mm=end_centers,
                cap_normals=[face.normalAt().toTuple() for face in caps],
                seam_axial_offset_mm=seam_offset,
                end_tangent_samples=[dict(seam_point_mm=p, tangent=t)
                                     for p, t in zip(tangent_points, tangents)],
                phase_turns=(theta/(2*pi)).tolist(),
                centerline_x_mm=centerline_x.tolist(),
                linear_helix_axial_residual_mm=float(abs(centerline_x-linear_x).max()),
                limitation='Seam and cap measurements, not an installed spring or global spline-error bound')


def support_map(knob, shaft):
    guide, support, center = measured_guide(knob, shaft)
    old = np.array(guide.Axis().Location().Coord())
    radius, shaft_radius = guide.Radius(), support.Radius()
    seat_x = old[0]
    shaft_axis = support.Axis().Location().Coord()
    old_outboard = cylinder(radius, shaft_axis[0], seat_x, old[1], old[2])
    shaft_void = cq.Solid.makeCylinder(shaft_radius, 40, (shaft_axis[0], shaft_axis[1], -85))
    restoration = old_outboard.cut(shaft_void).cut(knob)
    new_guide = cylinder(radius, shaft_axis[0], seat_x, center[1], center[2])
    removal = knob.intersect(new_guide)
    support_face = knob.Faces()[25]
    old_mouth = support_face.intersect(old_outboard)
    new_mouth = support_face.intersect(new_guide)
    remaining_support = support_face.cut(new_guide)
    # A complete 0.34 mm annular witness lies in a documented straight span.
    # Its front begins beyond the maximum X of the unchanged shaft bore; its
    # back terminates at the unchanged seat plane. A separate full disk proves
    # 2.39 mm of retained back-seat material. These are geometric bounds only.
    front_x = shaft_axis[0]+shaft_radius+.01
    wall = cylinder(radius+.34, front_x, seat_x, center[1], center[2]).cut(
        cylinder(radius, front_x, seat_x, center[1], center[2]))
    too_thick = cylinder(radius+.35, 64, seat_x, center[1], center[2]).cut(
        cylinder(radius, 64, seat_x, center[1], center[2]))
    seat = cylinder(radius+.34, seat_x, seat_x+2.39, center[1], center[2])
    # Examine permitted future support WITHOUT reconstructing a fitted body.
    witnesses = {}
    for name, witness in (('guide_wall_0_34', wall), ('back_seat_2_39', seat),
                           ('wall_0_35_counterexample', too_thick)):
        source_missing = witness.cut(knob)
        # CadQuery cannot boolean-cut a topologically empty result. Preserve
        # the exact empty result; do not replace a small positive volume by it.
        forbidden_missing = (source_missing.cut(restoration)
                             if source_missing.Solids() else source_missing)
        assert forbidden_missing.isValid() and forbidden_missing.Volume() >= 0
        witnesses[name] = dict(volume_mm3=witness.Volume(),
            source_missing_mm3=source_missing.Volume(),
            missing_outside_restoration_mm3=forbidden_missing.Volume(),
            bounds_mm=bounds(witness).tolist())
        print(json.dumps(dict(phase='support_witness', name=name, **witnesses[name])), flush=True)
    distances = {}
    guide_skin = next(face for face in cylinder(radius, 64, seat_x, center[1], center[2]).Faces()
                      if face.geomType() == 'CYLINDER')
    for name, index in (('top', 14), ('positive_y', 17), ('negative_y', 18)):
        distance, on_guide, on_outer = closest(guide_skin, knob.Faces()[index])
        distances[name] = dict(distance_mm=distance, on_guide_mm=on_guide, on_source_mm=on_outer)
    result = dict(guide_radius_mm=radius, nominal_ball_play_mm=radius-2.5,
                  nominal_coil_envelope_clearance_mm=radius-2.295-.255,
                  old_guide_axis_mm=old.tolist(), candidate_guide_center_mm=center.tolist(),
                  source_shaft_bore_radius_mm=shaft_radius, unchanged_seat_x_mm=seat_x,
                  restoration_region=dict(volume_mm3=restoration.Volume(), bounds_mm=bounds(restoration).tolist(),
                      definition='Native old outboard guide cylinder minus unchanged shaft void and source knob; no other void is authorized'),
                  removal_region=dict(volume_mm3=removal.Volume(), bounds_mm=bounds(removal).tolist(),
                      definition='Source knob inside source-radius relocated outboard cylinder'),
                  mouth_areas_mm2=dict(old_existing_support_intersection=old_mouth.Area(),
                                      new_removed_support=new_mouth.Area(), remaining_source_support=remaining_support.Area()),
                  wall_to_source_outer_faces=distances, support_witnesses=witnesses,
                  limitation='Pre-reconstruction local support feasibility only; no fitted body, ball path, guide-play retention or manufacturing qualification')
    return result, center, new_guide, restoration, wall, seat


def measure():
    source = native_source()
    record, center, candidate, restoration, wall, seat = support_map(source['knob'], source['shaft'])
    result = dict(kind='selector-guide-pre-reconstruction-gates',
                  planning_commit='da432fbdc7fe0e7f89e308237f281e9c3d368754',
                  scope='Read-only source and permitted-region feasibility; production remains unchanged',
                  support_map=record, numbered_seats=numbered_seats(source['shaft'], center),
                  spring_source_ends=spring_ends(source['spring'], record['old_guide_axis_mm']))
    figure, axes = plt.subplots(1, 3, figsize=(17, 6))
    yz = cq.Plane((66, 0, 0), (0, 1, 0), (1, 0, 0))
    xz = cq.Plane((0, float(center[1]), 0), (1, 0, 0), (0, -1, 0))
    for ax, plane, xlim, ylim, title in (
            (axes[0], yz, (-3.5, 3.5), (-59, -51.4), 'Native guide cross-section at X=66'),
            (axes[1], xz, (60, 76), (-59, -51.4), 'Native longitudinal section at new guide Y')):
        for shape, name, color, width in ((source['knob'], 'Unchanged source knob', 'black', 1),
                (restoration, 'Permitted old-cavity restoration', 'tab:blue', 1.5),
                (candidate, 'Candidate guide (not installed)', 'tab:red', 1.4),
                (wall, '0.34 mm continuous wall witness', 'tab:green', 1.5),
                (seat, '2.39 mm back-seat witness', 'tab:orange', 1.5)):
            plot_section(ax, plane, shape, name, color, width)
        ax.set(xlim=xlim, ylim=ylim, title=title)
        ax.set_aspect('equal')
        ax.grid(alpha=.25)
    axes[0].set(xlabel='Y (mm)', ylabel='Z (mm)')
    axes[1].set(xlabel='X (mm)', ylabel='Z (mm)')
    spring = result['spring_source_ends']
    theta, axial = np.array(spring['phase_turns']), np.array(spring['centerline_x_mm'])
    axes[2].plot(theta, axial-(axial[0]+(axial[-1]-axial[0])*theta/6.5))
    axes[2].set(xlabel='Measured winding (turns)', ylabel='Axial residual from linear helix (mm)',
                title='Actual source spring seam, offset corrected\nEnd shape is not assumed constant-pitch')
    axes[2].grid(alpha=.25)
    handles, labels = axes[1].get_legend_handles_labels()
    figure.legend(handles, labels, loc='lower center', ncol=3, fontsize=8)
    figure.suptitle('Selected selector: pre-reconstruction geometry gates\n'
                    'Source-derived feasibility witnesses; no production fit or strength claim')
    figure.tight_layout(rect=(0, .09, 1, .92))
    image = Path('_build_evidence/selector-fit-alignment.png')
    figure.savefig(image, dpi=170)
    plt.close(figure)
    result.update(image=str(image), image_sha256=hashlib.sha256(image.read_bytes()).hexdigest())
    output = Path('_build_evidence/selector-fit-alignment.json')
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(output), sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                          wall_distances=record['wall_to_source_outer_faces'],
                          spring_residual_mm=spring['linear_helix_axial_residual_mm'])), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    measure()
