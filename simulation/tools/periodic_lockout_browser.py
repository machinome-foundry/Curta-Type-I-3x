"""Check the source-backed periodic stop through the public browser run API.

Export simulation.periodic_lockout:PeriodicLockoutBench with --no-widget first.
This opens an isolated browser, not the pilot's Studio session. The report is
saved even when the long request fails, so a viewer correction can replay the
same acceptance unchanged. No framework or viewer implementation is imported.
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
    args = parser.parse_args()
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
            for target in (150, 840):
                case = page.evaluate('''async target => {
                    const run = curta.run();
                    await run.reset(); run.pause();
                    for (const [input,to] of [['crank_height',0], ['digit',3],
                        ['crank_angle',120], ['digit',0]]) {
                        const outcome = await run.move(input, {to});
                        if (outcome.some(x => x.status !== 'completed'))
                            throw Error(JSON.stringify(outcome));
                    }
                    const before = await run.snapshot();
                    const prepared = run.state();
                    let result = null, error = null;
                    try { result = await run.move('crank_angle', {to:target}); }
                    catch (failure) { error = String(failure); }
                    const after = await run.snapshot();
                    return {target, prepared, result, error, stopped:run.state(),
                        unchanged:JSON.stringify(before) === JSON.stringify(after),
                        worker:run.runsInWorker};
                }''', target)
                report['cases'].append(case)
                print(json.dumps(case), flush=True)
            page.screenshot(path=str(build / 'periodic-browser.png'), timeout=60000)
        finally:
            browser.close()
            (build / 'browser-acceptance.json').write_text(
                json.dumps(report, indent=2) + '\n')

    assert not report['page_errors'], report['page_errors']
    for case in report['cases']:
        assert abs(case['prepared']['ones.turn'] - 189.6) < 1e-8, case
        assert case['error'] is None, case
        assert case['result'][-1]['status'] == 'blocked', case
        assert abs(case['stopped']['crank_angle'] - 125.22) < 1e-7, case
        assert case['stopped']['ones.turn'] == case['prepared']['ones.turn'], case
    print('Both requests stop at the first surface with the shaft held.', flush=True)


if __name__ == '__main__':
    main()
