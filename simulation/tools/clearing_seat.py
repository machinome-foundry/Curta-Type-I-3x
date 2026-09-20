"""Measure pin/frame contact independently of any proposed carriage limit."""

import argparse
import json
import logging
import manifold3d as manifold
from simulation.clearing_interlock import SourceClearingSeatBench
from simulation.tools.interference import world_solids
from simulation.tools.carry_phase import solid


def probe(faceted=False):
    logging.disable(logging.INFO)
    bench = SourceClearingSeatBench()
    bench.set_state(elevation=0, shift=0, sweep=0)
    bench.assemble()
    bench.build_stls()
    pin = bench.carriage.carrier.upper_carriage_body_1.clearing_pin
    paths = ('Curta.carriage.carrier.upper_carriage_body_1.clearing_pin', 'Curta.frame')
    for shift in (0, 20, 40, 60, 80, 100):
        for sweep in (0, 1, 5, 14, 90, 218, 230, 231, 240, 360):
            bench.set_state(elevation=0, shift=shift, sweep=sweep)
            if faceted:
                moving, frame = solid(pin.mesh), solid(bench.frame.mesh)
            else:
                shapes = world_solids(bench, selected=set(paths))
                moving, frame = (shapes[path] for path in paths)

            def volume(height):
                raised = moving.translate((0, 0, height))
                if faceted:
                    overlap = raised ^ frame
                    if overlap.status() != manifold.Error.NoError:
                        raise ValueError(str(overlap.status()))
                    return overlap.volume()
                overlap = raised.intersect(frame)
                if not overlap.isValid():
                    raise ValueError(f'Invalid native contact: shift={shift}, sweep={sweep}, lift={height}')
                return overlap.Volume()

            samples = {height: volume(height) for height in (0, 1, 3, 6)}
            bracket = None
            if samples[0] > 0 and samples[6] == 0:
                low, high = 0, 6
                for _ in range(20):
                    middle = (low + high) / 2
                    if volume(middle) > 0:
                        low = middle
                    else:
                        high = middle
                bracket = (low, high)
            print(json.dumps({'kernel': 'faceted' if faceted else 'exact',
                              'shift': shift, 'sweep': sweep, 'pin_drop': pin.slide.value,
                              'pin_bounds': pin.mesh.bounds.tolist(),
                              'overlap_mm3_by_lift': samples,
                              'last_contact_first_free_lift': bracket}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--faceted', action='store_true')
    probe(parser.parse_args().faceted)
