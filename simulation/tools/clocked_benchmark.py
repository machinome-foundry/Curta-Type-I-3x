"""Finite, reproducible request timings; optionally compare the running twin."""

import argparse
import json
from statistics import median
from time import perf_counter


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--running', action='store_true')
    parser.add_argument('--samples', type=int, default=20)
    args = parser.parse_args()
    if args.samples < 1:
        parser.error('--samples must be positive')
    start = perf_counter()
    import solid_node
    from solid_node.simulation import Sim
    from simulation.clocked import ClockedCurta, register_reading
    report = {'framework_module': solid_node.__file__, 'import_seconds': perf_counter() - start}
    start = perf_counter()
    sim = Sim(ClockedCurta())
    report['construct_seconds'] = perf_counter() - start
    sim.move('digit_1', to=9)
    costs = []
    for _ in range(args.samples):
        start = perf_counter()
        sim.move('crank_rotation', by=360)
        costs.append(perf_counter() - start)
    report['clocked_stroke_median_seconds'] = median(costs)
    report['clocked_stroke_samples_seconds'] = costs
    report['readout'] = [register_reading(sim), register_reading(sim, True)]
    assert report['readout'] == [9 * args.samples, args.samples]
    sim.reset()
    sim.move('digit_1', to=9)
    start = perf_counter()
    for _ in range(20):
        sim.move('crank_rotation', by=18)
    report['clocked_stroke_with_20_poses_seconds'] = perf_counter() - start
    assert (register_reading(sim), register_reading(sim, True)) == (9, 1)
    if args.running:
        from simulation.running import OperatingCurta, register_reading as running_reading
        start = perf_counter()
        running = Sim(OperatingCurta(), dt=.1)
        report['running_construct_seconds'] = perf_counter() - start
        running.move('digit_1', to=9)
        start = perf_counter()
        running.move('crank_rotation', by=360, duration=2)
        running.run(2)
        report['running_stroke_seconds'] = perf_counter() - start
        assert (running_reading(running), running_reading(running, True)) == (9, 1)
        report['stroke_speedup'] = report['running_stroke_seconds'] / median(costs)
        report['same_pose_count_speedup'] = (
            report['running_stroke_seconds'] / report['clocked_stroke_with_20_poses_seconds'])
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
