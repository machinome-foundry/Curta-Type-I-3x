"""Bound every spring's continuous spread against permitted frame regions."""

import argparse
import logging
from pathlib import Path

from simulation.carry_bank_frame import CarryBankFrameBench, stations
from simulation.carry_bank_regions import maximally_relieved
from simulation.standard.parts import MainBody
from simulation.carry_bank_fits import CarryBankPassageFrame
from simulation.tools.carry_frame_interval import certify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--candidate', action='store_true', help='Test the actual .05 mm fit')
    args = parser.parse_args()
    if not args.output_dir.is_dir():
        parser.error('output directory must already exist')
    model = CarryBankFrameBench()
    maximum = CarryBankPassageFrame().shape() if args.candidate else maximally_relieved(MainBody().shape())
    label = 'candidate' if args.candidate else 'max-region'
    passed = True
    for path, node, slider in stations(model):
        counter = path.startswith('turns_carries')
        name = ('counter-' if counter else 'result-')+path.rsplit('_', 1)[-1]
        passed = certify(path, model=model, counter=counter, frame=maximum,
                         output=args.output_dir/f'carry-bank-{label}-spring-{name}.json') and passed
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
