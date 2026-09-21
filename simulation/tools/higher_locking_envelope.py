"""Measure the complete tens stack and bell at a declared carry position.

Independent pose instruments do not seed or alter an operating run. The first
normal-seat fixture is checked against the independently prepared actual-root
contact before these instruments are used to survey further phases.
"""

import argparse
import json
import logging
from itertools import product

import manifold3d as manifold

from simulation.higher_lockout import HigherLockoutBench
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.interference import rigid_leaves, world_solids

BELL = 'Curta.bell'
STACK = 'Curta.tens.p_10220_410003_1_419227'
CONTACT_PAIRS = {
    'upper_lock': ('results_locking_disc', 'pentagonal_lockout'),
    'lower_lock': ('tens_results_locking_disc', 'pentagonal_lockout'),
    'carry_tooth': ('results_counter_carry_ring', 'transmission_gear_0_6'),
}


def faceted_common_volume(common):
    """Measure spatial volume, recognizing exactly planar boundary contact.

    Manifold can retain coincident triangles whose signed tetrahedron sum
    rounds away from zero. An exactly zero extent proves zero 3D measure;
    no positive thickness or positive volume is discarded by a tolerance.
    Empty commons have inverted infinite bounds and likewise contain no body.
    """
    assert common.status() == manifold.Error.NoError
    bounds = common.bounding_box()
    if any(bounds[axis] >= bounds[axis+3] for axis in range(3)):
        return 0.0
    return common.volume()


def component_shapes(carry, crank, shaft, node_type=HigherLockoutBench):
    """Place native ingredients with the same operations as their complete print."""
    node = node_type()
    node.set_state(shaft_angle=shaft, crank_angle=crank, carry_position=carry, time=0)
    node.assemble()

    def shape_at(parts):
        chain = [node]
        for part in parts:
            chain.append(getattr(chain[-1], part))
        shape = chain[-1].shape()
        for body in reversed(chain):
            for operation in body.operations:
                if hasattr(operation, 'angle'):
                    shape = shape.rotate((0, 0, 0), operation.axis, operation.angle)
                elif hasattr(operation, 'translation'):
                    shape = shape.translate(operation.translation)
                else:
                    raise TypeError(type(operation).__name__)
        return shape

    stack = node.tens.p_10220_410003_1_419227
    bell_parts = {part.name: shape_at(('bell', part.name)) for part in node.bell.children}
    stack_parts = {part.name: shape_at(('tens', stack.name, part.name))
                   for part in stack.children}
    return bell_parts, stack_parts


def component_contacts(carry, crank, shaft, node_type=HigherLockoutBench):
    """Identify native contacting ingredients; never exempt them from a test.

    A FusionNode remains one complete printed body in all acceptance checks.
    This diagnostic only identifies which of its ingredients cause contact.
    """
    bell_parts, stack_parts = component_shapes(carry, crank, shaft, node_type)
    found = []
    for (bell_name, bell), (stack_name, upper) in product(bell_parts.items(), stack_parts.items()):
        common = bell.intersect(upper)
        assert common.isValid()
        if common.Volume() > 0:
            box = common.BoundingBox()
            found.append({'bell': bell_name, 'upper': stack_name,
                          'native_mm3': common.Volume(),
                          'centre': common.Center().toTuple(),
                          'z_range': (box.zmin, box.zmax)})
    return found


def contact_reader(carry=0, reference=140, shaft=169.6, node_type=HigherLockoutBench,
                   *, stack_path=STACK, bell_path=BELL):
    node = node_type()
    node.set_state(shaft_angle=shaft, crank_angle=reference, carry_position=carry, time=0)
    node.assemble()
    node.build_stls()
    native = world_solids(node, selected={bell_path, stack_path})
    leaves = dict(rigid_leaves(node))
    faceted = {path: mesh_solid(leaves[path].mesh) for path in (bell_path, stack_path)}

    def volume(crank, kernel):
        if kernel == 'native':
            common = native[stack_path].intersect(native[bell_path].rotate(
                (0, 0, 0), (0, 0, 1), reference-crank))
            assert common.isValid()
            return common.Volume()
        common = faceted[stack_path] ^ faceted[bell_path].rotate((0, 0, reference-crank))
        return faceted_common_volume(common)
    return volume


def pair_reader(carry, shaft, pair, node_type=HigherLockoutBench):
    bell_parts, stack_parts = component_shapes(carry, 140, shaft, node_type)
    bell_name, stack_name = CONTACT_PAIRS[pair]

    def volume(crank, kernel='native'):
        assert kernel == 'native'
        common = stack_parts[stack_name].intersect(bell_parts[bell_name].rotate(
            (0, 0, 0), (0, 0, 1), 140-crank))
        assert common.isValid()
        return common.Volume()
    return volume


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--carry', type=float, default=0)
    parser.add_argument('--shaft', type=float, default=169.6)
    parser.add_argument('--step', type=float, default=10)
    parser.add_argument('--from-angle', type=float, default=0)
    parser.add_argument('--to-angle', type=float, default=360)
    parser.add_argument('--sample-angle', type=float, action='append', default=[])
    parser.add_argument('--indexed', action='store_true',
                        help='Check all five indexed flats at five axial positions at crank 180.')
    parser.add_argument('--trial', action='store_true',
                        help='Measure the isolated T07 fit, not the production tens stack.')
    parser.add_argument('--components', action='store_true',
                        help='Identify native contacts between ingredients of the complete prints.')
    parser.add_argument('--crank', type=float, default=150,
                        help='Crank pose for --components.')
    parser.add_argument('--pair', choices=CONTACT_PAIRS,
                        help='Survey one identified native ingredient pair; not whole-print acceptance.')
    parser.add_argument('--bands', action='store_true',
                        help='Bracket all five indexed free bands of a locking-disc pair at crank 180.')
    args = parser.parse_args()
    assert 0 <= args.carry <= 1 and 0 < args.step <= 10
    assert 0 <= args.from_angle < args.to_angle <= 360
    assert all(args.from_angle <= angle <= args.to_angle for angle in args.sample_angle)
    node_type = HigherLockoutBench
    if args.trial:
        from simulation.higher_lockout_trial import HigherLockoutFitBench
        node_type = HigherLockoutFitBench
    if args.components:
        print(json.dumps({'carry': args.carry, 'crank': args.crank, 'shaft': args.shaft,
                          'trial': args.trial, 'contacts': component_contacts(
                              args.carry, args.crank, args.shaft, node_type)}), flush=True)
        return
    if args.bands:
        if args.pair not in ('upper_lock', 'lower_lock'):
            parser.error('--bands requires --pair upper_lock or lower_lock')
        for centre in (-16, 56, 128, 200, 272):
            def at(shaft):
                return pair_reader(args.carry, shaft, args.pair, node_type)(180)
            assert at(centre) <= 0, (centre, args.pair)
            bounds = []
            for direction in (-1, 1):
                free, blocked = centre, centre+5*direction
                assert at(blocked) > 0, (blocked, args.pair)
                for _ in range(18):
                    middle = (free+blocked)/2
                    if at(middle) > 0:
                        blocked = middle
                    else:
                        free = middle
                bounds.append({'last_free': free, 'first_contact': blocked})
            print(json.dumps({'pair': args.pair, 'carry': args.carry, 'index': centre,
                              'trial': args.trial, 'bounds': bounds}), flush=True)
        return
    if args.indexed:
        for carry in (0, .25, .5, .75, 1):
            for shaft in (-16, 56, 128, 200, 272):
                volume = contact_reader(carry, reference=180, shaft=shaft, node_type=node_type)
                print(json.dumps({'carry': carry, 'shaft': shaft, 'trial': args.trial,
                                  'native180': volume(180, 'native'),
                                  'faceted180': volume(180, 'faceted')}), flush=True)
        return
    if args.pair:
        volume = pair_reader(args.carry, args.shaft, args.pair, node_type)
    else:
        volume = contact_reader(args.carry, shaft=args.shaft, node_type=node_type)
    for kernel in (('native',) if args.pair else ('native', 'faceted')):
        samples = [(angle, volume(angle, kernel))
                   for angle in sorted({args.from_angle, args.to_angle, *args.sample_angle} | {
                       args.from_angle+args.step*i
                       for i in range(int((args.to_angle-args.from_angle)/args.step)+1)})]
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
                          'pair': args.pair,
                          'samples': samples, 'boundaries': boundaries}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
