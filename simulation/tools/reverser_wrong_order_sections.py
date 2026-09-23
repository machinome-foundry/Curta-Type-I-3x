"""Native sections of actual requests around the measured axial tooth contact.

This is a diagnostic, not a prescribed restraint or a whole-machine proof.
The retained root receives ordinary crank/reverser requests; no joint or
register is seeded. Each output file must be new.
"""

import argparse
import json
import logging
from pathlib import Path

import cadquery as cq
import matplotlib.pyplot as plt

from simulation.test_running_reverser_wrong_order import (
    DRUM, FIRST_CONTACT, GEAR, commons, prepare,
)
from simulation.tools.interference import world_solids


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--local-trial', action='store_true',
                        help='Inspect the explicitly limited crank-90 constraint experiment')
    args = parser.parse_args()
    for path in (args.image, args.report):
        if path.exists():
            parser.error(f'Preserve existing evidence: {path}')
    if args.local_trial:
        from simulation.reverser_contact_trial import LocalReverserContactTrial
        sim = prepare(LocalReverserContactTrial)
    else:
        sim = prepare()
    prepared = sim.snapshot()
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    records = []
    for axis, offset in zip(axes, (.01, -.01)):
        sim.restore(prepared)
        requested = FIRST_CONTACT+offset
        command = sim.move('reverser_height', to=requested)
        volumes = commons(sim)
        native = world_solids(sim.node, selected={GEAR, DRUM})
        plane = cq.Plane((0, 26.3, 0), (1, 0, 0), (0, -1, 0))
        for path, label, color in ((DRUM, 'Upper drum', 'tab:orange'),
                                   (GEAR, 'Counter ones input', 'tab:blue')):
            section = cq.Workplane(plane).add(native[path]).section().val()
            for index, edge in enumerate(section.Edges()):
                points, _ = edge.sample(80)
                axis.plot([p.x for p in points], [p.z for p in points],
                          color=color, label=label if index == 0 else None)
        axis.set(xlim=(-24.8, -22.6), ylim=(-48.3, -48.1),
                 xlabel='World X (mm)', ylabel='World Z (mm)',
                 title=f'Request {requested:.4f} mm: {command.status}\n'
                       f'Native common {volumes[0]:.9f} mm³')
        axis.grid(alpha=.3)
        axis.legend(fontsize=8)
        records.append(dict(request=requested, status=command.status,
                            bank=dict(sim.state), native_mm3=volumes[0],
                            world64_mm3=volumes[1]))
    fig.suptitle(('Local constraint trial; ' if args.local_trial else '')+
                 'Crank 90°; native section at world Y = 26.3 mm\n'
                 'Axial scale expanded; these are admitted poses, not a clearance claim')
    fig.tight_layout()
    fig.savefig(args.image, dpi=160)
    plt.close(fig)
    args.report.write_text(json.dumps(dict(
        gear=GEAR, drum=DRUM, records=records, local_trial=args.local_trial,
        scope='Two retained requests; sampled contact witness only, no continuous proof',
    ), indent=2)+'\n')
    print(json.dumps(dict(image=str(args.image), report=str(args.report),
                         samples=len(records))), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
