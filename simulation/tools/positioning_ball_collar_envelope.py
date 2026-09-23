"""Measure the source-STL collar's inward-pushing radial clearance envelope.

Point-to-triangle distance measures a 3.80 mm spherical gauge; final contact
checks retain the original 3.75 mm source ball. Only measuring copies move.
This supplies an upper envelope, not an operating law, force model or fit.
"""

import json
import logging
import math
import time

import numpy as np
import trimesh

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.interference import rigid_leaves
from simulation.tools.positioning_ball_contact import BALL, COLLAR, FRAME
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


def main():
    started = time.monotonic()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    saved = dict(sim.state)
    leaves = dict(rigid_leaves(sim.node))
    ball, frame = (mesh_solid(leaves[name].mesh) for name in (BALL, FRAME))
    print(json.dumps(dict(kind='measurement', kernel='source STL, world64',
                          ball_radius=3.75, normal_seat_allowance=.05,
                          native_collar_available=False, iterations=20,
                          scope='collar upper radial envelope only, no operating law')), flush=True)
    for quarter in range(25):
        lift = quarter/4
        collar_mesh = leaves[COLLAR].mesh.copy()
        collar_mesh.apply_translation((0, 0, lift))

        def distance(radius):
            _, distances, _ = trimesh.proximity.closest_point(
                collar_mesh, np.array([[radius, 0, 30]]))
            value = float(distances[0])
            assert math.isfinite(value) and value >= 0
            return value

        low, high = 7.5, 13
        assert distance(low) >= 3.8 > distance(high)
        for _ in range(20):
            middle = (low+high)/2
            if distance(middle) >= 3.8:
                low = middle
            else:
                high = middle
        candidate = ball.translate((low-9.627860318, 0, 0))
        collar = mesh_solid(collar_mesh)
        commons = {COLLAR: faceted_common_volume(candidate ^ collar),
                   FRAME: faceted_common_volume(candidate ^ frame)}
        row = dict(kind='sample', carriage_lift=lift, centre_radius=low,
                   radial_offset=low-9.627860318, bracket_mm=high-low,
                   normal_distance_mm=distance(low), world64_mm3=commons)
        print(json.dumps(row), flush=True)
        assert all(value == 0 for value in commons.values()), row
    assert dict(sim.state) == saved
    print(json.dumps(dict(kind='finished', wall_seconds=time.monotonic()-started,
                          bank_unchanged=True, coordinates=len(saved),
                          acceptance='25 sampled upper-envelope positions only; no operating adoption')),
          flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
