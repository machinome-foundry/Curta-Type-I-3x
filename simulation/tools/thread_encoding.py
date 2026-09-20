"""Audit generated fitting precision against an actual binary-STL round trip."""

import io
import json
import logging
import numpy as np
import trimesh
from simulation.cover_fits import FittedUpperHousing, fitted_mesh


if __name__ == '__main__':
    logging.disable(logging.INFO)
    part = FittedUpperHousing(thread_mesh_precision=0)
    source = trimesh.load_mesh(part.stl_source)
    body = part.fitted_body(source)
    for reset in (False, True):
        base = body.as_original() if reset else body
        for precision in (0, .000008, .000016, .00005, .0001, .0003, .001):
            candidate = base.simplify(precision)
            fresh = fitted_mesh(candidate)
            encoded = trimesh.load_mesh(io.BytesIO(fresh.export(file_type='stl')), file_type='stl')
            counts = np.bincount(encoded.edges_unique_inverse)
            print(json.dumps({'reset_face_provenance': reset, 'precision': precision,
                              'kernel_tolerance': candidate.get_tolerance(),
                              'triangles': len(fresh.faces),
                              'fresh_watertight': fresh.is_watertight,
                              'encoded_watertight': encoded.is_watertight,
                              'non_two_sided_edges': int(np.count_nonzero(counts != 2)),
                              'volume': encoded.volume}), flush=True)
