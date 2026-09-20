"""Read the two source clip mouths and compare their installed rivet spacing.

No deformation, mounting correction or deployment range is adopted here.
The source first-rivet swivel is only the already-calibrated diagnostic.
"""

import json
import logging
from math import cos, sin, radians, hypot
import numpy as np
from simulation.standard.parts import ClearingRing


def main():
    logging.disable(logging.INFO)
    loop = ClearingRing().shape()
    assert loop.isValid() and len(loop.Solids()) == 1
    arcs = {}
    for edge in loop.Edges():
        if edge.geomType() != 'CIRCLE' or abs(edge.radius()-3.825) > 1e-7:
            continue
        center = edge.arcCenter()
        arcs[tuple(round(v, 7) for v in center.toTuple())] = [
            edge.positionAt(t).toTuple() for t in (0, .5, 1)]
    for center, points in sorted(arcs.items()):
        print(json.dumps({'source_clip_center': center, 'arc_points': points}), flush=True)
    for edge in loop.Edges():
        ends = [edge.positionAt(t).toTuple() for t in (0, 1)]
        if (edge.geomType() == 'LINE' and all(abs(p[2]) < 1e-7 for p in ends)
                and any(15 < p[0] < 45 and 12 < p[1] < 45 for p in ends)):
            print(json.dumps({'second_clip_line_ends': ends}), flush=True)

    # Unchanged source placements from standard/layers.py. Work in their
    # common assembly frame, before the carriage's shared datum correction.
    pegs = np.array(((39.372124643, 10.943003894), (37.348717788, -16.582726336)))
    axis = np.array((.603780106, .797150916))
    axis /= np.linalg.norm(axis)
    rotation = 2*np.outer(axis, axis)-np.eye(2)  # source 180-degree 3D rotation
    origin = np.array((50.343540869, -28.04260917))
    centers = sorted({(c[0], c[1]) for c in arcs}, reverse=True)
    assert len(centers) == 2, centers
    placed = np.array(centers) @ rotation.T + origin
    assert np.linalg.norm(placed[0]-pegs[0]) < .00001
    print(json.dumps({'clip_spacing_mm': hypot(*(placed[1]-placed[0])),
                      'rivet_spacing_mm': hypot(*(pegs[1]-pegs[0])),
                      'source_placed_clip_centers': placed.tolist(),
                      'source_rivet_centers': pegs.tolist()}), flush=True)
    for angle in range(-95, -69):
        theta = radians(angle)
        swivel = np.array(((cos(theta), -sin(theta)), (sin(theta), cos(theta))))
        centers_at_angle = (placed-pegs[0]) @ swivel.T + pegs[0]
        # Express the peg relative to the clip in the original part frame;
        # compare this offset to the measured mouth, not only circle centres.
        relative = (pegs[1]-centers_at_angle[1]) @ swivel @ rotation
        print(json.dumps({'swivel_deg': angle,
                          'second_peg_offset_in_clip_frame': relative.tolist(),
                          'centre_distance_mm': float(np.linalg.norm(relative))}), flush=True)


if __name__ == '__main__':
    main()
