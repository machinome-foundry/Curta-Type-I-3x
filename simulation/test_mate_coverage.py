"""Audit the final operating tree, not only intermediate fitted assemblies."""

import unittest
from machinome.node import declared_children
from machinome.motion.joints import declared_joints
from machinome.motion.mates import declared_mates
from simulation.running import OperatingCurta


class OperatingMateCoverageTest(unittest.TestCase):
    def test_only_intrinsic_flexible_patches_lack_parent_mates(self):
        unattached = {}

        def visit(node, path):
            attached = {mate.moving.written.split('.')[0]
                        for mate in declared_mates(type(node)).values()}
            for name in declared_children(type(node)):
                child = getattr(node, name)
                child_path = f'{path}.{name}' if path else name
                joints = tuple(declared_joints(type(child)))
                if joints and name not in attached:
                    unattached[child_path] = joints
                visit(child, child_path)

        visit(OperatingCurta(), '')
        expected = {
            f'carry_mechanism.tens_bell.tens_bell_spring.{side}_hook': ('travel',)
            for side in ('left', 'right')}
        for bank, count in (('result', 11), ('turns', 6)):
            for index in range(1, count + 1):
                expected[f'carriage.registers.dial_detents.spider_spring.{bank}_{index}.tip'] = ('lift',)
        self.assertEqual(unattached, expected)
