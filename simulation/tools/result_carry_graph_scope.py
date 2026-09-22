"""Locate the first additional result station that changes an earlier carry.

This CAD-free diagnostic keeps the original physical requests and production
laws. It activates progressively more source stations in the existing reduction;
it is not an operating model or a workaround for a failed full-bank request.
"""

import argparse
from functools import reduce
import hashlib
import json
from operator import and_
from pathlib import Path
import time

from machinome.simulation import Sim
from simulation.carry_constraint_repro import CarryConstraintRepro
from simulation.result_carry_graph_repro import SourceRestLever
from simulation.running_laws import lever_motion, shaft_motion
from simulation.running_parts import RESULT_RESTS


def result_graph(active_stations):
    """Keep all source dials, enabling shaft/lever laws at stations 3..N."""
    if not 2 <= active_stations <= 11:
        raise ValueError('active_stations must be between 2 and 11')

    class PartialResultGraph(CarryConstraintRepro):
        for _index in range(2, active_stations):
            _rest = RESULT_RESTS[_index - 1]
            _lever = SourceRestLever(rest=_rest)
            locals()[f'lever_{_index}'] = _lever
            (CarryConstraintRepro.crank.turn & CarryConstraintRepro.height
             & CarryConstraintRepro.zero_setting & _lever.travel).drives(
                getattr(CarryConstraintRepro, f'shaft_{_index}').turn,
                law=shaft_motion(_index, lever_rest=_rest))
            reduce(and_, (CarryConstraintRepro.crank.turn,
                          CarryConstraintRepro.carriage_turn,
                          CarryConstraintRepro.carriage_lift, _lever.travel,
                          *(getattr(CarryConstraintRepro, f'wheel_{i}').turn
                            for i in range(11)))).drives(
                _lever.travel, law=lever_motion(_index, _rest))
        if active_stations > 2:
            del _index, _rest, _lever

    return PartialResultGraph


def measure(active_stations):
    start = time.monotonic()
    sim = Sim(result_graph(active_stations)(), dt=.1)
    requests = []
    for name, target in (('digit', 0), ('height', 9),
                         ('crank_angle', 90), ('crank_angle', 180)):
        command = sim.move(name, to=target)
        requests.append({'input': name, 'target': target,
                         'status': command.status, 'admitted': command.admitted})
    return {'active_result_stations': active_stations,
            'elapsed_s': time.monotonic() - start,
            'requests': requests, 'bank': dict(sim.state),
            # Nine direct 72-degree tooth throws, one carried throw, -16 datum.
            'expected_tens_turn': -16 + 9 * 72 + 72,
            'actual_tens_turn': sim.state['tens.turn']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stations', type=int, choices=range(2, 12),
                        action='append')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    sources = ('tools/result_carry_graph_scope.py', 'carry_constraint_repro.py',
               'result_carry_graph_repro.py', 'running_laws.py', 'running_parts.py')
    print(json.dumps({'scope': 'diagnostic, not operating acceptance',
                      'source_sha256': {name: hashlib.sha256(
                          (root / name).read_bytes()).hexdigest()
                          for name in sources}}), flush=True)
    for stations in args.stations or range(2, 12):
        print(json.dumps(measure(stations)), flush=True)
    print(json.dumps({'complete': True}), flush=True)


if __name__ == '__main__':
    main()
