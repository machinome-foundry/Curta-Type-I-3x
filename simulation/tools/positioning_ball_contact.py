"""Measure the source positioning ball's pocket and missing-following hypothesis.

Only copies of measured shapes move. This is not an adopted motion law.
"""

import argparse
import json
import logging
from pathlib import Path

from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.tools.interference import rigid_leaves, world_solids
from simulation.tools.crank_drum_contact import bounds
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume

BALL = 'Curta.carriage.positioning.p_6mm_ball_419094'
BELL = 'Curta.carry_mechanism.tens_bell.tens_bell_1'
DRUM = 'Curta.main_drive.stepped_drum.main_axle_step_drum_1.main_axle_step_drum_top_1'
COLLAR = 'Curta.carriage.registers.carrier.crank_collar'
FRAME = 'Curta.frame.upper_frame.main_body'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--section', required=True, type=Path)
    parser.add_argument('--actual-quarter-turn', action='store_true',
                        help='First admit a 90-degree crank request on the actual operating root')
    parser.add_argument('--orbit-trial', action='store_true',
                        help='Use the explicitly rejected whole-machine orbit candidate')
    parser.add_argument('--radial-sweep', action='store_true',
                        help='Measure outward translations of ball copies, without adopting a law')
    args = parser.parse_args()
    if args.orbit_trial:
        from simulation.positioning_ball_trial import OrbitingBallTrial
        model = OrbitingBallTrial
    else:
        model = OperatingCurta
    sim = Sim(model(), dt=.1, meshes=True)
    if args.actual_quarter_turn:
        command = sim.move('crank_rotation', by=90, duration=.5)
        sim.run(.5)
        assert command.status == 'completed'
    initial = dict(sim.state)
    leaves = dict(rigid_leaves(sim.node))
    names = (BALL, BELL, DRUM, COLLAR, FRAME)
    assert all(name in leaves for name in names)
    native = world_solids(sim.node, selected=set(names))
    meshes = {name: leaves[name].mesh for name in names}
    facets = {name: mesh_solid(mesh) for name, mesh in meshes.items()}
    report = {'scope': 'read-only source pocket and copied-shape motion measurements',
              'actual_base_crank_angle': sim.state['crank_rotation'],
              'model': model.__name__,
              'parts': {}, 'samples': []}
    for name, shape in native.items():
        report['parts'][name] = {'bounds': bounds(shape), 'volume': shape.Volume(),
            'pocket_circles': [{'radius': edge.radius(), 'center': edge.arcCenter().toTuple()}
                               for edge in shape.Edges() if edge.geomType() == 'CIRCLE'
                               and 24 < edge.arcCenter().z < 36]}
    for angle in (0, 18, 90, 180, 270, 360):
        for lift in (0, 9):
            moving = {BELL: native[BELL].rotate((0, 0, 0), (0, 0, 1), -angle),
                      DRUM: native[DRUM].rotate((0, 0, 0), (0, 0, 1), -angle).translate((0, 0, lift)),
                      FRAME: native[FRAME]}
            mesh_moving = {BELL: facets[BELL].rotate((0, 0, -angle)),
                           DRUM: facets[DRUM].rotate((0, 0, -angle)).translate((0, 0, lift)),
                           COLLAR: facets[COLLAR], FRAME: facets[FRAME]}
            variants = ((False, offset) for offset in (0, 1, 2, 2.125, 2.15, 2.2, 2.25, 2.5, 3)) if args.radial_sweep else ((False, 0), (True, 0))
            for follows, offset in variants:
                ball = native[BALL].rotate((0, 0, 0), (0, 0, 1), -angle if follows else 0)
                ball_mesh = facets[BALL].rotate((0, 0, -angle if follows else 0))
                ball = ball.translate((offset, 0, 0))
                ball_mesh = ball_mesh.translate((offset, 0, 0))
                row = {'angle': angle, 'drum_lift': lift, 'ball_follows_bell': follows,
                       'radial_offset': offset,
                       'native_mm3': {}, 'world64_mm3': {}, 'refusals': {}}
                for name, other in moving.items():
                    common = ball.intersect(other)
                    if not common.isValid():
                        row['refusals'][name] = 'invalid native common'
                    else:
                        row['native_mm3'][name] = common.Volume()
                for name, other in mesh_moving.items():
                    row['world64_mm3'][name] = faceted_common_volume(ball_mesh ^ other)
                report['samples'].append(row)
    import matplotlib.pyplot as plt
    figure, axes = plt.subplots(1, 2, figsize=(13, 7))
    for color, (name, mesh) in enumerate(meshes.items()):
        for axis, origin, normal, indices in (
                (axes[0], (0, 0, 0), (0, 1, 0), (0, 2)),
                (axes[1], (0, 0, 30), (0, 0, 1), (0, 1))):
            cut = mesh.section(plane_origin=origin, plane_normal=normal)
            if cut is not None:
                for index, line in enumerate(cut.discrete):
                    axis.plot(line[:, indices[0]], line[:, indices[1]], color=f'C{color}',
                              label=name.rsplit('.', 1)[-1] if index == 0 else None)
    axes[0].set(xlim=(-18, 18), ylim=(20, 40), title='Y=0: axial seats')
    axes[1].set(xlim=(-18, 18), ylim=(-18, 18), title='Z=30: radial ball pocket')
    for axis in axes:
        axis.set_aspect('equal')
        axis.grid()
        axis.legend()
    figure.tight_layout()
    figure.savefig(args.section, dpi=160)
    plt.close(figure)
    assert dict(sim.state) == initial
    report.update(bank_unchanged=True, coordinates=len(initial), image=str(args.section))
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
