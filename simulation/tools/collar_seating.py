"""Measure collar seating without changing the operating model or its bank.

Run with --section _build_checks/collar-seating.png for a world X/Z section.
All rises are diagnostic translations of the measuring solid only. Every
other rigid occurrence is checked; positive volumes are never thresholded.
The collar is the author's STL, so this probe is explicitly faceted.
"""

import argparse
import hashlib
import json
import logging
import math
from pathlib import Path

import numpy as np

from machinome.simulation import Sim
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume
from simulation.tools.interference import rigid_leaves


COLLAR = 'Curta.carriage.registers.carrier.crank_collar'
RISES = (0, .25, .5, .65, .7, .75, 1, 1.5, 2)
SECTION_PATHS = {
    'collar': COLLAR,
    'thrust ring': 'Curta.carriage.positioning.thrust_ring',
    'spider mount': 'Curta.carriage.registers.dial_detents.spider_spring.mount',
    'nut': 'Curta.carriage.registers.carrier.crank_collar_nut',
    'washer': 'Curta.carriage.registers.carrier.crank_collar_washer',
    'carrier': 'Curta.carriage.registers.carrier.upper_carriage_body_1.counter_body',
    'cover': 'Curta.carriage.registers.clearing_ring.clearing_cover',
}


def section(meshes, output):
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 2, figsize=(14, 8))
    for index, (name, path) in enumerate(SECTION_PATHS.items()):
        cut = meshes[path].section(plane_origin=(0, 0, 0),
                                   plane_normal=(0, 1, 0))
        if cut is None:
            continue
        for axis in axes:
            for number, line in enumerate(cut.discrete):
                axis.plot(line[:, 0], line[:, 2], color=f'C{index}',
                          label=name if number == 0 else None)
    axes[0].set(xlim=(0, 34), ylim=(5, 69), title='Whole collar stack')
    axes[1].set(xlim=(12, 30), ylim=(42, 50), title='Spider mounting seat')
    for axis in axes:
        axis.set(xlabel='World X (mm)', ylabel='World Z (mm)', aspect='equal')
        axis.grid()
    axes[0].legend()
    figure.suptitle('Unchanged OperatingCurta initial state; Y = 0 section')
    figure.tight_layout()
    figure.savefig(output, dpi=160)
    plt.close(figure)


def source_sections(output):
    """Compare source profiles only; invalid STEP facets are not contact proof."""
    import matplotlib.pyplot as plt
    from simulation.standard.parts import CrankCollar as StepCollar
    from simulation.print_parts import CrankCollar as PrintCollar

    figure, axes = plt.subplots(1, 2, figsize=(14, 8))
    readings = {}
    for color, (name, cls, style) in enumerate((
            ('source STL', PrintCollar, '-'),
            ('source STEP tessellation', StepCollar, '--'))):
        node = cls()
        node.assemble()
        node.build_stls()
        mesh = node.mesh
        readings[name] = {'local_bounds_mm': mesh.bounds.tolist(),
                          'watertight': bool(mesh.is_watertight),
                          'mesh_volume_mm3': float(mesh.volume)}
        cut = mesh.section(plane_origin=(0, 0, 0), plane_normal=(0, 1, 0))
        if cut is None:
            raise ValueError(f'No source section: {name}')
        for axis in axes:
            for index, line in enumerate(cut.discrete):
                axis.plot(line[:, 0], line[:, 2], style, color=f'C{color}',
                          label=name if index == 0 else None)
    axes[0].set(xlim=(0, 30), ylim=(-1, 60), title='Whole source collar')
    axes[1].set(xlim=(11, 26), ylim=(14, 43), title='Internal and spider seats')
    for axis in axes:
        axis.set(xlabel='Local X (mm)', ylabel='Local Z (mm)', aspect='equal')
        axis.grid()
        axis.legend()
    figure.suptitle('Source representation comparison, not valid-solid acceptance')
    figure.tight_layout()
    figure.savefig(output, dpi=160)
    plt.close(figure)
    print(json.dumps({'source_sections': readings}), flush=True)


def probe(rises=RISES, section_path=None):
    from simulation.running import OperatingCurta

    sim = Sim(OperatingCurta(), dt=.1, meshes=True)
    initial_bank = dict(sim.state)
    leaves = dict(rigid_leaves(sim.node))
    meshes = {path: node.mesh for path, node in leaves.items()}
    bounds = {path: mesh.bounds for path, mesh in meshes.items()}
    collar = mesh_solid(meshes[COLLAR])
    solids = {}
    source = Path(leaves[COLLAR].stl_source)
    print(json.dumps({
        'scope': 'pose-only collar translation against every other rigid occurrence',
        'model': 'simulation.running:OperatingCurta',
        'coordinates': len(initial_bank), 'rigid_occurrences': len(leaves),
        'kernel': 'source-STL/published-mesh Manifold', 'not_adopted': True,
        'collar_source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'section_parts_world_bounds_mm': {
            name: bounds[path].tolist() for name, path in SECTION_PATHS.items()},
    }), flush=True)
    for rise in rises:
        moved = collar.translate((0, 0, rise))
        moved_bounds = bounds[COLLAR] + np.array((0, 0, rise))
        positive = {}
        for path in meshes:
            if path == COLLAR:
                continue
            other = bounds[path]
            if not np.all(np.minimum(moved_bounds[1], other[1]) >
                          np.maximum(moved_bounds[0], other[0])):
                continue
            if path not in solids:
                solids[path] = mesh_solid(meshes[path])
            volume = faceted_common_volume(moved ^ solids[path])
            if not math.isfinite(volume) or volume < 0:
                raise ValueError((rise, path, volume))
            if volume > 0:
                positive[path] = volume
        print(json.dumps({'rise_mm': rise, 'positive_contacts_mm3': positive}),
              flush=True)
    if section_path is not None:
        section(meshes, section_path)
    assert dict(sim.state) == initial_bank, 'Measurement changed the run bank'
    print(json.dumps({'complete': True, 'all_rises_measured': len(rises),
                      'run_bank_unchanged': True}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rise', type=float, action='append')
    parser.add_argument('--section', type=Path)
    parser.add_argument('--source-sections', type=Path,
                        help='Compare source representations instead of the assembly')
    args = parser.parse_args()
    if args.rise is not None and not all(math.isfinite(x) for x in args.rise):
        parser.error('--rise must be finite')
    logging.disable(logging.INFO)
    if args.source_sections is not None:
        if args.rise is not None or args.section is not None:
            parser.error('--source-sections cannot be combined with assembly options')
        source_sections(args.source_sections)
    else:
        probe(RISES if args.rise is None else args.rise, args.section)
