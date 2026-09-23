"""Read-only transverse frame-guide measurements, including invalid booleans."""

import json
import logging

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.positioning_ball_contact import BALL, FRAME, COLLAR
from simulation.tools.interference import world_solids, rigid_leaves
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


def main():
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    saved = sim.snapshot()
    shapes = world_solids(sim.node, selected={BALL, FRAME})
    meshes = {p: mesh_solid(n.mesh) for p, n in rigid_leaves(sim.node)
              if p in {BALL, FRAME, COLLAR}}
    for radial in (-1.2252018554755857, 0, 2.213142830078919):
        for axis in (1, 2):
            for sign in (-1, 1):
                for travel in (.01, .2, .3, .4, .6, 1):
                    delta = [radial, 0, 0]
                    delta[axis] = travel * sign
                    ball = shapes[BALL].translate(tuple(delta))
                    mesh = meshes[BALL].translate(tuple(delta))
                    common = ball.intersect(shapes[FRAME])
                    print(json.dumps(dict(radial=radial, axis=axis, sign=sign, travel=travel,
                        native_valid=common.isValid(), native_frame_mm3=common.Volume(),
                        mesh_frame_mm3=faceted_common_volume(mesh ^ meshes[FRAME]),
                        mesh_collar_mm3=faceted_common_volume(mesh ^ meshes[COLLAR]))), flush=True)
    assert sim.snapshot() == saved
    print(json.dumps(dict(bank_unchanged=True, samples=72)), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
