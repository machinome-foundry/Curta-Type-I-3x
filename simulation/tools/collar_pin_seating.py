"""Check whether collar clocking, rather than material removal, clears its pins.

Only measuring copies rotate. The unchanged operating bank and both source pin
placements remain fixed. Contacts use the collar's source-STL representation.
"""

import argparse
import json
import logging
from pathlib import Path

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--section', type=Path)
    parser.add_argument('--source', action='store_true',
                        help='Reconstruct original collar/pin placements in the independent bench')
    parser.add_argument('--nut-phase', action='store_true',
                        help='Survey the nut about the pin-aligned collar at unchanged height')
    args = parser.parse_args()
    if args.source and args.nut_phase:
        parser.error('--source and --nut-phase are independent surveys')
    sim = None
    if args.source or args.nut_phase:
        from simulation.collar_pin_seat import CollarPinSeat, SourceCollarPinSeat
        bench = (SourceCollarPinSeat() if args.source else
                 CollarPinSeat(nut_angle=-54.282220532))
        bench.assemble()
        bench.build_stls()
        collar_mesh, nut_mesh = bench.collar.mesh, bench.nut.mesh
        pins = [bench.pin_left.mesh, bench.pin_right.mesh]
    else:
        sim = Sim(OperatingCurta(), dt=.1, meshes=True)
        bank = dict(sim.state)
        carrier = sim.node.carriage.registers.carrier
        collar_mesh, nut_mesh = carrier.crank_collar.mesh, carrier.crank_collar_nut.mesh
        pins = [getattr(carrier.upper_carriage_body_1, f'counter_body_pin_{i}').mesh
                for i in (1, 2)]
    collar = mesh_solid(collar_mesh)
    pin_solids = [mesh_solid(pin) for pin in pins]
    print(json.dumps({'scope': 'measuring copies only; no placement mutation',
                      'source_bench': args.source, 'nut_phase_bench': args.nut_phase,
                      'collar_bounds': collar_mesh.bounds.tolist(),
                      'pin_bounds': [pin.bounds.tolist() for pin in pins]}), flush=True)
    if args.nut_phase:
        nut = mesh_solid(nut_mesh)
        for angle in range(0, 361, 5):
            moved = nut.rotate((0, 0, angle))
            print(json.dumps({'nut_yaw_delta_deg': angle,
                              'overlap_mm3': faceted_common_volume(collar ^ moved)}),
                  flush=True)
    else:
        for angle in range(0, 181, 5):
            moved = collar.rotate((0, 0, angle))
            print(json.dumps({'yaw_delta_deg': angle,
                              'pin_overlap_mm3': [faceted_common_volume(moved ^ pin)
                                                  for pin in pin_solids]}), flush=True)
    if args.section:
        import matplotlib.pyplot as plt

        figure, axes = plt.subplots(1, 3, figsize=(13, 5))
        for axis, height in zip(axes, (46.9, 48, 49.4)):
            displayed = [('collar', collar_mesh),
                         *[(f'pin {i}', pin) for i, pin in enumerate(pins, 1)]]
            for part_index, (name, mesh) in enumerate(displayed):
                cut = mesh.section(plane_origin=(0, 0, height),
                                   plane_normal=(0, 0, 1))
                if cut is not None:
                    for index, line in enumerate(cut.discrete):
                        axis.plot(line[:, 0], line[:, 1],
                                  color=f'C{part_index}',
                                  label=name if index == 0 else None)
            axis.set(xlim=(-26, 26), ylim=(-26, 26), aspect='equal',
                     title=f'World Z = {height} mm',
                     xlabel='X (mm)', ylabel='Y (mm)')
            axis.grid()
            axis.legend()
        figure.tight_layout()
        figure.savefig(args.section, dpi=160)
        plt.close(figure)
    if sim is not None:
        assert dict(sim.state) == bank, 'Measurement changed the operating bank'
    print(json.dumps({'complete': True,
                      'bank_unchanged': True if sim is not None else None,
                      'coordinates': len(bank) if sim is not None else None}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
