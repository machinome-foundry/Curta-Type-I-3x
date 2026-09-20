"""Measure thread interference before choosing any local fit."""

import json
import logging
import numpy as np
import manifold3d as manifold
import trimesh
from simulation.housing_thread import HousingThreadBench
from simulation.cover_fits import mesh_solid


def extent(body):
    points = body.to_mesh64().vert_properties[:, :3]
    if not len(points):
        return None
    radii = np.linalg.norm(points[:, :2], axis=1)
    return {'bounds': [points.min(axis=0).tolist(), points.max(axis=0).tolist()],
            'radius': [float(radii.min()), float(radii.max())]}


def probe():
    logging.disable(logging.INFO)
    bench = HousingThreadBench()
    bench.assemble()
    bench.build_stls()
    housing_node = bench.upper_housing
    source = trimesh.load_mesh(housing_node.stl_source)
    current = trimesh.load_mesh(housing_node.stl_file)
    print(json.dumps({'housing_source_volume': source.volume,
                      'housing_fitted_volume': current.volume,
                      'removed_volume': source.volume - current.volume,
                      'fitted_triangles': len(current.faces),
                      'watertight': current.is_watertight}), flush=True)
    counts = np.bincount(current.edges_unique_inverse)
    bad_edges = current.edges_unique[counts != 2]
    if len(bad_edges):
        points = current.vertices[bad_edges]
        print(json.dumps({'non_two_sided_edges': len(bad_edges),
                          'edges': points.tolist()}), flush=True)
    cover, housing = (mesh_solid(node.mesh) for node in
                      (bench.digits_cover, bench.upper_housing))
    for height in (-.3, -.1, -.05, 0, .05, .1, .3):
        common = cover.translate((0, 0, height)) ^ housing
        assert common.status() == manifold.Error.NoError, common.status()
        print(json.dumps({'cover_rise': height, 'overlap_mm3': common.volume(),
                          'contact': extent(common)}), flush=True)
        if height == 0:
            for region in common.decompose():
                print(json.dumps({'region_mm3': region.volume(),
                                  'contact': extent(region)}), flush=True)


if __name__ == '__main__':
    probe()
