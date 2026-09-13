"""Inspect a completed public build document and every referenced artifact."""

import hashlib
import json
import logging
import os
from pathlib import Path

from simulation.curta import Curta


def inspect():
    build = Path(os.environ['SOLID_BUILD_DIR']).resolve()
    document_path = build/'viewer.json'
    document = json.loads(document_path.read_text())
    assert not (build/'errors.json').exists(), 'Publication retains a build error'
    assert document['format'] == 'solid-node-export' and document['version'] == 4
    rigid, flexible = {}, []

    def visit(node, parent=''):
        path = parent+'.'+node['name'] if parent else node['name']
        if 'model' in node:
            artifact = (build/node['model']).resolve()
            assert artifact.is_relative_to(build) and artifact.is_file(), path
            assert artifact.stat().st_size > 0, path
            rigid[path] = dict(model=node['model'],
                               sha256=hashlib.sha256(artifact.read_bytes()).hexdigest())
        elif 'flexible' in node:
            flexible.append(path)
        for child in node.get('children', []):
            visit(child, path)

    visit(document['root'])
    assert (len(rigid), len(flexible)) == (390, 38)
    assert (len(document['drivers']), len(document['instructions'])) == (8, 7)
    root = Curta()
    root.set_state(initial_result=0, initial_turns=0, operand=0, crank_turns=0,
                   subtract=0, carriage_position=0, carriage_lift=0, clear=0)
    root.assemble()
    frame = root.frame.upper_frame.main_body
    published = rigid['Curta.frame.upper_frame.main_body']
    assert (build/published['model']).resolve() == Path(frame.stl_file).resolve()
    assert type(frame).__name__ == 'CarryPassageFrame'
    assert frame.running_gap == .05
    shape = frame.shape()
    assert shape.isValid() and len(shape.Solids()) == 1
    assert abs(shape.Volume()-199441.6249710615) < 1e-6
    result = dict(kind='carry-frame-root-publication', document=str(document_path),
                  document_sha256=hashlib.sha256(document_path.read_bytes()).hexdigest(),
                  version=document['version'], bindings=len(document.get('bindings', [])),
                  drivers=sorted(document['drivers']), instructions=sorted(document['instructions']),
                  rigid_occurrences=len(rigid), flexible_occurrences=len(flexible),
                  fitted_frame=published, fitted_frame_native_volume_mm3=shape.Volume(),
                  artifacts=rigid, flexible_paths=flexible)
    output = Path('_build_evidence/carry-frame-publication.json')
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ('artifacts', 'flexible_paths')}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    inspect()
