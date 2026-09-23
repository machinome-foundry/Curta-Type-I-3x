"""Localize unchanged carry-slider/guide contacts; no fitted geometry or waiver."""

import argparse
import json
import logging
from pathlib import Path
from time import monotonic

import cadquery as cq
import matplotlib.pyplot as plt

from machinome.exact import intersect_shapes
from simulation.carry_bank_frame import FittedCarryBankFrameBench
from simulation.cover_fits import mesh_solid
from simulation.tools.higher_locking_envelope import faceted_common_volume
from simulation.tools.interference import world_solids


def bounds(shape):
    box = shape.BoundingBox()
    return {name: getattr(box, name) for name in
            ('xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path, required=True)
    parser.add_argument('--section-y', type=float,
                        help='Station-frame section plane; default is guide mid-plane')
    parser.add_argument('--z-range', type=float, nargs=2, metavar=('MIN', 'MAX'),
                        help='Optional section zoom, without changing the measured solids')
    parser.add_argument('--horizontal-z', type=float,
                        help='Inspect the transverse guide profile at this world Z')
    args = parser.parse_args()
    if args.horizontal_z is not None and (args.section_y is not None or args.z_range):
        parser.error('Horizontal sections cannot be combined with longitudinal options')
    if args.image.exists():
        parser.error('Choose a fresh image path; existing evidence is preserved')
    started = monotonic()
    root = FittedCarryBankFrameBench()
    root.set_state(drop_mm=0)
    root.assemble()
    root.build_stls()
    figure, axes = plt.subplots(2, 3, figsize=(16, 10))
    rows = []
    for row_index, (group, lever, slider, angle) in enumerate((
            ('result_carries', 'results_tens_lever_assembly_1',
             'tens_slider_for_results', 0),
            ('turns_carries', 'turns_tens_lever_assembly_1',
             'tens_slider_for_turns_counter', -130))):
        node = getattr(getattr(root, group), lever)
        prefix = 'Curta.' + group + '.' + lever + '.'
        names = (prefix + slider, prefix + 'tens_slide_bearing')
        for column, drop in enumerate((0, 2.1, 4.2)):
            root.set_state(drop_mm=drop)
            shapes = world_solids(root, selected=set(names))
            body, guide = (shapes[name] for name in names)
            measured = dict(station=group + '.' + lever, drop_mm=drop,
                            frame_rotation_degrees=angle)
            common = None
            try:
                common = intersect_shapes(body, guide, *names)
                measured['native_mm3'] = common.Volume()
                measured['common_world_bounds'] = bounds(common) if common.Solids() else None
            except RuntimeError as error:
                measured['native_refusal'] = str(error)
            measured['world64_mm3'] = faceted_common_volume(
                mesh_solid(getattr(node, slider).mesh) ^ mesh_solid(node.tens_slide_bearing.mesh))
            body = body.rotate((0, 0, 0), (0, 0, 1), angle)
            guide = guide.rotate((0, 0, 0), (0, 0, 1), angle)
            if common is not None and common.Solids():
                common = common.rotate((0, 0, 0), (0, 0, 1), angle)
                measured['common_station_bounds'] = bounds(common)
            measured['slider_station_bounds'] = bounds(body)
            measured['guide_station_bounds'] = bounds(guide)
            print(json.dumps(measured), flush=True)
            rows.append(measured)
            guide_box = guide.BoundingBox()
            y = ((guide_box.ymin + guide_box.ymax) / 2
                 if args.section_y is None else args.section_y)
            # Station-frame longitudinal section: X horizontal, Z vertical.
            plane = (cq.Plane((0, y, 0), (1, 0, 0), (0, -1, 0))
                     if args.horizontal_z is None else
                     cq.Plane((0, 0, args.horizontal_z), (1, 0, 0), (0, 0, 1)))
            axis = axes[row_index, column]
            for label, shape, color, width in (
                    ('unchanged guide', guide, 'tab:green', 1.8),
                    ('unchanged slider', body, 'tab:blue', 1.5),
                    ('native positive common', common, 'tab:red', 2.5)):
                if shape is None or not shape.Solids():
                    continue
                section = cq.Workplane(plane).add(shape).section().val()
                for index, edge in enumerate(section.Edges()):
                    points, _ = edge.sample(50)
                    axis.plot([point.x for point in points],
                              [point.z if args.horizontal_z is None else point.y for point in points],
                              color=color, linewidth=width, label=label if index == 0 else None)
            limits = (args.z_range or (guide_box.zmin-2, guide_box.zmax+2)
                      if args.horizontal_z is None else
                      (guide_box.ymin-1, guide_box.ymax+1))
            section_label = (f'Y={y:.6f}' if args.horizontal_z is None else
                             f'Z={args.horizontal_z:g}')
            axis.set(xlim=(guide_box.xmin-1, guide_box.xmax+1),
                     ylim=limits, aspect='equal', xlabel='Station X (mm)',
                     ylabel='World Z (mm)' if args.horizontal_z is None else 'Station Y (mm)',
                     title=f'{group}: drop {drop:g} mm\nsection {section_label} mm')
            axis.grid(alpha=.3)
            axis.legend(fontsize=7)
    figure.suptitle('Source guide contact diagnostic — no fit, no contact exemption')
    figure.tight_layout()
    figure.savefig(args.image, dpi=160)
    plt.close(figure)
    print(json.dumps(dict(kind='finished', rows=len(rows),
                         native_refusals=sum('native_refusal' in row for row in rows),
                         section_y=args.section_y, z_range=args.z_range,
                         horizontal_z=args.horizontal_z,
                         seconds=monotonic()-started,
                         acceptance='Read-only localization; no clearance acceptance')), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
