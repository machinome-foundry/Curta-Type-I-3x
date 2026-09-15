"""Read the built glyph bands through the actual posed part operations.

The expected source glyph boxes below are measured from the upstream drawings,
independently of the production marking declarations. A reversed wrap or a
digit-pitch clocking error must fail, even though its mesh stays on the cylinder.
"""

from functools import lru_cache
from pathlib import Path
import unittest

import numpy as np
import trimesh


# SVG bounding-box centres and widths in millimetres, in numerical order 0..9.
RESULT_GLYPHS = (
    (-3.238762, 3.000265), (2.698800, 2.100000), (8.636401, 3.000001),
    (14.667073, 2.813853), (20.511453, 3.000265), (26.449200, 3.000000),
    (-26.989251, 2.999714), (-21.060501, 2.982197),
    (-15.113869, 2.999714), (-9.176453, 3.000265),
)
INPUT_GLYPHS = (
    (55.512346, 3.749521), (49.106400, 2.625000), (43.825500, 3.750000),
    (38.098434, 3.517303), (31.763504, 3.749917), (26.295298, 3.749996),
    (20.452035, 3.749956), (14.693270, 3.727749),
    (8.765156, 3.749930), (2.921716, 3.749917),
)


def placed_nodes(node, ancestors=()):
    operations = (*node.operations, *ancestors)
    matrix = np.eye(4)
    for operation in operations:
        matrix = operation.matrix() @ matrix
    yield node, matrix
    for child in node.children:
        yield from placed_nodes(child, operations)


@lru_cache(maxsize=None)
def decal(path):
    return trimesh.load_mesh(path)


def check_glyph(test, node, matrix, digit):
    is_input = node.name == 'number_roll'
    radius, up = (9.3, -1) if is_input else (9.45, 1)
    outward = np.r_[matrix[:2, 3] / np.linalg.norm(matrix[:2, 3]), 0]
    viewing = outward if is_input else np.array([0, 0, 1])
    local_view = matrix[:3, :3].T @ viewing
    angle = np.arctan2(local_view[1], local_view[0])
    path = Path(node.stl_file).with_suffix('.marking-digits.stl')
    test.assertTrue(path.is_file(), f'{node.name}: build the digit decal first')
    mesh = decal(path)
    angles = (np.arctan2(mesh.vertices[:, 1], mesh.vertices[:, 0]) - angle + np.pi) % (2*np.pi) - np.pi
    selected = (np.abs(angles[mesh.faces]) < np.pi/10).all(axis=1)
    test.assertTrue(selected.any(), f'{node.name}: no glyph faces the reading position')
    x = up * radius * angles[np.unique(mesh.faces[selected])]
    center, width = (INPUT_GLYPHS if is_input else RESULT_GLYPHS)[digit]
    if is_input:
        cell = 55.5123 - 2*np.pi*9.3/10 * digit
    else:
        cell = -3.2388 + 2*np.pi*9.45/10 * (digit if digit < 6 else digit-10)
    np.testing.assert_allclose([x.min(), x.max()],
                               [center-cell-width/2, center-cell+width/2],
                               atol=.02, rtol=0,
                               err_msg=f'{node.name}: wrong glyph/clocking for {digit}')
    expected_up = np.array([0, 0, 1]) if is_input else -outward
    np.testing.assert_allclose(up * matrix[:3, 2], expected_up, atol=1e-6, rtol=0,
                               err_msg=f'{node.name}: upside-down artwork')


def check_bank(test, root, digit):
    counts = {'input': 0, 'register': 0}
    for node, matrix in placed_nodes(root):
        if node.name == 'number_roll' or node.name.startswith('results_dial'):
            check_glyph(test, node, matrix, digit)
            counts['input' if node.name == 'number_roll' else 'register'] += 1
    test.assertEqual(counts, {'input': 8, 'register': 17})


def check_poses(test, root):
    for digit in range(10):
        root.set_state(operand=digit*11111111, initial_result=digit*11111111111,
                       initial_turns=digit*111111, crank_turns=0, subtract=0,
                       carriage_position=0, carriage_lift=0, clear=0)
        check_bank(test, root, digit)
    # The decals inherit the same carriage lift and shift, not a separate pose.
    root.set_state(operand=0, initial_result=0, initial_turns=0,
                   carriage_position=5, carriage_lift=1)
    check_bank(test, root, 0)


def check_reversing_label(test, root):
    placed = list(placed_nodes(root))
    housing, frame = next((n, m) for n, m in placed if n.name == 'bottom_housing')
    knob = next(n for n, _ in placed if n.name == 'reversing_lever_knob')
    # The source "knob" includes a long internal lever. Measure only the
    # exposed operating pad, beyond R75, not the whole part's origin/centroid.
    vertices = knob.mesh.vertices
    radius = np.linalg.norm(vertices[:, :2] - frame[:2, 3], axis=1)
    exposed = vertices[radius > 75]
    test.assertGreater(len(exposed), 0)
    pad_height = (exposed[:, 2].min() + exposed[:, 2].max()) / 2
    path = Path(housing.stl_file).with_suffix('.marking-reversing_arrows.stl')
    test.assertTrue(path.is_file())
    sheet = decal(path)
    # This original sheet is symmetric about its centre dot, +/-12 mm high.
    center = frame @ [0, 0, sheet.bounds[:, 2].mean(), 1]
    test.assertAlmostEqual(center[2], pad_height, delta=.02,
                           msg='Reversing label must centre on the visible pad, not the lever origin')


if __name__ == '__main__':
    from simulation.curta import Curta
    model = Curta()
    model.set_state(operand=0, initial_result=0, initial_turns=0, crank_turns=0,
                    subtract=0, carriage_position=0, carriage_lift=0, clear=0)
    model.assemble()
    model.build_stls()
    check_poses(unittest.TestCase(), model)
    check_reversing_label(unittest.TestCase(), model)
    print('275 built-glyph checks passed: 25 rolls × 10 digits, plus lifted/shifted zero.')
    print('Reversing label aligned with the exposed operating pad.')
