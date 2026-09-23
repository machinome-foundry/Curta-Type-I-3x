"""Measure the two base-fastener contacts without changing the assembly.

Run ``python -m simulation.tools.base_fastener_contacts`` from the project.
The manual's page 35 calls for an M5 tap; imported product names alone do
not establish the modeled fasteners' dimensions or a finished thread fit.
"""

import json
import logging

from OCP.BRepAdaptor import BRepAdaptor_Surface


PATHS = (
    'Curta.enclosure.m5x30_countersunk_1',
    'Curta.enclosure.m5x30_countersunk_2',
    'Curta.frame.lower_bearing_plate.bearing_plate',
)


def bounds(shape):
    box = shape.BoundingBox()
    return [box.xmin, box.ymin, box.zmin, box.xmax, box.ymax, box.zmax]


def cylinders(shape):
    result = []
    for face in shape.Faces():
        if face.geomType() != 'CYLINDER':
            continue
        cylinder = BRepAdaptor_Surface(face.wrapped).Cylinder()
        result.append(dict(radius_mm=cylinder.Radius(),
                           axis_origin_mm=cylinder.Axis().Location().Coord(),
                           axis_direction=cylinder.Axis().Direction().Coord(),
                           bounds_mm=bounds(face)))
    return result


def main():
    logging.disable(logging.INFO)
    from machinome.simulation import Sim
    from simulation.running import OperatingCurta
    from simulation.tools.interference import world_solids

    root = OperatingCurta()
    Sim(root, dt=.1, meshes=False)
    root.assemble()
    shapes = world_solids(root, selected=set(PATHS))
    assert set(shapes) == set(PATHS)
    report = dict(parts={}, contacts=[])
    for path, shape in shapes.items():
        report['parts'][path] = dict(
            valid=shape.isValid(), volume_mm3=shape.Volume(),
            bounds_mm=bounds(shape), cylinders=cylinders(shape))
    for path in PATHS[:2]:
        common = shapes[path].intersect(shapes[PATHS[2]])
        report['contacts'].append(dict(
            pair=[path, PATHS[2]], valid=common.isValid(),
            volume_mm3=common.Volume(), bounds_mm=bounds(common),
            solids=len(common.Solids())))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
