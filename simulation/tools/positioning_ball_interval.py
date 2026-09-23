"""Conservative native bell/ball enclosures between measured profile knots.

This diagnostic does not adopt the radial law or certify other neighbours.
Every capsule includes all retained radial slack up to the collar's global
maximum, not only the ball placement exactly on the lower envelope.
"""

import argparse
import hashlib
import json
import logging
from math import radians
from pathlib import Path
import time

import cadquery as cq
import numpy as np

from machinome.simulation import Sim
from machinome.exact import intersect_shapes
from simulation.running import OperatingCurta
from simulation.positioning_ball_profiles import BELL_ENVELOPE
from simulation.tools.positioning_ball_contact import BALL, BELL
from simulation.tools.interference import world_solids, rigid_leaves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start', type=float, default=0)
    parser.add_argument('--end', type=float, default=360)
    args = parser.parse_args()
    assert 0 <= args.start < args.end <= 360
    started = time.monotonic()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    saved = dict(sim.state)
    native = world_solids(sim.node, selected={BALL, BELL})
    ball, bell = native[BALL], native[BELL]
    assert ball.isValid() and len(ball.Faces()) == 1 and ball.Faces()[0].geomType() == 'SPHERE'
    centre = np.asarray(ball.Center().toTuple())
    np.testing.assert_allclose(centre, (9.627860318, 0, 30), atol=1e-9, rtol=0)
    mesh = dict(rigid_leaves(sim.node))[BALL].mesh
    assert np.linalg.norm(mesh.vertices-centre, axis=1).max() < 3.750002
    profile = np.asarray(BELL_ENVELOPE)
    knots = sorted({args.start, args.end, *(float(a) for a, _ in BELL_ENVELOPE
                                           if args.start < a < args.end)})
    checks, accepted, invalid_coarse = 0, [], 0

    def prove(a, b, depth=0):
        nonlocal checks, invalid_coarse
        mid = (a+b)/2
        inner = float(min(np.interp(a, profile[:, 0], profile[:, 1]),
                          np.interp(b, profile[:, 0], profile[:, 1])))-.000001
        outer = 11.950001
        # Rotation of any centre of radius <=12 moves it by at most radius
        # times angular displacement. Bound the whole arc about its midpoint.
        radius = 3.750002 + 12*radians(b-a)/2 + .000001
        first, last = (inner, 0, 30), (outer, 0, 30)
        capsule = cq.Solid.makeCylinder(radius, outer-inner, first, (1, 0, 0)).fuse(
            cq.Solid.makeSphere(radius, first, angleDegrees1=-90),
            cq.Solid.makeSphere(radius, last, angleDegrees1=-90)).clean()
        capsule = capsule.rotate((0, 0, 0), (0, 0, 1), mid)
        checks += 1
        if checks % 100 == 0:
            print(json.dumps(dict(kind='enclosure-progress', start=a, end=b, depth=depth,
                                  checks=checks, certified_intervals=len(accepted))), flush=True)
        try:
            common = intersect_shapes(capsule, bell, 'conservative ball capsule', BELL)
            valid = common.isValid()
            refusal = None if valid else 'invalid Boolean'
        except RuntimeError as error:
            valid, refusal = False, str(error)
        if not valid:
            invalid_coarse += 1
        if valid and common.Volume() == 0:
            accepted.append((a, b, radius))
            return
        assert depth < 14, (a, b, common.Volume() if valid else refusal, 'unresolved enclosure')
        prove(a, mid, depth+1)
        prove(mid, b, depth+1)

    for a, b in zip(knots, knots[1:]):
        prove(a, b)
        print(json.dumps(dict(kind='profile-interval', start=a, end=b,
            cumulative_checks=checks, certified_intervals=len(accepted))), flush=True)
    assert dict(sim.state) == saved
    profile_path = Path('simulation/positioning_ball_profiles.py')
    print(json.dumps(dict(kind='finished', checks=checks, certified_intervals=len(accepted),
        invalid_coarse_refined=invalid_coarse,
        profile_sha256=hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        minimum_interval_degrees=min(b-a for a, b, _ in accepted),
        seconds=time.monotonic()-started, bank_unchanged=True,
        acceptance='Native bell/ball path only; published bell mesh and other neighbours separate')), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
