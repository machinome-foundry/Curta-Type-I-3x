"""Locate the thrust-ring seat before changing spring height or geometry.

Only measuring copies move. No operating run or source part is altered.
All collar contacts are explicitly faceted because the collar is source STL.
"""

import argparse
import json
import logging
import math

from simulation.thrust_seat_trial import ThrustSeatBench, SeatedThrustBench
from simulation.tools.ancestor_lockout_contact import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume
from simulation.tools.interference import world_solids


def probe(section_path=None, seated=False):
    node = SeatedThrustBench() if seated else ThrustSeatBench()
    node.set_state(travel=0, shift=0)
    node.assemble()
    node.build_stls()
    meshes = {name: getattr(node, name).mesh for name in (
        'collar', 'thrust_ring', 'carriage_spring_sleeve', 'spring_sleeve_c_clip')}
    meshes['spring_wire'] = node.carriage_spring.wire.mesh
    solids = {name: mesh_solid(mesh) for name, mesh in meshes.items()}
    native = world_solids(node)
    print(json.dumps({'scope': 'isolated positioning instrument, pose-only ring rise',
                      'seated_candidate': seated,
                      'bounds_mm': {k: v.bounds.tolist() for k, v in meshes.items()},
                      'spring_cap_centres_mm': meshes['spring_wire'].vertices[-2:].tolist(),
                      'native_horizontal_faces': {
                          path: [{'z_mm': f.Center().z, 'normal_z': f.normalAt().z,
                                  'area_mm2': f.Area(),
                                  'xy_bounds_mm': [f.BoundingBox().xmin,
                                                   f.BoundingBox().ymin,
                                                   f.BoundingBox().xmax,
                                                   f.BoundingBox().ymax]}
                                 for f in shape.Faces() if f.geomType() == 'PLANE'
                                 and abs(f.normalAt().z) > .999]
                          for path, shape in native.items()
                          if path in ('Curta.thrust_ring', 'Curta.carriage_spring_sleeve')},
                      'not_adopted': True}), flush=True)
    refusals = []
    rises = (0,) if seated else (0, .5, 1, 2, 3, 4, 5, 6, 7, 7.4, 7.45,
                                7.4775, 7.5, 7.5275, 7.55, 8, 9, 10)
    for rise in rises:
        ring = solids['thrust_ring'].translate((0, 0, rise))
        volume = faceted_common_volume(ring ^ solids['collar'])
        if not math.isfinite(volume) or volume < 0:
            refused = {'ring_rise_mm': rise, 'refused_common_mm3': volume}
            refusals.append(refused)
            print(json.dumps(refused), flush=True)
            continue
        print(json.dumps({'ring_rise_mm': rise, 'collar_common_mm3': volume}), flush=True)
    for pair in (('spring_wire', 'thrust_ring'), ('spring_wire', 'carriage_spring_sleeve'),
                 ('spring_wire', 'collar')):
        common = faceted_common_volume(solids[pair[0]] ^ solids[pair[1]])
        if not math.isfinite(common) or common < 0:
            refused = {'pair': pair, 'refused_common_mm3': common}
            refusals.append(refused)
            print(json.dumps(refused), flush=True)
            continue
        print(json.dumps({'pair': pair, 'common_mm3': common}), flush=True)
    if section_path:
        import matplotlib.pyplot as plt
        figure, axis = plt.subplots(figsize=(7, 10))
        for index, (name, mesh) in enumerate(meshes.items()):
            cut = mesh.section(plane_origin=(0, 0, 0), plane_normal=(0, 1, 0))
            if cut is None:
                continue
            for number, line in enumerate(cut.discrete):
                axis.plot(line[:, 0], line[:, 2], color=f'C{index}',
                          label=name if number == 0 else None)
        title = ('Unadopted seated positioning candidate' if seated
                 else 'Source positioning stack, no correction')
        axis.set(xlim=(8, 22), ylim=(22, 61), aspect='equal',
                 xlabel='World X (mm)', ylabel='World Z (mm)',
                 title=title + ': Y=0 section')
        axis.grid()
        axis.legend()
        figure.tight_layout()
        figure.savefig(section_path, dpi=160)
        plt.close(figure)
    print(json.dumps({'complete': True, 'refused_measurements': refusals}), flush=True)
    return not refusals


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--section')
    parser.add_argument('--seated', action='store_true')
    args = parser.parse_args()
    logging.disable(logging.INFO)
    raise SystemExit(0 if probe(args.section, args.seated) else 1)
