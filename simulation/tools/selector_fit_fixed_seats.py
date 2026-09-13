"""Classify only the two ratified selected-input fixed-source joints.

Canonical means the original setting-zero assembly frame. Compare actual
intersection regions there, not rotating world-volume roundoff or a maximum
overlap allowance. No moving-interface exemption is introduced.
"""

import hashlib
import json
import logging
from copy import deepcopy
from pathlib import Path

import cadquery as cq
import numpy as np

from simulation.selector_fit import SelectorFitBench
from simulation.standard.assembly import DigitSelectorAxle1
from simulation.tools.interference import world_solids
from simulation.tools.moving_seats import world_frames
from simulation.tools.open_run_transitions import bounds
from simulation.tools.selector_fit_measurements import PATHS


PAIRS = {'screw/knob': ('screw', 'knob'), 'shaft/top': ('shaft', 'top')}


def intersections(bodies):
    result = {}
    for name, (first, second) in PAIRS.items():
        common = bodies[first].intersect(bodies[second])
        assert common.isValid() and common.Volume() >= 0, name
        if common.Volume() > 0:
            result[name] = common
    return result


def verify_regions(reference, actual):
    """New, missing, changed or invalid regions fail, even at equal volume."""
    assert set(actual) == set(reference) == set(PAIRS), 'fixed-seat inventory identities'
    for name, expected in reference.items():
        observed = actual[name]
        assert observed.isValid() and len(observed.Solids()) > 0, name
        added, removed = observed.cut(expected), expected.cut(observed)
        assert added.isValid() and removed.isValid(), name
        assert added.Volume() == removed.Volume() == 0, (
            name, 'changed canonical region', added.Volume(), removed.Volume())


def relative_frames(frames):
    return {name: np.linalg.inv(frames[PATHS[first]]) @ frames[PATHS[second]]
            for name, (first, second) in PAIRS.items()}


def verify_frames(reference, actual):
    assert set(actual) == set(reference) == set(PAIRS), 'fixed-seat frame identities'
    for name in PAIRS:
        # Matrix roundoff, not an intersection-volume or physical-fit allowance.
        np.testing.assert_allclose(actual[name], reference[name], rtol=0, atol=1e-10,
                                   err_msg='changed fixed-seat relative pose: '+name)


def measure():
    imported = DigitSelectorAxle1()
    imported.assemble()
    names = set(name for pair in PAIRS.values() for name in pair)
    source_paths = {name: PATHS[name].replace('Curta.selector.', 'Curta.') for name in names}
    source_native = world_solids(imported, selected=set(source_paths.values()))
    source = {name: source_native[path] for name, path in source_paths.items()}
    reference = intersections(source)
    assert set(reference) == set(PAIRS)

    bench = SelectorFitBench()
    bench.set_state(setting=0, postcarry=0)
    bench.assemble()
    bench_native = world_solids(bench, selected={PATHS[name] for name in names})
    canonical = {name: bench_native[PATHS[name]] for name in names}
    actual = intersections(canonical)
    verify_regions(reference, actual)
    baseline = relative_frames(world_frames(bench))
    # Check placement against the unmodified source assembly independently.
    source_frames = world_frames(imported)
    expected_frames = {PATHS[name]: source_frames[source_paths[name]] for name in names}
    verify_frames(relative_frames(expected_frames), baseline)
    rows = []
    for postcarry in (0, 1):
        for direction, settings in (('forward', [i/4 for i in range(37)]),
                                    ('reverse', [i/4 for i in range(36, -1, -1)])):
            maximum = {name: 0. for name in PAIRS}
            for setting in settings:
                bench.set_state(setting=setting, postcarry=postcarry)
                bench.assemble()
                current = relative_frames(world_frames(bench))
                verify_frames(baseline, current)
                for name in PAIRS:
                    maximum[name] = max(maximum[name], float(abs(current[name]-baseline[name]).max()))
            rows.append(dict(postcarry=postcarry, direction=direction,
                             settings=settings, maximum_relative_matrix_error=maximum))

    mutations = []
    def rejected(name, check):
        try:
            check()
        except AssertionError as error:
            mutations.append(dict(name=name, rejected=True, reason=str(error)))
        else:
            raise AssertionError('Undetected mutation: '+name)

    rejected('missing_fixed_joint', lambda: verify_regions(reference, {'screw/knob': actual['screw/knob']}))
    rejected('new_moving_contact_entry', lambda: verify_regions(reference, actual | {'shaft/ball': actual['screw/knob']}))
    swapped = {'screw/knob': actual['shaft/top'], 'shaft/top': actual['screw/knob']}
    rejected('swapped_joint_region_identities', lambda: verify_regions(reference, swapped))
    changed = actual | {'screw/knob': actual['screw/knob'].translate((0, .01, 0))}
    # Rigid translation preserves volume; a volume-only inventory misses this.
    rejected('equal_volume_changed_thread_region', lambda: verify_regions(reference, changed))
    changed = actual | {'shaft/top': actual['shaft/top'].translate((0, 0, .01))}
    rejected('changed_axial_shaft_join_region', lambda: verify_regions(reference, changed))
    for name in PAIRS:
        changed_frames = deepcopy(baseline)
        changed_frames[name][0, 3] += .01
        rejected('changed_relative_pose_'+name, lambda f=changed_frames: verify_frames(baseline, f))

    # Verify that physical candidate changes really change the intersection,
    # rather than testing only manipulated registry metadata.
    shifted = canonical | {'screw': canonical['screw'].translate((0, .01, 0))}
    rejected('physical_screw_misplacement', lambda: verify_regions(reference, intersections(shifted)))
    shifted = canonical | {'top': canonical['top'].translate((0, 0, .01))}
    rejected('physical_shaft_join_misplacement', lambda: verify_regions(reference, intersections(shifted)))
    verify_regions(reference, intersections(canonical))

    result = dict(kind='selected-input-fixed-seat-classification',
        planning_commit='da432fbdc7fe0e7f89e308237f281e9c3d368754',
        canonical_frame='Unchanged source-installed setting-zero assembly frame',
        scope='Only two source-fixed joints; no moving-contact or whole-machine exemptions',
        pairs={name: dict(
            paths=[PATHS[p].replace('Curta.selector', 'Curta.input_selectors.selectors.digit_selector_axle_1')
                   for p in PAIRS[name]],
            volume_mm3=shape.Volume(), bounds_mm=bounds(shape).tolist(), solids=len(shape.Solids()),
            relative_matrix=baseline[name].tolist()) for name, shape in reference.items()},
        placement_runs=rows, mutations=mutations,
        continuous_relative_pose_argument={
            'screw/knob': 'Both fixed children of the same translating knob group: (K(q)S)^-1(K(q)N)=S^-1 N.',
            'shaft/top': 'Both use the same source Z axis and equal turn, top driven directly by bottom: (R(q)B)^-1(R(q)T)=B^-1 T; distinct source axial offsets remain unchanged.'},
        support_provenance={
            'screw/knob': 'Manual page 32 M4 tap/die engagement. Canonical region ends at X=54.2361268305, short of non-threaded tip X=54.3.',
            'shaft/top': 'Unchanged coaxial source shaft join, two overlap regions over the 0.025 mm source axial engagement; not a moving axial seat.'},
        limitations=['No thread strength, manufacturing fit or force claim',
                     'Later fitted parts must preserve these exact canonical joint regions and relative poses',
                     'All moving ball/spring/follower/gear/housing contacts remain independent acceptance gates'],
        sources_sha256={str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in (
            Path('simulation/selectors.py'), Path('simulation/standard/assembly.py'),
            Path('simulation/selector_fit.py'), Path(__file__).relative_to(Path.cwd()))})
    output = Path('_build_evidence/selector-fit-fixed-seats.json')
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(output), sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                          pairs=result['pairs'], placement_runs=rows,
                          mutations=mutations)), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    measure()
