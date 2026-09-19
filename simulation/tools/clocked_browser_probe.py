"""Finite browser smoke of the real clocked build and selected viewer bundle.

Use framework/viewer checkouts containing clocked-machine on PYTHONPATH.
Serves fixtures through Playwright interception: no persistent HTTP server.
"""

import argparse
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright
from simulation.clocked_cases import SCENARIOS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, default=Path('_build/clocked_curta'))
    parser.add_argument('--screenshot', type=Path,
                        default=Path('snapshot-clocked-browser.png'))
    args = parser.parse_args()
    build = args.build.resolve()
    viewer = json.loads(subprocess.check_output(
        [sys.executable, '-m', 'machinome_viewer', 'describe'], text=True))
    assert 8 in viewer['documentVersions'], viewer
    errors = []
    oracle = json.loads(Path(__file__).parents[1].joinpath('clocked_oracle.json').read_text())
    excluded = {'mid_stroke_carriage_shift', 'mid_stroke_reversing_lever',
                'mid_stroke_carriage_lift_and_sweep', 'crank_reversal',
                'sweep_stopped_between_teeth'}
    scenarios = {name: actions for name, actions in SCENARIOS.items() if name not in excluded}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'])
        page = browser.new_page(viewport={'width': 1200, 'height': 900})
        page.set_default_timeout(180000)
        page.on('pageerror', lambda error: errors.append(str(error)))

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
                route.fulfill(status=404, body='Missing fixture asset')

        page.route('http://clocked.test/**', serve)
        page.goto('http://clocked.test/')
        page.add_script_tag(path=viewer['path'])
        page.evaluate('''async () => {
            window.curta = await MachinomeWidget.mount('#view', 'viewer.json', {
                autoplay: false,
            });
        }''')
        result = page.evaluate('''({scenarios, oracle}) => {
            const machine = curta.machine();
            const check = (ok, message) => { if (!ok) throw Error(message); };
            const reading = (counter = false) => {
                const state = machine.state();
                const prefix = counter ? 'turns' : 'result';
                return Array.from({length: counter ? 6 : 11}, (_, place) =>
                    state[`${prefix}_${place}.value`] * 10 ** place)
                    .reduce((a, b) => a + b, 0);
            };
            check(machine !== null, 'No clocked machine handle');
            const names = {crank: 'crank_rotation', crank_lift: 'crank_elevation',
                carriage_lift: 'carriage_elevation', carriage_turn: 'carriage_rotation',
                ring: 'clearing_rotation'};
            let oracleReads = 0;
            for (const [name, actions] of Object.entries(scenarios)) {
                machine.reset();
                const readings = Object.fromEntries(oracle.scenarios[name].readings
                    .filter(row => row.label).map(row => [row.label, row]));
                for (const [kind, value] of actions) {
                    if (kind === 'digits') {
                        for (const [index, digit] of Object.entries(value))
                            machine.move(`digit_${index}`, {to: digit});
                    } else if (kind === 'read') {
                        if (machine.state().crank_rotation % 360 === 0) {
                            const expected = readings[value];
                            check(reading() === expected.result && reading(true) === expected.turns,
                                  `Oracle mismatch: ${name}/${value}`);
                            oracleReads++;
                        }
                    } else {
                        machine.move(names[kind],
                            kind === 'crank' || kind === 'ring' ? {by: value} : {to: value});
                    }
                }
            }
            machine.reset();
            machine.move('crank_rotation', {to: 34.5});
            machine.move('crank_rotation', {by: -360});
            const tooth = machine.state().crank_rotation;
            check(Math.abs(tooth - 357 * 11 / 116) < 1e-10, 'Ratchet tooth landing');
            check(machine.move('crank_rotation', {by: -360}).admitted === 0,
                  'Repeated reverse request forgot the captured tooth');
            machine.reset();
            machine.move('digit_1', {to: 9});
            machine.move('crank_rotation', {by: 90});
            check(reading() === 0, 'Partial stroke committed too early');
            check(machine.move('carriage_elevation', {to: 6}).admitted === 0,
                  'Mid-stroke carriage lift was not blocked');
            machine.move('crank_rotation', {by: 270});
            check(reading() === 9 && reading(true) === 1, 'First addition');
            machine.move('crank_rotation', {by: 720});
            check(reading() === 27 && reading(true) === 3, 'Repeated additions');
            const saved = machine.snapshot();
            machine.move('carriage_elevation', {to: 6});
            machine.move('clearing_rotation', {to: 230});
            check(reading() === 0 && reading(true) === 3, 'Result-bank clear');
            machine.move('clearing_rotation', {to: 360});
            check(reading() === 0 && reading(true) === 0, 'Counter-bank clear');
            machine.restore(saved);
            check(reading() === 27 && reading(true) === 3, 'Restore');
            const final = machine.snapshot();
            const samples = [];
            for (let index = 0; index < 20; index++) {
                const start = performance.now();
                machine.move('crank_rotation', {by: 360});
                samples.push(performance.now() - start);
            }
            check(reading() === 207 && reading(true) === 23, 'Timed additions');
            const start = performance.now();
            for (let index = 0; index < 20; index++)
                machine.move('crank_rotation', {by: 18});
            const stroke20PosesMs = performance.now() - start;
            check(reading() === 216 && reading(true) === 24, 'Timed partial poses');
            machine.restore(final);
            const sorted = [...samples].sort((a, b) => a - b);
            return {result: reading(), counter: reading(true),
                    drivers: Object.keys(machine.drivers()).length,
                    states: Object.keys(machine.states()).length,
                    oracleScenarios: Object.keys(scenarios).length, oracleReads,
                    strokeMedianMs: (sorted[9] + sorted[10]) / 2,
                    stroke20PosesMs, strokeSamplesMs: samples};
        }''', {'scenarios': json.loads(json.dumps(scenarios)), 'oracle': oracle})
        page.screenshot(path=str(args.screenshot))
        browser.close()
    assert not errors, errors
    print(json.dumps({'viewer': viewer, 'verified': result,
                      'screenshot': str(args.screenshot)}, indent=2))


if __name__ == '__main__':
    main()
