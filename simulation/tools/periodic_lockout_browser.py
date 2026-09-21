"""Check the source-backed periodic stop through the public browser run API.

Export simulation.periodic_lockout:PeriodicLockoutBench with --no-widget first.
This opens an isolated browser, not the pilot's Studio session. The report is
saved even when the long request fails, so a viewer correction can replay the
same acceptance unchanged. No framework or viewer implementation is imported.
For the broader five-flat restraint, export simulation.result_locking:ResultLocking
and use --measured. Expected stops are the seven native/mesh-certified Python
poses recorded in the periodic-lockout-first-contact framework cycle.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--measured', action='store_true',
                        help='Check ResultLocking against the seven Python/geometry-certified poses.')
    parser.add_argument('--operating', action='store_true',
                        help='Run that measured matrix on the complete OperatingCurta export.')
    args = parser.parse_args()
    if args.operating:
        args.measured = True
    names = ({'crank': 'crank_rotation', 'height': 'crank_elevation',
              'digit': 'digit_1', 'shaft': 'transmission.result.ones.turn'}
             if args.operating else {'crank': 'crank_angle', 'height': 'crank_height',
                                    'digit': 'digit', 'shaft': 'ones.turn'})
    build = args.build.resolve()
    manifest = build / 'manifest.json'
    viewer = json.loads(subprocess.check_output(
        [sys.executable, '-m', 'machinome_viewer', 'describe'], text=True))
    bundle = Path(viewer['path']).read_bytes()
    report = {
        'viewer': viewer,
        'bundle_sha256': hashlib.sha256(bundle).hexdigest(),
        'document_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest(),
        'cases': [], 'page_errors': [],
    }
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'])
        try:
            page = browser.new_page(viewport={'width': 1200, 'height': 900})
            page.set_default_timeout(120000)
            page.on('pageerror', lambda error: report['page_errors'].append(str(error)))

            def serve(route):
                name = unquote(urlsplit(route.request.url).path).lstrip('/')
                if not name:
                    route.fulfill(content_type='text/html', body=(
                        '<html><body style="margin:0"><div id="view" '
                        'style="width:1200px;height:900px"></div></body></html>'))
                    return
                asset = (build / name).resolve()
                if asset.is_relative_to(build) and asset.is_file():
                    route.fulfill(path=asset)
                else:
                    route.fulfill(status=404, body='Missing local acceptance asset')

            page.route('http://periodic-curta.test/**', serve)
            page.goto('http://periodic-curta.test/')
            page.add_script_tag(content=bundle.decode())
            page.evaluate('''async () => {
                window.curta = await MachinomeViewer.mount('#view', 'manifest.json', {
                    autoplay:false, run:{dt:.1}, partControls:'none',
                });
                curta.run().pause();
            }''')
            cases = ([{'withdrawal': 120, 'target': target, 'expected': 125.22}
                      for target in (150, 840)] if not args.measured else [
                {'withdrawal': 360*turns+withdrawal, 'target': 360*turns+840,
                 'expected': expected}
                for turns, withdrawal, expected in (
                    (0, 120, 125.22323837227304),
                    (1, 120, 485.2280105590762),
                    (2, 120, 845.2050994865567),
                    (3, 120, 1205.2280067446554),
                    (4, 120, 1565.2280067446554),
                    (0, 115, 120.38810729947272),
                    (0, 123, 129.82507171577254))])
            for descriptor in cases:
                case = page.evaluate('''async ({target,withdrawal,expected,measured,names,operating}) => {
                    const run = curta.run();
                    await run.reset(); run.pause();
                    const setup = [[names.height,0], [names.digit,3]];
                    // Fixture preparation only: the full ratchet has a
                    // 1,000-surface/tick guard. Reach later revolutions with
                    // ordinary turns; never split the challenged 720° request.
                    if (operating) for (let angle=360; angle<withdrawal; angle+=360)
                        setup.push([names.crank,angle]);
                    setup.push([names.crank,withdrawal], [names.digit,0]);
                    for (const [input,to] of setup) {
                        const outcome = await run.move(input, {to});
                        if (outcome.some(x => x.status !== 'completed'))
                            throw Error(JSON.stringify(outcome));
                    }
                    const before = await run.snapshot();
                    const prepared = run.state();
                    let result = null, error = null;
                    try { result = await run.move(names.crank, {to:target}); }
                    catch (failure) { error = String(failure); }
                    const after = await run.snapshot();
                    const stopped = run.state();
                    let replay = null, relief = null, idle = null, retry = null;
                    if (measured && !error) {
                        await run.restore(before);
                        await run.move(names.crank, {to:target});
                        replay = JSON.stringify(await run.snapshot()) === JSON.stringify(after);
                        relief = await run.move(names.crank, {by:-.05});
                        await run.step(1); idle = run.state();
                        retry = await run.move(names.crank, {to:target});
                    }
                    return {target, withdrawal, expected, prepared, result, error, stopped,
                        replay, relief, idle, retry, retried:run.state(),
                        unchanged:JSON.stringify(before) === JSON.stringify(after),
                        worker:run.runsInWorker};
                }''', descriptor | {'measured': args.measured, 'names': names,
                                     'operating': args.operating})
                report['cases'].append(case)
                print(json.dumps({key: case[key] for key in
                    ('target', 'withdrawal', 'expected', 'result', 'error', 'replay')}
                    | {'crank': case['stopped'][names['crank']],
                       'shaft': case['stopped'][names['shaft']]}), flush=True)
            if args.measured:
                report['legal'] = page.evaluate('''async ({names,operating}) => {
                    const run = curta.run(), found = [];
                    for (const [digit,height,expected] of [[0,0,4],[3,0,652],
                        [9,0,1948],[0,9,2164]]) {
                        await run.reset(); run.pause();
                        await run.move(names.digit, {to:digit});
                        await run.move(names.height, {to:height});
                        const completion = run.move(names.crank,
                            {by:1080, duration:operating ? 6 : 0});
                        if (operating) await run.step(60);
                        const result = await completion;
                        found.push({digit,height,expected,result,state:run.state()});
                    }
                    return found;
                }''', {'names': names, 'operating': args.operating})
            page.screenshot(path=str(build / 'periodic-browser.png'), timeout=60000)
        finally:
            browser.close()
            (build / 'browser-acceptance.json').write_text(
                json.dumps(report, indent=2) + '\n')

    assert not report['page_errors'], report['page_errors']
    for case in report['cases']:
        if not args.measured:
            assert abs(case['prepared'][names['shaft']] - 189.6) < 1e-8, case
        assert case['error'] is None, case
        assert case['result'][-1]['status'] == 'blocked', case
        assert abs(case['stopped'][names['crank']] - case['expected']) < 1e-7, case
        assert case['stopped'][names['shaft']] == case['prepared'][names['shaft']], case
        if args.measured:
            assert case['replay'], case
            assert case['relief'][-1]['status'] == 'completed', case
            assert abs(case['idle'][names['crank']] - case['expected'] + .05) < 1e-7, case
            assert case['retry'][-1]['status'] == 'blocked', case
            assert abs(case['retried'][names['crank']] - case['expected']) < 1e-7, case
            assert case['retried'][names['shaft']] == case['prepared'][names['shaft']], case
    for case in report.get('legal', []):
        assert case['result'][-1]['status'] == 'completed', case
        assert abs(case['state'][names['shaft']] - case['expected']) < 1e-7, case
    print(f"{len(cases)} first-contact cases and {len(report.get('legal', []))} legal moves pass.",
          flush=True)


if __name__ == '__main__':
    main()
