"""Bracket native indexing-key contact in both directions at each working slot."""

import json
import logging
import argparse
from simulation.carriage_frame import CarriageFrameBench
from simulation.tools.interference import world_solids


def probe(envelope=False):
    logging.disable(logging.INFO)
    bench = CarriageFrameBench()
    bench.set_state(angle=0, elevation=0)
    bench.assemble()
    path = 'Curta.carrier.upper_carriage_body_1.counter_body'
    shapes = world_solids(bench, selected={path, 'Curta.frame'})
    body, frame = shapes[path], shapes['Curta.frame']
    if envelope:
        for angle in (0, .1, .18, .188, .189, .19, .2, .25, .3, .4, .5, .6, .7,
                      .8, .9, 1, 1.2, 1.5, 2, 5, 10):
            rotated = body.rotate((0, 0, 0), (0, 0, 1), angle)

            def contact(height):
                common = rotated.translate((0, 0, height)).intersect(frame)
                assert common.isValid(), (angle, height)
                return common.Volume() > 0

            low, high = 0, 6
            if not contact(0):
                high = 0
            else:
                assert not contact(high), angle
                for _ in range(15):
                    middle = (low + high) / 2
                    if contact(middle):
                        low = middle
                    else:
                        high = middle
            print(json.dumps({'angle': angle, 'last_contact_lift': low,
                              'first_free_lift': high}), flush=True)
        return
    seating_contact = body.translate((0, 0, -.04)).intersect(frame)
    for part in seating_contact.Solids():
        box = part.BoundingBox()
        print(json.dumps({'lowering_004_contact_mm3': part.Volume(),
                          'bounds': [box.xmin, box.ymin, box.zmin,
                                     box.xmax, box.ymax, box.zmax]}), flush=True)
    for height in (0, 3, 5.8):
        raised = body.translate((0, 0, height))
        for working in range(0, 101, 20):
            for direction in (-1, 1):
                def blocked(travel):
                    posed = raised.rotate((0, 0, 0), (0, 0, 1), working + direction * travel)
                    common = posed.intersect(frame)
                    assert common.isValid(), (height, working, direction, travel)
                    return common.Volume() > 0

                low, high = 0, 2
                assert not blocked(low), (height, working, 'rest blocked')
                assert blocked(high), (height, working, 'no indexing contact')
                for _ in range(12):
                    middle = (low + high) / 2
                    if blocked(middle):
                        high = middle
                    else:
                        low = middle
                print(json.dumps({'height': height, 'working': working, 'direction': direction,
                                  'last_free_travel': low, 'first_contact_travel': high}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--envelope', action='store_true')
    probe(parser.parse_args().envelope)
