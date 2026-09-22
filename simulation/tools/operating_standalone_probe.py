"""Real pointer probe of an unmodified auto-mounted standalone export.

Uses only visible DOM and pointer events: never remounts, obtains a hidden run
handle or issues host movement calls. Four-decimal input readouts and terminal
UI outcomes are evidence at that precision, not a full retained-bank proof.
Hosted tests separately inspect pending commands and the complete coordinate bank.
"""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright


def validate_report(report):
    assert not report['errors'], report['errors']
    assert report['control'] in report['hover'].split(' · ')
    assert report['release_observed']
    assert report['outcome'] == 'completed' or report['outcome'].startswith('blocked after ')
    before, after = report['before'], report['after']
    assert set(before) == set(after) == set(report['declared_inputs'])
    assert float(after[report['input']]) != float(before[report['input']])
    if report.get('partial_turn'):
        assert 0 < float(after[report['input']])-float(before[report['input']]) < 360
    if report.get('expected_delta') is not None:
        assert float(after[report['input']])-float(before[report['input']]) == report['expected_delta']
    for name in before:
        if name != report['input']:
            assert after[name] == before[name], ('unrelated visible input movement', name)


def readouts(page):
    return page.eval_on_selector_all('.run-input[data-input]', '''rows =>
        Object.fromEntries(rows.map(row=>[row.dataset.input,
            row.querySelector('.run-readout-value').textContent]))''')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path)
    parser.add_argument('--control', required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--point', nargs=2, type=float)
    parser.add_argument('--orbit', nargs=2, type=float,
                        help='Public camera drag on empty canvas before the hover search')
    parser.add_argument('--drag', nargs=2, type=float, default=(0, -60))
    parser.add_argument('--press', action='store_true', help='Click the actual button-bearing part')
    parser.add_argument('--expected-delta', type=float)
    parser.add_argument('--partial-turn', action='store_true',
                        help='Require a positive visible crank delta below 360 degrees, not a timing-specific quantum')
    parser.add_argument('--deadline-seconds', type=float, default=120)
    args = parser.parse_args()
    assert not args.report.exists(), 'preserve earlier reports'
    build = args.build.resolve()
    manifest = json.loads((build/'manifest.json').read_text())
    assert args.control in manifest['controls']
    assert args.input in manifest['drivers']
    assert 0 < args.deadline_seconds <= 1200
    control = manifest['controls'][args.control]
    assert (control['kind'] == 'button') == args.press
    if args.partial_turn:
        assert args.input == 'crank_rotation' and not args.press
    report = dict(validation='pending', errors=[], control=args.control, input=args.input,
                  declared_inputs=list(manifest['drivers']),
                  coverage='unmodified standalone page; visible input readouts at four decimals',
                  program_identity=manifest['program']['identity'],
                  expected_delta=args.expected_delta, deadline_seconds=args.deadline_seconds,
                  partial_turn=args.partial_turn,
                  asset_sha256={name: hashlib.sha256((build/name).read_bytes()).hexdigest()
                      for name in ('manifest.json', 'index.html', 'machinome-viewer.js')})
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'])
        try:
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            page.set_default_timeout(60_000)
            page.on('pageerror', lambda error: report['errors'].append(str(error)))

            def serve(route):
                name = unquote(urlsplit(route.request.url).path).lstrip('/')
                asset = (build/name).resolve()
                if asset.is_relative_to(build) and asset.is_file():
                    route.fulfill(path=asset)
                else:
                    route.fulfill(status=404, body='Missing contained standalone asset')

            page.route('http://curta-standalone.test/**', serve)
            page.goto('http://curta-standalone.test/index.html?autoplay=0')
            page.wait_for_selector('.run-input[data-input]', state='attached')
            canvas = page.locator('#machinome-viewer .machinome-inspector-viewer canvas')
            canvas.wait_for()
            report['before'] = readouts(page)
            assert set(report['before']) == set(report['declared_inputs'])
            report['instruction_rows'] = page.locator('.run-instruction-control').count()
            rectangle = canvas.bounding_box()
            report['canvas'] = rectangle
            if args.orbit:
                ox = rectangle['x'] + rectangle['width']*.9
                oy = rectangle['y'] + rectangle['height']*.15
                page.mouse.move(ox, oy)
                page.evaluate('''async()=>{await new Promise(requestAnimationFrame);}''')
                assert not canvas.get_attribute('title'), 'Orbit must start off a controlled part'
                page.mouse.down()
                page.mouse.move(ox+args.orbit[0], oy+args.orbit[1], steps=20)
                page.mouse.up()
                page.evaluate('''async()=>{
                    await new Promise(requestAnimationFrame);
                    await new Promise(requestAnimationFrame);
                }''')
                assert readouts(page) == report['before'], 'Camera drag moved an input'
                report['camera_drag'] = dict(point=[ox, oy], by=args.orbit)
            # Hover-only search is public nearest-hit picking. Stop as soon as
            # the real canvas names this control; never synthesize a part hit.
            candidates = ([args.point] if args.point else
                [(rectangle['x'] + rectangle['width']*x,
                  rectangle['y'] + rectangle['height']*y)
                 for y in ((.62, .64, .66, .68, .60, .70, .58, .72)
                           if args.input.startswith('digit_') else
                           (.2, .3, .4, .5, .6, .7, .8, .1, .9))
                 for x in (.5, .485, .515, .47, .53, .455, .545, .44,
                           .56, .425, .575, .41, .59, .395, .605)])
            report['hover_attempts'] = []
            for x, y in candidates:
                page.mouse.move(x, y)
                page.evaluate('''async()=>{await new Promise(requestAnimationFrame);}''')
                title = canvas.get_attribute('title') or ''
                report['hover_attempts'].append(dict(point=[x, y], title=title))
                if args.control in title.split(' · '):
                    report['hover'] = title
                    break
            else:
                raise AssertionError('No actual visible hover hit for '+args.control)

            # Select the actual labelled overlapping-freedom handle, if any.
            handle = page.get_by_role('button', name=args.control, exact=True)
            if handle.count():
                box = handle.bounding_box()
                x, y = box['x']+box['width']/2, box['y']+box['height']/2
            report['gesture'] = dict(point=[x, y], drag=None if args.press else args.drag)
            page.evaluate('''()=>{
                window.standaloneRelease=false;
                window.addEventListener('pointerup', event=>{
                    if(event.composedPath().includes(document.querySelector('#machinome-viewer')))
                        standaloneRelease=true;
                }, {once:true});
            }''')
            page.mouse.move(x, y)
            page.mouse.down()
            if not args.press:
                page.mouse.move(x+args.drag[0], y+args.drag[1], steps=12)
            page.mouse.up()
            # Async loop is awaited explicitly, not an async wait_for_function
            # predicate. This observes UI retirement, not hidden command state.
            report['outcome'] = page.evaluate('''async ({name,instruction,seconds})=>{
                const deadline=performance.now()+seconds*1000;
                const row=instruction
                    ? [...document.querySelectorAll('.run-instruction-control')]
                        .find(row=>row.dataset.instruction===instruction)
                    : [...document.querySelectorAll('.run-input')]
                        .find(row=>row.dataset.input===name);
                while(performance.now()<deadline) {
                    const text=row.querySelector('.run-outcome').textContent;
                    if(standaloneRelease && (text==='completed'||text.startsWith('blocked after '))) {
                        await new Promise(requestAnimationFrame);
                        await new Promise(requestAnimationFrame);
                        if(row.querySelector('.run-outcome').textContent===text) return text;
                    }
                    await new Promise(resolve=>setTimeout(resolve,100));
                }
                throw Error('No terminal visible outcome after pointer release: '+name);
            }''', dict(name=args.input, instruction=control.get('instruction'),
                       seconds=args.deadline_seconds))
            report['release_observed'] = page.evaluate('standaloneRelease')
            report['after'] = readouts(page)
            validate_report(report)
            page.screenshot(path=str(args.report.with_suffix('.png')))
            report['validation'] = 'passed'
        except Exception as error:
            report['failure'] = f'{type(error).__name__}: {error}'
            if 'page' in locals():
                report['failure_readouts'] = readouts(page)
                page.screenshot(path=str(args.report.with_suffix('.png')))
            raise
        finally:
            browser.close()
            args.report.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
