"""Exercise the isolated result-bank export with actual running requests.

This is executor/render evidence, not pointer coverage or geometric clearance.
Optional Python reports compare complete stopped/relieved banks; their exact
station/request scope is recorded explicitly rather than inferred for others.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright


CHANNELS = {3: 'hundreds', 8: 'digit_8'}


def validate_report(report, expected=None):
    assert not report['errors'], report['errors']
    ids = set(report['coordinate_ids'])
    assert ids and len(ids) == len(report['coordinate_ids'])
    required = [(station, target) for station in CHANNELS
                for target in (170+20*(station-2), 860+20*(station-2))]
    assert [(row['station'], row['target']) for row in report['cases']] == required
    assert [row['station'] for row in report['prepared']] == list(CHANNELS)
    stops = {}
    for row in report['prepared']:
        station, bank = row['station'], row['bank']
        shift = 20*(station-2)
        assert set(bank) == ids
        assert bank['crank_rotation'] == 140+shift
        assert bank['main_drive.crank.turn'] == -140-shift
        assert bank[f'digit_{station}'] == 0
        assert abs(bank[f'transmission.result.{CHANNELS[station]}.turn']-(169.6-shift)) < 1e-7
    for row in report['cases']:
        station = row['station']
        shift = 20*(station-2)
        assert row['status'] == row['retry_status'] == 'blocked'
        assert row['relief_status'] == 'completed' and row['replay']
        angle = row['stopped']['crank_rotation']
        assert 140+shift < angle < 146+shift
        if station in stops:
            assert abs(stops[station]-angle) < 1e-7
        stops[station] = angle
        assert abs(row['relieved']['crank_rotation']-(angle-.05)) < 1e-7
        assert abs(row['retry']['crank_rotation']-angle) < 1e-7
        for state in ('stopped', 'relieved', 'retry'):
            bank = row[state]
            assert set(bank) == ids, (station, row['target'], state, 'coordinate coverage')
            assert abs(bank['main_drive.crank.turn']+bank['crank_rotation']) < 1e-9
            assert abs(bank[f'transmission.result.{CHANNELS[station]}.turn']-(169.6-shift)) < 1e-7
    compared = []
    if expected is not None:
        assert expected, 'empty Python report'
        keys = [(row['station'], row['target']) for row in expected]
        assert len(set(keys)) == len(keys)
        stations = {station for station, _ in keys}
        assert set(keys) == {key for key in required if key[0] in stations}
        for other in expected:
            key = (other['station'], other['target'])
            row = next(row for row in report['cases']
                       if (row['station'], row['target']) == key)
            for state in ('stopped', 'relieved'):
                assert row[state] == other[state], (key, state, 'Python bank mismatch')
            compared.append(key)
    return sorted(compared)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--python-report', type=Path)
    args = parser.parse_args()
    build = args.build.resolve()
    manifest = (build/'manifest.json').read_bytes()
    document = json.loads(manifest)
    expected = json.loads(args.python_report.read_text()) if args.python_report else None
    description = json.loads(subprocess.check_output(
        [sys.executable, '-m', 'machinome_viewer', 'describe'], text=True))
    bundle = Path(description['path']).read_bytes()
    report = {'errors': [], 'prepared': [], 'cases': [], 'validation': 'pending',
              'coordinate_ids': list(document['program']['coordinates']),
              'program_identity': document['program']['identity'],
              'python_report': str(args.python_report) if args.python_report else None,
              'python_compared_cases': [],
              'bundle_sha256': hashlib.sha256(bundle).hexdigest(),
              'document_sha256': hashlib.sha256(manifest).hexdigest()}
    output = build/'result-bank-browser-acceptance.json'
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'])
        try:
            page = browser.new_page(viewport={'width': 1200, 'height': 900})
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

            page.route('http://result-bank.test/**', serve)
            page.goto('http://result-bank.test/')
            page.add_script_tag(content=bundle.decode())
            page.evaluate('''async () => {
                window.curta=await MachinomeViewer.mount('#view','manifest.json',{
                    autoplay:false,run:{dt:.1},partControls:'none'});
                curta.run().pause();
                window.resultInitial=await curta.run().snapshot();
            }''')
            for station in CHANNELS:
                bank = page.evaluate('''async station => {
                    const run=curta.run(); await run.restore(resultInitial);
                    const shift=20*(station-2);
                    for(const [input,to] of [[`digit_${station}`,3],
                        ['crank_rotation',140+shift],[`digit_${station}`,0]]) {
                        const result=await run.move(input,{to});
                        if(result.some(row=>row.status!=='completed'))
                            throw Error(JSON.stringify(result));
                    }
                    window.resultPrepared=await run.snapshot();
                    return run.state();
                }''', station)
                report['prepared'].append({'station': station, 'bank': bank})
                print(json.dumps({'station': station, 'prepared': bank['crank_rotation']}), flush=True)
                for target in (170+20*(station-2), 860+20*(station-2)):
                    row = page.evaluate('''async ({station,target}) => {
                        const run=curta.run(); await run.restore(resultPrepared);
                        const result=await run.move('crank_rotation',{to:target});
                        const stopped=run.state(), saved=await run.snapshot();
                        await run.restore(resultPrepared);
                        await run.move('crank_rotation',{to:target});
                        const replay=JSON.stringify(saved)===JSON.stringify(await run.snapshot());
                        const relief=await run.move('crank_rotation',{by:-.05});
                        const relieved=run.state();
                        const retry=await run.move('crank_rotation',{to:target});
                        return {station,target,status:result.at(-1).status,stopped,replay,
                            relief_status:relief.at(-1).status,relieved,
                            retry_status:retry.at(-1).status,retry:run.state()};
                    }''', {'station': station, 'target': target})
                    report['cases'].append(row)
                    print(json.dumps({'station': station, 'target': target,
                                      'status': row['status'], 'stop': row['stopped']['crank_rotation'],
                                      'replay': row['replay']}), flush=True)
                page.screenshot(path=str(build/f'result-station-{station}-withdrawal.png'))
        except Exception as error:
            report['errors'].append(f'{type(error).__name__}: {error}')
            raise
        finally:
            browser.close()
            output.write_text(json.dumps(report, indent=2)+'\n')
    report['python_compared_cases'] = validate_report(report, expected)
    report['validation'] = 'passed'
    output.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
