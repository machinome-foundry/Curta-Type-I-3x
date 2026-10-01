"""Independent retained-joint witnesses for the central moving assemblies."""

import unittest

from machinome.node import AssemblyNode
from machinome.motion.joints import Revolute
from machinome.motion.mates import declared_mates
from machinome.motion.ports import Time
from machinome.simulation import Driver, Sim
from simulation import assemblies
from simulation.running_parts import (
    ContactBellAssembly, RetainedCarries, RetainedResultCarries,
    RetainedTurnsCarries, RetainedCarriage, RunningMainDrive,
)
from simulation.mechanistic import RadialRunningCarriage, LoopRunningCarriage
from simulation.clearing_loop_operating_parts import OperatingLoopMount, LoopRetainedCarriage
from simulation.test_mate_refactor import placed_basis


class LegacyCarries(assemblies.CarryMechanism):
    tens_bell = ContactBellAssembly(turn=Revolute(axis=(0, 0, 1)))
    result_carries = RetainedResultCarries()
    turns_carries = RetainedTurnsCarries()


class LegacyBellBench(AssemblyNode):
    time = Time.running()
    angle = Driver(default=0, unit='deg')
    subtract = Driver(default=0)
    mechanism = LegacyCarries()
    angle.drives(mechanism.tens_bell.turn)
    subtract.drives(mechanism.tens_bell.subtract)


class MatedBellBench(LegacyBellBench):
    mechanism = RetainedCarries()


class LegacyLoopCarriage(RetainedCarriage):
    clearing_ring = OperatingLoopMount(turn=Revolute(axis=(0, 0, 1)))


class LegacyLoopRunningCarriage(RadialRunningCarriage):
    registers = LegacyLoopCarriage()


class LegacyCarriageBench(AssemblyNode):
    time = Time.running()
    angle = Driver(default=0, unit='deg')
    elevation = Driver(default=0, unit='mm')
    clear = Driver(default=0, unit='deg')
    deploy = Driver(default=0, unit='deg')
    mechanism = LegacyLoopRunningCarriage()
    angle.drives(mechanism.registers.turn)
    elevation.drives(mechanism.registers.lift)
    clear.drives(mechanism.registers.clearing_ring.turn)
    deploy.drives(mechanism.registers.clearing_ring.deployment)
    for _index in range(6, 11):
        angle.drives(getattr(mechanism.registers.clearing_ring.decimal_markers,
                            f'decimal_marker_{_index}').turn, ratio=0)
    del _index


class MatedCarriageBench(LegacyCarriageBench):
    mechanism = LoopRunningCarriage()


class CoreMateTest(unittest.TestCase):
    def test_four_central_assemblies_reference_their_original_joints(self):
        for owner, name, joint in (
                (RunningMainDrive, 'drum_mount', 'stepped_drum.turn'),
                (RetainedCarries, 'bell_mount', 'tens_bell.turn'),
                (LoopRunningCarriage, 'carriage_mount', 'registers.turn'),
                (LoopRetainedCarriage, 'clearing_mount', 'clearing_ring.turn')):
            with self.subTest(owner=owner.__name__):
                mates = declared_mates(owner)
                self.assertIn(name, mates)
                self.assertEqual(mates[name].freedom.written, joint)

    def assertTwins(self, legacy, mated, requests, required):
        sims = (Sim(legacy(), dt=.1), Sim(mated(), dt=.1))
        for request in ((), *requests):
            for sim in sims:
                saved = sim.snapshot()
                outcomes = [sim.move(name, to=value).status for name, value in request]
                self.assertTrue(all(status == 'completed' for status in outcomes), outcomes)
                expected = sim.snapshot()
                sim.restore(saved)
                for name, value in request:
                    sim.move(name, to=value)
                self.assertEqual(sim.snapshot(), expected)
            self.assertEqual(list(sims[0].state), list(sims[1].state))
            self.assertEqual(dict(sims[0].state), dict(sims[1].state))
            before, after = (placed_basis(sim.node) for sim in sims)
            self.assertEqual(before.keys(), after.keys())
            for fragment in required:
                self.assertTrue(any(path.endswith(fragment) for path in before), fragment)
            for path, points in before.items():
                for first, second in zip(points, after[path]):
                    for a, b in zip(first, second):
                        self.assertAlmostEqual(a, b, places=8, msg=path)

    def test_bell_and_carried_spring_preserve_poses_state_and_replay(self):
        self.assertTwins(LegacyBellBench, MatedBellBench,
            tuple((('angle', angle), ('subtract', subtract))
                  for angle, subtract in ((-15, 0), (-90, 1), (-180, 1), (-360, 0), (0, 0))),
            ('.tens_bell.tens_bell_1', '.tens_bell.tens_bell_spring.left_hook'))

    def test_carriage_and_clearing_preserve_poses_state_and_replay(self):
        self.assertTwins(LegacyCarriageBench, MatedCarriageBench,
            ((('elevation', 6),), (('angle', 40),),
             (('deploy', 45), ('clear', 30)), (('clear', 180),),
             (('clear', 360), ('deploy', 0)), (('angle', 0), ('elevation', 0))),
            ('.registers.carrier.upper_carriage_body_1.counter_body',
             '.registers.clearing_ring.clearing_ring',
             '.positioning.p_6mm_ball_419094'))
