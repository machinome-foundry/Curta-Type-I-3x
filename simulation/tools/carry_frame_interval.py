"""Conservative continuous spring/frame enclosure, independent of its cutters.

Molejo's published Hermite/Catmull-Rom definition supplies Bezier control
hulls; lines/arcs use analytic extrema. Circular cross sections are enclosed
by bounding balls regardless of transported-frame roll. Subdivision
is over curve parameter AND the complete detent spread interval, not poses.
"""

import argparse
import hashlib
import json
import logging
from math import atan2, ceil, cos, floor, pi, sin
from pathlib import Path
from time import monotonic

import cadquery as cq
import numpy as np

from simulation.carry_frame import CarryFrameBench
from simulation.detents import RESULTS
from simulation.tools.open_run_transitions import bounds


ROUNDING = 1e-8
SURFACE_ALLOWANCE = 2e-6  # exceeds Molejo's declared 1e-6 mm sweep tolerance


def matrix(operations):
    result = np.eye(4)
    for op in operations:
        current = np.eye(4)
        if hasattr(op, 'angle'):
            axis = np.array(op.axis, dtype=float)
            axis /= np.linalg.norm(axis)
            x, y, z = axis
            skew = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
            theta = op.angle*pi/180
            current[:3, :3] = np.eye(3)+sin(theta)*skew+(1-cos(theta))*(skew@skew)
        elif hasattr(op, 'translation'):
            current[:3, 3] = op.translation
        else:
            raise ValueError('Unsupported public placement operation')
        result = current@result
    return result


def wire_frame(root, station):
    carry = getattr(root, station)
    spring = carry.carry_lever_spring
    return matrix([*spring.wire.operations, *spring.operations,
                   *carry.operations, *root.operations])


def literal(value, params):
    if isinstance(value, dict):
        if set(value) != {'param'}:
            raise ValueError('Not a plain Molejo parameter')
        return params[value['param']]
    if isinstance(value, list):
        return np.array([literal(item, params) for item in value])
    return value


def pieces(document, params, world):
    """Independent analytic centerline in the actual installed world frame."""
    rotation = world[:3, :3]
    point = lambda value: rotation@value+world[:3, 3]
    current = np.zeros(3)
    result = []
    for primitive in document['path']:
        kind = primitive['type']
        p = {key: literal(value, params) for key, value in primitive.items() if key != 'type'}
        if kind == 'line':
            result.append(dict(kind=kind, points=np.array([point(current), point(p['to'])])))
            current = p['to']
        elif kind == 'arc':
            axis = p['axis']/np.linalg.norm(p['axis'])
            arm = current-p['center']
            base = p['center']+axis*np.dot(axis, arm)
            radial = arm-axis*np.dot(axis, arm)
            side = np.cross(axis, radial)
            result.append(dict(kind=kind, base=point(base), a=rotation@radial,
                               b=rotation@side, angle=p['angle']))
            current = base+cos(p['angle'])*radial+sin(p['angle'])*side
        elif kind == 'spline':
            nodes = np.vstack([current, p['points']])
            nodes = np.array([point(node) for node in nodes])
            if 'start_tangent' not in p or 'end_tangent' not in p:
                raise ValueError('This certificate requires explicit spline end directions')
            directions = [rotation@p[name]/np.linalg.norm(p[name])
                          for name in ('start_tangent', 'end_tangent')]
            tangents = [(nodes[1]-nodes[0]), *( (nodes[i+1]-nodes[i-1])/2
                         for i in range(1, len(nodes)-1)), nodes[-1]-nodes[-2]]
            tangents[0] = directions[0]*np.linalg.norm(nodes[1]-nodes[0])
            tangents[-1] = directions[1]*np.linalg.norm(nodes[-1]-nodes[-2])
            for i in range(len(nodes)-1):
                result.append(dict(kind='bezier', points=np.array([
                    nodes[i], nodes[i]+tangents[i]/3,
                    nodes[i+1]-tangents[i+1]/3, nodes[i+1]]),
                    start_chord=nodes[1]-nodes[0] if i == 0 else None,
                    end_chord=nodes[-1]-nodes[-2] if i == len(nodes)-2 else None,
                    start_direction=directions[0], end_direction=directions[1]))
            current = literal(primitive['points'], params)[-1]
        else:
            raise ValueError('Unbounded primitive: '+kind)
    return result


def chord_interval(a, b):
    delta = b-a
    fraction = float(np.clip(-np.dot(a, delta)/np.dot(delta, delta), 0, 1)) if np.dot(delta, delta) else 0
    return np.array([np.linalg.norm(a+fraction*delta), max(np.linalg.norm(a), np.linalg.norm(b))])


def split(poles, t):
    rows = [poles]
    for _ in range(3):
        rows.append((1-t)*rows[-1][:-1]+t*rows[-1][1:])
    return np.array([row[0] for row in rows]), np.array([row[-1] for row in rows[::-1]])


def enclosure(a, b, u0, u1):
    if a['kind'] == 'bezier':
        # End tangent magnitudes are norms of affine chords, not assumed
        # affine. Enclose their interior minimum as well as endpoint maxima.
        poles = np.array([np.minimum(a['points'], b['points']), np.maximum(a['points'], b['points'])])
        for index, endpoint, name, sign in ((1, 0, 'start', 1), (2, 3, 'end', -1)):
            if a[name+'_chord'] is not None:
                lengths = chord_interval(a[name+'_chord'], b[name+'_chord'])
                direction = sign*a[name+'_direction']/3
                candidates = np.array([source['points'][endpoint]+length*direction
                    for source in (a, b) for length in lengths])
                poles[:, index] = [candidates.min(axis=0), candidates.max(axis=0)]
        restricted = []
        for boundary in poles:
            right = split(boundary, u0)[1]
            segment = split(right, (u1-u0)/(1-u0))[0] if u0 < 1 else right
            restricted.append(segment)
        return np.array([restricted[0].min(axis=0), restricted[1].max(axis=0)])
    candidates = []
    for piece in (a, b):
        if piece['kind'] == 'line':
            candidates.extend((1-u)*piece['points'][0]+u*piece['points'][1] for u in (u0, u1))
        else:
            lo, hi = sorted((u0*piece['angle'], u1*piece['angle']))
            angles = [lo, hi]
            for x, y in zip(piece['a'], piece['b']):
                extremum = atan2(y, x)
                angles.extend(extremum+k*pi for k in range(ceil((lo-extremum)/pi),
                                                           floor((hi-extremum)/pi)+1))
            candidates.extend(piece['base']+cos(t)*piece['a']+sin(t)*piece['b'] for t in angles)
    return np.array([np.min(candidates, axis=0), np.max(candidates, axis=0)])


def at(piece, u):
    if piece['kind'] == 'line':
        return (1-u)*piece['points'][0]+u*piece['points'][1]
    if piece['kind'] == 'arc':
        return piece['base']+cos(u*piece['angle'])*piece['a']+sin(u*piece['angle'])*piece['b']
    p = piece['points']
    return (1-u)**3*p[0]+3*u*(1-u)**2*p[1]+3*u*u*(1-u)*p[2]+u**3*p[3]


def certify(station, max_depth=24):
    started = monotonic()
    # This proof's affine parameter/placement hypothesis is the reviewed
    # project law, not a claim to infer arbitrary Python functions from samples.
    model_hash = hashlib.sha256(Path('simulation/carry_spring.py').read_bytes()).hexdigest()
    if model_hash != '68cff8e1e2b819d37d8ac6e6124ec3809ea52f6aecd0e204ada6b9ec37f07836':
        raise ValueError('Re-audit the changed spring law before using its continuous certificate')
    model = CarryFrameBench()
    captures = []
    for drop in (4.2, 2.562):
        model.set_state(drop_mm=drop)
        model.assemble()
        wire = getattr(model, station).carry_lever_spring.wire
        shape = wire.render()
        document = shape.to_dict()
        params = {name: getattr(wire, name).value for name in shape.params}
        captures.append((params, wire_frame(model, station)))
    if document['profile'] != {'type': 'circle', 'radius': .3}:
        raise ValueError('Expected the unchanged .6 mm wire')
    for primitive in document['path']:
        for name in ('axis', 'angle', 'start_tangent', 'end_tangent'):
            if 'param' in json.dumps(primitive.get(name)):
                raise ValueError('This enclosure requires fixed path angles and tangent directions')
    assert np.max(np.abs(captures[0][1][:3, :3]-captures[1][1][:3, :3])) < 1e-14
    spread_bounds = (min(y for _, y in RESULTS), max(y for _, y in RESULTS))
    assert spread_bounds == (.094711, 1.327148)
    cache = {}

    def curve(fraction):
        if fraction not in cache:
            values = {name: (1-fraction)*captures[0][0][name]+fraction*captures[1][0][name]
                      for name in captures[0][0]}
            world = (1-fraction)*captures[0][1]+fraction*captures[1][1]
            cache[fraction] = pieces(document, values, world)
        return cache[fraction]

    # Cross-check the independent definition against actual evaluated ring
    # centres and driver-owned values at every detent knot and the preload.
    max_error = 0
    for drop in sorted({4.2*x for x, _ in RESULTS} | {1.1630815}):
        model.set_state(drop_mm=drop)
        model.assemble()
        carry = getattr(model, station)
        wire = carry.carry_lever_spring.wire
        shape = wire.render()
        values = {name: getattr(wire, name).value for name in shape.params}
        fraction = (carry.carry_lever_spring.spread.value-spread_bounds[0])/(spread_bounds[1]-spread_bounds[0])
        expected_params = {name: (1-fraction)*captures[0][0][name]+fraction*captures[1][0][name] for name in values}
        assert max(abs(values[name]-expected_params[name]) for name in values) < 1e-12
        world = wire_frame(model, station)
        assert np.max(np.abs(world-((1-fraction)*captures[0][1]+fraction*captures[1][1]))) < 1e-12
        mesh = shape.evaluate(**values)
        centers = mesh.vertices[:-2].reshape(-1, 24, 3).mean(axis=1)
        centers = centers@world[:3, :3].T+world[:3, 3]
        evaluated = curve(fraction)
        independent = [at(p, k/24) for p in evaluated for k in range(24)]+[at(evaluated[-1], 1)]
        error = np.max(np.abs(centers-independent))
        max_error = max(max_error, float(error))
        if error > 1e-9:
            raise ValueError(f'Independent centerline does not match Molejo: {error}')
    frame = model.frame.main_body.shape()
    whole = [enclosure(a, b, 0, 1) for a, b in zip(curve(0), curve(1))]
    centerline_bounds = np.array([np.min([box[0] for box in whole], axis=0),
                                 np.max([box[1] for box in whole], axis=0)])
    initial = [(i, 0., 1., k/8, (k+1)/8, 0) for i in range(len(curve(0))) for k in range(8)]
    stack, checked, clear, unresolved = initial, 0, 0, []
    while stack:
        index, s0, s1, u0, u1, depth = stack.pop()
        box = enclosure(curve(s0)[index], curve(s1)[index], u0, u1)
        radius = .3+SURFACE_ALLOWANCE+ROUNDING
        center = box.mean(axis=0)
        # The circumsphere of the centerline box, expanded by the wire
        # radius, contains every cross section in this entire interval.
        # Unlike a radius-expanded box this converges to a round tube and
        # does not invent permanent square corners beside the pocket end.
        radius += np.linalg.norm(box[1]-box[0])/2
        ball = cq.Solid.makeSphere(radius, cq.Vector(*center),
                                  angleDegrees1=-90, angleDegrees2=90,
                                  angleDegrees3=360)
        assert abs(ball.Volume()-4*pi*radius**3/3) < 1e-8
        common = frame.intersect(ball)
        checked += 1
        if not common.isValid() or common.Volume() < 0:
            raise ValueError('Invalid/signed-negative native enclosure/frame Boolean')
        if common.Volume() == 0:
            clear += 1
        elif depth >= max_depth:
            unresolved.append(dict(piece=index, spread_fraction=[s0, s1], curve_parameter=[u0, u1],
                                   centerline_bounds_mm=box.tolist(), ball_radius_mm=float(radius),
                                   native_volume_mm3=common.Volume()))
        else:
            smid, umid = (s0+s1)/2, (u0+u1)/2
            options = [((s0, s1, u0, umid), (s0, s1, umid, u1)),
                       ((s0, smid, u0, u1), (smid, s1, u0, u1))]
            def score(children):
                return max(np.linalg.norm(np.diff(enclosure(curve(a)[index], curve(b)[index], c, d), axis=0))
                           for a, b, c, d in children)
            children = min(options, key=score)
            stack.extend((index, a, b, c, d, depth+1) for a, b, c, d in children)
        if checked % 100 == 0:
            print(json.dumps(dict(phase='interval', station=station, checked=checked,
                                 queued=len(stack), unresolved=len(unresolved))), flush=True)
        if len(unresolved) >= 8:
            break
    result = dict(kind='continuous-spring-frame-enclosure', station=station,
                  conservative_full_centerline_bounds_mm=centerline_bounds.tolist(),
                  spread_bounds_mm=spread_bounds, centerline_comparison_error_mm=max_error,
                  surface_allowance_mm=SURFACE_ALLOWANCE, rounding_allowance_mm=ROUNDING,
                  clear_enclosures=clear, native_checks=checked, max_depth=max_depth,
                  unresolved=unresolved, queued=len(stack), passed=not unresolved and not stack,
                  elapsed_seconds=monotonic()-started,
                  model_sha256=model_hash)
    path = Path('_build_evidence/carry-frame-interval-'+station+'.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)
    return result['passed']


if __name__ == '__main__':
    logging.disable(logging.INFO)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--station', choices=('first', 'second'), default='first')
    args = parser.parse_args()
    raise SystemExit(0 if certify(args.station) else 1)
