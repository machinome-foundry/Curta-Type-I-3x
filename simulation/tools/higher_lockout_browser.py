"""Compare the isolated tens restraint in Python and a fresh browser worker.

Export simulation.higher_result_locking:HigherResultLocking --no-widget first.
No running Studio session is touched. Geometry acceptance is a separate gate.
"""

import argparse
import hashlib
import json
import logging
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright
from machinome.simulation import Sim
from simulation.higher_result_locking import HigherResultLocking


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    args = parser.parse_args()
    build = args.build.resolve()
    expected = {}
    for carry in (0, 4.2):
        sim = Sim(HigherResultLocking(), dt=.1, state={'carry_latch': carry})
        sim.move('crank_angle', to=140)
        sim.move('digit', to=0)
        assert sim.move('crank_angle', to=170).status == 'blocked'
        expected[str(carry)] = sim.state['crank_angle']
    viewer = json.loads(subprocess.check_output(
        [sys.executable, '-m', 'machinome_viewer', 'describe'], text=True))
    bundle = Path(viewer['path']).read_bytes()
    report = {'python_stops': expected, 'cases': [], 'errors': [],
              'bundle_sha256': hashlib.sha256(bundle).hexdigest(),
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

            page.route('http://higher-curta.test/**', serve)
            page.goto('http://higher-curta.test/')
            page.add_script_tag(content=bundle.decode())
            page.evaluate('''async () => {
                window.curta = await MachinomeViewer.mount('#view', 'manifest.json', {
                    autoplay:false, run:{dt:.1}, partControls:'none'});
                curta.run().pause();
            }''')
            for carry in (0, 4.2):
                case = page.evaluate('''async carry => {
                    const run=curta.run(); await run.reset(); run.pause();
                    for(const [input,to] of [['carry_latch',carry],['digit',3],
                        ['crank_angle',140],['digit',0]]) {
                        const result=await run.move(input,{to});
                        if(result.some(x=>x.status!=='completed')) throw Error(JSON.stringify(result));
                    }
                    const saved=await run.snapshot();
                    const short=await run.move('crank_angle',{to:170});
                    const stopped=run.state(), snapshot=await run.snapshot();
                    await run.restore(saved);
                    const long=await run.move('crank_angle',{to:860});
                    const longState=run.state();
                    await run.restore(saved); await run.move('crank_angle',{to:170});
                    const replay=JSON.stringify(snapshot)===JSON.stringify(await run.snapshot());
                    const relief=await run.move('crank_angle',{by:-.05});
                    await run.step(1); const idle=run.state();
                    const retry=await run.move('crank_angle',{to:170});
                    return {carry,short,long,stopped,longState,replay,relief,idle,retry,
                        retried:run.state(),worker:run.runsInWorker};
                }''', carry)
                report['cases'].append(case)
                print(json.dumps({'carry': carry, 'python': expected[str(carry)],
                                  'browser': case['stopped']['crank_angle'],
                                  'replay': case['replay']}), flush=True)
            report['legal'] = page.evaluate('''async () => {
                const run=curta.run(), found=[];
                for(const carry of [0,4.2]) for(const [digit,height,count] of
                    [[0,0,0],[3,0,3],[9,0,9],[0,9,9]]) {
                    await run.reset(); run.pause();
                    for(const [input,to] of [['carry_latch',carry],['digit',digit],['crank_height',height]])
                        await run.move(input,{to});
                    const result=await run.move('crank_angle',{by:1080});
                    found.push({carry,digit,height,expected:-16+216*(count+(carry?1:0)),
                        result,state:run.state()});
                }
                return found;
            }''')
            report['free_support'] = page.evaluate('''async () => {
                const run=curta.run(); await run.reset(); run.pause();
                const withdrawal=133.5+(22.22+16)/(72/11.25);
                for(const [input,to] of [['carry_latch',4.2],['digit',1],
                    ['crank_angle',withdrawal],['digit',0]]) {
                    const result=await run.move(input,{to});
                    if(result.some(x=>x.status!=='completed')) throw Error(JSON.stringify(result));
                }
                const before=await run.snapshot();
                const result=await run.move('crank_angle',{to:146.3});
                const after=await run.snapshot(),state=run.state();
                await run.restore(before);
                await run.move('crank_angle',{to:146.3});
                return {result,state,replay:JSON.stringify(after)===
                    JSON.stringify(await run.snapshot())};
            }''')
            page.evaluate('''async () => {
                curta.setVisible(['drum'],false);
                curta.setView({camera:[85,-35,0],target:[34,0,-23]});
                await new Promise(requestAnimationFrame);
                await new Promise(requestAnimationFrame);
            }''')
            page.screenshot(path=str(build/'higher-free-support.png'))
            page.evaluate('''async () => {
                const run=curta.run(); await run.reset(); run.pause();
                await run.move('carry_latch',{to:4.2}); await run.move('digit',{to:3});
                await run.move('crank_angle',{to:140}); await run.move('digit',{to:0});
                await run.move('crank_angle',{to:170});
                curta.setVisible(['drum'],false);
                curta.setView({camera:[85,-35,0],target:[34,0,-23]});
                await new Promise(requestAnimationFrame);
                await new Promise(requestAnimationFrame);
            }''')
            page.screenshot(path=str(build/'higher-stopped.png'))
        finally:
            browser.close()
            (build/'higher-browser-acceptance.json').write_text(json.dumps(report, indent=2)+'\n')
    assert not report['errors'], report['errors']
    for case in report['cases']:
        stop = expected[str(case['carry'])]
        for outcome in ('short', 'long', 'retry'):
            assert case[outcome][-1]['status'] == 'blocked', case
        for state in ('stopped', 'longState', 'retried'):
            assert abs(case[state]['crank_angle']-stop) < 1e-7, case
            assert abs(case[state]['tens.turn']-169.6) < 1e-7, case
        assert case['replay'] and case['relief'][-1]['status'] == 'completed', case
        assert abs(case['idle']['crank_angle']-stop+.05) < 1e-7, case
    for case in report['legal']:
        assert case['result'][-1]['status'] == 'completed', case
        assert abs(case['state']['tens.turn']-case['expected']) < 1e-7, case
    free = report['free_support']
    assert free['result'][-1]['status'] == 'completed' and free['replay'], free
    assert abs(free['state']['crank_angle']-146.3) < 1e-7, free
    assert abs(free['state']['tens.turn']-22.22) < 1e-7, free
    print('Two retained-stop/replay cases, eight legal moves, and free-support replay pass.',
          flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
