"""Local hosted acceptance of the opt-in complete-Curta lockout diagnostic.

Only public viewer/run APIs and real pointer gestures. Does not touch the
pilot's Studio session, rebuild the viewer, or upload any asset.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright


def paths(tree, prefix=()):
    result = []
    for child in tree.get('children', []):
        path = (*prefix, child['name'])
        result.append(path)
        result.extend(paths(child, path))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--baseline', type=Path, required=True)
    args = parser.parse_args()
    build = args.build.resolve()
    document_path = build / 'manifest.json'
    document = json.loads(document_path.read_text())
    baseline = json.loads(args.baseline.read_text())
    assert paths(document['root']) == paths(baseline['root'])
    assert document['controls'] == baseline['controls']
    assert document['program']['coordinates'] == baseline['program']['coordinates']
    assert document['version'] == baseline['version'] == 7
    viewer = json.loads(subprocess.check_output(
        [sys.executable, '-m', 'machinome_viewer', 'describe'], text=True))
    # Hold the tested bytes even if an independent viewer cycle rebuilds later.
    bundle = Path(viewer['path']).read_bytes()
    report = {'viewer': viewer,
              'bundle_sha256': hashlib.sha256(bundle).hexdigest(),
              'document_sha256': hashlib.sha256(document_path.read_bytes()).hexdigest(),
              'baseline_sha256': hashlib.sha256(args.baseline.read_bytes()).hexdigest(),
              'version': document['version'], 'assembly_paths': len(paths(document['root'])),
              'controls': len(document['controls']), 'tree_controls_bank_unchanged': True}
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'])
        try:
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            page.set_default_timeout(120000)
            page.on('pageerror', lambda error: errors.append(str(error)))

            def serve(route):
                name = unquote(urlsplit(route.request.url).path).lstrip('/')
                if not name:
                    route.fulfill(content_type='text/html', body=(
                        '<html><body style="margin:0"><div id="view" '
                        'style="width:1440px;height:1000px"></div></body></html>'))
                    return
                asset = (build/name).resolve()
                if asset.is_relative_to(build) and asset.is_file():
                    route.fulfill(path=asset)
                else:
                    route.fulfill(status=404, body='Missing local acceptance asset')

            page.route('http://lockout.test/**', serve)
            page.goto('http://lockout.test/')
            page.add_script_tag(content=bundle.decode())
            report['host_request'] = page.evaluate('''async () => {
                window.curta = await MachinomeViewer.mount('#view', 'manifest.json', {
                    autoplay: false, partControls: 'inline', run: {dt: .1},
                });
                const run = curta.run(); run.pause();
                window.outcomes = [];
                run.onOutcome(outcome => outcomes.push(outcome));
                for (const [input,to] of [['digit_1',3], ['crank_rotation',90],
                    ['crank_rotation',120], ['digit_1',0]]) {
                    const result = await run.move(input, {to});
                    if (result.some(x => x.status !== 'completed')) throw Error(JSON.stringify(result));
                }
                window.prepared = await run.snapshot();
                const result = await run.move('crank_rotation', {to:150});
                const stopped = run.state();
                window.stopped = await run.snapshot();
                await run.restore(prepared);
                await run.move('crank_rotation', {to:150});
                const replay = JSON.stringify(await run.snapshot()) === JSON.stringify(window.stopped);
                const relief = await run.move('crank_rotation', {to:125.27});
                await run.step(1);
                const relieved = run.state();
                await run.restore(prepared);
                await new Promise(requestAnimationFrame);
                await new Promise(requestAnimationFrame);
                return {result, stopped, replay, relief, relieved, worker:run.runsInWorker};
            }''')
            host = report['host_request']
            assert host['result'][-1]['status'] == 'blocked', host
            assert abs(host['stopped']['crank_rotation']-125.32) < 1e-7, host
            assert abs(host['stopped']['transmission.result.ones.turn']-189.6) < 1e-10
            assert host['replay'], host
            assert host['relief'][-1]['status'] == 'completed'
            assert abs(host['relieved']['crank_rotation']-125.27) < 1e-7
            print('Host stop, relief and replay passed', flush=True)

            attempts = []
            for dx, dy in ((240, 0), (-240, 0), (0, -240), (0, 240)):
                page.evaluate('''async () => {
                    await curta.run().restore(prepared); outcomes.length = 0;
                    await new Promise(requestAnimationFrame);
                    await new Promise(requestAnimationFrame);
                }''')
                point = page.evaluate('''() => curta.controls().find(
                    c => c.name === 'turn crank').point''')
                assert point is not None, 'No reachable crank surface'
                page.mouse.move(point['x'], point['y'])
                page.evaluate('''async () => {
                    await new Promise(requestAnimationFrame);
                    await new Promise(requestAnimationFrame);
                }''')
                point = page.evaluate('''() => curta.controls().find(
                    c => c.name === 'turn crank').gesturePoint''')
                assert point is not None, 'No distinct crank turn handle'
                page.mouse.move(point['x'], point['y'])
                page.mouse.down()
                # Let each real pointer move reach a rendered frame and the
                # worker before the next one, rather than testing coalescing.
                for step in range(1, 13):
                    page.mouse.move(point['x']+dx*step/12, point['y']+dy*step/12)
                    page.evaluate('''async () => {
                        await new Promise(requestAnimationFrame);
                        await curta.run().snapshot();
                    }''')
                page.mouse.up()
                page.wait_for_function('outcomes.length > 0')
                attempt = page.evaluate('''async () => {
                    await curta.run().snapshot();
                    return {state:curta.run().state(), outcomes:[...outcomes]};
                }''')
                attempt['drag'] = [dx, dy]
                attempts.append(attempt)
                if (abs(attempt['state']['crank_rotation']-125.32) < 1e-7
                        and any(x['status'] == 'blocked' and x['input'] == 'crank_rotation'
                                for x in attempt['outcomes'])):
                    break
            report['pointer_attempts'] = attempts
            (build/'acceptance.json').write_text(json.dumps(report, indent=2)+'\n')
            assert abs(attempts[-1]['state']['crank_rotation']-125.32) < 1e-7, [
                (a['drag'], a['state']['crank_rotation'], a['outcomes']) for a in attempts]
            assert abs(attempts[-1]['state']['transmission.result.ones.turn']-189.6) < 1e-10
            report['stopped_view'] = page.evaluate('''async () => {
                curta.run().pause();
                const keep = new Set([
                    'carry_mechanism.tens_bell.tens_bell_1',
                    'transmission.result.ones.p_10221_1']);
                function visit(node) {
                    const path = node.path.join('.');
                    if (keep.has(path)) return;
                    if (path && ![...keep].some(name => name.startsWith(path+'.'))) {
                        curta.setVisible(node.path, false);
                    } else node.children.forEach(visit);
                }
                visit(curta.assembly());
                curta.setView({camera:[85,-35,0], target:[34,0,-23]});
                await new Promise(requestAnimationFrame);
                await new Promise(requestAnimationFrame);
                return {navigation:curta.navigation(), view:curta.view()};
            }''')
            report['page_errors'] = errors
            assert not errors, errors
            (build/'acceptance.json').write_text(json.dumps(report, indent=2)+'\n')
            page.screenshot(path=str(build/'stopped-lockout.png'), timeout=60000)
            print(json.dumps({key: report[key] for key in (
                'bundle_sha256', 'document_sha256', 'version', 'assembly_paths',
                'controls', 'tree_controls_bank_unchanged', 'page_errors')}
                | {'host_stop': host['stopped']['crank_rotation'],
                   'pointer_stop': attempts[-1]['state']['crank_rotation'],
                   'replay': host['replay']}), flush=True)
        finally:
            browser.close()


if __name__ == '__main__':
    main()
