"""Locate every residual collar/nut contact; no acceptance tolerance or waiver."""

import argparse
import json
import logging
from pathlib import Path

import numpy as np

from machinome.simulation import Sim
from simulation.operating_collar import OperatingCollarBench
from simulation.cover_fits import mesh_solid as mesh_solid64
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume
from simulation.tools.interference import rigid_leaves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--section', type=Path)
    args = parser.parse_args()
    sim = Sim(OperatingCollarBench(), dt=.1, meshes=True)
    bank = dict(sim.state)
    leaves = dict(rigid_leaves(sim.node))
    carrier = sim.node.carriage.registers.carrier
    solids, checked = {}, set()
    print(json.dumps({'scope': 'unadopted collar trial; all rigid rest neighbours',
                      'rigid_occurrences': len(leaves), 'coordinates': len(bank)}),
          flush=True)
    for changed in (carrier.crank_collar, carrier.crank_collar_nut):
        first = next(path for path, node in leaves.items() if node is changed)
        for second, other in leaves.items():
            pair = tuple(sorted((first, second)))
            if changed is other or pair in checked:
                continue
            checked.add(pair)
            a, b = changed.mesh.bounds, other.mesh.bounds
            if not np.all(np.minimum(a[1], b[1]) >= np.maximum(a[0], b[0])):
                continue
            for precision, make_solid in (('float32', mesh_solid),
                                           ('float64', mesh_solid64)):
                for path in pair:
                    if (precision, path) not in solids:
                        solids[precision, path] = make_solid(leaves[path].mesh)
                common = solids[precision, first] ^ solids[precision, second]
                raw = common.volume()
                if raw != 0:
                    bounds = common.bounding_box()
                    print(json.dumps({'pair': pair, 'precision': precision,
                                      'raw_signed_mm3': raw,
                                      'spatial_mm3': faceted_common_volume(common),
                                      'bounds': bounds,
                                      'extent_mm': [bounds[i + 3] - bounds[i]
                                                    for i in range(3)]}), flush=True)
    if args.section:
        import matplotlib.pyplot as plt

        figure, axes = plt.subplots(1, 2, figsize=(12, 7))
        displayed = (
            ('collar', carrier.crank_collar),
            ('nut', carrier.crank_collar_nut),
            ('washer', carrier.crank_collar_washer),
            ('main body', sim.node.frame.upper_frame.main_body),
            ('spider mount', sim.node.carriage.registers.dial_detents.spider_spring.mount),
            ('left pin', carrier.upper_carriage_body_1.counter_body_pin_1),
            ('right pin', carrier.upper_carriage_body_1.counter_body_pin_2),
        )
        for axis, origin, normal, columns in (
                (axes[0], (0, 0, 0), (0, 1, 0), (0, 2)),
                (axes[1], (0, 0, 48), (0, 0, 1), (0, 1))):
            for part_index, (name, node) in enumerate(displayed):
                section = node.mesh.section(plane_origin=origin, plane_normal=normal)
                if section is not None:
                    for index, line in enumerate(section.discrete):
                        axis.plot(line[:, columns[0]], line[:, columns[1]],
                                  color=f'C{part_index}',
                                  label=name if index == 0 else None)
            axis.set_aspect('equal')
            axis.grid()
            axis.legend(fontsize=8)
        axes[0].set(xlim=(-26, 26), ylim=(5, 68), xlabel='X (mm)',
                    ylabel='Z (mm)', title='Unadopted trial: Y=0 section')
        axes[1].set(xlim=(-25, 25), ylim=(-25, 25), xlabel='X (mm)',
                    ylabel='Y (mm)', title='Pin alignment: Z=48 mm')
        figure.tight_layout()
        figure.savefig(args.section, dpi=160)
        plt.close(figure)
    assert dict(sim.state) == bank
    print(json.dumps({'complete': True, 'pairs_considered': len(checked),
                      'bank_unchanged': True}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
