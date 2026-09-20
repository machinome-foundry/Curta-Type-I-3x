"""Locate axial obstructions with the complete six-input reverser bench.

Knob and gears move together here only as a diagnostic. The unfollowed ball
and spring are not certified by this probe; they have a separate seat probe.
"""

import json
import logging
import numpy as np
from simulation.reverser_assembly import ReverserAssemblyBench
from simulation.test_reverser_assembly import INPUTS
from simulation.tools.interference import rigid_leaves, world_solids


def probe():
    logging.disable(logging.INFO)
    bench = ReverserAssemblyBench()
    bench.set_state(knob_height=0, gear_height=0, crank_angle=0,
                    subtract=0, reversed_counter=0)
    bench.assemble()
    bench.build_stls()
    parts = dict(rigid_leaves(bench))
    gears = {f'Curta.{name}.{member}' for name, member in INPUTS}
    knobs = {path for path in parts if path.startswith('Curta.lever.reversing_lever_knob_1.')}
    excluded = {'Curta.lever.p_5mm_ball', 'Curta.lever.selector_knob_spring'}
    selected = set(parts) - excluded
    for height in (-7.6427, -6.8425, -6, -5.5, -5.0925, -4.5, 0, 3.4075, 3.9075):
        bench.set_state(knob_height=height, gear_height=height)
        native = world_solids(bench, selected=selected)
        assert selected <= set(native), selected - set(native)
        boxes = {path: parts[path].mesh.bounds for path in selected}
        collisions = {}
        for moving in sorted(gears | knobs):
            for other in sorted(selected - {moving}):
                if other in gears | knobs and other < moving:
                    continue
                a, b = boxes[moving], boxes[other]
                if not np.all(np.minimum(a[1], b[1]) > np.maximum(a[0], b[0])):
                    continue
                common = native[moving].intersect(native[other])
                if not common.isValid():
                    raise ValueError((height, moving, other, 'invalid native common'))
                volume = common.Volume()
                if volume > 0:
                    collisions[moving + ' / ' + other] = volume
        print(json.dumps({'height': height, 'overlap_mm3': collisions}), flush=True)


if __name__ == '__main__':
    probe()
