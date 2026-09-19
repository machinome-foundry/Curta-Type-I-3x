"""Measure the original pin seating against STEP or printable-STL frame."""

import json
import logging
import argparse
from machinome.test import TestCase
from simulation.carriage_stop import SourceCarriageStopBench, PrintedSourceCarriageStopBench


def probe(printed=False):
    logging.disable(logging.INFO)
    model = (PrintedSourceCarriageStopBench if printed else SourceCarriageStopBench)()
    model.set_state(angle=0, elevation=0)
    model.assemble()
    model.build_stls()
    checks = TestCase()
    pin = model.carrier.upper_carriage_body_1.counter_body_stop_pin
    body = model.carrier.upper_carriage_body_1.counter_body
    print(json.dumps({'pin_world_bounds': pin.mesh.bounds.tolist(),
                      'carrier_world_bounds': body.mesh.bounds.tolist(),
                      'carrier_bore_circles': sorted({
                          (round(edge.radius(), 6), tuple(round(v, 6) for v in edge.arcCenter().toTuple()))
                          for edge in body.shape().Edges()
                          if edge.geomType() == 'CIRCLE' and 2 < edge.radius() < 3}),
                      'frame_world_bounds': model.frame.mesh.bounds.tolist()}), flush=True)
    def clear(height):
        model.set_state(angle=0, elevation=height)
        try:
            checks.assertNotIntersecting(pin, model.frame)
        except AssertionError:
            return False
        return True

    low, high = 0, .5
    assert not clear(low) and clear(high)
    for _ in range(20):
        middle = (low + high) / 2
        if clear(middle):
            high = middle
        else:
            low = middle
    print(json.dumps({'pin_seating_rise_last_contact': low,
                      'pin_seating_rise_first_free': high}), flush=True)
    for lift in (0, .5, 1, 1.5, 3, 6):
        for angle in (-20, -1, 0, .1, 1, 5, 10, 19, 20, 40, 60, 80,
                      100, 101, 120, 180, 270):
            model.set_state(angle=angle, elevation=lift)
            try:
                checks.assertNotIntersecting(pin, model.frame)
                contact = None
            except AssertionError as error:
                contact = str(error)
            print(json.dumps({'elevation': lift, 'angle': angle,
                              'pin_world_bounds': pin.mesh.bounds.tolist(),
                              'contact': contact}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--printed', action='store_true', help='Use the original STL main body')
    probe(parser.parse_args().printed)
