"""Measure complete-bell/ones-lockout contact over both periodic angles.

This is a contact probe, not an adopted restraint or a collision solver.
The source-backed contact bench retains the complete printed bell and
complete ones upper assembly. Positive volume is never discarded.
"""

import argparse
import json
import logging

import manifold3d as manifold

from machinome.simulation import Sim
from simulation.ones_lockout import OnesLockoutBench
from simulation.tools.ancestor_lockout_contact import mesh_solid, contact_shapes
from simulation.tools.interference import rigid_leaves, world_solids

BELL = 'Curta.bell'
LOCKOUT = 'Curta.ones'


def contact_reader(kernel):
    node = OnesLockoutBench()
    node.set_state(shaft_angle=4, crank_angle=0, time=0)
    node.assemble()
    node.build_stls()
    if kernel == 'faceted':
        leaves = dict(rigid_leaves(node))
        bell, lockout = (mesh_solid(leaves[path].mesh) for path in (BELL, LOCKOUT))
    else:
        shapes = world_solids(node, selected={BELL, LOCKOUT})
        bell, lockout = (shapes[path] for path in (BELL, LOCKOUT))

    def at_phase(shaft):
        if kernel == 'faceted':
            fixed = lockout.translate((-40.5, 0, 0)).rotate(
                (0, 0, shaft-4)).translate((40.5, 0, 0))

            def volume(crank):
                common = fixed ^ bell.rotate((0, 0, -crank))
                assert common.status() == manifold.Error.NoError
                return common.volume()
        else:
            fixed = lockout.rotate((40.5, 0, 0), (40.5, 0, 1), shaft-4)

            def volume(crank):
                common = fixed.intersect(bell.rotate((0, 0, 0), (0, 0, 1), -crank))
                assert common.isValid()
                return common.Volume()
        return volume
    return at_phase


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel', choices=('faceted', 'exact'), default='faceted')
    parser.add_argument('--phase-step', type=float, default=2)
    parser.add_argument('--phase', type=float, action='append')
    parser.add_argument('--all-flats', action='store_true',
                        help='Survey a full shaft revolution, not a repeated ideal pentagon.')
    parser.add_argument('--opening-grid', action='store_true',
                        help='Resolve mesh release islands with a quarter-degree opening survey.')
    parser.add_argument('--index-bands', action='store_true')
    parser.add_argument('--operating-index', action='store_true')
    args = parser.parse_args()
    assert 0 < args.phase_step <= 72
    if args.operating_index:
        from simulation.running import OperatingCurta
        from simulation.tools.ancestor_lockout_contact import BELL as FULL_BELL, LOCKOUT as FULL_LOCKOUT
        sim = Sim(OperatingCurta(), dt=.1, meshes=True)
        sim.move('digit_1', to=3)
        sim.move('crank_rotation', to=90)
        request = sim.move('crank_rotation', to=180)
        bell, lockout = contact_shapes(sim.node)
        common = bell.intersect(lockout)
        assert common.isValid()
        leaves = dict(rigid_leaves(sim.node))
        faceted = mesh_solid(leaves[FULL_BELL].mesh) ^ mesh_solid(leaves[FULL_LOCKOUT].mesh)
        assert faceted.status() == manifold.Error.NoError
        print(json.dumps({'operating_request': request.status,
                          'crank': sim.state['crank_rotation'],
                          'shaft': sim.state['transmission.result.ones.turn'],
                          'native_mm3': common.Volume(), 'faceted_mm3': faceted.volume(),
                          'native_solids': [{'volume': solid.Volume(),
                              'centre': solid.Center().toTuple(),
                              'size': [solid.BoundingBox().xlen, solid.BoundingBox().ylen,
                                       solid.BoundingBox().zlen]} for solid in common.Solids()]}), flush=True)
        return
    reader = contact_reader(args.kernel)
    if args.index_bands:
        # The closed circular land bounds the free indexed orientation.
        # Check all five flats independently, rather than assume the fitted
        # source profile is perfectly rotationally symmetric.
        for centre in (4, 76, 148, 220, 292):
            centre_volume = reader(centre)(180)
            if centre_volume > 0:
                print(json.dumps({'kernel': args.kernel, 'index': centre,
                                  'nominal_overlap_mm3': centre_volume,
                                  'bounds': None}), flush=True)
                continue
            bounds = []
            for direction in (-1, 1):
                free, blocked = centre, centre+direction*5
                assert reader(blocked)(180) > 0
                for _ in range(18):
                    mid = (free+blocked)/2
                    if reader(mid)(180) > 0:
                        blocked = mid
                    else:
                        free = mid
                bounds.append({'last_free': free, 'first_contact': blocked})
            print(json.dumps({'kernel': args.kernel, 'index': centre,
                              'bounds': bounds}), flush=True)
        return
    span = 360 if args.all_flats else 72
    phases = args.phase or sorted(
        {4+args.phase_step*i for i in range(int(span/args.phase_step)+1)}
        | {45.6+72*i for i in range(5 if args.all_flats else 1)})
    for shaft in phases:
        volume = reader(shaft)
        cranks = set(range(0, 361, 10))
        if args.opening_grid:
            cranks.update(i/4 for i in range(81))
        samples = [(crank, volume(crank)) for crank in sorted(cranks)]
        boundaries = []
        for (a, va), (b, vb) in zip(samples, samples[1:]):
            if (va > 0) == (vb > 0):
                continue
            left_contact = va > 0
            for _ in range(18):
                mid = (a+b)/2
                if (volume(mid) > 0) == left_contact:
                    a = mid
                else:
                    b = mid
            boundaries.append({'left': a, 'right': b,
                               'enters_contact': not left_contact})
        print(json.dumps({'kernel': args.kernel, 'shaft': shaft,
                          'boundaries': boundaries, 'samples': samples}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
