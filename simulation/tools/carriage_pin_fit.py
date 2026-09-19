"""Independent exact intersections using public world placements."""

import json
import logging
from simulation.carriage_stop import SourceCarriageStopBench
from simulation.tools.interference import world_solids
from simulation.standard.parts import CounterBody, CounterBodyStopPin


def probe():
    logging.disable(logging.INFO)
    model = SourceCarriageStopBench()
    model.set_state(angle=0, elevation=0)
    model.assemble()
    prefix = 'Curta.carrier.upper_carriage_body_1.'
    paths = {prefix + 'counter_body', prefix + 'counter_body_stop_pin'}
    shapes = world_solids(model, selected=paths)
    body, pin = (shapes[prefix + name] for name in ('counter_body', 'counter_body_stop_pin'))
    # Keep this reproduction on the original native STEP pin even after the
    # operating carrier switches to the author-supplied print.
    pin = pin.translate((0, 0, .51))
    for name, shape in (('body', body), ('pin', pin)):
        box = shape.BoundingBox()
        print(json.dumps({'part': name, 'bounds': [box.xmin, box.xmax, box.ymin, box.ymax,
                                                  box.zmin, box.zmax],
                          'volume_mm3': shape.Volume(),
                          'bore_circles': [(round(edge.radius(), 6), edge.arcCenter().toTuple())
                                           for edge in shape.Edges()
                                           if edge.geomType() == 'CIRCLE' and 2 < edge.radius() < 3]}), flush=True)
    for shift in (-1, -.3, -.15, -.1, -.05, 0, .05, .1, .15, .3, 1):
        moved = pin.translate((shift, 0, 0))
        overlap = moved.intersect(body)
        print(json.dumps({'shift_x': shift, 'pin_valid': moved.isValid(),
                          'body_valid': body.isValid(), 'overlap_valid': overlap.isValid(),
                          'overlap_mm3': overlap.Volume()}), flush=True)
    for z in (26, 30, 34, 38, 44):
        for radial in (2.1, 2.31, 2.5, 3.3):
            point = (-23.640728 + radial, 16.553416, z)
            print(json.dumps({'point': point, 'inside_body': body.isInside(point),
                              'inside_shifted_pin': pin.translate((.15, 0, 0)).isInside(point)}),
                  flush=True)
    moved = pin.translate((.15, 0, 0))
    for label, first, second in (('swapped', body, moved),
                                 ('cleaned', moved.clean(), body.clean())):
        print(json.dumps({'boolean': label, 'overlap_mm3': first.intersect(second).Volume(),
                          'cut_volume_loss_mm3': first.Volume() - first.cut(second).Volume()}),
              flush=True)
    local_body = CounterBody().shape()
    local_pin = CounterBodyStopPin().shape().translate((23.640728 - .15, 16.553416, 8.945589482))
    print(json.dumps({'boolean': 'unrotated_source_pair',
                      'overlap_mm3': local_pin.intersect(local_body).Volume()}), flush=True)


if __name__ == '__main__':
    probe()
