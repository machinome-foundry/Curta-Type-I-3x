"""Check between-knot radial placements; no operating-following claim."""

import json
import logging
import time

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.positioning_ball_profiles import bell_limit, collar_limit
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.tools.positioning_ball_contact import BALL, BELL, FRAME, COLLAR
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


def main():
    started = time.monotonic()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    saved = dict(sim.state)
    native = world_solids(sim.node, selected={BALL, BELL, FRAME})
    leaves = dict(rigid_leaves(sim.node))
    facets = {name: mesh_solid(leaves[name].mesh) for name in (BALL, BELL, FRAME, COLLAR)}
    print(json.dumps(dict(kind='scope', bell_degrees_step=.1,
                          bell_dense_intervals=((0, 30), (330, 360)),
                          bell_land_step=1, collar_lift_step=.05,
                          assertion='exact-zero commons, unchanged source ball',
                          operating_following=False)), flush=True)
    samples = 0
    phases = sorted(set([i/10 for i in range(301)] +
                        [i/10 for i in range(3300, 3601)] +
                        list(range(31, 330))))
    for kind, values in (('bell', phases), ('collar', [i/20 for i in range(121)])):
        for value in values:
            angle, lift = (value, 0) if kind == 'bell' else (0, value)
            offset = float(bell_limit(-angle) if kind == 'bell' else collar_limit(lift))
            ball = native[BALL].translate((offset, 0, 0))
            ball_mesh = facets[BALL].translate((offset, 0, 0))
            row = dict(kind=kind, value=value, offset=offset, native_mm3={}, world64_mm3={})
            for name, shape in ((BELL, native[BELL].rotate((0, 0, 0), (0, 0, 1), -angle)),
                                (FRAME, native[FRAME])):
                common = ball.intersect(shape)
                assert common.isValid(), (kind, value, name, 'invalid native common')
                row['native_mm3'][name] = common.Volume()
            for name in (BELL, FRAME, COLLAR):
                shape = facets[name]
                if name == BELL:
                    shape = shape.rotate((0, 0, -angle))
                elif name == COLLAR:
                    shape = shape.translate((0, 0, lift))
                row['world64_mm3'][name] = faceted_common_volume(ball_mesh ^ shape)
            print(json.dumps(row), flush=True)
            assert all(v == 0 for v in (*row['native_mm3'].values(),
                                        *row['world64_mm3'].values())), row
            samples += 1
    assert dict(sim.state) == saved
    print(json.dumps(dict(kind='finished', samples=samples, bank_unchanged=True,
                          wall_seconds=time.monotonic()-started)), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
