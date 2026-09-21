"""Replay the actual carry preparation in an isolated browser worker.

The expected request completes; an engine exception is recorded and remains
a failing acceptance result. Never operates the pilot's Studio session.
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
    parser.add_argument('--python-report', type=Path,
                        help='Compare full retained banks from the real Python test')
    args = parser.parse_args()
    build = args.build.resolve()
    expected = json.loads(args.python_report.read_text()) if args.python_report else None
    viewer = json.loads(subprocess.check_output(
        [sys.executable, '-m', 'machinome_viewer', 'describe'], text=True))
    bundle = Path(viewer['path']).read_bytes()
    report = {'errors': [], 'bundle_sha256': hashlib.sha256(bundle).hexdigest(),
              'document_sha256': hashlib.sha256((build/'manifest.json').read_bytes()).hexdigest()}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'])
        try:
            page = browser.new_page(viewport={'width': 1200, 'height': 900})
            page.set_default_timeout(120000)
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
                    route.fulfill(status=404, body='Missing local acceptance asset')

            page.route('http://higher-operating.test/**', serve)
            page.goto('http://higher-operating.test/')
            page.add_script_tag(content=bundle.decode())
            report['request'] = page.evaluate('''async () => {
                window.curta=await MachinomeViewer.mount('#view','manifest.json',{
                    autoplay:false,run:{dt:.1},partControls:'none'});
                const run=curta.run(); run.pause();
                const setup=await run.move('digit_1',{to:9});
                const before=await run.snapshot(); let result=null,error=null;
                try {result=await run.move('crank_rotation',{to:360});}
                catch(failure) {error=String(failure);}
                return {setup,result,error,state:run.state(),worker:run.runsInWorker,
                    unchanged:JSON.stringify(before)===JSON.stringify(await run.snapshot())};
            }''')
            request = report['request']
            print(json.dumps({key: request[key] for key in
                              ('setup', 'result', 'error', 'worker', 'unchanged')} |
                             {'crank_rotation': request['state']['crank_rotation']}), flush=True)
            page.screenshot(path=str(build/'carry-preparation.png'))
            report['cases'] = []
            for carried in (False, True):
                case = page.evaluate('''async carried => {
                    const run=curta.run(); await run.reset(); run.pause();
                    const complete=async (input,to)=>{
                        const result=await run.move(input,{to});
                        if(result.some(x=>x.status!=='completed')) throw Error(JSON.stringify(result));
                    };
                    let carryReplay=null;
                    if(carried) {
                        await complete('digit_1',9);
                        const before=await run.snapshot();
                        await complete('crank_rotation',360);
                        const after=await run.snapshot();
                        await run.restore(before); await complete('crank_rotation',360);
                        carryReplay=JSON.stringify(after)===JSON.stringify(await run.snapshot());
                        await complete('digit_1',1);
                    }
                    const withdrawal=carried?500:140;
                    await complete('digit_2',3); await complete('crank_rotation',withdrawal);
                    await complete('digit_2',0);
                    const saved=await run.snapshot();
                    const short=await run.move('crank_rotation',{to:withdrawal+30});
                    const stopped=run.state(), snapshot=await run.snapshot();
                    await run.restore(saved); await run.move('crank_rotation',{to:withdrawal+30});
                    const replay=JSON.stringify(snapshot)===JSON.stringify(await run.snapshot());
                    await run.restore(saved);
                    const long=await run.move('crank_rotation',{to:withdrawal+720});
                    const longState=run.state();
                    const relief=await run.move('crank_rotation',{by:-.05});
                    await run.step(1);
                    return {carried,carryReplay,short,long,stopped,longState,replay,relief,
                        idle:run.state(),worker:run.runsInWorker};
                }''', carried)
                report['cases'].append(case)
                print(json.dumps({'carried': carried, 'stop': case['stopped']['crank_rotation'],
                                  'replay': case['replay'], 'carry_replay': case['carryReplay']}),
                      flush=True)
            page.screenshot(path=str(build/'carry-withdrawal-relieved.png'))
            report['free_support'] = page.evaluate('''async () => {
                const run=curta.run(); await run.reset(); run.pause();
                const withdrawal=360+133.5+(22.22+16)/(72/11.25);
                for(const [input,to] of [['digit_1',9],['crank_rotation',360],
                    ['digit_1',1],['digit_2',1],['crank_rotation',withdrawal],['digit_2',0]]) {
                    const result=await run.move(input,{to});
                    if(result.some(x=>x.status!=='completed')) throw Error(JSON.stringify(result));
                }
                const before=await run.snapshot();
                const result=await run.move('crank_rotation',{to:506.3});
                const state=run.state(), after=await run.snapshot();
                await run.restore(before);
                await run.move('crank_rotation',{to:506.3});
                return {result,state,replay:JSON.stringify(after)===
                    JSON.stringify(await run.snapshot())};
            }''')
            print(json.dumps({'free_support': report['free_support']['result'],
                              'replay': report['free_support']['replay']}), flush=True)
            page.screenshot(path=str(build/'carry-free-support.png'))
        finally:
            browser.close()
            (build/'carry-browser-acceptance.json').write_text(json.dumps(report, indent=2)+'\n')
    assert not report['errors'], report['errors']
    assert report['request']['error'] is None, report['request']['error']
    assert report['request']['result'][-1]['status'] == 'completed', report['request']
    assert report['request']['state']['crank_rotation'] == 360, report['request']
    free = report['free_support']
    assert free['result'][-1]['status'] == 'completed' and free['replay'], free
    assert abs(free['state']['crank_rotation']-506.3) < 1e-7, free
    assert abs(free['state']['transmission.result.tens.turn']-22.22) < 1e-7, free
    assert abs(free['state']['transmission.result.tens.p_10220_410003_1_419227.travel']) < 1e-7, free
    for case in report['cases']:
        withdrawal = 500 if case['carried'] else 140
        angle = case['stopped']['crank_rotation']
        assert withdrawal < angle < withdrawal+6, case
        assert case['short'][-1]['status'] == case['long'][-1]['status'] == 'blocked', case
        assert case['relief'][-1]['status'] == 'completed' and case['replay'], case
        assert not case['carried'] or case['carryReplay'], case
        assert abs(case['longState']['crank_rotation']-angle) < 1e-7, case
        assert abs(case['idle']['crank_rotation']-angle+.05) < 1e-7, case
        assert abs(case['stopped']['transmission.result.tens.turn']-169.6) < 1e-7, case
        if expected is not None:
            other = next(e for e in expected if e['carried'] == case['carried'])
            for state in ('stopped', 'idle'):
                assert set(case[state]) == set(other[state]), (state, 'bank keys')
                for name, value in other[state].items():
                    assert abs(case[state][name]-value) < 1e-7, (state, name, value, case[state][name])


if __name__ == '__main__':
    main()
