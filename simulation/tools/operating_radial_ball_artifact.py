"""Build the production radial-ball export or its complete-bank Python oracle."""

import argparse
import json
import logging
from pathlib import Path

from machinome.simulation import Sim
from simulation.running import OperatingCurta


def oracle():
    sim = Sim(OperatingCurta(), dt=.1)
    report = {}

    def record(name, status):
        report[name] = dict(status=status, bank=dict(sim.state))

    def move(name, value, duration=None):
        command = sim.move(name, to=value, **({} if duration is None else {'duration': duration}))
        if duration is not None:
            sim.run(duration)
        return command.status

    record('rest', 'rest')
    record('lift', move('carriage_elevation', 6))
    saved = sim.snapshot()
    command = sim.move('crank_rotation', to=90, duration=.5)
    sim.run(.1)
    record('blocked', command.status)
    stopped = sim.snapshot()
    sim.restore(saved)
    command = sim.move('crank_rotation', to=90, duration=.5)
    sim.run(.1)
    assert sim.snapshot() == stopped
    record('replay', command.status)
    record('relief', move('carriage_elevation', 0))
    record('after_relief', move('crank_rotation', 90, .5))
    sim.reset()
    record('outward', move('crank_rotation', 90, .5))
    record('return', move('crank_rotation', 360, 1.5))
    assert report['outward']['bank']['carriage.positioning.p_6mm_ball_419094.slide'] == report['return']['bank']['carriage.positioning.p_6mm_ball_419094.slide']
    print(json.dumps(report, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', type=Path)
    args = parser.parse_args()
    if args.export:
        from machinome.core.export import export_node
        from machinome.simulation.enumeration import bind_declared_defaults
        assert not args.export.exists(), 'preserve earlier artifacts'
        node = OperatingCurta()
        bind_declared_defaults(node)
        manifest = export_node(node, args.export)
        print(json.dumps(dict(path=str(args.export), version=manifest['version'],
                              coordinates=len(manifest['program']['coordinates']))), flush=True)
    else:
        oracle()


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
