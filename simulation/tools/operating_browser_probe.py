"""Mount the actual operating export through the viewer's public host API.

This checks two pointer prerequisites, not complete pointer/arithmetic acceptance. Assets
are served locally through Playwright routing; nothing is uploaded and no
persistent server is opened. A refused control remains a failing result.
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
    parser.add_argument('--build', type=Path, default=Path('_build/operating_curta'))
    parser.add_argument('--screenshot', type=Path,
                        default=Path('_build_running/operating-browser-prerequisite.png'))
    args = parser.parse_args()
    build = args.build.resolve()
    document = json.loads((build / 'viewer.json').read_text())
    viewer = json.loads(subprocess.check_output(
        [sys.executable, '-m', 'machinome_viewer', 'describe'], text=True))
    bundle = Path(viewer['path'])
    errors = []
    report = {'viewer': viewer, 'bundle_sha256': hashlib.sha256(bundle.read_bytes()).hexdigest(),
              'document_version': document['version'],
              'declared_controls': {name: control['kind']
                                    for name, control in document['controls'].items()}}
    assert document['version'] in viewer['documentVersions'], report
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'])
        try:
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            page.set_default_timeout(60000)
            page.on('pageerror', lambda error: errors.append(str(error)))

            def serve(route):
                name = unquote(urlsplit(route.request.url).path).lstrip('/')
                if not name:
                    route.fulfill(content_type='text/html', body=(
                        '<html><body style="margin:0"><div id="view" '
                        'style="width:1440px;height:1000px"></div></body></html>'))
                    return
                asset = (build / name).resolve()
                if asset.is_relative_to(build) and asset.is_file():
                    route.fulfill(path=asset)
                else:
                    route.fulfill(status=404, body='Missing fixture asset')

            page.route('http://operating.test/**', serve)
            page.goto('http://operating.test/')
            page.add_script_tag(path=str(bundle))
            report['mount'] = page.evaluate('''async () => {
                try {
                    window.curta = await MachinomeViewer.mount('#view', 'viewer.json', {
                        autoplay: false, partControls: 'inline',
                    });
                    // Projected/raycast control locations need a rendered frame.
                    await new Promise(requestAnimationFrame);
                    await new Promise(requestAnimationFrame);
                    return {ok: true, hasRun: curta.run() !== null, runState: curta.run().state(),
                            controls: curta.controls()};
                } catch (error) {
                    return {ok: false, error: String(error)};
                }
            }''')
            if report['mount']['ok']:
                crank = next(control for control in report['mount']['controls']
                             if control['name'] == 'lift crank')
                if crank['point']:
                    page.mouse.move(crank['point']['x'], crank['point']['y'])
                    page.evaluate('''async () => {
                        await new Promise(requestAnimationFrame);
                        await new Promise(requestAnimationFrame);
                    }''')
                    report['crank_hover_controls'] = page.evaluate('''() =>
                        curta.controls().filter(control => control.name.includes('crank') ||
                                                control.name === 'one revolution')''')
                    lift = next(control for control in report['crank_hover_controls']
                                if control['name'] == 'lift crank')
                    point = lift['gesturePoint']
                    assert point is not None, 'No distinct gesture target for the selected crank lift'
                    page.mouse.move(point['x'], point['y'])
                    page.mouse.down()
                    page.mouse.move(point['x'], point['y'] - 60, steps=12)
                    page.mouse.up()
                    page.wait_for_function('curta.run().state().crank_elevation >= .999999', timeout=60000)
                    report['pointer_crank_lift'] = page.evaluate('''() => {
                        const state = curta.run().state();
                        return {input: state.crank_elevation, lift: state['main_drive.crank.lift'],
                                rotation: state.crank_rotation, turn: state['main_drive.crank.turn']};
                    }''')
                    # Separate prerequisite cases start from a fresh run bank;
                    # this is fixture setup, not a simulated clearing action.
                    page.evaluate('async () => { await curta.run().reset(); }')
                    page.wait_for_function('curta.run().state().crank_elevation === 0')
                selector = page.evaluate('''() => curta.controls().find(
                    control => control.name === 'set digit 1')''')
                point = selector['gesturePoint']
                assert point is not None, 'The first selector has no reachable gesture target'
                page.mouse.move(point['x'], point['y'])
                page.mouse.down()
                page.mouse.move(point['x'], point['y'] + 60, steps=12)
                page.mouse.up()
                page.wait_for_function('curta.run().state().digit_1 >= .999999', timeout=60000)
                report['pointer_selector'] = page.evaluate('''() => {
                    const state = curta.run().state();
                    return {digits: Array.from({length: 8}, (_, index) => state[`digit_${index + 1}`]),
                            shaft: state['input_selectors.selectors.digit_selector_axle_1.selector_shaft_bottom.turn'],
                            crank: state.crank_rotation};
                }''')
            page.screenshot(path=str(args.screenshot))
        except Exception as error:
            report['probe_error'] = f'{type(error).__name__}: {error}'
            if 'page' in locals():
                report['failure_state'] = page.evaluate(
                    '() => window.curta ? curta.run().state() : null')
                page.screenshot(path=str(args.screenshot))
        finally:
            browser.close()
    report['page_errors'] = errors
    report['screenshot'] = str(args.screenshot)
    print(json.dumps(report, indent=2), flush=True)
    assert 'probe_error' not in report, report.get('probe_error')
    assert report['mount']['ok'], report['mount']
    assert report['mount']['hasRun'], 'The mounted document has no retained run'
    assert not errors, errors
    assert {control['name'] for control in report['mount']['controls']} == set(document['controls'])
    lifted = report['pointer_crank_lift']
    assert 0 < lifted['input'] <= 9 and abs(lifted['lift'] - lifted['input']) < .00001, lifted
    assert lifted['rotation'] == lifted['turn'] == 0, lifted
    selected = report['pointer_selector']
    assert 0 < selected['digits'][0] <= 9 and selected['digits'][1:] == [0] * 7, selected
    assert abs(selected['shaft'] - 36 * selected['digits'][0]) < .00001 and selected['crank'] == 0, selected


if __name__ == '__main__':
    main()
