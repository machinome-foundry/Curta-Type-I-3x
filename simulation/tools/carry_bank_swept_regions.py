"""Bound full slider strokes against the named prospective or candidate frame."""

import argparse
import logging
from pathlib import Path

from simulation.carry_bank_frame import CarryBankFrameBench, stations
from simulation.carry_bank_regions import maximally_relieved, RESULT_ANGLES, COUNTER_ANGLES
from simulation.standard.parts import MainBody
from simulation.carry_bank_fits import CarryBankPassageFrame
from simulation.tools.interference import world_solids
from simulation.tools.carry_frame_swept import certify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    names = [f'result-{i}' for i in range(1, 11)] + [f'counter-{i}' for i in range(1, 6)]
    parser.add_argument('--station', choices=names, action='append', required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--candidate', action='store_true', help='Test the actual .05 mm fit')
    args = parser.parse_args()
    if not args.output_dir.is_dir():
        parser.error('output directory must already exist')
    model = CarryBankFrameBench()
    model.set_state(drop_mm=0)
    model.assemble()
    chosen = {}
    for path, node, slider in stations(model):
        counter = path.startswith('turns_carries')
        index = int(path.rsplit('_', 1)[-1])
        name = ('counter-' if counter else 'result-')+str(index)
        if name in args.station:
            angle = (COUNTER_ANGLES if counter else RESULT_ANGLES)[index-1]
            chosen[name] = ('Curta.'+path+'.'+slider, -angle)
    native = world_solids(model, selected={path for path, angle in chosen.values()})
    maximum = CarryBankPassageFrame().shape() if args.candidate else maximally_relieved(MainBody().shape())
    label = 'candidate' if args.candidate else 'max-region'
    passed = True
    for name in args.station:
        path, angle = chosen[name]
        passed = certify(name, source_shapes=(native[path], maximum), alignment=angle,
                         output=args.output_dir/f'carry-bank-{label}-sweep-{name}.json') and passed
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
