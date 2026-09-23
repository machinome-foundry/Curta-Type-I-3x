"""Actual hosted crank handle and part button, with arithmetic-aware checks.

Only pointers request motion. Public reset is independent case setup; the
normal viewer timestep and declared instruction duration remain unchanged.
This does not certify whole-machine geometry or real-time performance.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright
from simulation.tools.operating_pointer_matrix import checkpoint_report


COUNTER_ONES = 'carriage.registers.turns_register.p_10203_3.turn'


def validate_attempt(case):
    assert case['release_observed'] and case['hit_verified']
    assert not case['commands'] and not case['errors']
    assert not any(row['status'] == 'refused' for row in case['outcomes'])
    before, after = case['before'], case['after']
    assert set(before) == set(after)
    for key in case['drivers']:
        if key != 'crank_rotation':
            assert after[key] == before[key], ('unrelated input', key)


def validate_case(case):
    validate_attempt(case)
    outcomes = [row for row in case['outcomes'] if row['input'] == 'crank_rotation']
    assert outcomes and outcomes[-1]['status'] == 'completed'
    before, after = case['before'], case['after']
    travel = after['crank_rotation']-before['crank_rotation']
    if case['control'] == 'turn crank':
        assert 0 < travel < 360
        return
    assert case['control'] == 'one revolution' and travel == 360
    assert all(before[f'digit_{n}'] == 0 for n in range(1, 9))
    result = [key for key in before if '.result_register.' in key and key.endswith('.turn')]
    counter = [key for key in before if '.turns_register.' in key and key.endswith('.turn')]
    assert len(result) == 11 and len(counter) == 6 and COUNTER_ONES in counter
    assert all(after[key] == before[key] for key in result)
    assert all(after[key] == before[key] for key in counter if key != COUNTER_ONES)
    assert math.isclose(after[COUNTER_ONES]-before[COUNTER_ONES], -36,
                        rel_tol=0, abs_tol=1e-9), 'One zero-entry turn must count once'


def bank_sha256(bank, bits=None):
    digest = hashlib.sha256()
    for key in sorted(bank):
        value = bytes.fromhex(bits[key]) if bits is not None else struct.pack('<d', bank[key])
        digest.update(key.encode()+b'\0'+value)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path)
    args = parser.parse_args()
    assert not args.report.exists(), 'Preserve earlier reports'
    build = args.build.resolve()
    document = json.loads((build/'manifest.json').read_text())
    button = document['controls']['one revolution']
    assert button['kind'] == 'button'
    assert document['instructions'][button['instruction']] == dict(by={'crank_rotation': 360}, duration=2)
    report = dict(validation='pending', errors=[], cases=[], attempts=[], coverage=__doc__.strip(),
                  program_identity=document['program']['identity'],
                  asset_sha256={name: hashlib.sha256((build/name).read_bytes()).hexdigest()
                      for name in ('manifest.json', 'index.html', 'machinome-viewer.js')})
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'])
        try:
            page = browser.new_page(viewport=dict(width=1200, height=900))
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
                    route.fulfill(status=404, body='Missing contained crank asset')

            page.route('http://curta-crank.test/**', serve)
            page.goto('http://curta-crank.test/')
            page.add_script_tag(path=str(build/'machinome-viewer.js'))
            report['initial'] = page.evaluate('''async () => {
                window.curta=await MachinomeViewer.mount('#view','manifest.json',{
                    autoplay:false,partControls:'inline'});
                window.crankOutcomes=[];
                curta.run().onOutcome(row=>crankOutcomes.push(row));
                return {dt:curta.run().dt(),bank:curta.run().state()};
            }''')
            assert report['initial']['dt'] == 1/240
            assert len(report['initial']['bank']) == 216
            checkpoint_report(args.report, report)
            for name in ('turn crank', 'one revolution'):
                press = name == 'one revolution'
                for dx, dy in ((0, 0),) if press else ((0,60),(60,0),(0,-60),(-60,0)):
                    before = page.evaluate('''async () => {
                        curta.run().pause(); await curta.run().reset(); crankOutcomes.length=0;
                        await new Promise(requestAnimationFrame);
                        await new Promise(requestAnimationFrame);
                        return curta.run().state();
                    }''')
                    assert before == report['initial']['bank']
                    control = page.evaluate('name=>curta.controls().find(c=>c.name===name)', name)
                    assert control and control['point'], name
                    origin = control['point']
                    page.mouse.move(origin['x'], origin['y'])
                    control = page.evaluate('''async name => {
                        await new Promise(requestAnimationFrame);
                        await new Promise(requestAnimationFrame);
                        return curta.controls().find(c=>c.name===name);
                    }''', name)
                    point = control['point'] if press else control['gesturePoint']
                    assert point, name
                    hover = page.locator('#view canvas').get_attribute('title') or ''
                    assert name in hover.split(' · '), (name, hover)
                    page.evaluate('''()=>{
                        window.crankReleased=false;
                        window.addEventListener('pointerup',e=>{
                            if(e.composedPath().includes(document.querySelector('#view')))
                                crankReleased=true;
                        },{once:true});
                    }''')
                    print(json.dumps(dict(starting=name, point=point, drag=[dx,dy])), flush=True)
                    page.mouse.move(point['x'], point['y'])
                    page.mouse.down()
                    if not press:
                        page.mouse.move(point['x']+dx, point['y']+dy, steps=12)
                    page.mouse.up()
                    data = page.evaluate('''async () => {
                        const start=performance.now();
                        while(performance.now()-start<1200000) {
                            const snapshot=await curta.run().snapshot();
                            if(crankReleased && snapshot.commands.length===0 &&
                               (crankOutcomes.length || performance.now()-start>3000)) {
                                const bits=Object.fromEntries(Object.entries(snapshot.bank).map(([key,value])=>{
                                    const data=new DataView(new ArrayBuffer(8)); data.setFloat64(0,value,true);
                                    return [key,[...new Uint8Array(data.buffer)]
                                        .map(byte=>byte.toString(16).padStart(2,'0')).join('')];
                                }));
                                return {after:snapshot.bank,commands:snapshot.commands,
                                    tick:snapshot.tick,outcomes:[...crankOutcomes],
                                    release_observed:crankReleased,bank_bits:bits};
                            }
                            await new Promise(resolve=>setTimeout(resolve,100));
                        }
                        throw Error('Crank pointer did not retire');
                    }''')
                    case = dict(data, control=name, before=before, errors=list(report['errors']),
                                drivers=list(document['drivers']), hit_verified=True, hover=hover,
                                gesture=dict(point=point, drag=None if press else [dx,dy]))
                    report['attempts'].append(case)
                    validate_attempt(case)
                    if not press and case['after']['crank_rotation'] <= before['crank_rotation']:
                        continue
                    validate_case(case)
                    case['bank_sha256'] = bank_sha256(case['after'], case['bank_bits'])
                    case['validation'] = 'passed'
                    report['cases'].append(case)
                    checkpoint_report(args.report, report)
                    page.screenshot(path=str(args.report.with_name(
                        args.report.stem+('-button.png' if press else '-turn.png'))), timeout=180_000)
                    print(json.dumps(dict(passed=name, bank_sha256=case['bank_sha256'])), flush=True)
                    break
                else:
                    raise AssertionError('No positive partial crank gesture')
            assert len(report['cases']) == 2 and not report['errors']
            report['validation'] = 'passed'
        except Exception as error:
            report['validation'] = 'failed'
            report['failure'] = f'{type(error).__name__}: {error}'
            raise
        finally:
            browser.close()
            checkpoint_report(args.report, report)


if __name__ == '__main__':
    main()
