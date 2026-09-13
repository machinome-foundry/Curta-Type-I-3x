"""Independent red contracts for the selected input; no overlap-volume waiver."""

import json
from math import pi
from pathlib import Path

import numpy as np
from solid_node.test import TestCase
from simulation.curta import Curta
from simulation.selector_fit import SelectorFitBench
from simulation.tools.interference import world_solids
from simulation.tools.open_run_selector import (SELECTOR, INPUT_GROUP, MOVERS,
                                                move_shape, retained_state, vertex_error)
from simulation.tools.open_run_transitions import physical_nodes


KNOB = 'selector.selector_knob_1_419057.'
NAMES = dict(ball=KNOB+'p_5mm_ball', spring=KNOB+'selector_knob_spring',
             screw=KNOB+'digit_selector_screw', knob=KNOB+'selector_knob',
             shaft='selector.selector_shaft_bottom',
             top='selector.selector_shaft_top_1_419054.selector_shaft_top',
             roll='selector.selector_shaft_top_1_419054.number_roll',
             group='channel.p_10219_410002_1', housing='housing.bottom_housing')


def part(node, name):
    for attribute in NAMES[name].split('.'):
        node = getattr(node, attribute)
    return node


class SelectedInputFitTest(TestCase):
    node = SelectorFitBench

    def clear_at(self, first, second, setting, postcarry):
        self.node.set_state(setting=setting, postcarry=postcarry)
        self.assertNotIntersecting(part(self.node, first), part(self.node, second))

    def test_manual_ball_is_five_mm(self):
        sphere = part(self.node, 'ball').shape()
        self.assertTrue(sphere.isValid())
        self.assertEqual(len(sphere.Solids()), 1)
        self.assertAlmostEqual((3*sphere.Volume()/(4*pi))**(1/3)*2, 5., delta=1e-6)

    def test_selected_parts_are_valid_connected_solids(self):
        self.node.set_state(setting=0, postcarry=0)
        for name in NAMES:
            shape = part(self.node, name).shape()
            self.assertTrue(shape.isValid(), name)
            self.assertEqual(len(shape.Solids()), 1, name)

    def test_numbered_one_is_retained_by_ball_detent(self):
        # Independent radial-support measurement for the approved 5 mm ball.
        # A held pose on a ramp is not a seated detent. The source guide is
        # along X; use the actual occurrence's Y/Z at each neighbouring pose.
        from simulation.tools.selector_fit_contacts import radial_support
        brackets = []
        selected = {'Curta.'+NAMES[name] for name in ('shaft', 'ball')}
        for setting in (.975, 1, 1.025):
            self.node.set_state(setting=setting, postcarry=0)
            self.node.assemble()
            actual = world_solids(self.node, selected=selected)
            center = actual['Curta.'+NAMES['ball']].Center()
            support = radial_support(actual['Curta.'+NAMES['shaft']], center.z, center.y)
            brackets.append(support['center_x_bracket_mm'])
        left, seated, right = brackets
        self.assertLessEqual(seated[1], min(left[0], right[0]),
            'Numbered one has an adjacent position requiring less spring compression; '
            f'ball-center X brackets left/one/right: {brackets}')

    def test_aligned_guide_retains_a_continuous_wall(self):
        # Independent source pocket and shaft-bore datums, not the bore of a
        # fitted adapter. The source/fit comparison alone would permit no fit.
        from simulation.standard.assembly import DigitSelectorAxle1
        from simulation.tools.selector_fit_alignment import cylinder, measured_guide
        original = DigitSelectorAxle1()
        original.assemble()
        source_paths = {
            'knob': 'Curta.selector_knob_1_419057.selector_knob',
            'shaft': 'Curta.selector_shaft_bottom'}
        raw = world_solids(original, selected=set(source_paths.values()))
        guide, support, center = measured_guide(raw[source_paths['knob']], raw[source_paths['shaft']])
        radius = guide.Radius()
        first = support.Axis().Location().X()+support.Radius()+.01
        back = guide.Axis().Location().X()
        wall = cylinder(radius+.34, first, back, center[1], center[2]).cut(
            cylinder(radius, first, back, center[1], center[2]))
        self.node.set_state(setting=0, postcarry=0)
        self.node.assemble()
        path = 'Curta.'+NAMES['knob']
        actual = world_solids(self.node, selected={path})[path]
        missing = wall.cut(actual)
        self.assertTrue(missing.isValid())
        self.assertEqual(missing.Volume(), 0,
            'Aligned guide lacks its continuous 0.34 mm retaining wall; '
            'an unclosed obsolete bore cannot be replaced by a chosen centerline')

    def test_fixed_source_joints_keep_exact_regions_and_relative_poses(self):
        from simulation.standard.assembly import DigitSelectorAxle1
        from simulation.tools.moving_seats import world_frames
        from simulation.tools.selector_fit_fixed_seats import (
            PAIRS, intersections, relative_frames, verify_frames, verify_regions)
        from simulation.tools.selector_fit_measurements import PATHS
        original = DigitSelectorAxle1()
        original.assemble()
        names = set(name for pair in PAIRS.values() for name in pair)
        source_paths = {name: PATHS[name].replace('Curta.selector.', 'Curta.') for name in names}
        raw = world_solids(original, selected=set(source_paths.values()))
        expected = intersections({name: raw[path] for name, path in source_paths.items()})
        source_frames = world_frames(original)
        frames = relative_frames({PATHS[name]: source_frames[source_paths[name]] for name in names})
        self.node.set_state(setting=0, postcarry=0)
        self.node.assemble()
        actual = world_solids(self.node, selected={PATHS[name] for name in names})
        verify_regions(expected, intersections({name: actual[PATHS[name]] for name in names}))
        for fixture in (0, 1):
            for setting in (*range(10), .125, .375, .625, .875, 4.5, 8.5):
                self.node.set_state(setting=setting, postcarry=fixture)
                self.node.assemble()
                verify_frames(frames, relative_frames(world_frames(self.node)))

    def test_full_stroke_and_fixed_housing(self):
        self.node.set_state(setting=0, postcarry=0)
        before = {name: part(self.node, name).mesh.vertices.copy()
                  for name in ('knob', 'group', 'housing')}
        self.node.set_state(setting=9, postcarry=0)
        for name, reference in before.items():
            expected = reference if name == 'housing' else reference-(0, 0, 54)
            np.testing.assert_allclose(part(self.node, name).mesh.vertices, expected,
                                       atol=1e-5, rtol=0, err_msg=name)

    def test_independent_bench_matches_both_complete_frozen_fixtures(self):
        baseline = json.loads(Path('simulation/docs/evidence/open-run-selector-2026-09-13.json').read_text())
        mapping = {path: path.replace(SELECTOR, 'Curta.selector') for path in MOVERS}
        mapping[INPUT_GROUP] = 'Curta.channel.p_10219_410002_1'
        mapping['Curta.enclosure.lower_housing_1.bottom_housing'] = 'Curta.housing.bottom_housing'
        for postcarry in (0, 1):
            root = Curta()
            root.set_state(initial_result=99, initial_turns=0, operand=1,
                           crank_turns=postcarry, subtract=0, carriage_position=0,
                           carriage_lift=0, clear=0)
            root.assemble()
            frozen = retained_state(root)
            self.assertEqual(frozen, baseline['runs'][postcarry]['frozen_state'])
            inventory = [dict(path=path, representation='native' if node.exact else 'source-mesh')
                         for path, node in sorted(physical_nodes(root))]
            self.assertEqual(inventory, baseline['physical_inventory'])
            source = world_solids(root, selected=set(mapping))
            self.assertEqual(set(source), set(mapping))
            for digit in (*range(10), .5, 4.5, 8.5):
                self.node.set_state(setting=digit, postcarry=postcarry)
                self.node.assemble()
                actual = world_solids(self.node, selected=set(mapping.values()))
                self.assertEqual(set(actual), set(mapping.values()))
                for path, target in mapping.items():
                    expected = (move_shape(path, source[path], digit, 1)
                                if path in MOVERS else source[path])
                    self.assertLess(vertex_error(actual[target], expected), 1e-5, target)
                    self.assertAlmostEqual(actual[target].Volume(), expected.Volume(),
                                           delta=1e-5, msg=target)
                self.assertEqual(retained_state(root), frozen)


def contact_test(first, second, setting, postcarry):
    def test(self):
        self.clear_at(first, second, setting, postcarry)
    return test


# Separate names ensure a first failure cannot hide the second home fixture
# or the stronger between-detent ball/shaft counterexample.
for _postcarry, _fixture in enumerate(('initial', 'postcarry')):
    for _first, _second, _setting, _label in (
        ('ball', 'knob', 0, 'ball_guide'),
        ('spring', 'ball', 0, 'spring_ball_seat'),
        ('spring', 'knob', 0, 'spring_back_seat'),
        ('shaft', 'ball', 0, 'seated_ball_shaft'),
        ('shaft', 'ball', .5, 'between_detent_ball_shaft'),
        ('shaft', 'screw', .5, 'between_detent_screw_groove'),
        ('knob', 'housing', 5, 'knob_housing_slot'),
        ('roll', 'housing', 0, 'number_roll_window'),
    ):
        _test = contact_test(_first, _second, _setting, _postcarry)
        _test.__name__ = 'test_'+_fixture+'_'+_label+'_clears'
        setattr(SelectedInputFitTest, _test.__name__, _test)
