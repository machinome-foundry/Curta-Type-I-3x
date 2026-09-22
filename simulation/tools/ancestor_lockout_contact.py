"""Complete-bell contact in the unchanged operating assembly.

Runs the actual wrong-order sequence before measuring its locally retained
ones lockout. OCCT and Manifold each locate a free/contact bracket; no positive
volume is ignored. This is measurement, not a whole-machine collision solver.
"""

import json
import logging
import manifold3d as manifold
import numpy as np

from machinome.simulation import Sim
from simulation.tools.interference import world_solids
from simulation.tools.interference import rigid_leaves

BELL = 'Curta.carry_mechanism.tens_bell.tens_bell_1'
LOCKOUT = 'Curta.transmission.result.ones.p_10221_1'
SHAFT = 'transmission.result.ones.turn'


def prepare(sim):
    for name, value in (('digit_1', 3), ('crank_rotation', 90),
                        ('crank_rotation', 120), ('digit_1', 0)):
        command = sim.move(name, to=value)
        assert command.status == 'completed', (name, value, command.status)
    assert abs(sim.state[SHAFT]-189.6) < 1e-10


def contact_shapes(node):
    shapes = world_solids(node, selected={BELL, LOCKOUT})
    assert set(shapes) == {BELL, LOCKOUT}, set(shapes)
    return shapes[BELL], shapes[LOCKOUT]


def mesh_solid(mesh, *, world_precision=32):
    """Convert placed meshes; use 64 to avoid a second world-float32 rounding."""
    if world_precision == 64:
        result = manifold.Manifold(manifold.Mesh64(
            np.asarray(mesh.vertices, dtype=np.float64),
            np.asarray(mesh.faces, dtype=np.uint64)))
    elif world_precision == 32:
        result = manifold.Manifold(manifold.Mesh(
            np.asarray(mesh.vertices, dtype=np.float32),
            np.asarray(mesh.faces, dtype=np.uint32)))
    else:
        raise ValueError('world_precision must be 32 or 64')
    assert result.status() == manifold.Error.NoError, result.status()
    return result


def measure():
    from simulation.running import OperatingCurta

    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    prepare(sim)
    bell, lockout = contact_shapes(sim.node)
    print(json.dumps({'prepared': {k: sim.state[k] for k in
        ('crank_rotation', 'main_drive.crank.turn', SHAFT)}}), flush=True)
    # Judge the actual published meshes, not a second tessellation of a
    # transformed BREP whose coincident vertices may weld differently.
    leaves = dict(rigid_leaves(sim.node))
    faceted_bell = mesh_solid(leaves[BELL].mesh)
    faceted_lockout = mesh_solid(leaves[LOCKOUT].mesh)

    def volume(crank, faceted=False, phase_offset=0):
        if faceted:
            fixed = faceted_lockout.translate((-40.5, 0, 0)).rotate(
                (0, 0, phase_offset)).translate((40.5, 0, 0))
            common = fixed ^ faceted_bell.rotate((0, 0, 120-crank))
            assert common.status() == manifold.Error.NoError
            return common.volume()
        fixed = lockout.rotate((40.5, 0, 0), (40.5, 0, 1), phase_offset)
        common = fixed.intersect(bell.rotate((0, 0, 0), (0, 0, 1), 120-crank))
        assert common.isValid()
        return common.Volume()

    for faceted in (False, True):
        for offset in (0, -.001, .001):
            free, blocked = 120., 150.
            assert volume(free, faceted, offset) <= 0
            assert volume(blocked, faceted, offset) > 0
            for _ in range(20):
                mid = (free+blocked)/2
                if volume(mid, faceted, offset) > 0:
                    blocked = mid
                else:
                    free = mid
            print(json.dumps({'kernel': 'Manifold' if faceted else 'OCCT',
                'shaft': 189.6+offset, 'last_free': free, 'first_contact': blocked,
                'at_150_mm3': volume(150, faceted, offset),
                'samples': {str(angle): volume(angle, faceted, offset)
                            for angle in (120, 122, 124, 125, 125.3, 125.32, 125.33, 125.34, 126, 130, 140, 150)}}), flush=True)
    result = sim.move('crank_rotation', to=150)
    actual_bell, actual_lockout = contact_shapes(sim.node)
    common = actual_bell.intersect(actual_lockout)
    assert common.isValid() and common.Volume() > 0
    assert result.status == 'completed'
    print(json.dumps({'unconstrained_request': result.status,
                      'actual_endpoint_overlap_mm3': common.Volume(),
                      'shaft': sim.state[SHAFT]}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    measure()
