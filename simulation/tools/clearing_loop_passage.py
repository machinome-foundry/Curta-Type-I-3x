"""Local contact patches during the second clip's rigid swivel hypothesis."""

import json
import logging
from math import sin, cos, radians
import cadquery as cq
import numpy as np
from simulation.clearing_loop_seat import SeatedLoop


def second_peg_position(angle):
    # Independently measured installed rivet at -90 degrees, in loop frame.
    pivot = np.array((40.5, 0))
    deployed = np.array((31.095555539, 25.948341482))
    theta = radians(angle + 90)
    rotation = np.array(((cos(theta), -sin(theta)), (sin(theta), cos(theta))))
    # Source frame flips world Z, so increasing world swivel increases the
    # fixed peg's angle when expressed back in the moving source frame.
    return pivot + rotation @ (deployed-pivot)


def main():
    logging.disable(logging.INFO)
    loop = SeatedLoop().shape()
    for angle in (-90, -89, -87, -84, -80, -75, -70, -67, -63, -60):
        x, y = second_peg_position(angle)
        peg = cq.Solid.makeCylinder(3.75, 5.46, cq.Vector(x, y, 0))
        common = loop.intersect(peg)
        assert common.isValid()
        patches = []
        for patch in common.Solids():
            box = patch.BoundingBox()
            patches.append({'volume_mm3': patch.Volume(),
                            'bounds': [box.xmin, box.ymin, box.xmax, box.ymax]})
        print(json.dumps({'angle': angle, 'peg_xy': [x, y],
                          'patches': patches}), flush=True)


if __name__ == '__main__':
    main()
