"""Progress and committed-state evidence for the full calibration run."""

import faulthandler
import argparse
from time import monotonic

from solid_node.simulation import Sim
from simulation.running import OperatingCurta, register_reading


def probe(ticks=None):
    faulthandler.dump_traceback_later(60, repeat=True)
    started = monotonic()
    sim = Sim(OperatingCurta(), dt=.1)
    print('constructed', monotonic() - started, flush=True)
    for units, tens, expected in ((0, 0, 0), (1, 0, 1), (9, 0, 10), (0, 9, 100)):
        sim.move('digit_1', to=units)
        sim.move('digit_2', to=tens)
        command = sim.move('crank_rotation', by=360, duration=2)
        print('input', units, tens, 'target reading', expected, flush=True)
        for _ in range(20):
            before = monotonic()
            try:
                sim.run(.1)
            except BaseException:
                print('uncommitted tick after', sim.tick, sim.state, flush=True)
                raise
            print('tick', sim.tick, 'seconds', monotonic() - before,
                  'result', register_reading(sim), 'counter', register_reading(sim, True),
                  flush=True)
            if ticks is not None and sim.tick >= ticks:
                faulthandler.cancel_dump_traceback_later()
                return
        assert command.status == 'completed', command.status
        assert register_reading(sim) == expected, sim.snapshot()
    faulthandler.cancel_dump_traceback_later()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ticks', type=int, help='stop after this many ticks (timing probe only)')
    arguments = parser.parse_args()
    if arguments.ticks is not None and arguments.ticks <= 0:
        parser.error('--ticks must be positive')
    probe(arguments.ticks)
