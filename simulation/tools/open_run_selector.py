"""Evidence-only selector travel in a frozen installed Curta home fixture.

Never change the root operand during a sweep: that old prescribed input
reconstructs wheel/carry state. Move native copies of the eight physical input
bodies instead, after matching every seated setting to public standalone
benches. Include every installed neighbour and keep source-mesh checks named.
This diagnostic does not implement a running law or certify unsampled travel.
"""

import argparse
import hashlib
import json
import logging
import os
from pathlib import Path
import resource
import subprocess
from time import monotonic


SELECTOR = 'Curta.input_selectors.selectors.digit_selector_axle_1'
INPUT_GROUP = 'Curta.transmission.result.ones.p_10219_410002_1'
MOVERS = {
    SELECTOR+'.selector_shaft_bottom': 'rotation',
    SELECTOR+'.selector_shaft_top_1_419054.selector_shaft_top': 'rotation',
    SELECTOR+'.selector_shaft_top_1_419054.number_roll': 'rotation',
    SELECTOR+'.selector_knob_1_419057.selector_knob_spring': 'translation',
    SELECTOR+'.selector_knob_1_419057.p_5mm_ball': 'translation',
    SELECTOR+'.selector_knob_1_419057.digit_selector_screw': 'translation',
    SELECTOR+'.selector_knob_1_419057.selector_knob': 'translation',
    INPUT_GROUP: 'translation',
}


def move_shape(path, shape, setting, source_setting):
    delta = setting-source_setting
    if MOVERS.get(path) == 'translation':
        return shape.translate((0, 0, -6*delta))
    if MOVERS.get(path) == 'rotation':
        return shape.rotate((58.5, 0, 0), (58.5, 0, 1), 36*delta)
    raise ValueError('Unlisted moving body: '+path)


def retained_state(root):
    register = root.carriage.registers.result_register
    shafts = root.transmission.result
    carries = root.carry_mechanism.result_carries
    return dict(
        drivers={name: getattr(root, name) for name in
                 ('initial_result', 'initial_turns', 'operand', 'crank_turns',
                  'subtract', 'carriage_position', 'carriage_lift', 'clear')},
        result=root.result.value,
        selected_setting=root.input_selectors.selectors.digit_selector_axle_1.setting.value,
        shaft_degrees=[getattr(shafts, name).turn.value for name in ('ones', 'tens', 'hundreds')],
        dial_degrees=[getattr(register, name).turn.value for name in ('p_10203_1', 'p_10203_2', 'p_10205_1')],
        carry_fractions=[getattr(carries, 'results_tens_lever_assembly_'+str(i)).engage.value
                         for i in (1, 2)])


def vertex_error(first, second):
    """Symmetric native-vertex distance; only a placement guard, not clearance."""
    import numpy as np
    a = np.array([v.toTuple() for v in first.Vertices()])
    b = np.array([v.toTuple() for v in second.Vertices()])
    if not len(a) or not len(b):
        raise ValueError('A placement witness has no native vertices')
    def directed(x, y):
        return max(float(np.min(np.linalg.norm(chunk[:, None]-y[None, :], axis=2), axis=1).max())
                   for chunk in (x[i:i+64] for i in range(0, len(x), 64)))
    return max(directed(a, b), directed(b, a))


def verify_bindings(root, native, source_setting):
    import numpy as np
    from simulation.selectors import SelectorBank
    from simulation.transmission import TransmissionBench
    from simulation.fit import INPUT_CLOCKING
    from simulation.tools.interference import world_solids
    from simulation.tools.open_run_transitions import bounds

    selectors, transmission = SelectorBank(), TransmissionBench()
    advance = (root.transmission.result.ones.turn.value-INPUT_CLOCKING)/72
    mapping = {path: path.replace(SELECTOR, 'Curta.digit_selector_axle_1')
               for path in MOVERS if path != INPUT_GROUP}
    initial = retained_state(root)
    max_vertex, max_volume = 0., 0.
    for digit in range(10):
        selectors.set_state(input_number=digit)
        selectors.assemble()
        transmission.set_state(digit=digit, advance=advance)
        transmission.assemble()
        expected = world_solids(selectors, selected=set(mapping.values()))
        group = world_solids(transmission, selected={'Curta.p_10219_410002_1'})
        assert set(expected) == set(mapping.values()) and len(group) == 1
        expected = {**{path: expected[other] for path, other in mapping.items()},
                    INPUT_GROUP: group['Curta.p_10219_410002_1']}
        for path in MOVERS:
            independent = move_shape(path, native[path], digit, source_setting)
            reference = expected[path]
            error = vertex_error(independent, reference)
            volume = abs(independent.Volume()-reference.Volume())
            max_vertex, max_volume = max(max_vertex, error), max(max_volume, volume)
            assert error < 1e-5 and volume < 1e-5, (digit, path, error, volume)
            np.testing.assert_allclose(bounds(independent), bounds(reference), atol=1e-5, rtol=0)
        assert retained_state(root) == initial, 'A standalone bench changed the frozen root'

    knob = SELECTOR+'.selector_knob_1_419057.selector_knob'
    shaft = SELECTOR+'.selector_shaft_bottom'
    negative = {}
    for name, path, mutant in (
        ('reverse-knob-travel', knob, native[knob].translate((0, 0, -6))),
        ('omit-input-travel', INPUT_GROUP, native[INPUT_GROUP]),
        ('wrong-selector-axis', shaft, native[shaft].rotate((0, 0, 0), (0, 0, 1), -36)),
    ):
        error = vertex_error(move_shape(path, native[path], 0, source_setting), mutant)
        assert error > 1, (name, error)
        negative[name] = dict(detected=True, native_vertex_error_mm=error)
    return dict(seated_settings=list(range(10)), moving_bodies=len(MOVERS),
                maximum_native_vertex_error_mm=max_vertex, maximum_volume_error_mm3=max_volume,
                negative_controls=negative)


def sweep(fixture, samples):
    import numpy as np
    import manifold3d as manifold
    import solid_node
    from itertools import combinations
    from simulation.curta import Curta
    from simulation.tools.carry_frame_regression import fingerprint
    from simulation.tools.carry_phase import solid as manifold_solid
    from simulation.tools.interference import world_solids
    from simulation.tools.open_run_transitions import bounds, overlaps_bounds, physical_nodes

    started = monotonic()
    limit = resource.getrlimit(resource.RLIMIT_AS)[0]
    assert 0 < limit <= 8*1024**3, 'Use the 8 GiB address-space guard'
    assert all(os.environ.get(key) == '1' for key in
               ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'))
    assert samples >= 2
    sources = fingerprint()
    root = Curta()
    root.set_state(initial_result=99, initial_turns=0, operand=1,
                   crank_turns=0 if fixture == 'initial' else 1, subtract=0,
                   carriage_position=0, carriage_lift=0, clear=0)
    root.assemble()
    frozen = retained_state(root)
    source_setting = frozen['selected_setting']
    assert source_setting == 1
    if fixture == 'postcarry':
        assert frozen['result'] == 100 and frozen['carry_fractions'] == [0, 1], frozen
    else:
        np.testing.assert_allclose(frozen['carry_fractions'], [1.1630815/4.2]*2, atol=1e-8, rtol=0)
    nodes = dict(physical_nodes(root))
    assert len(nodes) == 428 and set(MOVERS) <= set(nodes)
    assert {path for path in nodes if path.startswith(SELECTOR+'.')} == set(MOVERS)-{INPUT_GROUP}
    print(json.dumps(dict(phase='native inventory', fixture=fixture, physical_bodies=len(nodes))), flush=True)
    native = world_solids(root, include_flexible=True)
    assert set(MOVERS) <= set(native), 'Every selected moving body needs native geometry'
    scene_bounds = {path: bounds(shape) for path, shape in native.items()}
    original_bounds = {path: box.copy() for path, box in scene_bounds.items()}
    mesh_only = {}
    for path, node in nodes.items():
        if path not in native:
            assert not node.exact
            node.build_stls()
            mesh_only[path] = node.mesh
            scene_bounds[path] = mesh_only[path].bounds.copy()
    assert set(scene_bounds) == set(nodes)
    inventory = [dict(path=p, representation='native' if p in native else 'source-mesh')
                 for p in sorted(nodes)]
    guards = verify_bindings(root, native, source_setting)
    print(json.dumps(dict(phase='bindings verified', fixture=fixture, **guards)), flush=True)
    static = sorted(set(nodes)-set(MOVERS))
    candidates = {path: set() for path in MOVERS}
    source_meshes, static_manifolds = {}, {}
    positive, invalid, negative = {}, {}, {}
    comparisons = dict(native=0, faceted=0)
    current = {}

    def faceted(path, digit):
        if path not in MOVERS:
            if path not in static_manifolds:
                static_manifolds[path] = manifold_solid(mesh_only[path])
            return static_manifolds[path]
        if path not in current:
            if path not in source_meshes:
                nodes[path].build_stls()
                source_meshes[path] = nodes[path].mesh
            mesh = source_meshes[path].copy()
            delta = digit-source_setting
            if MOVERS[path] == 'translation':
                mesh.apply_translation((0, 0, -6*delta))
            else:
                angle = np.deg2rad(36*delta)
                rotation = np.array([[np.cos(angle), -np.sin(angle), 0],
                                     [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
                transform = np.eye(4)
                transform[:3, :3] = rotation
                axis = np.array([58.5, 0, 0])
                transform[:3, 3] = axis-rotation@axis
                mesh.apply_transform(transform)
            current[path] = manifold_solid(mesh)
        return current[path]

    def compare(first, second, active, digit):
        a, b = active[first], active.get(second, native.get(second))
        key = first+' / '+second
        if b is not None:
            common = a.intersect(b)
            method = 'native'
            good, volume = common.isValid(), common.Volume()
        else:
            common = faceted(first, digit) ^ faceted(second, digit)
            method = 'faceted'
            good, volume = common.status() == manifold.Error.NoError, common.volume()
        comparisons[method] += 1
        bucket = invalid if not good else positive if volume > 0 else negative if volume < 0 else None
        if bucket is not None:
            entry = bucket.setdefault(key, dict(samples=0, first_setting=float(digit),
                                               setting_at_maximum=float(digit), volume_mm3=volume,
                                               kernel=method))
            entry['samples'] += 1
            if abs(volume) >= abs(entry['volume_mm3']):
                entry.update(setting_at_maximum=float(digit), volume_mm3=volume)
                if good and volume > 0 and method == 'native':
                    entry.update(bounds_mm=bounds(common).tolist(), center_mm=common.Center().toTuple())

    for index, digit in enumerate(np.linspace(0, 9, samples)):
        current.clear()
        active = {path: move_shape(path, native[path], digit, source_setting) for path in MOVERS}
        boxes = {path: bounds(shape) for path, shape in active.items()}
        for first in MOVERS:
            for second in static:
                if overlaps_bounds(boxes[first], scene_bounds[second]):
                    candidates[first].add(second)
                    compare(first, second, active, digit)
        for first, second in combinations(MOVERS, 2):
            if overlaps_bounds(boxes[first], boxes[second]):
                candidates[first].add(second)
                compare(first, second, active, digit)
        assert retained_state(root) == frozen, 'The retained root state changed during selector travel'
        if index % 5 == 0 or index == samples-1:
            print(json.dumps(dict(phase='travel', fixture=fixture, sample=index+1, samples=samples,
                                  positive_pairs=len(positive), invalid_pairs=len(invalid),
                                  negative_pairs=len(negative))), flush=True)
    for path, before in original_bounds.items():
        np.testing.assert_allclose(bounds(native[path]), before, atol=1e-10, rtol=0)
    assert fingerprint() == sources, 'Source drift during the probe'
    result = dict(kind='frozen-installed-selector-travel', fixture=fixture, samples=samples,
                  frozen_state=frozen, retained_state_unchanged=True, original_native_placements_unchanged=True,
                  bindings=guards, physical_bodies=len(nodes), native_bodies=len(native),
                  physical_inventory=inventory, mesh_only_bodies=sorted(mesh_only),
                  full_physical_inventory_sha256=hashlib.sha256(json.dumps(inventory, sort_keys=True).encode()).hexdigest(),
                  moving_bodies=MOVERS, candidate_neighbours={p: sorted(values) for p, values in candidates.items()},
                  comparisons=comparisons, positive_pairs=positive, invalid_pairs=invalid,
                  negative_volume_diagnostics=negative,
                  passed=not positive and not invalid and not negative,
                  limitation='Discrete independent source-pose checks, not continuous clearance or physical selector coupling/detent proof',
                  source_content_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                  source_sha256=sources, framework_import=solid_node.__file__,
                  address_space_bytes=limit, numerical_threads=1, wall_seconds=monotonic()-started)
    output = Path(f'_build_evidence/open-run-selector-{fixture}-{samples}.json')
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(output), passed=result['passed'], comparisons=comparisons,
                          positive_pairs=len(positive), invalid_pairs=len(invalid),
                          negative_pairs=len(negative), wall_seconds=result['wall_seconds'])), flush=True)
    return result['passed']


if __name__ == '__main__':
    logging.disable(logging.INFO)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture', choices=('initial', 'postcarry'), default='initial')
    parser.add_argument('--samples', type=int, default=10)
    args = parser.parse_args()
    raise SystemExit(0 if sweep(args.fixture, args.samples) else 1)
