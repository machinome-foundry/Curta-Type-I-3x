"""Independent dimensional readings and negative controls for the local fit."""

import json
import logging
from pathlib import Path

import cadquery as cq

from simulation.carry_frame import CarryFrameBench
from simulation.frame_fits import CarryPassageFrame, passages
from simulation.standard.parts import MainBody
from simulation.test_frame_fits import forbidden_removal, registration_lands, region, seat_edge_exceptions
from simulation.tools.interference import world_solids
from simulation.tools.open_run_transitions import bounds


def clearance_sites(frame, wire):
    readings = dict(lowered_x_mm=frame.distance(cq.Vertex.makeVertex(52.725, -7.155, -16.35)),
                    raised_z_mm=frame.distance(cq.Vertex.makeVertex(50.5, -7.2, -21.6)))
    for name, low, high in (('spring_left', 53.4, 54.3), ('spring_right', 60.3, 61.2)):
        walls = [face for face in frame.Faces() if face.geomType() == 'PLANE'
                 and abs(face.normalAt().y) > .999999
                 and low < face.Center().x < high and -11.5 < face.Center().y < -11.2]
        if len(walls) != 1:
            raise ValueError(f'Expected one measured {name} back wall, got {len(walls)}')
        readings[name+'_normal_mm'] = wire.distance(walls[0])
        readings[name+'_wall_y_mm'] = walls[0].Center().y
    return readings


def fit_from(original, *, stations=(0, -20), omitted=()):
    fitted = original
    for _, _, tool in passages(.05, stations, omitted):
        fitted = fitted.cut(tool)
    return fitted


def report():
    bench = CarryFrameBench()
    bench.set_state(drop_mm=2.562)
    bench.assemble()
    relevant = {'Curta.'+station+'.'+part for station in ('first', 'second')
                for part in ('tens_slide_bearing', 'carry_lever_spring.wire')}
    bodies = world_solids(bench, include_flexible=True, selected=relevant)
    original, fitted = MainBody().shape(), bench.frame.main_body.shape()
    result = dict(kind='carry-frame-dimensional-and-negative-controls',
                  frame_original_mm3=original.Volume(), frame_fitted_mm3=fitted.Volume(),
                  removed_mm3=original.Volume()-fitted.Volume(), seats={}, gaps=[], mutations=[])
    for station, angle in (('first', 0), ('second', -20)):
        lands = []
        for patch in registration_lands(original, bodies['Curta.'+station+'.tens_slide_bearing']):
            remaining = patch
            for exception in seat_edge_exceptions(angle):
                remaining = remaining.cut(exception)
            after = patch.intersect(fitted)
            lost = remaining.cut(fitted)
            if not lost.isValid() or lost.Area() > 1e-7:
                raise ValueError('Lost protected registration land')
            lands.append(dict(source_mm2=patch.Area(), retained_mm2=after.Area(),
                              protected_mm2=remaining.Area(), bounds_mm=bounds(patch).tolist()))
        result['seats'][station] = dict(lands=lands, original_mm2=sum(p['source_mm2'] for p in lands),
                                       retained_mm2=sum(p['retained_mm2'] for p in lands))
    for gap in (.04, .05, .06):
        frame = CarryPassageFrame(running_gap=gap).shape()
        for station, angle in (('first', 0), ('second', 20)):
            aligned = frame.rotate((0, 0, 0), (0, 0, 1), angle)
            wire = bodies['Curta.'+station+'.carry_lever_spring.wire'].rotate((0, 0, 0), (0, 0, 1), angle)
            readings = clearance_sites(aligned, wire)
            result['gaps'].append(dict(gap_parameter_mm=gap, station=station, **readings))
    # Independent physical contact witnesses at the actual named endpoints.
    poses = {}
    for drop in (0, 1.1630815, 4.2):
        bench.set_state(drop_mm=drop)
        bench.assemble()
        selection = {'Curta.'+station+'.'+part for station in ('first', 'second')
                     for part in ('tens_slider_for_results', 'carry_lever_spring.wire')}
        poses[drop] = world_solids(bench, include_flexible=True, selected=selection)
    for family, drop, suffix in (('raised-shoulder', 0, 'tens_slider_for_results'),
                                 ('lowered-edge', 4.2, 'tens_slider_for_results'),
                                 ('spring-left', 1.1630815, 'carry_lever_spring.wire'),
                                 ('spring-right', 1.1630815, 'carry_lever_spring.wire')):
        mutant = fit_from(original, omitted=(family,))
        for station in ('first', 'second'):
            common = mutant.intersect(poses[drop]['Curta.'+station+'.'+suffix])
            assert common.isValid() and common.Volume() > 0, (family, station)
            result['mutations'].append(dict(mutation='omit-'+family, station=station,
                                             detected=True, overlap_mm3=common.Volume()))
    for name, stations in (('omit-second', (0,)), ('misplace-second', (0, -40))):
        mutant = fit_from(original, stations=stations)
        common = mutant.intersect(poses[0]['Curta.second.tens_slider_for_results'])
        assert common.isValid() and common.Volume() > 0
        result['mutations'].append(dict(mutation=name, detected=True, overlap_mm3=common.Volume()))
    # Overcut a measured retained portion of the actual X=52.8 seating face.
    overcut = fitted.cut(region((52.78, -9, -20), (52.82, -8.5, -19.9)))
    outside = forbidden_removal(original, overcut)
    assert outside.isValid() and outside.Volume() > 0
    result['mutations'].append(dict(mutation='overcut-protected-seat', detected=True,
                                     forbidden_removal_mm3=outside.Volume()))
    # Simulate an ignored .06 mm parameter by supplying the .05 mm frame.
    measured = fitted.distance(cq.Vertex.makeVertex(52.725, -7.155, -16.35))
    assert abs(measured-.06) > 1e-5
    result['mutations'].append(dict(mutation='ignore-gap-parameter', detected=True,
                                     requested_mm=.06, measured_mm=measured))
    output = Path('_build_evidence/carry-frame-fit-report.json')
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    report()
