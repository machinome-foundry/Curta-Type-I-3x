"""Observe counter-ones withdrawal using only actual operating requests.

This diagnostic changes no model declaration. It reports whole upper/bell and
all six lower-input/both-drum contacts before interpreting a missing restraint.
It is not a whole-machine interference certificate.
"""

import json
import logging

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.interference import world_solids, rigid_leaves
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


SHAFT = 'transmission.turns.ones.turn'
UPPER = 'Curta.transmission.turns.ones.p_10222_1'
BELL = 'Curta.carry_mechanism.tens_bell.tens_bell_1'
DRUMS = tuple('Curta.main_drive.stepped_drum.main_axle_step_drum_1.'+name
              for name in ('main_axle_step_drum_top_1', 'main_axle_step_drum_bottom_1'))
LOWERS = tuple('Curta.transmission.turns.'+name+'.'+member for name, member in (
    ('ones', 'p_10218_1'), ('tens', 'p_10230_410008_1_419080'),
    ('hundreds', 'p_10230_410008_1_419068'), ('digit_4', 'p_10230_410008_1_419182'),
    ('digit_5', 'p_10230_410008_1_419105'), ('digit_6', 'p_10230_410008_1_419237')))


def contact_evidence(sim, label):
    selected = {UPPER, BELL, *LOWERS, *DRUMS}
    native = world_solids(sim.node, selected=selected)
    leaves = dict(rigid_leaves(sim.node))
    assert selected <= native.keys(), selected-native.keys()
    mesh = {path: mesh_solid(leaves[path].mesh) for path in selected}
    contacts = []
    pairs = ((UPPER, BELL), *((lower, drum) for lower in LOWERS for drum in DRUMS))
    for first, second in pairs:
        common = native[first].intersect(native[second])
        assert common.isValid(), (first, second)
        contacts.append({'pair': (first, second), 'native': common.Volume(),
                         'faceted': faceted_common_volume(mesh[first] ^ mesh[second])})
    return {'label': label, 'crank': sim.state['crank_rotation'],
            'knob': sim.state['reverser_height'], 'shaft': sim.state[SHAFT],
            'contacts': contacts}


def prepare_partial_turn(sim, *, report=False):
    """Physical test setup only: no register seeds or model-state overrides."""
    for name, value in (('crank_elevation', 9), ('reverser_height', -4.9425),
                        ('crank_rotation', 90), ('crank_rotation', 160),
                        ('crank_rotation', 170)):
        command = sim.move(name, to=value)
        if report:
            print(json.dumps({'input': name, 'target': value, 'status': command.status,
                              'shaft': sim.state[SHAFT]}), flush=True)
        assert command.status == 'completed', (name, value, command.status)


def measure():
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    print('constructed', flush=True)
    prepare_partial_turn(sim, report=True)
    print(json.dumps(contact_evidence(sim, 'before lever withdrawal')), flush=True)
    for step in range(1, 11):
        command = sim.move('reverser_height', to=-4.9425-.2*step)
        assert command.status == 'completed', command.status
        print(json.dumps(contact_evidence(sim, f'lever withdrawal {step}')), flush=True)
    command = sim.move('crank_rotation', to=180)
    print(json.dumps({'final_request_status': command.status}), flush=True)
    print(json.dumps(contact_evidence(sim, 'after wrong-order crank request')), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    measure()
