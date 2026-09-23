"""Locate installed protected hardware relative to maximum permitted removal."""

import json
import logging
import time

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.carry_bank_regions import maximally_relieved
from simulation.standard.parts import MainBody
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.tools.open_run_transitions import bounds


def main():
    started = time.monotonic()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    bank = dict(sim.state)
    protected = set()
    for path, node in rigid_leaves(sim.node):
        name = path.rsplit('.', 1)[-1]
        if path == 'Curta.frame.upper_frame.main_body':
            continue
        if (name.startswith(('m3', 'm4', 'm5', 'm6', 'frame_support'))
                or path.startswith('Curta.frame.')):
            protected.add(path)
    shapes = world_solids(sim.node, selected=protected)
    assert set(shapes) == protected, ('missing native protected body', protected-set(shapes))
    source = MainBody().shape()
    removed = source.cut(maximally_relieved(source))
    assert removed.isValid() and removed.Volume() > 0
    failures = []
    for path in sorted(protected):
        distance = removed.distance(shapes[path])
        print(json.dumps(dict(path=path, removal_distance_mm=distance,
                              bounds_mm=bounds(shapes[path]).tolist())), flush=True)
        if distance <= 0:
            failures.append(path)
    assert dict(sim.state) == bank
    print(json.dumps(dict(kind='finished', protected_bodies=len(protected), failures=failures,
                          bank_unchanged=True, wall_seconds=time.monotonic()-started,
                          acceptance='Prospective permitted-region gate; production frame unchanged')),
          flush=True)
    assert not failures


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
