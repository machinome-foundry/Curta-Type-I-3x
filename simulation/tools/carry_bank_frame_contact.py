"""Inventory every installed carry slider against the complete fixed frame.

Translated solids are read-only stroke witnesses, not admitted operating
motions. No symmetry assumption, new fit, exemption or whole-path claim.
"""

import json
import logging
import time

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.tools.moving_seats import world_frames
from simulation.tools.open_run_transitions import bounds
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume

FRAME = 'Curta.frame.upper_frame.main_body'


def main():
    started = time.monotonic()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    bank = dict(sim.state)
    leaves = dict(rigid_leaves(sim.node))
    sliders = sorted(path for path in leaves if path.startswith('Curta.carry_mechanism.')
                     and path.rsplit('.', 1)[-1] in
                     ('tens_slider_for_results', 'tens_slider_for_turns_counter'))
    assert len(sliders) == 15
    shapes = world_solids(sim.node, selected={FRAME, *sliders})
    frames = world_frames(sim.node, include_assemblies=True)
    frame_mesh = mesh_solid(leaves[FRAME].mesh)
    for path in sliders:
        native, mesh = shapes[path], mesh_solid(leaves[path].mesh)
        # The site-declared slider joint is in its parent's frame, not the
        # imported solid's own rotated frame. Transport the parent-frame -Z.
        direction = frames[path.rsplit('.', 1)[0]][:3, :3] @ (0, 0, -1)
        for drop in (0, 2.1, 4.2):
            displacement = tuple(float(value * drop) for value in direction)
            common = native.translate(displacement).intersect(shapes[FRAME])
            assert common.isValid()
            record = dict(path=path, stroke_from_initial_mm=drop,
                          travel_at_initial=bank[path.removeprefix('Curta.')+'.travel'],
                          world_displacement_mm=displacement,
                          native_mm3=common.Volume(),
                          world64_mm3=faceted_common_volume(mesh.translate(displacement) ^ frame_mesh))
            if common.Vertices():
                record['native_common_bounds_mm'] = bounds(common).tolist()
            print(json.dumps(record), flush=True)
    assert dict(sim.state) == bank
    print(json.dumps(dict(kind='finished', stations=len(sliders), witnesses=3*len(sliders),
                          bank_unchanged=True, wall_seconds=time.monotonic()-started,
                          acceptance='Read-only stroke witnesses; no fit or clearance acceptance')),
          flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
