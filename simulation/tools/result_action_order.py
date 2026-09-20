"""Report actual retained tooth contact after mid-cycle selector requests."""

import json
import logging
from machinome.simulation import Sim
from simulation.result_action_order import ResultActionOrder
from simulation.tools.interference import world_solids


def main():
    logging.disable(logging.INFO)
    node = ResultActionOrder()
    sim = Sim(node, dt=.1, meshes=True)
    drum_path = 'Curta.drum.main_axle_step_drum_bottom_1'
    gear_paths = ('Curta.ones.p_10219_410002_1', 'Curta.ones.p_10221_1',
                  'Curta.tens.p_10230_410008_1_419229',
                  'Curta.tens.p_10220_410003_1_419227')
    selected = {drum_path, 'Curta.bell', *gear_paths}
    sim.move('crank_height', to=0)
    sim.move('digit', to=3)
    commands = [('crank_angle', 90), ('crank_angle', 120), ('digit', 0),
                ('crank_angle', 150), ('digit', 3)]
    commands += [('crank_angle', angle) for angle in range(180, 481, 15)]
    for driver, target in commands:
        command = sim.move(driver, to=target)
        shapes = world_solids(node, selected=selected)
        contacts = {}
        for path in gear_paths:
            for neighbour in (drum_path, 'Curta.bell'):
                common = shapes[path].intersect(shapes[neighbour])
                assert common.isValid()
                if common.Volume() > 0:
                    contacts[f'{path} / {neighbour}'] = common.Volume()
        print(json.dumps({'request': [driver, target], 'status': command.status,
                          'crank': sim.state['crank_angle'], 'digit': sim.state['digit'],
                          'ones_turn': sim.state['ones.turn'],
                          'tens_turn': sim.state['tens.turn'],
                          'contact_mm3': contacts}), flush=True)


if __name__ == '__main__':
    main()
