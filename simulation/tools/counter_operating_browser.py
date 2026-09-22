"""Exercise any counter station's withdrawal on an isolated full-model export.

Uses public running requests, not arithmetic shortcuts or the pilot's live
session. This tests the browser executor and render; it does not claim real
pointer coverage or geometric clearance from pixels. Optional Python reports
are compared across every retained coordinate, exactly by default. An explicit
option classifies the independently traced three-ULP p9 cam-path residual;
it records that difference and never changes a geometric contact check.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright


SHAFTS = tuple(f'transmission.turns.{name}.turn'
               for name in ('ones', 'tens', 'hundreds', 'digit_4', 'digit_5', 'digit_6'))
SHAFT = SHAFTS[0]
P9_DETENT = 'carriage.registers.dial_detents.p_6mm_ball_419241_9.lift'


def compare_banks(actual, expected, *, allow_measured_detent_rounding=False):
    """Keep all IDs/other values exact; optionally report one measured residue."""
    assert set(actual) == set(expected), 'bank coordinate mismatch'
    differences = []
    for key, value in actual.items():
        reference = expected[key]
        if value == reference:
            continue
        assert allow_measured_detent_rounding and key == P9_DETENT, (key, value, reference)
        assert math.isfinite(value) and math.isfinite(reference), (key, value, reference)
        ulps = abs(value-reference)/max(math.ulp(value), math.ulp(reference))
        assert ulps <= 3, (key, value, reference, ulps)
        differences.append({'coordinate': key, 'browser': value, 'python': reference,
                            'ulps': ulps})
    return differences


def validate_report(report, expected=None, *, station=1, allow_measured_detent_rounding=False):
    differences = []
    assert station in range(1, 7)
    assert report.get('station', station) == station
    shaft = SHAFTS[station-1]
    shift = 20*(station-1)
    shaft_angle = 167.6-shift
    ids = set(report['coordinate_ids'])
    assert ids and len(ids) == len(report['coordinate_ids'])
    assert set(report['prepared']) == ids
    assert not report['errors'], report['errors']
    assert report['prepared']['crank_rotation'] == 170+shift
    assert report['prepared']['main_drive.crank.turn'] == -170-shift
    assert abs(report['prepared'][shaft]-shaft_angle) < 1e-9
    targets = [180+shift, 900+shift]
    assert [case['target'] for case in report['cases']] == targets
    if expected is not None:
        assert [row['target'] for row in expected] == targets
    first_stop = report['cases'][0]['stopped']['crank_rotation']
    for case in report['cases']:
        assert case['status'] == case['retry_status'] == 'blocked', case['target']
        assert case['relief_status'] == 'completed' and case['replay'], case['target']
        stop = case['stopped']['crank_rotation']
        assert 170+shift < stop < 175+shift and abs(stop-first_stop) < 1e-7, stop
        assert abs(case['idle']['crank_rotation']-(stop-.05)) < 1e-7
        assert abs(case['retry']['crank_rotation']-stop) < 1e-7
        for state in ('stopped', 'idle', 'retry'):
            bank = case[state]
            assert set(bank) == ids, (state, 'coordinate coverage')
            assert abs(bank[shaft]-shaft_angle) < 1e-9, (state, shaft, bank[shaft])
            assert abs(bank['main_drive.crank.turn']+bank['crank_rotation']) < 1e-9
        if expected is not None:
            other = next(row for row in expected if row['target'] == case['target'])
            for state in ('stopped', 'idle'):
                for difference in compare_banks(case[state], other[state],
                        allow_measured_detent_rounding=allow_measured_detent_rounding):
                    differences.append(dict(difference, target=case['target'], state=state))
    return differences


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--python-report', type=Path)
    parser.add_argument('--station', type=int, choices=range(1, 7), default=1)
    parser.add_argument('--allow-measured-detent-rounding', action='store_true',
                        help='Record the traced p9 cam-path residue, at most three ULPs; all other state remains exact.')
    args = parser.parse_args()
    build = args.build.resolve()
    expected = json.loads(args.python_report.read_text()) if args.python_report else None
    document = json.loads((build/'manifest.json').read_text())
    shift = 20*(args.station-1)
    shaft = SHAFTS[args.station-1]
    requests = ([['crank_elevation', 9], ['reverser_height', -4.9425],
                 ['crank_rotation', 90], ['crank_rotation', 160], ['crank_rotation', 170],
                 ['reverser_height', -6.9425]] if args.station == 1 else
                [['reverser_height', -3], ['crank_rotation', 160+shift],
                 ['crank_rotation', 170+shift], ['reverser_height', 3.9075]])
    viewer = json.loads(subprocess.check_output(
        [sys.executable, '-m', 'machinome_viewer', 'describe'], text=True))
    bundle = Path(viewer['path']).read_bytes()
    report = {'errors': [], 'cases': [], 'station': args.station, 'validation': 'pending',
              'coordinate_ids': list(document['program']['coordinates']),
              'program_identity': document['program']['identity'],
              'python_report': str(args.python_report) if args.python_report else None,
              'bundle_sha256': hashlib.sha256(bundle).hexdigest(),
              'document_sha256': hashlib.sha256((build/'manifest.json').read_bytes()).hexdigest()}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'])
        try:
            page = browser.new_page(viewport={'width': 1200, 'height': 900})
            # The full assembly can exceed the default 30 s capture deadline
            # under concurrent native geometry checks; retain a finite limit.
            page.set_default_timeout(60_000)
            page.on('pageerror', lambda error: report['errors'].append(str(error)))

            def serve(route):
                name = unquote(urlsplit(route.request.url).path).lstrip('/')
                if not name:
                    route.fulfill(content_type='text/html', body=(
                        '<html><body style="margin:0"><div id="view" '
                        'style="width:1200px;height:900px"></div></body></html>'))
                    return
                asset = (build/name).resolve()
                if asset.is_relative_to(build) and asset.is_file():
                    route.fulfill(path=asset)
                else:
                    route.fulfill(status=404, body='Missing acceptance asset')

            page.route('http://counter-operating.test/**', serve)
            page.goto('http://counter-operating.test/')
            page.add_script_tag(content=bundle.decode())
            report['prepared'] = page.evaluate('''async requests => {
                window.curta=await MachinomeViewer.mount('#view','manifest.json',{
                    autoplay:false,run:{dt:.1},partControls:'none'});
                const run=curta.run(); run.pause();
                for(const [input,to] of requests) {
                    const result=await run.move(input,{to});
                    if(result.some(row=>row.status!=='completed')) throw Error(JSON.stringify(result));
                }
                window.counterPrepared=await run.snapshot();
                return run.state();
            }''', requests)
            print(json.dumps({'prepared': report['prepared']['crank_rotation'],
                              'shaft': report['prepared'][shaft]}), flush=True)
            page.screenshot(path=str(build/'counter-withdrawal-prepared.png'))
            for target in (180+shift, 900+shift):
                case = page.evaluate('''async target => {
                    const run=curta.run(); await run.restore(counterPrepared);
                    const result=await run.move('crank_rotation',{to:target});
                    const stopped=run.state(), snapshot=await run.snapshot();
                    await run.restore(counterPrepared);
                    await run.move('crank_rotation',{to:target});
                    const replay=JSON.stringify(snapshot)===JSON.stringify(await run.snapshot());
                    const relief=await run.move('crank_rotation',{by:-.05});
                    await run.step(1); const idle=run.state();
                    const retry=await run.move('crank_rotation',{to:target});
                    return {target,status:result.at(-1).status,stopped,replay,
                        relief_status:relief.at(-1).status,idle,
                        retry_status:retry.at(-1).status,retry:run.state()};
                }''', target)
                report['cases'].append(case)
                print(json.dumps({'target': target, 'status': case['status'],
                                  'stop': case['stopped']['crank_rotation'],
                                  'replay': case['replay']}), flush=True)
            page.screenshot(path=str(build/'counter-withdrawal-stopped.png'))
            report['bank_differences'] = validate_report(report, expected, station=args.station,
                allow_measured_detent_rounding=args.allow_measured_detent_rounding)
            report['bank_comparison'] = ('exact except explicitly measured p9 cam residual <=3 ULPs'
                if args.allow_measured_detent_rounding else 'exact')
            report['validation'] = 'passed'
        finally:
            browser.close()
            (build/'counter-browser-acceptance.json').write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
