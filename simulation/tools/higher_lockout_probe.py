"""Measure a higher result channel after actual mid-turn selector withdrawal.

This deliberately exercises an as-yet-unrestrained action order. It reports
the complete installed upper stack against the complete bell in both kernels;
it neither declares a stop nor copies the fixed-height ones profile.
"""

import argparse
import json
import logging

import manifold3d as manifold
from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.running_parts import CHANNEL_NAMES
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.interference import rigid_leaves, world_solids


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--channel', type=int, choices=range(2, 9), default=2)
    parser.add_argument('--locate', action='store_true',
                        help='Bracket the first closing contact of the prepared retained stack.')
    parser.add_argument('--carry', action='store_true',
                        help='For channel 2, enter 9 then 1 to latch its actual carry before withdrawal.')
    args = parser.parse_args()
    if args.carry and args.channel != 2:
        parser.error('--carry currently measures the first result carry only')
    if args.carry and args.locate:
        parser.error('the carry changes shaft phase during the request; use the '
                     'phase/height envelope, not a frozen-shaft closing bracket')
    channel = CHANNEL_NAMES[args.channel-1]
    # Twenty-degree station spacing is declared by the source drive law.
    withdrawal = 120 + 20*(args.channel-1)
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    if args.carry:
        for input_name, value in (('digit_1', 9), ('crank_rotation', 360), ('digit_1', 1)):
            request = sim.move(input_name, to=value)
            assert request.status == 'completed', (input_name, value, request.status)
        withdrawal += 360
    for input_name, value in ((f'digit_{args.channel}', 3),
                              ('crank_rotation', withdrawal),
                              (f'digit_{args.channel}', 0)):
        request = sim.move(input_name, to=value)
        assert request.status == 'completed', (input_name, value, request.status)
    bell_path = 'Curta.carry_mechanism.tens_bell.tens_bell_1'
    prefix = f'Curta.transmission.result.{channel}.'
    stacks = [path for path, node in rigid_leaves(sim.node)
              if path.startswith(prefix) and path.rsplit('.', 1)[-1].startswith('p_10220_')]
    assert len(stacks) == 1, stacks
    shaft_key = f'transmission.result.{channel}.turn'
    travel_key = stacks[0].removeprefix('Curta.')+'.travel'
    if args.carry:
        assert abs(sim.state[travel_key]) < 1e-8, sim.state[travel_key]
    held = sim.state[shaft_key]
    for target in (withdrawal, withdrawal+30):
        request = sim.move('crank_rotation', to=target)
        solids = world_solids(sim.node, selected={bell_path, stacks[0]})
        native = solids[bell_path].intersect(solids[stacks[0]])
        leaves = dict(rigid_leaves(sim.node))
        faceted = mesh_solid(leaves[bell_path].mesh) ^ mesh_solid(leaves[stacks[0]].mesh)
        assert native.isValid()
        assert faceted.status() == manifold.Error.NoError
        print(json.dumps({'channel': args.channel, 'requested': target,
                          'status': request.status, 'crank': sim.state['crank_rotation'],
                          'prepared_shaft': held, 'shaft': sim.state[shaft_key],
                          'upper_stack_travel': sim.state[travel_key],
                          'native_mm3': native.Volume(), 'faceted_mm3': faceted.volume()}),
              flush=True)
    if args.locate:
        # Pose complete copies for measurement, never the admitted run bank.
        # At the observed endpoint, bell rotation is -target about world Z.
        at = sim.state['crank_rotation']
        bell = solids[bell_path]
        stack = solids[stacks[0]]
        bell_mesh = mesh_solid(leaves[bell_path].mesh)
        stack_mesh = mesh_solid(leaves[stacks[0]].mesh)
        for kernel in ('native', 'faceted'):
            def volume(angle):
                if kernel == 'native':
                    common = stack.intersect(bell.rotate((0, 0, 0), (0, 0, 1), at-angle))
                    assert common.isValid()
                    return common.Volume()
                common = stack_mesh ^ bell_mesh.rotate((0, 0, at-angle))
                assert common.status() == manifold.Error.NoError
                return common.volume()

            free, blocked = withdrawal, withdrawal+30
            assert volume(free) <= 0 and volume(blocked) > 0
            for _ in range(20):
                middle = (free+blocked)/2
                if volume(middle) > 0:
                    blocked = middle
                else:
                    free = middle
            print(json.dumps({'channel': args.channel, 'kernel': kernel,
                              'shaft': sim.state[shaft_key],
                              'upper_stack_travel': sim.state[travel_key],
                              'last_free': free, 'first_contact': blocked}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
