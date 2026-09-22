"""Sequential guarded regression, with named historical failures kept visible."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import sys
import time


def fingerprint():
    paths = subprocess.check_output(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '--', 'simulation'],
        text=True).splitlines()
    return {path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
            for path in sorted(set(paths)) if Path(path).suffix in ('.py', '.mjs', '.toml')}


def failed_test_names(output):
    # The runner writes `.FAIL!` immediately after a test name. Do not let
    # the capture consume that marker as though it were part of the name.
    blocks = re.split(r'Running (\w+\.test_\w+)', output)[1:]
    return [name for name, body in zip(blocks[::2], blocks[1::2]) if 'FAIL!' in body]


def run(kernels, selected):
    limit = resource.getrlimit(resource.RLIMIT_AS)[0]
    assert 0 < limit <= 8*1024**3, 'Launch under the 8 GiB address-space guard'
    assert all(os.environ.get(name) == '1' for name in
               ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'))
    baseline = Path('simulation/docs/resumption-validation-2026-09-11.md').read_text()
    rows = re.findall(r'^\| ([\w/]+)\.py \| (\d+)/(\d+) \| (\d+)/(\d+) \|$', baseline, re.M)
    assert len(rows) == 37, 'Historical matrix changed; review the comparison baseline'
    matrix = {name: {'faceted': (int(fp), int(ft)), 'exact': (int(np), int(nt))}
              for name, fp, ft, np, nt in rows}
    matrix.update(carry_frame={'faceted': (10, 10), 'exact': (10, 10)},
                  frame_fits={'faceted': (7, 7), 'exact': (7, 7)})
    modules = selected or list(matrix)
    assert set(modules) <= set(matrix)
    start = time.monotonic()
    sources = fingerprint()
    result = dict(kind='carry-frame-regression', sources_sha256=sources,
                  address_space_bytes=limit, numerical_threads=1, results=[])
    output_dir = Path('_build_evidence')
    output_dir.mkdir(exist_ok=True)
    manifest = output_dir/('carry-frame-regression-'+('-'.join(kernels))+
                           ('-selected' if selected else '')+'.json')
    solid = str(Path(sys.executable).with_name('solid'))
    known = {
        ('faceted', 'bearing'): ('ShaftBearingTest.test_tip_clears_frame_through_a_turn',
                                ('intersection volume 3.240210',)),
        ('faceted', 'curta'): ('CurtaTest.test_assembly_integrity',
                              ('digits_cover', 'upper_housing', '224.32750533797636')),
        ('exact', 'curta'): ('CurtaTest.test_assembly_integrity',
                            ('digits_cover', 'upper_housing', '224.32750533797636')),
    }
    for kernel in kernels:
        for module in modules:
            assert fingerprint() == sources, 'Source changed during the regression'
            log = output_dir/f'carry-frame-regression-{kernel}-{module.replace("/", "-")}.log'
            command = ['/usr/bin/time', '-f', 'RESOURCE wall=%e rss_kib=%M exit=%x',
                       'timeout', '--kill-after=10', '2400', solid, 'test',
                       '--'+kernel, 'simulation/'+module+'.py']
            print(json.dumps(dict(phase='start', kernel=kernel, module=module)), flush=True)
            begun = time.monotonic()
            with log.open('w') as stream:
                process = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
            text = log.read_text()
            summaries = re.findall(r'Ran (\d+) tests in ([\d.]+) seconds: (\d+) passed, (\d+) failed', text)
            failed_names = failed_test_names(text)
            assertions = re.findall(r'^AssertionError: (.*)$', text, re.M)
            expected_passed, expected_total = matrix[module][kernel]
            expected_failed = expected_total-expected_passed
            matches = (len(summaries) == 1 and process.returncode == int(expected_failed > 0))
            if summaries:
                total, _, passed, failed = summaries[-1]
                matches &= (int(total), int(passed), int(failed)) == (
                    expected_total, expected_passed, expected_failed)
            if expected_failed:
                name, fragments = known[(kernel, module)]
                # Python may spell the historical bearing volume in decimal
                # or scientific notation; compare its value, never waive it.
                matches &= failed_names == [name]
                if module == 'bearing':
                    values = re.findall(r'intersection volume ([\deE.+-]+)', '\n'.join(assertions))
                    matches &= (len(values) == 1 and format(float(values[0]), '.11g') ==
                                format(3.2402102747e-6, '.11g'))
                else:
                    matches &= all(fragment in '\n'.join(assertions) for fragment in fragments)
            else:
                matches &= not failed_names and not assertions
            usage = re.findall(r'RESOURCE wall=([\d.]+) rss_kib=(\d+) exit=(\d+)', text)
            entry = dict(kernel=kernel, module=module, exit=process.returncode,
                         summary=summaries, failed_tests=failed_names, assertions=assertions,
                         matches_recorded_baseline=bool(matches), log=str(log),
                         log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),
                         elapsed_seconds=time.monotonic()-begun, resource=usage)
            result['results'].append(entry)
            result.update(elapsed_seconds=time.monotonic()-start,
                          unchanged_sources=fingerprint() == sources)
            manifest.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
            print(json.dumps(entry), flush=True)
            if not matches or not result['unchanged_sources']:
                return False
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernels', nargs='+', choices=('faceted', 'exact'), default=['faceted', 'exact'])
    parser.add_argument('--modules', nargs='+')
    args = parser.parse_args()
    raise SystemExit(0 if run(args.kernels, args.modules) else 1)
