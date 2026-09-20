"""Measure the actual ball and separate knob/yoke seat; adopt no correction."""

import json
import logging
from math import cos, sin, radians
from OCP.BRepAdaptor import BRepAdaptor_Surface
from simulation.standard.assembly import ReversingLever1
from simulation.tools.interference import world_solids
from simulation.cover_fits import mesh_solid


def bounds(shape):
    if not shape.Vertices():
        return None
    b = shape.BoundingBox()
    return [b.xmin, b.ymin, b.zmin, b.xmax, b.ymax, b.zmax]


def probe():
    logging.disable(logging.INFO)
    lever = ReversingLever1()
    lever.assemble()
    lever.build_stls()
    selected = {'Curta.p_5mm_ball',
                'Curta.upper_reversing_lever_spacer',
                'Curta.reversing_lever_knob_1.reversing_lever_knob',
                'Curta.reversing_lever_knob_1.reversing_actuator'}
    shapes = world_solids(lever, selected=selected)
    for path, shape in shapes.items():
        print(json.dumps({'part': path, 'bounds': bounds(shape),
                          'volume': shape.Volume(), 'valid': shape.isValid()}), flush=True)
        for face in shape.Faces():
            if face.geomType() == 'SPHERE':
                sphere = BRepAdaptor_Surface(face.wrapped).Sphere()
                print(json.dumps({'sphere_part': path, 'radius': sphere.Radius(),
                                  'center': sphere.Location().Coord()}), flush=True)
            elif face.geomType() == 'CYLINDER' and path.endswith('reversing_lever_knob'):
                cylinder = BRepAdaptor_Surface(face.wrapped).Cylinder()
                print(json.dumps({'knob_cylinder_radius': cylinder.Radius(),
                                  'center': cylinder.Location().Coord(),
                                  'axis': cylinder.Axis().Direction().Coord(),
                                  'bounds': bounds(face)}), flush=True)
            elif face.geomType() == 'PLANE' and abs(face.normalAt().z) > .999:
                print(json.dumps({'horizontal_face_part': path,
                                  'center': face.Center().toTuple(),
                                  'area': face.Area(), 'normal': face.normalAt().toTuple(),
                                  'bounds': bounds(face)}), flush=True)
    knob = shapes['Curta.reversing_lever_knob_1.reversing_lever_knob']
    yoke = shapes['Curta.reversing_lever_knob_1.reversing_actuator']
    mesh_knob = mesh_solid(lever.reversing_lever_knob_1.reversing_lever_knob.mesh)
    mesh_yoke = mesh_solid(lever.reversing_lever_knob_1.reversing_actuator.mesh)
    spacer = shapes['Curta.upper_reversing_lever_spacer']
    mesh_spacer = mesh_solid(lever.upper_reversing_lever_spacer.mesh)
    for height in (-.6, -.3, -.1, 0, .1, .3, .5, .55, .59, .6, .61, .7, .9):
        common = knob.intersect(yoke.translate((0, 0, height)))
        faceted = mesh_knob ^ mesh_yoke.translate((0, 0, height))
        top_common = spacer.intersect(yoke.translate((0, 0, height)))
        top_faceted = mesh_spacer ^ mesh_yoke.translate((0, 0, height))
        print(json.dumps({'yoke_relative_rise': height, 'native_valid': common.isValid(),
                          'native_overlap': common.Volume(), 'native_bounds': bounds(common),
                          'faceted_status': str(faceted.status()),
                          'faceted_overlap': faceted.volume(),
                          'spacer_native_valid': top_common.isValid(),
                          'spacer_native_overlap': top_common.Volume(),
                          'spacer_faceted_status': str(top_faceted.status()),
                          'spacer_faceted_overlap': top_faceted.volume()}), flush=True)
    ball = shapes['Curta.p_5mm_ball']
    mesh_ball = mesh_solid(lever.p_5mm_ball.mesh)
    for radius in (2.5, 3, 3.5, 3.84, 4.25, 4.48, 5, 5.5310689635676225, 6, 6.4, 6.5):
        shift = tuple((radius - 5.5310689635676225) * value for value in
                      (cos(radians(70)), sin(radians(70)), 0))
        common = knob.intersect(ball.translate(shift))
        faceted = mesh_knob ^ mesh_ball.translate(shift)
        print(json.dumps({'ball_center_radius': radius,
                          'ball_knob_native_valid': common.isValid(),
                          'ball_knob_native_overlap': common.Volume(),
                          'ball_knob_faceted_status': str(faceted.status()),
                          'ball_knob_faceted_overlap': faceted.volume()}), flush=True)


if __name__ == '__main__':
    probe()
