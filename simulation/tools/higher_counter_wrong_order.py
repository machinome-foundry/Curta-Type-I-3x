"""Observe counter-tens input withdrawal through actual operating requests.

This is a diagnostic, not a control macro or a passing restraint test. It
changes no declaration or register state, and stops on an unexpected refusal
instead of repairing the preparation. The full retained bank and complete
upper/bell contacts accompany each observed request.
"""

import json
import logging
import math

SHAFT = 'transmission.turns.tens.turn'
UPPER = 'Curta.transmission.turns.tens.p_10220_410003_1_419081'
BELL = 'Curta.carry_mechanism.tens_bell.tens_bell_1'
REQUESTS = (
    ('crank_elevation', 9), ('reverser_height', -4.9425),
    ('crank_rotation', 90), ('crank_rotation', 180),
    ('crank_rotation', 190), ('reverser_height', -6.9425),
    ('crank_rotation', 200),
)


def pair_contacts(sim):
    from simulation.tools.interference import world_solids, rigid_leaves
    from simulation.tools.ancestor_lockout_contact import mesh_solid
    from simulation.tools.higher_locking_envelope import faceted_common_volume

    shapes = world_solids(sim.node, selected={UPPER, BELL})
    common = shapes[UPPER].intersect(shapes[BELL])
    if not common.isValid():
        raise ValueError('Invalid counter-tens native common')
    leaves = dict(rigid_leaves(sim.node))
    values = {
        'native': common.Volume(),
        'faceted': faceted_common_volume(
            mesh_solid(leaves[UPPER].mesh) ^ mesh_solid(leaves[BELL].mesh)),
    }
    if any(not math.isfinite(value) or value < 0 for value in values.values()):
        raise ValueError(f'Invalid counter-tens contact measurement: {values}')
    return values


def withdrawal_trace(sim, *, contacts=pair_contacts):
    for index, (name, value) in enumerate(REQUESTS):
        request = sim.move(name, to=value)
        yield {'input': name, 'target': value, 'status': request.status,
               'crank': sim.state['crank_rotation'], 'shaft': sim.state[SHAFT],
               'common_mm3': contacts(sim), 'bank': dict(sim.state),
               'stops': [{'coordinate': stop.coordinate, 'bound': stop.bound}
                         for stop in sim.stops]}
        if index < len(REQUESTS)-1 and request.status != 'completed':
            return


def main():
    from machinome.simulation import Sim
    from simulation.running import OperatingCurta

    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    print(json.dumps({'model': 'simulation.running:OperatingCurta',
                      'coordinates': len(sim.state), 'acceptance': 'diagnostic-only'}), flush=True)
    rows = []
    for row in withdrawal_trace(sim):
        rows.append(row)
        print(json.dumps(row), flush=True)
    print(json.dumps({'complete': True, 'sequence_completed': len(rows) == len(REQUESTS),
                      'final_request_status': rows[-1]['status']}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
