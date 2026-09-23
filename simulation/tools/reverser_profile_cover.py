"""Investigate convex covers of the actual extruded tooth profiles.

This is an offline instrument, not an operating law. A named outward linear
cover allowance is checked against each native source solid. No volume
epsilon, angular symmetry, interpolated-clearance claim or source edit is
involved. Complete installed-print/mesh coverage and retained-motion admission
are separate obligations before any result can become an operating bound.
"""

import argparse
from collections import Counter
from fractions import Fraction
import json
import logging
from math import cos, isfinite, radians, sin
from pathlib import Path


def cross(a, b, c):
    """Exact orientation of the supplied finite binary coordinates."""
    ax, ay = map(Fraction, a)
    bx, by = map(Fraction, b)
    cx, cy = map(Fraction, c)
    return (bx-ax)*(cy-ay)-(by-ay)*(cx-ax)


def convex_partition(points, triangles):
    """Merge conforming triangles only across shared edges into convex pieces.

    The caller supplies a triangulated face. This does not repair overlapping
    triangles or infer a missing face from a point cloud. Exact orientation
    prevents a numeric concavity tolerance from filling a notch.
    """
    if not points or any(len(p) != 2 or not all(isfinite(v) for v in p)
                         for p in points):
        raise ValueError('Expected finite planar points')
    polygons = []
    for triangle in triangles:
        if (len(triangle) != 3 or len(set(triangle)) != 3 or
                any(not isinstance(i, int) or not 0 <= i < len(points) for i in triangle)):
            raise ValueError('Invalid triangle indices')
        a, b, c = triangle
        sign = cross(points[a], points[b], points[c])
        if sign == 0:
            raise ValueError('Degenerate triangle')
        polygons.append([a, b, c] if sign > 0 else [a, c, b])
    if not polygons:
        raise ValueError('Expected at least one triangle')
    directed = Counter((u, v) for polygon in polygons
                       for u, v in zip(polygon, polygon[1:]+polygon[:1]))
    if any(count != 1 for count in directed.values()):
        raise ValueError('Folded or overlapping triangle neighbours')
    while True:
        edges = {}
        merged = False
        for index, polygon in enumerate(polygons):
            for offset, (u, v) in enumerate(zip(polygon, polygon[1:]+polygon[:1])):
                other = edges.get((v, u))
                if other is None:
                    edges[u, v] = index, offset
                    continue
                previous, start = other
                before = polygons[previous]
                first = before[start+1:]+before[:start+1]
                second = polygon[offset+1:]+polygon[:offset+1]
                candidate = first+second[1:-1]
                if len(candidate) != len(set(candidate)):
                    continue
                vertices = [points[i] for i in candidate]
                if all(cross(a, b, c) >= 0 for a, b, c in
                       zip(vertices, vertices[1:]+vertices[:1], vertices[2:]+vertices[:2])):
                    polygons[previous] = candidate
                    del polygons[index]
                    merged = True
                    break
            if merged:
                break
        if not merged:
            return polygons


def outer_boundary(triangles):
    counts = Counter(tuple(sorted((u, v))) for t in triangles
                     for u, v in zip(t, t[1:]+t[:1]))
    adjacency = {}
    for (u, v), count in counts.items():
        if count > 2:
            raise ValueError('Nonmanifold triangulation')
        if count == 1:
            adjacency.setdefault(u, []).append(v)
            adjacency.setdefault(v, []).append(u)
    if not adjacency or any(len(v) != 2 for v in adjacency.values()):
        raise ValueError('Expected one closed boundary')
    start = next(iter(adjacency))
    order, previous, current = [start], None, start
    while True:
        following = next(v for v in adjacency[current] if v != previous)
        if following == start:
            break
        if following in order:
            raise ValueError('Self-connected boundary')
        order.append(following)
        previous, current = current, following
    if len(order) != len(adjacency):
        raise ValueError('Multiple boundaries, not an unperforated profile')
    return order


def posed_polygons(report, angle=0, translation=(0, 0)):
    """Rigidly place the recorded convex pieces; no vertex welding/symmetry."""
    c, s = cos(radians(angle)), sin(radians(angle))
    tx, ty = translation
    points = [(c*x-s*y+tx, s*x+c*y+ty) for x, y in report['points']]
    result = [[points[i] for i in polygon] for polygon in report['polygons']]
    for polygon in report.get('mesh_cover_polygons', ()):
        result.append([(c*x-s*y+tx, s*x+c*y+ty) for x, y in polygon])
    return result


def projected_mesh_triangles(vertices, faces):
    """Keep each nondegenerate projected face, deduplicating exact footprints.

    No hull, angular copy, tolerance, new source vertex, or mesh repair is
    involved. These pieces describe a full XY projection, not axial slabs.
    """
    points = [tuple(float(v) for v in point[:2]) for point in vertices]
    if not points or any(len(p) != 2 or not all(isfinite(v) for v in p) for p in points):
        raise ValueError('Expected finite source mesh points')
    seen, polygons = set(), []
    for face in faces:
        if len(face) != 3:
            raise ValueError('Expected triangular mesh faces')
        polygon = [points[i] for i in face]
        sign = cross(*polygon)
        if sign == 0:
            continue
        key = tuple(sorted(polygon))
        if key in seen:
            continue
        seen.add(key)
        if sign < 0:
            polygon[1], polygon[2] = polygon[2], polygon[1]
        polygons.append(polygon)
    if not polygons:
        raise ValueError('Source mesh has no spatial XY footprint')
    return polygons


def axial_allowance(report):
    """Read a declared axial length, keeping old isotropic evidence readable."""
    value = report.get('axial_allowance_mm', report['allowance_mm'])
    if not isfinite(value) or value <= 0:
        raise ValueError('Name a positive axial cover allowance')
    return value


def cover_mesh_arrays(report):
    """Extrude the planar triangulation using shared topological indices.

    CAD tessellation returns separate vertices per face. Constructing this
    new candidate directly avoids repairing/welding such a triangle soup.
    It changes neither a source mesh nor a native print.
    """
    points, boundary = report['points'], list(report['boundary'])
    low, high = report['source_height']
    allowance = axial_allowance(report)
    count = len(points)
    vertices = [(x, y, z) for z in (low-allowance, high+allowance) for x, y in points]
    faces = []
    for a, b, c in report['triangles']:
        orientation = cross(points[a], points[b], points[c])
        if orientation == 0:
            raise ValueError('Degenerate cover triangle')
        if orientation < 0:
            b, c = c, b
        faces.extend(((a, c, b), (a+count, b+count, c+count)))
    area = sum(Fraction(points[a][0])*Fraction(points[b][1])
               - Fraction(points[b][0])*Fraction(points[a][1])
               for a, b in zip(boundary, boundary[1:]+boundary[:1]))
    if area == 0:
        raise ValueError('Degenerate cover boundary')
    if area < 0:
        boundary.reverse()
    for a, b in zip(boundary, boundary[1:]+boundary[:1]):
        faces.extend(((a, b, b+count), (a, b+count, a+count)))
    return vertices, faces


def profiles_overlap(first, second):
    """Numeric offline SAT witness, including contact of the outward covers.

    These Python branches are not a portable framework law. AABB rejection
    and early contact exit are instrumentation optimizations only.
    """
    if not first or not second:
        raise ValueError('Both profiles must contain convex pieces')

    def bounded(polygons):
        result = []
        for polygon in polygons:
            if len(polygon) < 3 or any(not all(isfinite(v) for v in p) for p in polygon):
                raise ValueError('Expected finite convex polygons')
            xs, ys = zip(*polygon)
            result.append((polygon, (min(xs), min(ys), max(xs), max(ys))))
        return result

    left, right = bounded(first), bounded(second)
    for a, ba in left:
        for b, bb in right:
            if ba[2] < bb[0] or bb[2] < ba[0] or ba[3] < bb[1] or bb[3] < ba[1]:
                continue
            separated = False
            for polygon in (a, b):
                for u, v in zip(polygon, polygon[1:]+polygon[:1]):
                    nx, ny = u[1]-v[1], v[0]-u[0]
                    pa = [x*nx+y*ny for x, y in a]
                    pb = [x*nx+y*ny for x, y in b]
                    if max(pa) < min(pb) or max(pb) < min(pa):
                        separated = True
                        break
                if separated:
                    break
            if not separated:
                return True
    return False


def checked_native_remainder(outside, native_exclusion=None):
    """Require exact zero outside the cover/exclusion union, with valid results."""
    volume = outside.Volume()
    if not outside.isValid() or not isfinite(volume) or volume < 0:
        raise ValueError(f'Unresolved native cover difference: {volume!r} mm3')
    uncovered = outside
    if native_exclusion is not None:
        if not native_exclusion.isValid():
            raise ValueError('Invalid independently supplied native exclusion')
        if volume > 0:
            uncovered = outside.copy().cut(native_exclusion.copy())
    union_volume = uncovered.Volume()
    if not uncovered.isValid() or not isfinite(union_volume) or union_volume != 0:
        raise ValueError(f'Candidate does not contain native profile: {volume!r} mm3')
    return volume, union_volume


def profile_cover(part, allowance=.005, *, linear_deflection=.0001,
                  angular_deflection=.025, join='arc', include_mesh=False,
                  native_exclusion=None, axial_allowance_mm=None):
    """Cover the source, optionally with a separately proved exclusion solid.

    The caller owes geometric separation of any exclusion from its mating
    prints. This instrument checks coverage of the union; it never turns an
    uncovered positive volume into zero with a numeric tolerance.
    """
    import cadquery as cq

    if not isfinite(allowance) or allowance <= 0:
        raise ValueError('Name a positive outward cover allowance')
    axial = axial_allowance(dict(allowance_mm=allowance,
        axial_allowance_mm=allowance if axial_allowance_mm is None else axial_allowance_mm))
    if any(not isfinite(v) or v <= 0 for v in (linear_deflection, angular_deflection)):
        raise ValueError('Expected positive candidate tessellation settings')
    shape = part.shape().copy()
    if not shape.isValid():
        raise ValueError('Invalid source profile')
    faces = [f for f in shape.Faces() if f.geomType() == 'PLANE'
             and f.normalAt().x == 0 and f.normalAt().y == 0]
    face = max(faces, key=lambda f: f.Area())
    expanded, = face.outerWire().offset2D(allowance, kind=join)
    planar = cq.Face.makeFromWires(expanded)
    # CadQuery's tolerance is relative. It is an input to this candidate,
    # never itself a containment certificate: the native remainder is checked.
    vertices, triangles = planar.tessellate(linear_deflection, angular_deflection)
    points = [(p.x, p.y) for p in vertices]
    polygons = convex_partition(points, triangles)
    boundary = outer_boundary(triangles)
    box = shape.BoundingBox()
    wire = cq.Wire.makePolygon([(points[i][0], points[i][1], box.zmin-axial)
                                for i in boundary], close=True)
    cover = cq.Solid.extrudeLinear(wire, [], cq.Vector(0, 0, box.zlen+2*axial))
    if not cover.isValid():
        raise ValueError('Invalid candidate cover')
    outside = shape.copy().cut(cover.copy())
    volume, union_volume = checked_native_remainder(outside, native_exclusion)
    report = dict(part=type(part).__name__, allowance_mm=allowance,
                axial_allowance_mm=axial,
                offset_join=join,
                linear_deflection=linear_deflection, angular_deflection=angular_deflection,
                source_volume_mm3=shape.Volume(), native_outside_volume_mm3=volume,
                points=points, triangles=triangles, polygons=polygons, boundary=boundary,
                source_height=[box.zmin, box.zmax],
                scope='Offline native profile cover; installed meshes and operation unproved')
    if native_exclusion is not None:
        report['native_outside_cover_and_exclusion_mm3'] = union_volume
        report['scope'] = ('Native cover plus caller-supplied exclusion; caller owes '
                           'exclusion separation and installed mesh/operation proofs')
    if include_mesh:
        from simulation.cover_fits import mesh_solid
        part.assemble()
        part.build_stls()
        mesh_solid(part.mesh)  # Refuse an invalid input before projecting it.
        report['mesh_cover_polygons'] = projected_mesh_triangles(part.mesh.vertices,
                                                                part.mesh.faces)
        report['source_mesh_vertices'] = len(part.mesh.vertices)
        report['source_mesh_faces'] = len(part.mesh.faces)
        report['source_mesh_height'] = list(map(float, part.mesh.bounds[:, 2]))
        report['scope'] = ('Offline native and standalone-source-mesh XY cover; '
                           'complete installed prints, axial slabs and operation unproved')
    return report


def main():
    from simulation.fit import FittedCounterPinion
    from simulation.reverser_inputs import ReversingCounterPinion
    from simulation.standard.parts import (OneToothTurnsStepDrumSegment,
                                            NineToothTurnsStepDrumSegment)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--allowance', type=float, default=.005)
    parser.add_argument('--linear-deflection', type=float, default=.0001)
    parser.add_argument('--angular-deflection', type=float, default=.025)
    parser.add_argument('--join', choices=('arc', 'intersection'), default='arc')
    parser.add_argument('--include-mesh', action='store_true')
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f'Preserve existing evidence: {args.output}')
    with args.output.open('x') as output:
        for part in (FittedCounterPinion(), ReversingCounterPinion(),
                     OneToothTurnsStepDrumSegment(), NineToothTurnsStepDrumSegment()):
            report = profile_cover(part, args.allowance,
                                   linear_deflection=args.linear_deflection,
                                   angular_deflection=args.angular_deflection, join=args.join,
                                   include_mesh=args.include_mesh)
            print(json.dumps(report), file=output, flush=True)
            print(json.dumps(dict(part=report['part'], points=len(report['points']),
                                  triangles=len(report['triangles']),
                                  convex_pieces=len(report['polygons']),
                                  mesh_pieces=len(report.get('mesh_cover_polygons', ())),
                                  outside_mm3=report['native_outside_volume_mm3'])), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
