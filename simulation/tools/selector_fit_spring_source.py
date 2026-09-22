"""Compare source spring ends with the public analytic-helix representation.

Uninstalled source-height comparison only. No operating spring, inferred end
shape equivalence, or silently added library capability is introduced.
"""

import hashlib
import json
import logging
from pathlib import Path

import cadquery as cq
from molejo import Circle, Helix, Shape

from simulation.tools.selector_fit_alignment import native_source
from simulation.tools.selector_fit_contacts import BALL_Z, closest
from simulation.tools.selector_fit_measurements import body_measurements


def measure():
    source = native_source()['spring']
    shape = Shape(profile=Circle(.255), path=[Helix(radius=2.295, turns=6.5, height=11.1)],
                  path_samples=1300, profile_samples=32)
    brep = shape.brep()
    native = cq.Shape.cast(brep.solid).rotate((0, 0, 0), (1, 0, 1), 180).translate(
        (63, 0, BALL_Z+2.295))
    source_caps = sorted([face for face in source.Faces() if face.geomType() == 'PLANE'],
                         key=lambda face: face.Center().x)
    candidate_caps = sorted([face for face in native.Faces() if face.geomType() == 'PLANE'],
                            key=lambda face: face.Center().x)
    assert len(source_caps) == len(candidate_caps) == 2
    result = dict(kind='source-spring-analytic-representation-comparison',
        scope='Uninstalled comparison; a helix is not declared source-equivalent by its dimensions',
        source=body_measurements(source), analytic=body_measurements(native),
        analytic_spec=shape.to_dict(), analytic_tolerance_mm=brep.tolerance,
        ends=[dict(source_center_mm=a.Center().toTuple(), source_normal=a.normalAt().toTuple(),
                   candidate_center_mm=b.Center().toTuple(), candidate_normal=b.normalAt().toTuple(),
                   center_distance_mm=closest(cq.Vertex.makeVertex(*a.Center().toTuple()),
                                              cq.Vertex.makeVertex(*b.Center().toTuple()))[0])
              for a, b in zip(source_caps, candidate_caps)],
        limitations=['No source equivalence from equal radius/turn count alone',
                     'No installed seating, compression, force or continuous-motion claim'])
    output = Path('_build_evidence/selector-fit-spring-source.json')
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(output), sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                          ends=result['ends'], source_volume_mm3=source.Volume(),
                          analytic_volume_mm3=native.Volume(), analytic_tolerance_mm=brep.tolerance)), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    measure()
