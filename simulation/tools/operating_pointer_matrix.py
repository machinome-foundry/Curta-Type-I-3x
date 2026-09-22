"""Independent selector/marker pointer gates on an ordinary public hosted viewer.

This is not standalone-page coverage, loop coverage, or a geometry certificate.
No motion is requested through the host API: reset is separate case setup.
The normal viewer timestep is preserved. Reports include terminal outcomes and
the pending-command bank rather than accepting a mid-gesture readback.
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


INPUTS = {**{f'digit_{n}': f'set digit {n}' for n in range(1, 9)},
          **{f'marker_{n}_rotation': f'move decimal marker {n}' for n in range(1, 11)}}


def validate_attempt(case):
    name = case['input']
    assert case['release']['observed'], 'viewer pointer release was not observed'
    assert not case['commands'], 'pointer command has not retired'
    assert not any(row['status'] == 'refused' for row in case['outcomes'])
    before, after = case['before'], case['after']
    assert set(before) == set(after)
    assert case['register_coordinates'], 'no register coordinates were checked'
    for key in (*case['drivers'], *case['register_coordinates']):
        if key != name:
            assert after[key] == before[key], (name, 'unrelated motion', key)


def validate_case(case):
    validate_attempt(case)
    name = case['input']
    outcomes = [row for row in case['outcomes'] if row['input'] == name]
    assert outcomes and outcomes[-1]['status'] in ('completed', 'blocked'), outcomes
    assert case['after'][name] != case['before'][name], 'no admitted pointer motion'


def wait_for_gesture(page, name):
    # Playwright's Page.wait_for_function tests Promise truthiness, not the
    # resolved boolean. page.evaluate explicitly awaits this async loop.
    return page.evaluate('''async name => {
        const deadline=performance.now()+120000;
        while(performance.now()<deadline) {
            if(pointerRelease.observed) {
                const snapshot=await curta.run().snapshot();
                if(snapshot.commands.length===0)
                    return snapshot;
            }
            await new Promise(resolve=>setTimeout(resolve,100));
        }
        throw Error('Pointer release/command retirement deadline exceeded: '+name);
    }''', name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--inputs', nargs='+', choices=tuple(INPUTS), default=list(INPUTS))
    args = parser.parse_args()
    assert not args.report.exists(), 'preserve previous acceptance reports'
    build = args.build.resolve()
    document_path = next((build/name for name in ('manifest.json', 'viewer.json')
                          if (build/name).is_file()))
    document = json.loads(document_path.read_text())
    viewer = json.loads(subprocess.check_output(
        [sys.executable, '-m', 'machinome_viewer', 'describe'], text=True))
    bundle = Path(viewer['path']).read_bytes()
    report = {'validation': 'pending', 'errors': [], 'cases': [], 'attempts': [],
              'coverage': 'ordinary-hosted selector/marker pointers; default timestep',
              'program_identity': document['program']['identity'],
              'bundle_sha256': hashlib.sha256(bundle).hexdigest(),
              'document_sha256': hashlib.sha256(document_path.read_bytes()).hexdigest()}
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
                    route.fulfill(status=404, body='Missing local pointer asset')

            page.route('http://curta-pointers.test/**', serve)
            page.goto('http://curta-pointers.test/')
            page.add_script_tag(content=bundle.decode())
            report['dt'] = page.evaluate('''async document => {
                window.curta=await MachinomeViewer.mount('#view',document,{
                    autoplay:false,partControls:'inline'});
                window.pointerOutcomes=[];
                curta.run().onOutcome(row=>pointerOutcomes.push(row));
                return curta.run().dt();
            }''', document_path.name)
            for name in args.inputs:
                report['active_input'] = name
                print(json.dumps({'starting': name}), flush=True)
                control_name = INPUTS[name]
                passed = False
                for dx, dy in ((0, 60), (60, 0), (0, -60), (-60, 0)):
                    before = page.evaluate('''async () => {
                        curta.run().pause(); await curta.run().reset();
                        pointerOutcomes.length=0;
                        return curta.run().state();
                    }''')
                    point = None
                    # Camera-only exploration is ordinary inspection, not a
                    # hidden-part proxy or bypass of nearest-hit picking.
                    views = [None] + [{'camera': [320*math.cos(n*math.pi/4),
                              320*math.sin(n*math.pi/4), z], 'target': [0, 0, -40]}
                              for z in (60, -160) for n in range(8)]
                    for view in views:
                        control = page.evaluate('''async ({view,name}) => {
                            if(view) curta.setView(view);
                            await new Promise(requestAnimationFrame);
                            await new Promise(requestAnimationFrame);
                            return curta.controls().find(c=>c.name===name);
                        }''', {'view': view, 'name': control_name})
                        if not control or not control['point']:
                            continue
                        page.mouse.move(control['point']['x'], control['point']['y'])
                        control = page.evaluate('''async name => {
                            await new Promise(requestAnimationFrame);
                            await new Promise(requestAnimationFrame);
                            return curta.controls().find(c=>c.name===name);
                        }''', control_name)
                        point = control['gesturePoint']
                        if point:
                            break
                    assert point, f'No actual reachable control for {control_name}'
                    page.evaluate('''() => {
                        window.pointerRelease={observed:false};
                        window.addEventListener('pointerup', event=>{
                            if(event.composedPath().includes(document.querySelector('#view')))
                                pointerRelease={observed:true,tick:curta.run().tick(),
                                    outcome_count:pointerOutcomes.length};
                        },{once:true});
                    }''')
                    page.mouse.move(point['x'], point['y'])
                    page.mouse.down()
                    page.mouse.move(point['x']+dx, point['y']+dy, steps=12)
                    page.mouse.up()
                    wait_for_gesture(page, name)
                    case = page.evaluate('''async name => {
                        const snapshot=await curta.run().snapshot();
                        return {input:name,after:snapshot.bank,commands:snapshot.commands,
                            outcomes:[...pointerOutcomes],release:pointerRelease,
                            drivers:Object.keys(curta.drivers()),
                            register_coordinates:Object.keys(snapshot.bank).filter(key=>
                                /\\.(result_register|turns_register)\\..*\\.turn$/.test(key))};
                    }''', name)
                    case.update(before=before, gesture={'point': point, 'dx': dx, 'dy': dy})
                    report['attempts'].append(case)
                    # An axis-aligned drag can submit no angular quantum.
                    # Keep it as a no-op attempt, never as accepted coverage;
                    # a later direction cannot hide unrelated motion/refusal.
                    validate_attempt(case)
                    if case['after'][name] == before[name]:
                        continue
                    validate_case(case)
                    report['cases'].append(case)
                    print(json.dumps({'input': name, 'outcome': case['outcomes'][-1],
                                      'admitted': case['after'][name]-before[name]}), flush=True)
                    passed = True
                    break
                assert passed, f'No admitted terminal pointer movement for {name}'
            assert not report['errors'], report['errors']
            assert len(report['cases']) == len(args.inputs)
            page.evaluate('''async () => {
                curta.run().pause();
                await new Promise(requestAnimationFrame);
                await new Promise(requestAnimationFrame);
            }''')
            page.screenshot(path=str(args.report.with_suffix('.png')))
            report['validation'] = 'passed'
        except Exception as error:
            report['failure'] = f'{type(error).__name__}: {error}'
            try:
                report['failure_context'] = page.evaluate('''async () => ({
                    release:window.pointerRelease, outcomes:window.pointerOutcomes,
                    snapshot:window.curta ? await curta.run().snapshot() : null,
                    controls:window.curta ? curta.controls() : []
                })''')
            except Exception as capture_error:
                report['failure_context_error'] = str(capture_error)
            raise
        finally:
            browser.close()
            args.report.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
