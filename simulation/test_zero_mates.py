"""Frozen pre-mate zero mechanism: native placements, state and replay.

Only geometry adapters and the existing motion law are shared. The reference
owns its old joints and placements independently of the new attachment frames.
"""

import unittest

from machinome.node.assembly import AssemblyNode
from machinome.motion.joints import Revolute, Prismatic
from machinome.motion.mates import declared_mates
from machinome.motion.ports import Port, Time
from machinome.simulation import Driver, Sim
from simulation.flexibles import MountedZeroSpring, FIXED_PIN, ZERO_PIVOT
from simulation.standard.parts import (
    M5Nut, M5x30HexBolt, ZeroPositioningDiscPin,
    ZeroPositioningM5BoltSleeve, ZeroPositioningDiscSecuringSpring,
)
from simulation.zero import ZeroCam, ZeroFollower, ZeroPositioning, follower_angle
from simulation.test_mate_refactor import placed_basis


class LegacyZeroPositioning(AssemblyNode):
    turn = Port(unit='deg')
    subtract = Port()
    zero_positioning_disc = ZeroCam(turn=Revolute(axis=(0, 0, 1)))
    zero_positioning_disc_pin = ZeroPositioningDiscPin(
        turn=Revolute(axis=(0, 0, 1)), lift=Prismatic(axis=(0, 0, 1)))
    follower = ZeroFollower(turn=Revolute(axis=(0, 0, 1), at=(*ZERO_PIVOT, 0)))
    documented_spring = MountedZeroSpring()
    m5_nut_1 = M5Nut()
    zero_positioning_m5_bolt_sleeve = ZeroPositioningM5BoltSleeve()
    m5x30_hex_bolt = M5x30HexBolt()
    zero_positioning_disc_securing_spring = ZeroPositioningDiscSecuringSpring()

    turn.drives(zero_positioning_disc.turn)
    turn.drives(zero_positioning_disc_pin.turn)
    subtract.drives(zero_positioning_disc_pin.lift, ratio=9)
    turn.drives(follower.turn, law=follower_angle)
    follower.turn.drives(documented_spring.deflection)

    def render(self):
        self.zero_positioning_disc.rotate(-180, (.70774875, -.706464229, 0))
        self.zero_positioning_disc.translate((0, 0, -138.45))
        self.zero_positioning_disc_pin.rotate(-179.92640235, (.707106635, .000642261, .707106635))
        self.zero_positioning_disc_pin.translate((-14.99997525, -.027248799, -165.75))
        self.m5_nut_1.rotate(180, (1, 0, 0)).translate((40.5, 33.6, -128.25))
        self.zero_positioning_m5_bolt_sleeve.rotate(-90, (0, 0, 1))
        self.zero_positioning_m5_bolt_sleeve.translate((40.5, 33.6, -161.85))
        self.m5x30_hex_bolt.rotate(180, (0, 1, 0)).translate((40.5, 33.6, -128.25))
        self.zero_positioning_disc_securing_spring.rotate(180, (.999999588, .000908294, 0))
        self.zero_positioning_disc_securing_spring.translate((.029065386, -15.9999736, -142.2))
        self.documented_spring.translate(FIXED_PIN)


class LegacyZeroBench(AssemblyNode):
    time = Time.running()
    angle = Driver(default=0, unit='deg')
    subtract = Driver(default=0)
    mechanism = LegacyZeroPositioning()
    angle.drives(mechanism.turn)
    subtract.drives(mechanism.subtract)


class MatedZeroBench(LegacyZeroBench):
    mechanism = ZeroPositioning()


class ZeroMateTest(unittest.TestCase):
    def test_cam_pin_and_follower_use_their_existing_joints_in_mates(self):
        mates = declared_mates(ZeroPositioning)
        self.assertEqual(len(mates), 3)
        self.assertEqual({mate.freedom.written for mate in mates.values()}, {
            'zero_positioning_disc.turn', 'zero_positioning_disc_pin.turn',
            'follower.turn'})

    def test_old_and_mated_zero_mechanisms_preserve_pose_state_and_replay(self):
        sims = (Sim(LegacyZeroBench(), dt=.1), Sim(MatedZeroBench(), dt=.1))
        for angle, subtract in ((0, 0), (-4, .5), (-14, 1), (-90, 0),
                                (-180, 1), (-350, .25), (-360, 0), (0, 0)):
            for sim in sims:
                saved = sim.snapshot()
                for driver, value in (('angle', angle), ('subtract', subtract)):
                    self.assertEqual(sim.move(driver, to=value).status, 'completed')
                expected = sim.snapshot()
                sim.restore(saved)
                for driver, value in (('angle', angle), ('subtract', subtract)):
                    self.assertEqual(sim.move(driver, to=value).status, 'completed')
                self.assertEqual(sim.snapshot(), expected)
            self.assertEqual(list(sims[0].state), list(sims[1].state))
            self.assertEqual(dict(sims[0].state), dict(sims[1].state))
            before, after = (placed_basis(sim.node) for sim in sims)
            self.assertEqual(before.keys(), after.keys())
            for path in ('.mechanism.zero_positioning_disc',
                         '.mechanism.zero_positioning_disc_pin',
                         '.mechanism.follower.zero_positioning_disc_roller',
                         '.mechanism.documented_spring.wire'):
                self.assertIn(path, before)
            for path, points in before.items():
                for first, second in zip(points, after[path]):
                    for a, b in zip(first, second):
                        self.assertAlmostEqual(a, b, places=8, msg=path)
