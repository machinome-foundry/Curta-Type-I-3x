"""Read spring wire dimensions and the knob's spring seat from source solids."""

import json
import logging
from OCP.BRepAdaptor import BRepAdaptor_Surface
from simulation.standard.parts import SelectorKnobSpring, ReversingLeverKnob


def bounds(shape):
    box = shape.BoundingBox()
    return [box.xmin, box.ymin, box.zmin, box.xmax, box.ymax, box.zmax]


def main():
    logging.disable(logging.INFO)
    for cls in (SelectorKnobSpring, ReversingLeverKnob):
        shape = cls().shape()
        print(json.dumps({'part': cls.__name__, 'bounds': bounds(shape),
                          'volume': shape.Volume(), 'valid': shape.isValid()}), flush=True)
        for face in shape.Faces():
            if face.geomType() == 'PLANE':
                print(json.dumps({'plane': face.Center().toTuple(), 'area': face.Area(),
                                  'normal': face.normalAt().toTuple(), 'bounds': bounds(face)}), flush=True)
            elif face.geomType() == 'CYLINDER':
                cylinder = BRepAdaptor_Surface(face.wrapped).Cylinder()
                print(json.dumps({'cylinder_radius': cylinder.Radius(),
                                  'axis': cylinder.Axis().Direction().Coord(),
                                  'location': cylinder.Location().Coord(), 'bounds': bounds(face)}), flush=True)
        if cls is SelectorKnobSpring:
            for edge in shape.Edges():
                if edge.geomType() == 'BSPLINE':
                    points = [edge.positionAt(index/100).toTuple() for index in range(101)]
                    print(json.dumps({'spline_length': edge.Length(), 'points': points}), flush=True)


if __name__ == '__main__':
    main()
