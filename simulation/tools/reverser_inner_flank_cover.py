"""Reproduce whole-print coverage for the explicitly isolated inner-flank fit.

Both outputs must be new paths. A failed prefix is retained as failed evidence,
never resumed or treated as a completed certificate.
"""

import argparse
import hashlib
import json
import logging
from pathlib import Path


def main():
    from simulation.reverser_ones_fit_trial import TrialOnesPinion, TrialOperatingCurta
    from simulation.tools.reverser_profile_cover import profile_cover
    from simulation.tools.reverser_installed_profile_cover import probe

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-profiles', type=Path, required=True)
    parser.add_argument('--source-output', type=Path, required=True)
    parser.add_argument('--installed-output', type=Path, required=True)
    args = parser.parse_args()
    if any(path.exists() for path in (args.source_output, args.installed_output)):
        parser.error('Preserve existing evidence; choose two new output paths')
    if args.source_output.resolve() == args.installed_output.resolve():
        parser.error('Source and installed evidence need distinct paths')
    raw = args.source_profiles.read_bytes()
    profiles = {row['part']: row for row in map(json.loads, raw.splitlines())}
    candidate = profile_cover(TrialOnesPinion(), axial_allowance_mm=.001,
                              include_mesh=True)
    with args.source_output.open('x') as output:
        json.dump(candidate, output)
    candidate_digest = hashlib.sha256(args.source_output.read_bytes()).hexdigest()
    profiles['FittedCounterPinion'] = candidate
    count = 0
    with args.installed_output.open('x') as output:
        for row in probe(profiles, axial_allowance_mm=.001, model=TrialOperatingCurta):
            row['source_profiles_sha256'] = hashlib.sha256(raw).hexdigest()
            row['ones_candidate_profile_sha256'] = candidate_digest
            print(json.dumps(row), file=output, flush=True)
            print(json.dumps({key: row[key] for key in
                ('kind', 'path', 'component', 'separated', 'remainder_mm3') if key in row}),
                flush=True)
            count += 1
    print(json.dumps(dict(rows=count, source_sha256=candidate_digest,
        installed_sha256=hashlib.sha256(args.installed_output.read_bytes()).hexdigest())),
        flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
