"""Finite local browser check of the inspection's real sliders and buttons."""

import json
import re
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright


def main():
    build = Path('_build/reverser_inspection').resolve()
    description = json.loads(subprocess.check_output(
        [sys.executable, '-m', 'machinome_viewer', 'describe'], text=True))
    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'])
        try:
            page = browser.new_page(viewport={'width': 1500, 'height': 1000})
            page.set_default_timeout(30000)
            page.on('pageerror', lambda error: errors.append(str(error)))

            def serve(route):
                name = unquote(urlsplit(route.request.url).path).lstrip('/')
                if not name:
                    route.fulfill(content_type='text/html', body=(
                        '<html><body style="margin:0"><div id="view" '
                        'style="width:1500px;height:1000px"></div></body></html>'))
                    return
                asset = (build / name).resolve()
                if asset.is_relative_to(build) and asset.is_file():
                    route.fulfill(path=asset)
                else:
                    route.fulfill(status=404, body='Missing fixture asset')

            page.route('http://inspection.test/**', serve)
            page.goto('http://inspection.test/')
            page.add_script_tag(path=description['path'])
            page.evaluate('''async () => {
                window.inspector = await MachinomeViewer.mountInspector(
                    '#view', 'viewer.json', {autoplay: false, sidebar: 'open'});
                window.view = inspector.viewer;
                view.setView({camera: [105, 75, -20], target: [-8, 30, -49]});
            }''')
            def values():
                return page.get_by_role('slider').evaluate_all(
                    '(inputs) => Object.fromEntries(inputs.map(x => '
                    '[x.getAttribute("aria-label").split(" ")[0], Number(x.value)]))')

            def expect_values(expected):
                page.wait_for_function('''expected => Object.entries(expected).every(([name, v]) => {
                    const input = [...document.querySelectorAll('input[type=range]')].find(
                        x => x.getAttribute('aria-label').startsWith(name + ' '));
                    return input && Math.abs(Number(input.value) - v) < 1e-8;
                })''', arg=expected)

            assert page.get_by_role('slider').count() == 4
            expect_values({'lever_height': -6.8425, 'gear_offset': .185,
                           'drum_angle': 101.25, 'pinion_probe': 0})
            for name in ('drum_angle', 'gear_offset', 'lever_height', 'pinion_probe'):
                before = values()
                page.get_by_role('slider', name=name + ' ', exact=False).press('ArrowRight')
                after = values()
                assert after[name] != before[name], (name, before, after)
                assert all(after[k] == v for k, v in before.items() if k != name)
            for button, expected in (
                    ('Lower centre', {'lever_height': -6.8425, 'gear_offset': 0}),
                    ('Best slot play', {'lever_height': -6.8425, 'gear_offset': .185}),
                    ('Align teeth - unseated', {'lever_height': -5.035, 'gear_offset': .185}),
                    ('Probe -12 deg', {'pinion_probe': -12}),
                    ('Probe zero', {'pinion_probe': 0}),
                    ('Best slot play', {'lever_height': -6.8425, 'pinion_probe': 0})):
                page.get_by_role('button').filter(has_text=re.compile('^' + re.escape(button) + '$')).click()
                expect_values(expected)
            page.screenshot(path='_build_running/reverser-inspection-browser.png')
            # Use the actual navigation controls the pilot will use, not a
            # custom page or hand-edited viewer document.
            page.get_by_role('checkbox', name='Visibility for detent', exact=True).uncheck()
            page.get_by_role('checkbox', name='Visibility for fork', exact=True).uncheck()
            page.evaluate('''() => view.setView({
                camera: [100, 80, -49], target: [-10, 32, -49]})''')
            page.screenshot(path='_build_running/reverser-inspection-gap-browser.png')
            page.get_by_role('button').filter(has_text=re.compile('^Align teeth - unseated$')).click()
            expect_values({'lever_height': -5.035})
            page.screenshot(path='_build_running/reverser-inspection-aligned-browser.png')
            print(json.dumps({'sliders': 4, 'preset_buttons': 5,
                              'navigation': page.evaluate('() => view.navigation()'),
                              'final_values': values(), 'page_errors': errors}), flush=True)
            assert not errors, errors
        except Exception:
            print(json.dumps({'page_errors': errors,
                              'buttons': page.get_by_role('button').all_text_contents(),
                              'body': page.locator('body').inner_text()}), flush=True)
            page.screenshot(path='_build_running/reverser-inspection-browser-failure.png')
            raise
        finally:
            browser.close()


if __name__ == '__main__':
    main()
