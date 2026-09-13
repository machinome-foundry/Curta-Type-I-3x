"""Evidence-only frozen-event sweep; no running model or geometry is changed.

Pose the old Curta once at a candidate event, then independently move the
selected slider, its coupled sleeve and its fitted spring along the proposed
instantaneous transition. Other bodies stay fixed. Include every physical
body in the published assembly, with no hidden or omitted-neighbour exemption.
Print JSON records to stdout; callers retain them as project evidence.
"""

import argparse
import hashlib
import json
import logging
from itertools import combinations
from time import monotonic

import numpy as np
import manifold3d as manifold

from solid_node.simulation import Driver
from simulation.carry import CarryBench
from simulation.carry_profiles import PIN_DROP, RESET_LIFT
from simulation.curta import Curta
from simulation.cycle import RESULT_INPUT_END, RESULT_CARRY_END, TOOTH_PITCH
from simulation.standard.carry import ResultsLever2
from simulation.tools.carry_phase import solid as manifold_solid
from simulation.tools.interference import world_solids


class SecondCarryBench(ResultsLever2):
    engaged = Driver(default=0, range=(0, 1))
    engaged.drives(ResultsLever2.engage)


def crossing(points, height):
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if y0 <= height < y1:
            return x0 + (height-y0)*(x1-x0)/(y1-y0)
    raise ValueError(f'No rising crossing of {height}')


def event_definition(name):
    stage = int(name[-1])
    if name.startswith('trip'):
        digit = crossing(PIN_DROP, .61*4.2)
        end = RESULT_INPUT_END if stage == 1 else RESULT_CARRY_END + 20
        angle = end-TOOTH_PITCH + (digit-9)*TOOTH_PITCH
        return dict(name=name, stage=stage, crank_deg=angle,
                    driving_digit=digit, start_drop_mm=.61*4.2, end_drop_mm=4.2)
    return dict(name=name, stage=stage,
                crank_deg=crossing(RESET_LIFT, 1.85)+20*(stage-1),
                start_drop_mm=4.2-1.85, end_drop_mm=0.0)


def physical_nodes(node, path='Curta'):
    if node.rigid or not node.children:
        yield path, node
    else:
        for child in node.children:
            yield from physical_nodes(child, path+'.'+child.name)


def bounds(shape):
    box = shape.BoundingBox()
    return np.array([[box.xmin, box.ymin, box.zmin],
                     [box.xmax, box.ymax, box.zmax]])


def overlaps_bounds(a, b):
    return bool(np.all(np.minimum(a[1], b[1]) >= np.maximum(a[0], b[0])))


def paths_for(stage):
    prefix = 'Curta.carry_mechanism.result_carries.results_tens_lever_assembly_'+str(stage)
    sleeve = ('Curta.transmission.result.tens.p_10220_410003_1_419227' if stage == 1
              else 'Curta.transmission.result.hundreds.p_10220_410003_1_419086')
    return (prefix+'.tens_slider_for_results', sleeve,
            prefix+'.carry_lever_spring.wire')


def emit(record):
    print(json.dumps(record, sort_keys=True), flush=True)


def sweep(event, samples, kernel, include_inventory):
    started = monotonic()
    definition = event_definition(event)
    stage = definition['stage']
    moving_paths = paths_for(stage)
    root = Curta()
    root.set_state(initial_result=99, initial_turns=0, operand=1,
                   crank_turns=definition['crank_deg']/360, subtract=0,
                   carriage_position=0, carriage_lift=0, clear=0)
    root.assemble()
    nodes = dict(physical_nodes(root))
    assert set(moving_paths) <= set(nodes), moving_paths
    emit(dict(kind='progress', phase='native inventory', event=definition,
              physical_bodies=len(nodes)))
    native = world_solids(root, include_flexible=True)
    assert set(native) <= set(nodes), sorted(set(native)-set(nodes))
    mesh_only = {}
    scene_bounds = {path: bounds(shape) for path, shape in native.items()}
    for path, node in nodes.items():
        if path not in native:
            assert not node.exact, path
            node.assemble()
            node.build_stls()
            mesh_only[path] = node.mesh
            scene_bounds[path] = mesh_only[path].bounds.copy()
    assert set(scene_bounds) == set(nodes)
    inventory = [dict(path=p, representation='native' if p in native else 'source-mesh')
                 for p in sorted(nodes)]
    inventory_hash = hashlib.sha256(json.dumps(inventory, sort_keys=True).encode()).hexdigest()

    carry = getattr(root.carry_mechanism.result_carries,
                    'results_tens_lever_assembly_'+str(stage))
    current_drop = 4.2*carry.engage.value
    bench = (CarryBench if stage == 1 else SecondCarryBench)()
    active_meshes = {}
    active_manifolds = {}
    sleeve_mesh = None

    def moving(drop):
        nonlocal sleeve_mesh
        bench.set_state(engaged=drop/4.2)
        bench.assemble()
        assert abs(bench.engage.value-drop/4.2) < 1e-12
        parts = world_solids(bench, include_flexible=True)
        active_meshes.clear()
        active_manifolds.clear()
        if kernel == 'faceted' or mesh_only:
            bench.build_stls()
            if sleeve_mesh is None:
                nodes[moving_paths[1]].build_stls()
                sleeve_mesh = nodes[moving_paths[1]].mesh
            shifted = sleeve_mesh.copy()
            shifted.apply_translation((0, 0, current_drop-drop))
            active_meshes.update({
                moving_paths[0]: bench.tens_slider_for_results.mesh,
                moving_paths[1]: shifted,
                moving_paths[2]: bench.carry_lever_spring.wire.mesh,
            })
        return {
            moving_paths[0]: parts['Curta.tens_slider_for_results'],
            moving_paths[1]: native[moving_paths[1]].translate((0, 0, current_drop-drop)),
            moving_paths[2]: parts['Curta.carry_lever_spring.wire'],
        }

    # Standalone source placements must reproduce the installed frame first.
    reference = moving(current_drop)
    for path in moving_paths:
        assert np.max(np.abs(bounds(reference[path])-scene_bounds[path])) < 1e-5, path
        assert abs(reference[path].Volume()-native[path].Volume()) < 1e-5, path
    a = moving(0)[moving_paths[0]]
    b = moving(4.2)[moving_paths[0]]
    assert np.max(np.abs(bounds(b)-bounds(a)-(0,0,-4.2))) < 1e-5

    static_paths = sorted(set(nodes)-set(moving_paths))
    candidates = {p: set() for p in moving_paths}
    positive, invalid, nonpositive = {}, {}, {}
    comparisons = dict(native=0, faceted=0)
    mesh_cache = {}

    def faceted(path):
        if path in active_meshes:
            if path not in active_manifolds:
                active_manifolds[path] = manifold_solid(active_meshes[path])
            return active_manifolds[path]
        if path not in mesh_cache:
            if path not in mesh_only:
                nodes[path].build_stls()
            mesh = mesh_only[path] if path in mesh_only else nodes[path].mesh
            mesh_cache[path] = manifold_solid(mesh)
        return mesh_cache[path]

    def compare(first, second, active, drop):
        aa = active[first]
        bb = active[second] if second in active else native.get(second)
        key = first+' / '+second
        if kernel == 'exact' and bb is not None:
            contact = aa.intersect(bb)
            comparisons['native'] += 1
            good, volume = contact.isValid(), contact.Volume()
            method = 'native'
        else:
            contact = faceted(first) ^ faceted(second)
            comparisons['faceted'] += 1
            good, volume = contact.status() == manifold.Error.NoError, contact.volume()
            method = 'faceted'
        if not good:
            invalid[key] = dict(drop_mm=drop, kernel=method, volume_mm3=volume)
        elif volume > 0:
            previous = positive.get(key)
            if previous is None or volume > previous['volume_mm3']:
                positive[key] = dict(drop_mm=drop, kernel=method, volume_mm3=volume)
                if method == 'native':
                    positive[key]['center_mm'] = contact.Center().toTuple()
                    positive[key]['bounds_mm'] = bounds(contact).tolist()
        elif volume < 0:
            nonpositive[key] = dict(drop_mm=drop, kernel=method, volume_mm3=volume)

    drops = np.linspace(definition['start_drop_mm'], definition['end_drop_mm'], samples)
    for index, drop in enumerate(drops):
        active = moving(float(drop))
        boxes = {p: bounds(shape) for p, shape in active.items()}
        for first in moving_paths:
            for second in static_paths:
                if overlaps_bounds(boxes[first], scene_bounds[second]):
                    candidates[first].add(second)
                    compare(first, second, active, float(drop))
        for first, second in combinations(moving_paths, 2):
            if overlaps_bounds(boxes[first], boxes[second]):
                candidates[first].add(second)
                compare(first, second, active, float(drop))
        if index % 10 == 0 or index == samples-1:
            emit(dict(kind='progress', event=event, sample=index+1, samples=samples,
                      positive_pairs=len(positive), invalid_pairs=len(invalid)))
    result = dict(kind='result', event=definition, kernel=kernel, samples=samples,
                  method='Frozen prescribed background; independent slider/sleeve/spring transition; no source geometry edits',
                  limitation='Discrete pose checks only, not a continuous path or spring-force certificate',
                  full_physical_inventory_sha256=inventory_hash,
                  physical_bodies=len(nodes), native_bodies=len(native),
                  mesh_only_bodies=sorted(mesh_only), moving_paths=moving_paths,
                  original_prescribed_drop_mm=current_drop,
                  frame_and_stroke_guards_passed=True,
                  candidate_neighbours={p: sorted(v) for p,v in candidates.items()},
                  positive_pairs=positive, invalid_pairs=invalid,
                  negative_volume_diagnostics=nonpositive,
                  comparisons=comparisons, wall_seconds=monotonic()-started)
    if include_inventory:
        result['physical_inventory'] = inventory
    emit(result)
    return not positive and not invalid


if __name__ == '__main__':
    logging.disable(logging.INFO)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--event', choices=['trip1','trip2','reset1','reset2'], required=True)
    parser.add_argument('--samples', type=int, default=41)
    parser.add_argument('--kernel', choices=['exact','faceted'], default='faceted')
    parser.add_argument('--inventory', action='store_true')
    args = parser.parse_args()
    if args.samples < 2:
        parser.error('--samples must include at least both endpoints')
    raise SystemExit(0 if sweep(args.event,args.samples,args.kernel,args.inventory) else 1)
