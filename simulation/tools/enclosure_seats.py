"""Compare native seats and source datums before adopting a correction."""

import json
import logging
from simulation.assemblies import Enclosure
from simulation.tools.interference import world_solids


def describe(shape):
    box = shape.BoundingBox() if shape.Vertices() else None
    return {'bounds': None if box is None else
            [box.xmin, box.ymin, box.zmin, box.xmax, box.ymax, box.zmax],
            'valid': shape.isValid(), 'volume': shape.Volume()}


def probe():
    logging.disable(logging.INFO)
    # Preserve the original datum probe after the operating enclosure is fitted.
    bench = Enclosure()
    bench.assemble()
    bench.build_stls()
    names = ('upper_outer_sleeve', 'lower_housing_1.bottom_housing',
             'lower_housing_1.lower_housing', 'base_plate')
    selected = {'Curta.' + name for name in names}
    solids = world_solids(bench, selected=selected)
    for path, shape in solids.items():
        circles = sorted({(round(edge.radius(), 6),
                           tuple(round(v, 6) for v in edge.arcCenter().toTuple()))
                          for edge in shape.Edges() if edge.geomType() == 'CIRCLE'})
        print(json.dumps({'part': path, **describe(shape), 'circles': circles}), flush=True)
    sleeve = solids['Curta.upper_outer_sleeve']
    bottom = solids['Curta.lower_housing_1.bottom_housing']
    housing = solids['Curta.lower_housing_1.lower_housing']
    plate = solids['Curta.base_plate']
    for shift in ((0, 0, 0), (.406900356, -.745841949, 0)):
        common = sleeve.intersect(bottom.translate(shift))
        assert common.isValid(), ('sleeve/bottom', shift)
        print(json.dumps({'lower_group_translation': shift, 'sleeve_bottom': describe(common)}), flush=True)
    for height in (-.01, -.001, 0, .001, .01):
        common = housing.intersect(plate.translate((0, 0, height)))
        assert common.isValid(), ('housing/base', height)
        print(json.dumps({'base_lift': height, 'housing_base': describe(common)}), flush=True)


if __name__ == '__main__':
    probe()
