"""Source-local detent and fork dimensions, before choosing a reversal fit."""

import json
from simulation.standard.parts import ReversingShaft, ReversingActuator, TransmissionGear0_5


def probe():
    shapes = {}
    for part_type in (ReversingShaft, ReversingActuator, TransmissionGear0_5):
        part = part_type()
        part.assemble()
        shapes[part_type.__name__] = part.shape()
    detents = sorted((face.BoundingBox().zmin + face.BoundingBox().zmax) / 2
                     for face in shapes['ReversingShaft'].Faces()
                     if face.geomType() == 'CONE')
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


if __name__ == '__main__':
    probe()
