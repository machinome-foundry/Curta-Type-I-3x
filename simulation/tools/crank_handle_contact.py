"""Retain strict geometric evidence for the two newly observed handle commons."""

import json
import logging
import time

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.operating_demonstrations import replay
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume

CRANK = 'Curta.main_drive.crank.crank_handle_1.main_crank'
HANDLE = 'Curta.main_drive.crank.crank_handle_1.crank_handle'


def main():
    started = time.monotonic()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    initial = sim.snapshot()
    seen = []

    def sample():
        if round(sim.time, 1) not in (1.6, 3.7):
            return
        leaves = dict(rigid_leaves(sim.node))
        native = world_solids(sim.node, selected={CRANK, HANDLE})
        common = mesh_solid(leaves[CRANK].mesh) ^ mesh_solid(leaves[HANDLE].mesh)
        exact = native[CRANK].intersect(native[HANDLE])
        seen.append(sim.time)
        print(json.dumps(dict(time=sim.time, crank=sim.state['crank_rotation'],
                              native_valid=exact.isValid(), native_mm3=exact.Volume(),
                              world64_mm3=faceted_common_volume(common),
                              raw_sum_mm3=common.volume(), bounds=common.bounding_box(),
                              common_vertices=common.to_mesh64().vert_properties[:, :3].tolist(),
                              mesh_bounds={path:leaves[path].mesh.bounds.tolist()
                                           for path in (CRANK,HANDLE)},
                              crank_top_z=sorted(set(leaves[CRANK].mesh.vertices[:, 2]))[-5:],
                              handle_bottom_z=sorted(set(leaves[HANDLE].mesh.vertices[:, 2]))[:5])),
              flush=True)

    sim.every(.1, sample)
    outcomes = replay(sim, 'addition', initial)
    assert len(seen) == 2
    print(json.dumps(dict(kind='finished', samples=len(seen), outcomes=outcomes,
                          wall_seconds=time.monotonic()-started,
                          acceptance='diagnostic only; no overlap waiver or fit')), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
