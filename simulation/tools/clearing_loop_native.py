"""Native circle inventory for the unmodified loop, rivet and cover."""

import json
from simulation.standard.parts import ClearingRing, ClearingRingRivet, ClearingCover


if __name__ == '__main__':
    for part_type in (ClearingRing, ClearingRingRivet, ClearingCover):
        shape = part_type().shape()
        box = shape.BoundingBox()
        circles = sorted({(round(edge.radius(), 6),
                           tuple(round(v, 6) for v in edge.arcCenter().toTuple()))
                          for edge in shape.Edges() if edge.geomType() == 'CIRCLE'})
        print(json.dumps({'part': part_type.__name__, 'valid': shape.isValid(),
                          'bounds': [box.xmin, box.ymin, box.zmin,
                                     box.xmax, box.ymax, box.zmax],
                          'circles': circles}), flush=True)
