"""Read-only native selector measurements; no operating replacement or relief.

All coordinates are the source-installed setting-zero world frame. Surface
identities and complete bounds are retained so a fitting region can be checked
independently of any later cutter.
"""

from collections import Counter
import hashlib
import json
import logging
from pathlib import Path

from OCP.BRepAdaptor import BRepAdaptor_Surface

from simulation.selector_fit import SelectorFitBench
from simulation.tools.interference import world_solids
from simulation.tools.open_run_transitions import bounds


PREFIX = 'Curta.selector.selector_knob_1_419057.'
PATHS = dict(ball=PREFIX+'p_5mm_ball', spring=PREFIX+'selector_knob_spring',
             screw=PREFIX+'digit_selector_screw', knob=PREFIX+'selector_knob',
             shaft='Curta.selector.selector_shaft_bottom',
             top='Curta.selector.selector_shaft_top_1_419054.selector_shaft_top',
             roll='Curta.selector.selector_shaft_top_1_419054.number_roll',
             group='Curta.channel.p_10219_410002_1', housing='Curta.housing.bottom_housing')


def body_measurements(shape):
    assert shape.isValid() and len(shape.Solids()) == 1
    faces = []
    for index, face in enumerate(shape.Faces()):
        item = dict(index=index, type=face.geomType(), area_mm2=face.Area(),
                    center_mm=face.Center().toTuple(), bounds_mm=bounds(face).tolist())
        adaptor = BRepAdaptor_Surface(face.wrapped)
        if item['type'] == 'CYLINDER':
            cylinder = adaptor.Cylinder()
            item.update(radius_mm=cylinder.Radius(),
                        axis_origin_mm=cylinder.Axis().Location().Coord(),
                        axis_direction=cylinder.Axis().Direction().Coord())
        elif item['type'] == 'PLANE':
            plane = adaptor.Plane()
            item.update(normal=plane.Axis().Direction().Coord())
        elif item['type'] == 'SPHERE':
            sphere = adaptor.Sphere()
            item.update(radius_mm=sphere.Radius(), sphere_center_mm=sphere.Location().Coord())
        elif item['type'] == 'TORUS':
            torus = adaptor.Torus()
            item.update(major_radius_mm=torus.MajorRadius(), minor_radius_mm=torus.MinorRadius(),
                        axis_origin_mm=torus.Axis().Location().Coord(),
                        axis_direction=torus.Axis().Direction().Coord())
        elif item['type'] == 'CONE':
            cone = adaptor.Cone()
            item.update(semi_angle_rad=cone.SemiAngle(), reference_radius_mm=cone.RefRadius(),
                        axis_origin_mm=cone.Axis().Location().Coord(),
                        axis_direction=cone.Axis().Direction().Coord(), apex_mm=cone.Apex().Coord())
        faces.append(item)
    edges = []
    for index, edge in enumerate(shape.Edges()):
        item = dict(index=index, type=edge.geomType(), length_mm=edge.Length(),
                    bounds_mm=bounds(edge).tolist())
        if item['type'] == 'CIRCLE':
            item.update(radius_mm=edge.radius(), center_mm=edge.arcCenter().toTuple())
        edges.append(item)
    return dict(volume_mm3=shape.Volume(), bounds_mm=bounds(shape).tolist(),
                face_types=dict(Counter(f['type'] for f in faces)), faces=faces, edges=edges)


def measure():
    bench = SelectorFitBench()
    bench.set_state(setting=0, postcarry=0)
    bench.assemble()
    native = world_solids(bench, selected=set(PATHS.values()))
    assert set(native) == set(PATHS.values())
    result = dict(kind='selector-fit-source-surface-measurements', setting=0, postcarry=0,
                  scope='Read-only source geometry, no fitted parts or running behavior',
                  paths=PATHS, parts={name: body_measurements(native[path])
                                     for name, path in PATHS.items()})
    output = Path('_build_evidence/selector-fit-source-surfaces.json')
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(output), sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                          parts={name: {key: item[key] for key in ('volume_mm3', 'bounds_mm', 'face_types')}
                                 for name, item in result['parts'].items()})), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    measure()
