"""Capture resource-guarded CAD command output without flooding the console."""

import json
from pathlib import Path
import re
import subprocess
import sys
import time


def main():
    name, *command = sys.argv[1:]
    if not re.fullmatch(r'[a-z0-9-]+', name) or not command:
        raise ValueError('Expected a log name and command')
    path = Path('_build_evidence/carry-frame-'+name+'.log')
    path.parent.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    with path.open('w') as output:
        result = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT)
    lines = path.read_text().splitlines()
    selected = [line for line in lines if re.search(
        r'Running \w+Test\.|AssertionError|Ran \d+ tests|Traceback|Error:|^\{', line)]
    for line in selected[-20:]:
        if line.startswith('{'):
            record = json.loads(line)
            # Keep the complete native inventory in the log; the console
            # needs outcomes, diagnostics and timings, not 428 repeated paths.
            for key in ('physical_inventory', 'candidate_neighbours'):
                record.pop(key, None)
            line = json.dumps(record)
        print(line, flush=True)
    print(json.dumps(dict(log=str(path), exit=result.returncode,
                          elapsed_seconds=time.monotonic()-start)), flush=True)
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
