"""Independent world-axis contact checks for the candidate reversal throws."""

import json
from math import radians
import trimesh
import manifold3d as manifold

from simulation.counter_reversal import CounterReversalBench
from simulation.tools.carry_phase import solid


def probe():
    for stroke in (12, 9):
        model = CounterReversalBench(stroke=stroke)
        model.set_state(crank_angle=101.25, subtract=0)
        model.assemble()
        model.build_stls()
        for angle in (101.25, 146.25, 191.25):
            model.set_state(crank_angle=angle, subtract=0)
            gear = model.counter
            drum = model.drum.main_axle_step_drum_top_1
            pinion, driver = solid(gear.mesh), solid(drum.mesh)
            volumes = {}
            for perturb in (-12, 0, 12):
                transform = trimesh.transformations.rotation_matrix(
                    radians(perturb), (0, 0, 1), (-13.851815805, 38.057551142, 0))
                overlap = pinion.transform(transform[:3]) ^ driver
                assert overlap.status() == manifold.Error.NoError
                volumes[perturb] = overlap.volume()
            print(json.dumps({'stroke': stroke, 'crank': angle,
                              'gear_bounds': gear.mesh.bounds.tolist(),
                              'overlap_mm3': volumes}), flush=True)


if __name__ == '__main__':
    probe()
