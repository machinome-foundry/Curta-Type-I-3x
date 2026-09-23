"""Actual exported reverser admission through the public hosted viewer.

The independent Python oracle uses the same explicit requests and preserves
every coordinate's IEEE bits. Pointer setup uses a saved prepared state, then
only the actual visible part is dragged. This is not standalone coverage or a
continuous geometry certificate. Every report path must be new.
"""

import argparse
import hashlib
import json
import logging
import math
from pathlib import Path
import struct
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright


EXPECTED_STATUSES = ['completed', 'completed', 'blocked', 'blocked', 'blocked',
                     'completed', 'completed', 'completed', 'completed']


def bank_bits(bank):
    return {name: struct.pack('>d', float(value)).hex() for name, value in bank.items()}


def python_oracle(model, cases=None):
    from machinome.simulation import Sim

    sim = Sim(model(), dt=1/240, meshes=False)
    initial = sim.snapshot()
    cases = [] if cases is None else cases

    def move(label, name, target):
        request = sim.move(name, to=target)
        cases.append(dict(label=label, status=request.status,
                          bank=dict(sim.state), bits=bank_bits(sim.state)))
        print(json.dumps(dict(python_case=label, status=request.status,
            crank=sim.state['crank_rotation'], lever=sim.state['reverser_height'])), flush=True)

    move('prepare', 'crank_rotation', 90)
    prepared = sim.snapshot()
    move('precontact', 'reverser_height', 1.0675)
    sim.restore(prepared)
    move('blocked', 'reverser_height', -3)
    stopped = sim.snapshot()
    move('retry', 'reverser_height', -3)
    assert sim.snapshot() == stopped
    sim.restore(prepared)
    move('replay', 'reverser_height', -3)
    assert sim.snapshot() == stopped
    move('relief', 'reverser_height', 3.9075)
    assert sim.snapshot() == prepared
    sim.restore(initial)
    move('reverse-first', 'reverser_height', -4.9425)
    move('alternate-crank', 'crank_rotation', 90)
    move('alternate-withdrawal', 'reverser_height', 3.9075)
    # The ideal decimal angle is not exactly representable after graph
    # arithmetic. Runtime-to-runtime bank comparisons below remain bit-exact.
    assert math.isclose(sim.state['transmission.turns.ones.turn'], 231.6,
                        rel_tol=0, abs_tol=1e-9)
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--trial', action='store_true')
    parser.add_argument('--capture-timeout-seconds', type=float, default=180,
                        help='Screenshot readback cap; does not change command deadlines')
    args = parser.parse_args()
    assert not args.report.exists(), 'Preserve previous acceptance reports'
    assert 0 < args.capture_timeout_seconds <= 1200
    build = args.build.resolve()
    raw = (build/'manifest.json').read_bytes()
    document = json.loads(raw)
    if args.trial:
        from simulation.reverser_compiled_trial import CompiledReverserTrial as model
    else:
        from simulation.running import OperatingCurta as model
    viewer = json.loads(subprocess.check_output(
        [sys.executable, '-m', 'machinome_viewer', 'describe'], text=True))
    bundle = Path(viewer['path']).read_bytes()
    report = dict(validation='pending', errors=[], cases=[], pointer_attempts=[],
        model=model.__name__, viewer=viewer, coverage='hosted retained requests and wrong-order pointer',
        program_identity=document['program']['identity'],
        expected_statuses=EXPECTED_STATUSES,
        capture_timeout_seconds=args.capture_timeout_seconds,
        document_sha256=hashlib.sha256(raw).hexdigest(),
        bundle_sha256=hashlib.sha256(bundle).hexdigest())
    try:
        report['python'] = []
        python_oracle(model, report['python'])
        print(json.dumps(dict(python_cases=len(report['python']))), flush=True)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=[
                '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'])
            try:
                page = browser.new_page(viewport=dict(width=1200, height=900))
                page.set_default_timeout(120_000)
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
                        route.fulfill(status=404, body='Missing local reverser asset')

                page.route('http://curta-reverser.test/**', serve)
                page.goto('http://curta-reverser.test/')
                page.add_script_tag(content=bundle.decode())
                report['dt'] = page.evaluate('''async () => {
                    window.curta=await MachinomeViewer.mount('#view','manifest.json',{
                        autoplay:false,partControls:'inline'});
                    window.bits=bank=>Object.fromEntries(Object.entries(bank).map(([name,value])=>{
                        const view=new DataView(new ArrayBuffer(8)); view.setFloat64(0,value,false);
                        return [name,view.getBigUint64(0,false).toString(16).padStart(16,'0')];
                    }));
                    window.initial=await curta.run().snapshot();
                    return curta.run().dt();
                }''')
                assert report['dt'] == 1/240
                report['cases'] = page.evaluate('''async () => {
                    const run=curta.run(), cases=[];
                    const move=async(label,input,to)=>{
                        const result=await run.move(input,{to});
                        const bank=run.state();
                        cases.push({label,status:result.at(-1).status,bank,bits:bits(bank)});
                    };
                    await move('prepare','crank_rotation',90);
                    window.prepared=await run.snapshot();
                    await move('precontact','reverser_height',1.0675);
                    await run.restore(prepared);
                    await move('blocked','reverser_height',-3);
                    await move('retry','reverser_height',-3);
                    await run.restore(prepared);
                    await move('replay','reverser_height',-3);
                    await move('relief','reverser_height',3.9075);
                    await run.restore(initial);
                    await move('reverse-first','reverser_height',-4.9425);
                    await move('alternate-crank','crank_rotation',90);
                    await move('alternate-withdrawal','reverser_height',3.9075);
                    return cases;
                }''')
                for actual, expected in zip(report['cases'], report['python'], strict=True):
                    for key in ('label', 'status', 'bits'):
                        assert actual[key] == expected[key], (actual['label'], key)
                print(json.dumps(dict(browser_cases=len(report['cases']), exact_bank_parity=True)), flush=True)

                from simulation.tools.operating_pointer_matrix import wait_for_gesture
                passed = False
                for dx, dy in ((0, 100), (100, 0), (0, -100), (-100, 0)):
                    page.evaluate('''async () => {
                        await curta.run().restore(prepared); window.pointerOutcomes=[];
                        window.pointerRelease={observed:false};
                    }''')
                    point = None
                    for z in (60, -160):
                        for n in range(8):
                            camera = [320*math.cos(n*math.pi/4), 320*math.sin(n*math.pi/4), z]
                            control = page.evaluate('''async camera => {
                                curta.setView({camera,target:[0,0,-40]});
                                await new Promise(requestAnimationFrame);
                                await new Promise(requestAnimationFrame);
                                return curta.controls().find(c=>c.name==='reverse counter');
                            }''', camera)
                            if not control or not control['point']:
                                continue
                            page.mouse.move(control['point']['x'], control['point']['y'])
                            point = page.evaluate('''async () => {
                                await new Promise(requestAnimationFrame);
                                await new Promise(requestAnimationFrame);
                                return curta.controls().find(c=>c.name==='reverse counter').gesturePoint;
                            }''')
                            if point:
                                break
                        if point:
                            break
                    assert point, 'No reachable actual reversing-lever control'
                    page.evaluate('''() => {
                        window.removeOutcome?.();
                        window.removeOutcome=curta.run().onOutcome(row=>pointerOutcomes.push(row));
                        window.addEventListener('pointerup',()=>pointerRelease.observed=true,{once:true});
                    }''')
                    page.mouse.move(point['x'], point['y'])
                    page.mouse.down()
                    page.mouse.move(point['x']+dx, point['y']+dy, steps=12)
                    page.mouse.up()
                    snapshot = wait_for_gesture(page, 'reverser_height')
                    row = page.evaluate('''() => ({outcomes:pointerOutcomes,release:pointerRelease,
                        bank:curta.run().state(),bits:bits(curta.run().state())})''')
                    row.update(gesture=dict(point=point, dx=dx, dy=dy), commands=snapshot['commands'])
                    report['pointer_attempts'].append(row)
                    print(json.dumps(dict(pointer_attempt=len(report['pointer_attempts']),
                        height=row['bank']['reverser_height'],
                        statuses=[r['status'] for r in row['outcomes']])), flush=True)
                    assert row['release']['observed'] and not row['commands']
                    assert not any(r['status'] == 'refused' for r in row['outcomes'])
                    before = report['python'][0]['bits']
                    for name in document['drivers']:
                        if name != 'reverser_height':
                            assert row['bits'][name] == before[name], name
                    for name in before:
                        if name.endswith('.turn'):
                            assert row['bits'][name] == before[name], name
                    if row['bank']['reverser_height'] == 3.9075:
                        continue
                    assert 1.0575 <= row['bank']['reverser_height'] < 3.9075
                    assert any(r['input'] == 'reverser_height' and r['status'] == 'blocked'
                               for r in row['outcomes'])
                    passed = True
                    break
                assert passed, 'No terminal wrong-order pointer stop observed'
                assert not report['errors'], report['errors']
                page.screenshot(path=str(args.report.with_suffix('.png')),
                                timeout=args.capture_timeout_seconds * 1000)
                # Keep unexpected statuses as diagnostic evidence through the
                # paired browser replay, but never mark the report accepted.
                assert [c['status'] for c in report['python']] == EXPECTED_STATUSES, [
                    (c['label'], c['status']) for c in report['python']]
                report['validation'] = 'passed'
            finally:
                browser.close()
    except Exception as error:
        report['validation'] = 'failed'
        report['failure'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        args.report.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
