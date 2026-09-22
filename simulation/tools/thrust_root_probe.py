"""Check the seated thrust/spring measuring copy against the actual rest root.

No operating model or run bank is changed. Every rigid occurrence plus the
changed spring wire is included; this is not an all-flexible motion audit.
"""

import json
import logging
import math

import numpy as np
from scipy.spatial import cKDTree

from machinome.simulation import Sim
from simulation.thrust_seat_trial import ThrustSeatBench, SeatedThrustBench
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume
from simulation.tools.interference import rigid_leaves


PREFIX = 'Curta.carriage.positioning.'
WIRE = PREFIX + 'carriage_spring.wire'
RING = PREFIX + 'thrust_ring'
COLLAR = 'Curta.carriage.registers.carrier.crank_collar'


def probe():
    from simulation.running import OperatingCurta

    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    bank = dict(sim.state)
    leaves = dict(rigid_leaves(sim.node))
    original = {path: node.mesh for path, node in leaves.items()}
    original[WIRE] = sim.node.carriage.positioning.carriage_spring.wire.mesh
    baseline = ThrustSeatBench()
    baseline.set_state(travel=0, shift=0)
    baseline.assemble()
    baseline.build_stls()
    mappings = {
        COLLAR: baseline.collar.mesh,
        RING: baseline.thrust_ring.mesh,
        WIRE: baseline.carriage_spring.wire.mesh,
        PREFIX + 'carriage_spring_sleeve': baseline.carriage_spring_sleeve.mesh,
        PREFIX + 'spring_sleeve_c_clip': baseline.spring_sleeve_c_clip.mesh,
    }
    distances = {}
    for path, mesh in mappings.items():
        a = np.concatenate((mesh.vertices, mesh.triangles_center))
        b = np.concatenate((original[path].vertices, original[path].triangles_center))
        d = float(max(cKDTree(a).query(b)[0].max(), cKDTree(b).query(a)[0].max()))
        if d > .00001:
            raise ValueError(('Source instrument differs from actual root', path, d))
        distances[path] = d
    candidate = SeatedThrustBench()
    candidate.set_state(travel=0, shift=0)
    candidate.assemble()
    candidate.build_stls()
    trial = dict(original)
    trial[RING] = candidate.thrust_ring.mesh
    trial[WIRE] = candidate.carriage_spring.wire.mesh
    print(json.dumps({'scope': 'two changed measuring meshes against every rigid occurrence',
                      'rigid_occurrences': len(leaves), 'coordinates': len(bank),
                      'source_fixture_distances_mm': distances,
                      'kernel': 'published/source meshes, Manifold',
                      'not_adopted': True}), flush=True)
    for name, meshes in (('original', original), ('candidate', trial)):
        solids, positive, checked = {}, {}, set()
        for first in (RING, WIRE):
            for second in meshes:
                if first == second:
                    continue
                pair = tuple(sorted((first, second)))
                if pair in checked:
                    continue
                checked.add(pair)
                a, b = meshes[first].bounds, meshes[second].bounds
                if not np.all(np.minimum(a[1], b[1]) > np.maximum(a[0], b[0])):
                    continue
                for path in pair:
                    if path not in solids:
                        solids[path] = mesh_solid(meshes[path])
                common = faceted_common_volume(solids[first] ^ solids[second])
                if not math.isfinite(common) or common < 0:
                    raise ValueError((name, pair, common))
                if common > 0:
                    positive[' / '.join(pair)] = common
        print(json.dumps({'case': name, 'pairs_considered': len(checked),
                          'positive_common_mm3': positive}), flush=True)
    assert dict(sim.state) == bank
    print(json.dumps({'complete': True, 'run_bank_unchanged': True}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    probe()
