"""Locate the retained carriage/frame contacts before declaring shift stops."""

import json
import logging
import cadquery as cq
from simulation.clearing_interlock import SourceClearingSeatBench
from simulation.tools.interference import world_solids


def extent(shape):
    box = shape.BoundingBox()
    return [box.xmin, box.ymin, box.zmin, box.xmax, box.ymax, box.zmax]


def probe():
    logging.disable(logging.INFO)
    bench = SourceClearingSeatBench()
    bench.set_state(elevation=0, shift=0, sweep=0)
    bench.assemble()
    prefix = 'Curta.carriage.carrier.upper_carriage_body_1.'
    names = ('counter_body', 'counter_body_pin_1', 'counter_body_pin_2')
    paths = {'Curta.frame', *(prefix + name for name in names)}
    initial = world_solids(bench, selected=paths)
    for path, shape in initial.items():
        print(json.dumps({'part': path, 'bounds': extent(shape),
                          'circles': sorted({(round(edge.radius(), 6),
                                              tuple(round(v, 6) for v in edge.arcCenter().toTuple()))
                                             for edge in shape.Edges() if edge.geomType() == 'CIRCLE'
                                             and 6 < edge.radius() < 25})}), flush=True)
    frame = initial['Curta.frame']
    contact = initial[prefix + 'counter_body'].intersect(frame)
    for radius in (28, 29, 30, 30.5, 31, 31.5, 31.65, 31.7, 31.75, 32, 34.2, 34.25):
        cylinder = cq.Solid.makeCylinder(radius, 20, cq.Vector(0, 0, 20))
        clipped = contact.intersect(cylinder)
        assert clipped.isValid(), radius
        print(json.dumps({'rest_contact_inside_radius': radius,
                          'volume_mm3': clipped.Volume()}), flush=True)
    for lift in (0, 1, 3, 6):
        for shift in (0, .5, 1, 2, 5, 10, 19, 20, 40, 100):
            bench.set_state(elevation=lift, shift=shift)
            shapes = world_solids(bench, selected=paths)
            for name in names:
                overlap = shapes[prefix + name].intersect(frame)
                assert overlap.isValid(), (lift, shift, name)
                print(json.dumps({'lift': lift, 'shift': shift, 'part': name,
                                  'overlap_mm3': overlap.Volume(),
                                  'regions': [{'bounds': extent(part), 'volume_mm3': part.Volume()}
                                              for part in overlap.Solids()]}), flush=True)


if __name__ == '__main__':
    probe()
