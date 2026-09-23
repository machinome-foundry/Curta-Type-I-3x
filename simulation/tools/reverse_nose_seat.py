"""Measure and section the adopted plate at an actual admitted half-turn."""

import argparse
import json
import logging
from pathlib import Path

from machinome.simulation import Sim
from simulation.reverse_nose_seat import ReverseNoseSeatTrial
from simulation.test_reverse_nose_seat import PLATE, DRUM
from simulation.tools.interference import rigid_leaves, world_solids, inventory
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path, required=True)
    args = parser.parse_args()
    sim = Sim(ReverseNoseSeatTrial(), dt=.1, meshes=True)
    rest = inventory(sim.node, world_precision=64)
    command = sim.move('crank_rotation', to=180, duration=1)
    sim.run(1)
    assert command.status == 'completed'
    native = world_solids(sim.node, selected={PLATE, DRUM})
    common = native[PLATE].intersect(native[DRUM])
    assert common.isValid() and common.Volume() == 0
    leaves = dict(rigid_leaves(sim.node))
    overlap = faceted_common_volume(mesh_solid(leaves[PLATE].mesh) ^ mesh_solid(leaves[DRUM].mesh))
    assert overlap == 0
    import matplotlib.pyplot as plt
    figure, axes = plt.subplots(1, 2, figsize=(12, 6))
    for color, (label, path) in enumerate((('plate', PLATE), ('drum', DRUM))):
        cut = leaves[path].mesh.section(plane_origin=(0, 0, 0), plane_normal=(0, 1, 0))
        assert cut is not None
        for axis in axes:
            for index, line in enumerate(cut.discrete):
                axis.plot(line[:, 0], line[:, 2], color=f'C{color}',
                          label=label if index == 0 else None)
    axes[0].set(xlim=(-21, 2), ylim=(-123, -112), title='Original placement and captured slot')
    axes[1].set(xlim=(-9.2, -8.6), ylim=(-119.95, -119.65), title='.05 mm lower-face seat relief')
    for axis in axes:
        axis.set(xlabel='World X (mm)', ylabel='World Z (mm)', aspect='equal')
        axis.grid()
        axis.legend()
    figure.suptitle('Operating reverse-nose seat, actual admitted 180-degree crank turn')
    figure.tight_layout()
    figure.savefig(args.image, dpi=160)
    plt.close(figure)
    print(json.dumps(dict(model='ReverseNoseSeatTrial', production_adopted=True,
                          rest_inventory=rest, crank=sim.state['crank_rotation'],
                          native_mm3=common.Volume(), world64_mm3=overlap,
                          image=str(args.image))), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
