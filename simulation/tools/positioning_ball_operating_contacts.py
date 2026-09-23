"""Audit the candidate ball against every rigid and flexible mesh during demos."""

import argparse
import json
import logging
import time

import numpy as np

from machinome.simulation import Sim
from machinome.exact import intersect_shapes
from simulation.running import OperatingCurta
from simulation.operating_demonstrations import DEMONSTRATIONS, replay
from simulation.positioning_ball_trial import RadialBallTrial
from simulation.test_carry_bank_trial import flexible_meshes
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.tools.positioning_ball_contact import BALL
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demonstrations', nargs='+', choices=tuple(DEMONSTRATIONS),
                        default=list(DEMONSTRATIONS))
    parser.add_argument('--model', choices=('trial', 'production'), default='trial')
    args = parser.parse_args()
    started = time.monotonic()
    sim = Sim((OperatingCurta if args.model == 'production' else RadialBallTrial)(), dt=.1, meshes=True)
    initial = sim.snapshot()
    current, count, findings = None, 0, []

    def sample():
        nonlocal count
        leaves = dict(rigid_leaves(sim.node))
        meshes = {path: part.mesh for path, part in leaves.items()}
        flexible = dict(flexible_meshes(sim.node))
        assert not meshes.keys() & flexible.keys()
        meshes.update(flexible)
        assert len(leaves) == 389 and len(flexible) > 30
        ball = meshes[BALL]
        bounds = ball.bounds
        candidates = {path for path, mesh in meshes.items() if path != BALL and
            np.all(np.minimum(bounds[1], mesh.bounds[1]) >= np.maximum(bounds[0], mesh.bounds[0]))}
        native = world_solids(sim.node, include_flexible=True, selected=candidates | {BALL})
        ball_mesh = mesh_solid(ball)
        positive = {}
        for path in sorted(candidates):
            mesh_volume = faceted_common_volume(ball_mesh ^ mesh_solid(meshes[path]))
            native_volume = None
            if path in native:
                common = intersect_shapes(native[BALL], native[path], BALL, path)
                assert common.isValid(), (current, sim.time, path)
                native_volume = common.Volume()
            if mesh_volume > 0 or native_volume is not None and native_volume > 0:
                positive[path] = dict(native_mm3=native_volume, world64_mm3=mesh_volume)
        count += 1
        row = dict(kind='sample', demonstration=current, time=sim.time,
            crank_degrees=sim.state['crank_rotation'], lift_mm=sim.state['carriage_elevation'],
            shift_degrees=sim.state['carriage_rotation'],
            ball_mm=sim.state['carriage.positioning.p_6mm_ball_419094.slide'],
            rigid_occurrences=len(leaves), flexible_leaves=len(flexible),
            neighbours_considered=len(meshes)-1, spatial_candidates=len(candidates), positive=positive)
        print(json.dumps(row), flush=True)
        if positive:
            findings.append(row)

    sim.every(.1, sample)
    sample()
    for name in args.demonstrations:
        current = name
        outcomes = replay(sim, name, initial)
        print(json.dumps(dict(kind='demonstration-completed', name=name, outcomes=outcomes)), flush=True)
    print(json.dumps(dict(kind='finished', samples=count, positive_samples=len(findings),
        seconds=time.monotonic()-started, model=args.model,
        acceptance='Ball interface only; other pairs not waived')), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
