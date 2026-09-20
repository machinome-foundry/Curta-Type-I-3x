"""Measure ball seating on the unchanged shaft, not assumed detent endpoints.

The shaft-local radial direction is +X. Heights are displacements from the
source knob/ball pose. No operating stroke or spring law is chosen here.
"""

import argparse
import json
import math
from pathlib import Path
import cadquery as cq
import trimesh
import manifold3d as manifold
from simulation.standard.parts import ReversingShaft
from simulation.tools.carry_phase import solid


def probe(native=False, z_seam=False, ball_radius=2.7):
    shaft = ReversingShaft().shape()
    print_mesh = trimesh.load_mesh(Path(__file__).resolve().parents[2] /
        'STLs/27 - Assemble Reversing Lever/reversing shaft.stl')
    printed = solid(print_mesh)
    # Actual STEP sphere is R2.7 despite the 5mm part name. Manual p28 calls
    # for a nominal 5mm bought ball; --ball-radius 2.5 compares that separately.
    sphere = solid(trimesh.creation.icosphere(subdivisions=4, radius=ball_radius))
    radius = math.hypot(19.505705679 - 17.613968679,
                        59.407726119 - 54.210221429)
    for height in (-7.6427, -6.8425, -6, -5.5, -5.0925, -4.5, -3, 0,
                   3, 3.4075, 3.9075, 4.5, 5.1575):
        z = 85.4425 + height

        def overlap(radial):
            ball = cq.Solid.makeSphere(ball_radius, cq.Vector(radial, 0, z),
                                       dir=cq.Vector(0, 0, 1) if z_seam else cq.Vector(1, 1, 1),
                                       angleDegrees1=-90, angleDegrees2=90)
            common = shaft.intersect(ball)
            if not common.isValid():
                raise ValueError((height, radial, 'invalid native common'))
            return common.Volume()

        def mesh_overlap(radial):
            common = printed ^ sphere.translate((radial, 0, z))
            if common.status() != manifold.Error.NoError:
                raise ValueError((height, radial, common.status()))
            return common.volume()

        ml, mh = 2., 9.
        assert mesh_overlap(ml) > 0 and mesh_overlap(mh) <= 0
        for _ in range(20):
            middle = (ml + mh) / 2
            if mesh_overlap(middle) > 0:
                ml = middle
            else:
                mh = middle
        row = {'knob_height': height, 'ball_local_z': z,
               'ball_radius': ball_radius,
               'faceted_contact_radius_bracket': [ml, mh],
               'source_ball_center_radius': radius,
               'source_radial_overlap_mm3_faceted': mesh_overlap(radius)}
        if native:
            # Native common is an independently audited diagnostic here, not
            # the reference: it has disagreed with the source print and with
            # the analytic cone on the lower flank. Never silently adopt it.
            try:
                row['native_common_at_mesh_contact_minus_.01'] = overlap(ml - .01)
                row['native_common_at_mesh_contact_plus_.01'] = overlap(mh + .01)
            except ValueError as error:
                row['native_refusal'] = str(error)
        print(json.dumps(row), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', action='store_true',
                        help='Audit native common beside the print contact, not as a reference')
    parser.add_argument('--z-seam', action='store_true',
                        help='Reproduce the refused pole-aligned native Boolean')
    parser.add_argument('--ball-radius', type=float, default=2.7,
                        help='Actual CAD sphere radius by default; use 2.5 for manual hardware')
    args = parser.parse_args()
    if not math.isfinite(args.ball_radius) or args.ball_radius <= 0:
        parser.error('--ball-radius must be finite and positive')
    probe(args.native, args.z_seam, args.ball_radius)
