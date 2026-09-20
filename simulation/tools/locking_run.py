"""Time actual candidate run stages without building or simplifying geometry."""

import json
import logging
import time

from machinome.simulation import Sim
from simulation.result_locking import ResultLocking


def main():
    start = time.monotonic()
    sim = Sim(ResultLocking(), dt=.1, state={'digit': 3, 'crank_height': 0})
    print(json.dumps({'stage': 'construct', 'seconds': time.monotonic()-start}), flush=True)
    for name, value in (('crank_angle', 120), ('digit', 0), ('crank_angle', 150)):
        start = time.monotonic()
        result = sim.move(name, to=value)
        print(json.dumps({'input': name, 'requested': value, 'status': result.status,
                          'crank': sim.state['crank_angle'], 'shaft': sim.state['ones.turn'],
                          'seconds': time.monotonic()-start}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
