"""All requested controls through an unmodified standalone page's visible UI.

No mount handle, host movement, camera API or coordinate-bank setter is used.
Reset and camera orbit are ordinary visible-page setup between pointer cases.
Acceptance covers terminal UI outcomes and four-decimal input readouts; the
separate hosted matrix checks the full bank and command retirement.
"""

import argparse
import hashlib
import json
from pathlib import Path
from time import monotonic
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright
from simulation.tools.operating_standalone_probe import readouts, validate_report


def validate_matrix(required, cases, errors):
    assert required and len(set(required)) == len(required)
    assert not errors, errors
    assert len(cases) == len(required)
    assert {row['control'] for row in cases} == set(required)
    assert all(row['validation'] == 'passed' for row in cases)


def frames(page):
    page.evaluate('''async()=>{
        await new Promise(requestAnimationFrame);
        await new Promise(requestAnimationFrame);
    }''')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--controls', nargs='+', help='Defaults to every declared control')
    parser.add_argument('--views', type=int, default=6)
    args = parser.parse_args()
    assert not args.report.exists(), 'preserve earlier evidence'
    assert 1 <= args.views <= 8
    build = args.build.resolve()
    document = json.loads((build/'manifest.json').read_text())
    required = args.controls or list(document['controls'])
    assert required and set(required) <= set(document['controls'])
    report = dict(validation='pending', errors=[], cases=[], attempts=[], searches=[],
                  required=required, camera_drags=[],
                  coverage='unmodified standalone; visible UI outcomes and four-decimal inputs',
                  program_identity=document['program']['identity'],
                  asset_sha256={name: hashlib.sha256((build/name).read_bytes()).hexdigest()
                      for name in ('manifest.json', 'index.html', 'machinome-viewer.js')})
    started = monotonic()

    def checkpoint(stage):
        report['elapsed_seconds'] = monotonic()-started
        args.report.write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(dict(stage=stage, elapsed_seconds=report['elapsed_seconds'],
                              passed=len(report['cases']), required=len(required))), flush=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'])
        try:
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            page.set_default_timeout(60_000)
            page.on('pageerror', lambda error: report['errors'].append(str(error)))

            def serve(route):
                asset = (build/unquote(urlsplit(route.request.url).path).lstrip('/')).resolve()
                if asset.is_relative_to(build) and asset.is_file():
                    route.fulfill(path=asset)
                else:
                    route.fulfill(status=404, body='Missing contained standalone asset')

            page.route('http://curta-standalone.test/**', serve)
            page.goto('http://curta-standalone.test/index.html?autoplay=0')
            page.wait_for_selector('.run-input[data-input]', state='attached')
            canvas = page.locator('#machinome-viewer .machinome-inspector-viewer canvas')
            canvas.wait_for()
            initial = readouts(page)
            assert set(initial) == set(document['drivers'])
            report['initial'] = initial
            report['canvas'] = canvas.bounding_box()
            checkpoint('page_ready')

            def reset():
                page.get_by_role('button', name='Reset the run to its initial state', exact=True).click()
                deadline = monotonic()+60
                while monotonic() < deadline:
                    frames(page)
                    if readouts(page) == initial:
                        return
                raise AssertionError('Visible Reset did not restore every input')

            def hover(point):
                page.mouse.move(*point)
                frames(page)
                # Overlay titles must not masquerade as a new scene hit.
                on_canvas = page.evaluate('''({x,y})=>document.elementFromPoint(x,y) ===
                    document.querySelector('#machinome-viewer .machinome-inspector-viewer canvas')''',
                    dict(x=point[0], y=point[1]))
                return (canvas.get_attribute('title') or '') if on_canvas else ''

            def exercise(name, point, view):
                report['active_control'] = name
                checkpoint('starting '+name)
                control = document['controls'][name]
                press = control['kind'] == 'button'
                if press:
                    relative = document['instructions'][control['instruction']]['by']
                    assert relative == {'crank_rotation': 360}, 'Expected crank-only instruction'
                    input_name = 'crank_rotation'
                else:
                    input_name = control['input']
                for dx, dy in ((0, 60), (60, 0), (0, -60), (-60, 0)):
                    reset()
                    title = hover(point)
                    if name not in title.split(' · '):
                        return False
                    x, y = point
                    handle = page.get_by_role('button', name=name, exact=True)
                    if not press and handle.count():
                        box = handle.bounding_box()
                        x, y = box['x']+box['width']/2, box['y']+box['height']/2
                    before = readouts(page)
                    page.evaluate('''()=>{
                        window.standaloneRelease=false;
                        window.addEventListener('pointerup', event=>{
                            if(event.composedPath().includes(document.querySelector('#machinome-viewer')))
                                standaloneRelease=true;
                        },{once:true});
                    }''')
                    page.mouse.move(x, y)
                    page.mouse.down()
                    if not press:
                        page.mouse.move(x+dx, y+dy, steps=12)
                    page.mouse.up()
                    outcome = page.evaluate('''async ({name,instruction})=>{
                        const row=instruction
                            ? [...document.querySelectorAll('.run-instruction-control')]
                                .find(row=>row.dataset.instruction===instruction)
                            : [...document.querySelectorAll('.run-input')]
                                .find(row=>row.dataset.input===name);
                        const started=performance.now();
                        while(performance.now()-started<1200000) {
                            const text=row.querySelector('.run-outcome').textContent;
                            if(standaloneRelease && (text==='completed'||text==='refused'||text.startsWith('blocked after '))) {
                                await new Promise(requestAnimationFrame);
                                await new Promise(requestAnimationFrame);
                                if(row.querySelector('.run-outcome').textContent===text) return text;
                            }
                            // No angular quantum is an unsuccessful search
                            // direction, never accepted pointer coverage.
                            if(standaloneRelease && !text && performance.now()-started>3000) return '';
                            await new Promise(resolve=>setTimeout(resolve,100));
                        }
                        throw Error('No terminal visible outcome after pointer release');
                    }''', dict(name=input_name, instruction=control.get('instruction')))
                    row = dict(control=name, input=input_name, hover=title,
                               declared_inputs=list(document['drivers']), errors=list(report['errors']),
                               release_observed=page.evaluate('standaloneRelease'), outcome=outcome,
                               before=before, after=readouts(page), view=view,
                               hover_point=list(point), gesture=dict(point=[x, y],
                                   drag=None if press else [dx, dy]))
                    report['attempts'].append(row)
                    assert not row['errors'] and row['release_observed']
                    assert outcome != 'refused', row
                    assert all(row['after'][key] == value for key, value in before.items()
                               if key != input_name), 'Unrelated visible input moved'
                    if row['after'][input_name] == before[input_name]:
                        continue
                    if input_name == 'crank_rotation':
                        if press:
                            row['expected_delta'] = 360
                        else:
                            row['partial_turn'] = True
                            if float(row['after'][input_name]) <= float(before[input_name]):
                                continue
                    validate_report(row)
                    row['validation'] = 'passed'
                    report['cases'].append(row)
                    checkpoint('passed '+name)
                    return True
                return False

            for view in range(args.views):
                if len(report['cases']) == len(required):
                    break
                reset()
                if view:
                    start = (1130, 150)
                    assert not hover(start), 'Orbit must start off a controlled part'
                    page.mouse.down()
                    page.mouse.move(start[0]+200, start[1], steps=12)
                    page.mouse.up()
                    frames(page)
                    assert readouts(page) == initial, 'Camera drag moved an input'
                    report['camera_drags'].append(dict(point=list(start), by=[200, 0]))
                # These are inspected screen locations plus ordinary hover
                # searches, not synthetic part hits or projected host points.
                seeds = [(897, 331), (840, 250), (736, 500), (596, 550)]
                seeds += [(x, y) for x, y in ((730,410),(748,408),(766,405),(785,402),(801,400),
                                              (728,767),(743,769),(760,770),(777,770),(792,768))]
                seeds += [(x, y) for y in (600, 620, 640, 660, 680)
                          for x in (610, 650, 690, 730, 770, 810, 850)]
                for point in seeds:
                    reset()
                    title = hover(point)
                    report['searches'].append(dict(view=view, point=list(point), title=title))
                    completed = {row['control'] for row in report['cases']}
                    for name in title.split(' · '):
                        if name in required and name not in completed:
                            exercise(name, point, view)
                    if len(report['cases']) == len(required):
                        break
                checkpoint('view '+str(view))
            validate_matrix(required, report['cases'], report['errors'])
            page.screenshot(path=str(args.report.with_suffix('.png')), timeout=180_000)
            report['validation'] = 'passed'
        except Exception as error:
            report['validation'] = 'failed'
            report['failure'] = f'{type(error).__name__}: {error}'
            report['unreached'] = sorted(set(required)-{row['control'] for row in report['cases']})
            if 'page' in locals():
                page.screenshot(path=str(args.report.with_suffix('.png')), timeout=180_000)
            raise
        finally:
            browser.close()
            checkpoint(report['validation'])


if __name__ == '__main__':
    main()
