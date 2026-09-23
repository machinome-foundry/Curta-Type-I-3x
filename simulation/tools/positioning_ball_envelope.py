"""Measure a radial guide's bell clearance envelope, not a follower law.

A point-to-source-solid distance locates the centre of a 3.80 mm-radius gauge
(the unchanged 3.75 mm ball plus a declared .05 mm normal seating allowance).
Final commons use the unchanged source ball, native and world64. Bisection
limits positional measurement; no positive common is accepted by a tolerance.
Only measuring copies move. The operating model and its retained bank do not.
"""

import argparse
import json
import logging
import math
import time

import cadquery as cq

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.tools.positioning_ball_contact import BALL, BELL, FRAME, COLLAR
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--step', type=int, choices=(1, 2, 5, 10), default=1)
    args = parser.parse_args()
    started = time.monotonic()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    saved = dict(sim.state)
    native = world_solids(sim.node, selected={BALL, BELL, FRAME})
    leaves = dict(rigid_leaves(sim.node))
    facets = {name: mesh_solid(leaves[name].mesh) for name in (BALL, BELL, FRAME, COLLAR)}
    centre = native[BALL].Center().toTuple()
    assert abs(centre[0]-9.627860318) < 1e-8 and abs(centre[2]-30) < 1e-8
    gauge_radius, outer_land_radius = 3.8, 8.041
    print(json.dumps(dict(kind='measurement', model='OperatingCurta',
                          ball_radius=3.75, normal_seat_allowance=.05,
                          native_gauge_radius=gauge_radius, iterations=20,
                          step_degrees=args.step, source_centre=centre,
                          scope='radial lower clearance envelope, not a driven pose or force law')), flush=True)
    for angle in range(0, 361, args.step):
        bell = native[BELL].rotate((0, 0, 0), (0, 0, 1), -angle)

        def distance(radius):
            value = cq.Vertex.makeVertex(radius, 0, 30).distance(bell)
            assert math.isfinite(value) and value >= 0
            return value

        low, high = outer_land_radius, outer_land_radius+gauge_radius+.001
        assert distance(low) < gauge_radius <= distance(high)
        for _ in range(20):
            middle = (low+high)/2
            if distance(middle) >= gauge_radius:
                high = middle
            else:
                low = middle
        offset = high-centre[0]
        ball = native[BALL].translate((offset, 0, 0))
        ball_mesh = facets[BALL].translate((offset, 0, 0))
        row = dict(kind='sample', angle=angle, centre_radius=high,
                   radial_offset=offset, bracket_mm=high-low,
                   normal_distance_mm=distance(high), native_mm3={}, world64_mm3={})
        for name, shape in ((BELL, bell), (FRAME, native[FRAME])):
            common = ball.intersect(shape)
            assert common.isValid(), (angle, name, 'invalid native common')
            row['native_mm3'][name] = common.Volume()
        for name in (BELL, FRAME, COLLAR):
            shape = facets[name].rotate((0, 0, -angle)) if name == BELL else facets[name]
            row['world64_mm3'][name] = faceted_common_volume(ball_mesh ^ shape)
        print(json.dumps(row), flush=True)
        assert all(value == 0 for value in (*row['native_mm3'].values(),
                                            *row['world64_mm3'].values())), row
    assert dict(sim.state) == saved
    print(json.dumps(dict(kind='finished', wall_seconds=time.monotonic()-started,
                          bank_unchanged=True, coordinates=len(saved),
                          acceptance='finite sampled radial envelope only; no operating adoption')),
          flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
