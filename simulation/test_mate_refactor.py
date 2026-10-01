"""Mate adoption preserves the crank's actual coordinates and placement.

The independent joint-declared drive below is the pre-migration witness,
not a second production implementation. No source geometry is changed.
"""

import hashlib
import json
import math
import unittest

from machinome.node import AssemblyNode, declared_children
from machinome.motion.joints import Bound, Revolute, Prismatic
from machinome.motion.mates import declared_mates
from machinome.motion.ports import Time
from machinome.simulation import Driver, Sim
from simulation.mechanism import MainDrive
from simulation.mechanistic import MechanisticCurta
from simulation.running_parts import RunningMainDrive, RunningReversingAssembly
from simulation.crank_coupling_parts import SeatedCrankAssembly
from simulation.running_pawl import RetainedAntiReversal, reverse_stop


class JointDeclaredDrive(MainDrive):
    anti_reversal = RetainedAntiReversal()
    reversing_lever = RunningReversingAssembly()
    crank = SeatedCrankAssembly(
        turn=Revolute(axis=(0, 0, 1), range=(None, Bound(reverse_stop,
            reads=(anti_reversal.reverse_rotation_prevention_pawl.turn,)))),
        lift=Prismatic(axis=(0, 0, 1), range=(0, 9)))


class JointDeclaredBench(AssemblyNode):
    time = Time.running()
    rotation = Driver(default=0, unit='deg')
    elevation = Driver(default=0, unit='mm')
    reverser = Driver(default=3.9075, unit='mm')
    drive = JointDeclaredDrive()
    rotation.drives(drive.turn, ratio=-1)
    elevation.drives(drive.subtract, ratio=1 / 9)
    reverser.drives(drive.reversing_lever.reversing_lever_1.displacement)


class MatedBench(JointDeclaredBench):
    drive = RunningMainDrive()


def placed_basis(root):
    """Compare public operations on four independent points, without meshing."""
    result = {}

    def transform(point, operation):
        if hasattr(operation, 'translation'):
            return tuple(a + b for a, b in zip(point, operation.translation))
        if not hasattr(operation, 'angle'):
            raise TypeError(type(operation).__name__)
        axis = tuple(operation.axis)
        length = math.sqrt(sum(a * a for a in axis))
        x, y, z = (a / length for a in axis)
        px, py, pz = point
        cosine = math.cos(math.radians(operation.angle))
        sine = math.sin(math.radians(operation.angle))
        dot = x * px + y * py + z * pz
        cross = (y * pz - z * py, z * px - x * pz, x * py - y * px)
        return tuple(p * cosine + c * sine + a * dot * (1 - cosine)
                     for p, c, a in zip(point, cross, (x, y, z)))

    def visit(node, path, ancestors):
        operations = [*node.operations, *ancestors]
        points = []
        for point in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)):
            for operation in operations:
                point = transform(point, operation)
            points.append(point)
        result[path] = points
        # A meshes=False Sim evaluates declared nodes without populating
        # the exported/rendered children list. Walk the public declarations
        # as well; checking only node.children would compare two bare roots.
        children = list(node.children)
        for name in declared_children(type(node)):
            declared = getattr(node, name)
            for child in declared if isinstance(declared, (list, tuple)) else (declared,):
                if not any(child is existing for existing in children):
                    children.append(child)
        for child in children:
            visit(child, path + '.' + child.name, operations)

    visit(root, '', [])
    return result


class MateRefactorTest(unittest.TestCase):
    def test_operating_crank_is_attached_by_a_mate(self):
        self.assertIn('turn', declared_mates(RunningMainDrive))

    def test_crank_controls_select_the_assembly_mate(self):
        for name in ('turn crank', 'one revolution'):
            self.assertEqual(MechanisticCurta.controls[name].selected, 'main_drive.turn')

    def test_initial_bank_keeps_the_pre_refactor_witness(self):
        # Reuse the independently pinned crank-seat witness unchanged; do
        # not bless a new hash just because the declaration spelling changed.
        bank = dict(Sim(MechanisticCurta(), dt=.1).state)
        self.assertEqual(len(bank), 216)
        for key in ('loop_deployment',
                    'carriage.registers.clearing_ring.clearing_ring.swivel',
                    'carriage.positioning.p_6mm_ball_419094.slide'):
            self.assertEqual(bank.pop(key), 0)
        self.assertEqual(hashlib.sha256(json.dumps(bank, sort_keys=True,
            separators=(',', ':')).encode()).hexdigest(),
            'ea39d95d50f06580db66c894f5b3f700ab6ed930cee113b2b9ffe4689935f5b7')

    def test_joint_witness_and_mate_keep_bank_poses_stops_and_replay(self):
        roots = (JointDeclaredBench(), MatedBench())
        sims = tuple(Sim(root, dt=.1) for root in roots)

        def compare():
            self.assertEqual(dict(sims[0].state), dict(sims[1].state))
            poses = tuple(placed_basis(root) for root in roots)
            self.assertIn('.drive.crank.crank_handle_1.main_crank', poses[0])
            self.assertGreater(len(poses[0]), 20)
            self.assertEqual(poses[0].keys(), poses[1].keys())
            for path, points in poses[0].items():
                for before, after in zip(points, poses[1][path]):
                    for a, b in zip(before, after):
                        self.assertAlmostEqual(a, b, places=9, msg=path)

        compare()
        for lift in (0, 9):
            for sim in sims:
                sim.reset()
                self.assertEqual(sim.move('elevation', to=lift).status, 'completed')
            compare()
            for angle in (10, 0, 0, 15):
                statuses = []
                for sim in sims:
                    saved = sim.snapshot()
                    command = sim.move('rotation', to=angle, duration=.1)
                    sim.run(.1)
                    statuses.append(command.status)
                    expected = sim.snapshot()
                    sim.restore(saved)
                    retry = sim.move('rotation', to=angle, duration=.1)
                    sim.run(.1)
                    self.assertEqual(retry.status, command.status)
                    self.assertEqual(sim.snapshot(), expected)
                self.assertEqual(statuses[0], statuses[1])
                self.assertEqual(statuses[0], 'blocked' if angle == 0 else 'completed')
                compare()
