"""Source-local detent and fork dimensions, before choosing a reversal fit."""

import json
from OCP.BRepAdaptor import BRepAdaptor_Surface
from simulation.standard.parts import ReversingShaft, ReversingActuator, TransmissionGear0_5


def probe():
    shapes = {}
    for part_type in (ReversingShaft, ReversingActuator, TransmissionGear0_5):
        part = part_type()
        part.assemble()
        shapes[part_type.__name__] = part.shape()
    cones = sorted((face for face in shapes['ReversingShaft'].Faces()
                    if face.geomType() == 'CONE'), key=lambda face: face.Center().z)
    detents = [BRepAdaptor_Surface(face.wrapped).Cone().Location().Z()
               for face in cones]
    assert len(detents) == 2, detents
    fork_planes = sorted(face.Center().z for face in shapes['ReversingActuator'].Faces()
                         if face.geomType() == 'PLANE' and abs(face.normalAt().z) > .999)
    assert len(fork_planes) == 4, fork_planes
    gear = shapes['TransmissionGear0_5'].BoundingBox()
    slot = fork_planes[2] - fork_planes[1]
    print(json.dumps({'frame': 'source part local', 'units': 'mm',
                      'shaft_detent_z': detents, 'detent_separation': detents[1] - detents[0],
                      'fork_z_planes': fork_planes, 'fork_slot': slot,
                      'gear_thickness': gear.zlen,
                      'axial_clearance': slot - gear.zlen}), flush=True)
    for face in cones:
        box = face.BoundingBox()
        cone = BRepAdaptor_Surface(face.wrapped).Cone()
        circles = [{'radius': edge.radius(), 'center': edge.arcCenter().toTuple()}
                   for edge in face.Edges() if edge.geomType() == 'CIRCLE']
        print(json.dumps({'detent_cone_bounds': [box.xmin, box.ymin, box.zmin,
                                                box.xmax, box.ymax, box.zmax],
                          'cone_location': cone.Location().Coord(),
                          'cone_axis': cone.Axis().Direction().Coord(),
                          'cone_apex': cone.Apex().Coord(),
                          'cone_semia_angle': cone.SemiAngle(),
                          'circles': circles}), flush=True)


if __name__ == '__main__':
    probe()
