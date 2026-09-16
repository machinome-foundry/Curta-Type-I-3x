"""Measure the source markers' angular footprints around the machine axis."""

import json
import logging
import argparse
import numpy as np
from simulation.standard.layers import LowerDecimalMarkers, UpperDecimalMarkers
from simulation.tools.carry_phase import solid


def probe():
    logging.disable(logging.INFO)
    for kind, cls, indices, center in (
            ('lower', LowerDecimalMarkers, range(1, 6), (-.406900356, .745841949, 0)),
            ('upper', UpperDecimalMarkers, range(6, 11), (.386511579, -.028412332, 0))):
        bank = cls()
        bank.assemble()
        bank.build_stls()
        markers = []
        for index in indices:
            node = getattr(bank, f'decimal_marker_{index}')
            mesh = node.position_marker.mesh
            mesh.apply_translation(-np.asarray(center))
            vertices = mesh.vertices
            angles = np.degrees(np.arctan2(vertices[:, 1], vertices[:, 0]))
            print(json.dumps({'bank': kind, 'marker': index,
                              'angular_bounds': [float(angles.min()), float(angles.max())],
                              'xyz_bounds': node.position_marker.mesh.bounds.tolist()}), flush=True)
            markers.append((index, solid(mesh), float(angles.mean())))
        for (index, body, angle), (other, neighbour, other_angle) in zip(
                markers, markers[1:] + markers[:1]):
            separation = (angle - other_angle) % 360
            low, high = max(0, separation - 15), separation
            assert (body.rotate((0, 0, -low)) ^ neighbour).is_empty()
            assert not (body.rotate((0, 0, -high)) ^ neighbour).is_empty()
            for _ in range(30):
                middle = (low + high) / 2
                if (body.rotate((0, 0, -middle)) ^ neighbour).is_empty():
                    low = middle
                else:
                    high = middle
            print(json.dumps({'bank': kind, 'clockwise_pair': [index, other],
                              'last_free_deg': low, 'first_contact_deg': high}), flush=True)


def native_probe():
    from solid_node.test import TestCase
    from simulation.decimal_markers import MarkerGeometryBench, LOWER_GAPS, UPPER_GAPS
    logging.disable(logging.INFO)
    bench = MarkerGeometryBench()
    bench.set_state(**{f'marker_{i}': 0 for i in range(1, 11)})
    bench.assemble()
    bench.build_stls()
    checks = TestCase()
    for name, first, gaps in (('lower', 1, LOWER_GAPS), ('upper', 6, UPPER_GAPS)):
        bank = getattr(bench, name)
        for offset, guess in enumerate(gaps):
            index = first + offset
            other = first + (offset + 1) % 5
            moving = getattr(bank, f'decimal_marker_{index}').position_marker
            fixed = getattr(bank, f'decimal_marker_{other}').position_marker
            bench.set_state(**{f'marker_{i}': 0 for i in range(1, 11)})
            def clear(angle):
                bench.set_state(**{f'marker_{index}': -angle})
                try:
                    checks.assertNotIntersecting(moving, fixed)
                except AssertionError:
                    return False
                return True
            low, high = max(0, guess - 1), guess + 1
            assert clear(low), (name, index, 'initial overlap')
            assert not clear(high), (name, index, 'no contact')
            for _ in range(20):
                middle = (low + high) / 2
                if clear(middle):
                    low = middle
                else:
                    high = middle
            print(json.dumps({'kernel': 'exact', 'bank': name,
                              'clockwise_pair': [index, other],
                              'last_free_deg': low, 'first_contact_deg': high}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', action='store_true')
    if parser.parse_args().native:
        native_probe()
    else:
        probe()
