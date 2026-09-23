"""Section the lower grip seat and measure its protected retaining-screw common."""

import argparse
import json
import logging
from pathlib import Path

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.standard.parts import CrankHandle, CrankHandlePinScrew
from simulation.tools.interference import rigid_leaves
from simulation.tools.crank_handle_contact import CRANK, HANDLE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path, required=True)
    args = parser.parse_args()
    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    fitted = sim.node.main_drive.crank.crank_handle_1.crank_handle.shape()
    source = CrankHandle().shape()
    # Source assembly placements, expressed in the grip's source frame.
    pin = CrankHandlePinScrew().shape().rotate((0, 0, 0), (0, 1, 0), 90)
    pin = pin.translate((50.720609937 - 49.319648043, 0, 115.35 - 94.35))
    before, after = source.intersect(pin), fitted.intersect(pin)
    assert before.isValid() and after.isValid()
    removed, added = before.cut(after), after.cut(before)
    assert removed.Volume() == added.Volume() == 0
    leaves = dict(rigid_leaves(sim.node))
    y = 13.025505425 + .337283020
    import matplotlib.pyplot as plt
    figure, axes = plt.subplots(1, 2, figsize=(12, 6))
    for color, (label, path) in enumerate((('crank', CRANK), ('grip', HANDLE))):
        cut = leaves[path].mesh.section(plane_origin=(0, y, 0), plane_normal=(0, 1, 0))
        assert cut is not None
        for axis in axes:
            for index, line in enumerate(cut.discrete):
                axis.plot(line[:, 0], line[:, 2], color=f'C{color}',
                          label=label if index == 0 else None)
    axes[0].set(xlim=(34, 65), ylim=(85, 132), title='Grip and unchanged central shaft')
    axes[1].set(xlim=(54.5, 55.5), ylim=(94.2, 94.7), title='.05 mm lower-face seating gap')
    for axis in axes:
        axis.set(xlabel='World X (mm)', ylabel='World Z (mm)', aspect='equal')
        axis.grid()
        axis.legend()
    figure.suptitle('Operating Curta crank grip: scoped seat section at rest')
    figure.tight_layout()
    figure.savefig(args.image, dpi=160)
    plt.close(figure)
    print(json.dumps(dict(native_source_pin_common_mm3=before.Volume(),
                          native_fitted_pin_common_mm3=after.Volume(),
                          pin_common_removed_mm3=removed.Volume(),
                          pin_common_added_mm3=added.Volume(),
                          image=str(args.image),
                          acceptance='Scoped seat evidence; source pin overlap is not waived')))


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
