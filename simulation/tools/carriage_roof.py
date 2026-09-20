"""Inspect the bounded pocket-roof cut and independent Boolean decompositions."""

import json
import cadquery as cq
from simulation.standard.parts import CounterBody
from simulation.carriage_frame_fit import FittedCounterBody


def describe(name, shape):
    box = shape.BoundingBox() if shape.Solids() else None
    print(json.dumps({'name': name, 'volume': shape.Volume(), 'valid': shape.isValid(),
                      'solids': len(shape.Solids()),
                      'bounds': [box.xmin, box.ymin, box.zmin, box.xmax, box.ymax, box.zmax]
                      if box else None}),
          flush=True)


if __name__ == '__main__':
    original = CounterBody().shape()
    fitted = FittedCounterBody().shape()
    zone = cq.Solid.makeCylinder(34.25, .05, cq.Vector(0, 0, 14.05)).cut(
        cq.Solid.makeCylinder(21.9, .05, cq.Vector(0, 0, 14.05)))
    shifted = original.translate((0, 0, -.05))
    skin = original.cut(shifted).intersect(zone)
    removed = original.cut(fitted).intersect(zone)
    for face in original.Faces():
        if abs(face.Center().z - 14.1) < .001:
            print(json.dumps({'roof_normal': face.normalAt().toTuple(),
                              'area': face.Area(), 'wires': len(face.Wires())}), flush=True)
    for name, shape in [('skin', skin), ('removed', removed),
                        ('common', removed.intersect(shifted)),
                        ('outside_skin', removed.cut(skin)),
                        ('shifted_removed_cut', shifted.cut(removed)),
                        ('shifted', shifted)]:
        describe(name, shape)
    import math
    from collections import Counter
    counts = Counter()
    lost_key_points = []
    for radius in (22.5, 25, 28, 31, 33):
        for angle in range(360):
            point = (radius * math.cos(math.radians(angle)),
                     radius * math.sin(math.radians(angle)), 14.075)
            occupied = tuple(s.isInside(point, tolerance=1e-7) for s in (original, shifted, fitted))
            counts[str(occupied)] += 1
            if occupied == (True, True, False):
                lost_key_points.append((radius, angle))
    print(json.dumps({'classifications': counts, 'lost_key_points': lost_key_points}), flush=True)
