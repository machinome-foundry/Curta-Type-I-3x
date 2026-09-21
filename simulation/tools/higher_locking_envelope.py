"""Measure the complete tens stack and bell at a declared carry position.

Independent pose instruments do not seed or alter an operating run. The first
normal-seat fixture is checked against the independently prepared actual-root
contact before these instruments are used to survey further phases.
"""

import argparse
import json
import logging

import manifold3d as manifold

from simulation.higher_lockout import HigherLockoutBench
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.interference import rigid_leaves, world_solids

BELL = 'Curta.bell'
STACK = 'Curta.tens.p_10220_410003_1_419227'


def contact_reader(carry=0, reference=140, shaft=169.6, node_type=HigherLockoutBench):
    node = node_type()
    node.set_state(shaft_angle=shaft, crank_angle=reference, carry_position=carry, time=0)
    node.assemble()
    node.build_stls()
    native = world_solids(node, selected={BELL, STACK})
    leaves = dict(rigid_leaves(node))
    faceted = {path: mesh_solid(leaves[path].mesh) for path in (BELL, STACK)}

    def volume(crank, kernel):
        if kernel == 'native':
            common = native[STACK].intersect(native[BELL].rotate(
                (0, 0, 0), (0, 0, 1), reference-crank))
            assert common.isValid()
            return common.Volume()
        common = faceted[STACK] ^ faceted[BELL].rotate((0, 0, reference-crank))
        assert common.status() == manifold.Error.NoError
        return common.volume()
    return volume


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--carry', type=float, default=0)
    parser.add_argument('--shaft', type=float, default=169.6)
    parser.add_argument('--step', type=float, default=10)
    parser.add_argument('--indexed', action='store_true',
                        help='Check all five indexed flats at five axial positions at crank 180.')
    parser.add_argument('--trial', action='store_true',
                        help='Measure the isolated T07 fit, not the production tens stack.')
    args = parser.parse_args()
    assert 0 <= args.carry <= 1 and 0 < args.step <= 10
    node_type = HigherLockoutBench
    if args.trial:
        from simulation.higher_lockout_trial import HigherLockoutFitBench
        node_type = HigherLockoutFitBench
    if args.indexed:
        for carry in (0, .25, .5, .75, 1):
            for shaft in (-16, 56, 128, 200, 272):
                volume = contact_reader(carry, reference=180, shaft=shaft, node_type=node_type)
                print(json.dumps({'carry': carry, 'shaft': shaft, 'trial': args.trial,
                                  'native180': volume(180, 'native'),
                                  'faceted180': volume(180, 'faceted')}), flush=True)
        return
    volume = contact_reader(args.carry, shaft=args.shaft, node_type=node_type)
    for kernel in ('native', 'faceted'):
        samples = [(angle, volume(angle, kernel))
                   for angle in sorted({0., 360.} | {
                       args.step*i for i in range(int(360/args.step)+1)})]
        boundaries = []
        for (left, vl), (right, vr) in zip(samples, samples[1:]):
            if (vl > 0) == (vr > 0):
                continue
            enters = vr > 0
            for _ in range(18):
                middle = (left+right)/2
                if (volume(middle, kernel) > 0) == enters:
                    right = middle
                else:
                    left = middle
            boundaries.append({'left': left, 'right': right, 'enters_contact': enters})
        print(json.dumps({'kernel': kernel, 'shaft': args.shaft, 'carry': args.carry,
                          'trial': args.trial,
                          'samples': samples, 'boundaries': boundaries}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
