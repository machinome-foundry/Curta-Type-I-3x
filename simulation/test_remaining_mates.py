"""Independent source-placement witnesses for the last operating attachments."""

import unittest
from machinome.node import AssemblyNode
from machinome.motion.mates import declared_mates
from machinome.motion.joints import Revolute
from machinome.motion.ports import Time
from machinome.simulation import Driver, Sim
from simulation.positioning import RadialCarriagePositioning
from simulation.running_parts import RetainedAxleCarrier, RetainedCarriageStructure, RetainedCarries
from simulation.mechanism import TensBellAssembly
from simulation.higher_lockout_parts import ContactBell
from simulation.mechanistic import RadialRunningCarriage
from simulation.clearing_loop_operating_parts import OperatingLoopMount, LoopRetainedCarriage
from simulation.test_mate_refactor import placed_basis


class LegacyBell(TensBellAssembly):
    tens_bell_1 = ContactBell()


class LegacyRemainingBench(AssemblyNode):
    time = Time.running()
    rise = Driver(default=0, unit='mm')
    radial = Driver(default=0, unit='mm')
    press = Driver(default=0, unit='mm')
    deploy = Driver(default=0, unit='deg')
    subtract = Driver(default=0)
    positioning = RadialCarriagePositioning()
    carrier = RetainedAxleCarrier()
    loop = OperatingLoopMount(turn=Revolute(axis=(0, 0, 1)))
    bell = LegacyBell(turn=Revolute(axis=(0, 0, 1)))
    rise.drives(positioning.lift)
    radial.drives(positioning.p_6mm_ball_419094.slide)
    press.drives(carrier.clearing_pin.slide)
    deploy.drives(loop.deployment)
    subtract.drives(bell.subtract)
    deploy.drives(loop.turn, ratio=0)
    subtract.drives(bell.turn, ratio=0)
    for _index in range(6, 11):
        deploy.drives(getattr(loop.decimal_markers, f'decimal_marker_{_index}').turn, ratio=0)
    del _index


_Positioning = type(RadialRunningCarriage().positioning)
_Carrier = type(RetainedCarriageStructure().upper_carriage_body_1)
_Loop = type(LoopRetainedCarriage().clearing_ring)
_Bell = type(RetainedCarries().tens_bell)


class MatedRemainingBench(LegacyRemainingBench):
    positioning = _Positioning()
    carrier = _Carrier()
    loop = _Loop()
    bell = _Bell()


class RemainingMateTest(unittest.TestCase):
    def test_production_attachments_select_original_joints(self):
        root = MatedRemainingBench()
        for child, expected in (
                (root.positioning, {'thrust_ring.slide', 'carriage_spring.slide',
                                    'p_6mm_ball_419094.slide'}),
                (root.carrier, {'clearing_pin.slide', 'clearing_pin_spring.slide'}),
                (root.loop, {'clearing_ring.swivel'}),
                (root.bell, {None})):
            with self.subTest(child=child.name):
                mates = declared_mates(type(child))
                self.assertEqual(len(mates), len(expected))
                self.assertEqual({m.freedom.written if m.freedom is not None else None
                                  for m in mates.values()}, expected)

    def test_source_poses_shape_values_and_replay_are_preserved(self):
        sims = tuple(Sim(cls(), dt=.1) for cls in (LegacyRemainingBench, MatedRemainingBench))
        for rise, radial, press, deploy, subtract in (
                (0, 0, 0, 0, 0), (2, .1, 1, 30, .25), (6, .3, 2, 90, 1),
                (1, .05, .5, -.4, .7), (0, 0, 0, 0, 0)):
            request = dict(rise=rise, radial=radial, press=press, deploy=deploy,
                           subtract=subtract)
            for sim in sims:
                saved = sim.snapshot()
                for name, value in request.items():
                    self.assertEqual(sim.move(name, to=value).status, 'completed')
                expected = sim.snapshot()
                sim.restore(saved)
                for name, value in request.items():
                    sim.move(name, to=value)
                self.assertEqual(sim.snapshot(), expected)
            self.assertEqual(list(sims[0].state), list(sims[1].state))
            self.assertEqual(dict(sims[0].state), dict(sims[1].state))
            before, after = (placed_basis(sim.node) for sim in sims)
            self.assertEqual(before.keys(), after.keys())
            for path in ('.positioning.thrust_ring', '.positioning.carriage_spring.wire',
                         '.positioning.p_6mm_ball_419094', '.carrier.clearing_pin',
                         '.carrier.clearing_pin_spring.wire', '.loop.clearing_ring',
                         '.bell.tens_bell_spring'):
                self.assertIn(path, before)
            for path in before:
                for first, second in zip(before[path], after[path]):
                    for a, b in zip(first, second):
                        self.assertAlmostEqual(a, b, places=8, msg=path)
            for path in ('positioning.carriage_spring.wire.height',
                         'carrier.clearing_pin_spring.wire.height',
                         'bell.tens_bell_spring.spread'):
                values = []
                for sim in sims:
                    value = sim.node
                    for name in path.split('.'):
                        value = getattr(value, name)
                    values.append(value.value)
                self.assertEqual(*values)
