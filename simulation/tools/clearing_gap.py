"""Measure the missing-tooth clearance band; never choose a solver epsilon.

Companion to clearing_zero.py: rotate the zero dial about its validated
radial axle and sweep the actual fitted tooth row across it. This faceted
probe brackets a candidate band; native contact checks must confirm it.
"""

import json
from math import cos, sin, radians

import manifold3d as manifold
import numpy as np
import trimesh

from simulation.clearing_contact import ClearingContactBench
from simulation.tools.carry_phase import solid


def probe():
    model = ClearingContactBench()
    model.set_state(digit=0, clear=0)
    model.assemble()
    model.build_stls()
    for name, part, row, station in (
            ('outer', model.results.p_10203_1.results_dial_type_1,
             model.clearing.tooth_stack.outer_teeth, 0),
            ('inner', model.results.p_10205_1.results_dial_type_2,
             model.clearing.tooth_stack.inner_teeth, -40)):
        wheel, strip = solid(part.mesh), solid(row.mesh)
        axis = np.array((cos(radians(station)), sin(radians(station)), 0))
        pivot = 71.474057463 * axis + (0, 0, 33.9)
        samples = [(float(angle), strip.transform(trimesh.transformations.rotation_matrix(
            radians(-angle), (0, 0, 1))[:3])) for angle in np.arange(0, 80.01, .25)]
        for displacement in (0, -.25, .25, -.5, .5, -1, 1, -2, 2, -4, 4, -8, 8, -12, 12):
            placed = wheel.transform(trimesh.transformations.rotation_matrix(
                radians(displacement), axis, pivot)[:3])
            contact = None
            for angle, rack in samples:
                overlap = placed ^ rack
                if overlap.status() != manifold.Error.NoError:
                    raise RuntimeError(overlap.status())
                if overlap.volume() > 0:
                    contact = {'ring_angle': angle, 'volume_mm3': overlap.volume()}
                    break
            print(json.dumps({'row': name, 'dial_displacement': displacement,
                              'first_contact': contact}), flush=True)


if __name__ == '__main__':
    probe()
