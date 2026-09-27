"""Source-placement witnesses for the pawl and the reversing-lever guides."""

import unittest

from machinome.node import AssemblyNode
from machinome.motion.mates import declared_mates
from machinome.motion.ports import Time
from machinome.parameters import Length
from machinome.simulation import Driver, Sim
from simulation.running_pawl import RetainedAntiReversal
from simulation.running_parts import RunningReverser, RunningMainDrive
from simulation.test_mate_refactor import placed_basis


class LegacyDriveDetailBench(AssemblyNode):
    time = Time.running()
    seat_rise = Length(1.9, min=0, max=2)
    rotation = Driver(default=0, unit='deg')
    height = Driver(default=3.9075, unit='mm')
    pawl = RetainedAntiReversal()
    lever = RunningReverser(seat_rise=seat_rise)
    rotation.drives(pawl.turn)
    height.drives(lever.displacement)


_ProductionPawl = type(RunningMainDrive().anti_reversal)
_ProductionLever = type(RunningMainDrive().reversing_lever.reversing_lever_1)


class MatedDriveDetailBench(LegacyDriveDetailBench):
    pawl = _ProductionPawl()
    lever = _ProductionLever(seat_rise=LegacyDriveDetailBench.seat_rise)


class DriveDetailMateTest(unittest.TestCase):
    def test_pawl_and_lever_use_existing_joint_and_rigid_attachments(self):
        root = MatedDriveDetailBench()
        with self.subTest(assembly='pawl'):
            mates = declared_mates(type(root.pawl))
            self.assertEqual(len(mates), 2)
            self.assertEqual(mates['pawl_mount'].freedom.written,
                             'reverse_rotation_prevention_pawl.turn')
            self.assertIsNone(mates['spring_mount'].freedom)
        with self.subTest(assembly='reverser'):
            mates = declared_mates(type(root.lever))
            self.assertEqual(len(mates), 3)
            self.assertEqual({mate.freedom.written for mate in mates.values()},
                             {'p_5mm_ball.lift', 'reversing_lever_knob_1.lift',
                              'selector_knob_spring.lift'})

    def test_source_and_mated_guides_preserve_motion_shape_and_replay(self):
        for seat_rise in (1.9, 1.8, 2):
            sims = tuple(Sim(cls(seat_rise=seat_rise), dt=.1) for cls in
                         (LegacyDriveDetailBench, MatedDriveDetailBench))
            for rotation, height in ((0, 3.9075), (-1, 0), (-3.4, -6.9425),
                                     (-120, -4), (-360, 3.9075), (-359.95, 1)):
                for sim in sims:
                    saved = sim.snapshot()
                    for name, value in (('rotation', rotation), ('height', height)):
                        self.assertEqual(sim.move(name, to=value).status, 'completed')
                    expected = sim.snapshot()
                    sim.restore(saved)
                    sim.move('rotation', to=rotation)
                    sim.move('height', to=height)
                    self.assertEqual(sim.snapshot(), expected)
                self.assertEqual(list(sims[0].state), list(sims[1].state))
                self.assertEqual(dict(sims[0].state), dict(sims[1].state))
                before, after = (placed_basis(sim.node) for sim in sims)
                self.assertEqual(before.keys(), after.keys())
                for path in ('.pawl.reverse_rotation_prevention_pawl',
                             '.lever.p_5mm_ball', '.lever.selector_knob_spring.wire',
                             '.lever.reversing_lever_knob_1.reversing_actuator'):
                    self.assertIn(path, before)
                for path in before:
                    for first, second in zip(before[path], after[path]):
                        for a, b in zip(first, second):
                            self.assertAlmostEqual(a, b, places=8, msg=path)
                self.assertEqual(sims[0].node.lever.selector_knob_spring.wire.height.value,
                                 sims[1].node.lever.selector_knob_spring.wire.height.value)
                self.assertEqual(sims[0].node.pawl.documented_spring.deflection.value,
                                 sims[1].node.pawl.documented_spring.deflection.value)
