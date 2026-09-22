"""Inspect the actual clearing-cover/counter-body seat, without posing a bank.

Output is a world Y=0 mesh section of the default operating root;
the independently transformed exact solids supply the contact measurement.
"""

import argparse
import json
import logging
from pathlib import Path

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.interference import world_solids


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    bank = dict(sim.state)
    registers = sim.node.carriage.registers
    paths = {'Curta.carriage.registers.clearing_ring.clearing_cover',
             'Curta.carriage.registers.carrier.upper_carriage_body_1.counter_body'}
    first, second = world_solids(sim.node, selected=paths).values()
    common = first.intersect(second)
    if not common.isValid():
        raise ValueError('Invalid complete-print native intersection')

    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 2, figsize=(12, 6))
    bodies = (('counter body', registers.carrier.upper_carriage_body_1.counter_body),
              ('clearing cover', registers.clearing_ring.clearing_cover))
    for color, (name, node) in enumerate(bodies):
        section = node.mesh.section(plane_origin=(0, 0, 0), plane_normal=(0, 1, 0))
        if section is None:
            raise ValueError(f'Missing Y=0 section for {name}')
        for axis in axes:
            for index, line in enumerate(section.discrete):
                axis.plot(line[:, 0], line[:, 2], color=f'C{color}',
                          label=name if index == 0 else None)
    axes[0].set(xlim=(15, 64), ylim=(23, 59), title='Inner body and outer flange')
    axes[1].set(xlim=(46.4, 49.3), ylim=(43.7, 45.4), title='Outer top seat, enlarged')
    for axis in axes:
        axis.set(xlabel='World X (mm)', ylabel='World Z (mm)', aspect='equal')
        axis.grid()
        axis.legend()
    figure.suptitle(f'Operating counter-body seat; native common {common.Volume():.9f} mm³')
    figure.tight_layout()
    figure.savefig(args.output, dpi=160)
    plt.close(figure)
    if dict(sim.state) != bank:
        raise ValueError('Section inspection changed the retained bank')
    print(json.dumps({'model': 'simulation.running:OperatingCurta',
                      'native_common_mm3': common.Volume(),
                      'coordinates': len(bank), 'bank_unchanged': True,
                      'section': str(args.output)}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
