"""Index independent real-pointer cases from byte-identical standalone exports.

An explicitly named interrupted matrix contributes only its individually
validated cases. Its source report remains pending, never relabeled passed.
Coverage is independent reachability, not a continuous operation sequence or
full-bank, complete-stroke, performance or geometric acceptance.
"""

import argparse
import hashlib
import json
from pathlib import Path

from simulation.tools.operating_standalone_matrix import validate_matrix
from simulation.tools.operating_standalone_probe import validate_report


def collect(document, assets, sources):
    initial = {key: f"{value['default']:.4f}" for key, value in document['drivers'].items()}
    rows = []
    assert len({name for name, _, _ in sources}) == len(sources)
    for name, source, interrupted in sources:
        assert source['asset_sha256'] == assets, name
        assert source['program_identity'] == document['program']['identity'], name
        assert not source['errors'] and not source.get('failure'), name
        if interrupted:
            assert source['validation'] == 'pending' and source.get('cases'), name
            assert set(source['required']) == set(document['controls']), name
        else:
            assert source['validation'] == 'passed', name
        cases = source['cases'] if 'cases' in source else [source]
        if 'cases' in source:
            assert source['initial'] == initial, name
        for index, case in enumerate(cases):
            assert case['validation'] == 'passed', (name, index)
            validate_report(case)
            assert case['before'] == initial, (name, index)
            assert set(case['declared_inputs']) == set(document['drivers']), (name, index)
            control = document['controls'][case['control']]
            if control['kind'] == 'button':
                relative = document['instructions'][control['instruction']]['by']
                assert len(relative) == 1 and case['input'] in relative
                assert case.get('expected_delta') == relative[case['input']]
            else:
                assert case['input'] == control['input'], (name, index)
                if case['input'] == 'crank_rotation':
                    assert case.get('partial_turn') is True
            rows.append(dict(case, source_report=name, source_case_index=index,
                             source_validation=source['validation'],
                             source_interrupted=interrupted))
    validate_matrix(list(document['controls']), rows, [])
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', required=True, type=Path)
    parser.add_argument('--reports', nargs='+', required=True, type=Path)
    parser.add_argument('--interrupted-matrix', action='append', default=[], type=Path,
                        help='Explicitly acknowledge an interrupted pending matrix among --reports')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    assert not args.output.exists(), 'Preserve previous indexes'
    document = json.loads((args.build/'manifest.json').read_text())
    assets = {name: hashlib.sha256((args.build/name).read_bytes()).hexdigest()
              for name in ('manifest.json', 'index.html', 'machinome-viewer.js')}
    interrupted = {path.resolve() for path in args.interrupted_matrix}
    assert interrupted <= {path.resolve() for path in args.reports}
    sources, records = [], []
    for path in args.reports:
        raw = path.read_bytes()
        data = json.loads(raw)
        acknowledged = path.resolve() in interrupted
        sources.append((str(path), data, acknowledged))
        records.append(dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(),
                            validation=data['validation'], interrupted=acknowledged))
    rows = collect(document, assets, sources)
    result = dict(validation='passed', coverage=__doc__.strip(),
                  program_identity=document['program']['identity'], asset_sha256=assets,
                  sources=records, cases=rows, errors=[])
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(validation='passed', controls=len(rows), sources=len(sources))))


if __name__ == '__main__':
    main()
