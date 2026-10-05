"""Independent source-placement witness for a transmission attachment."""

import unittest

from machinome.node.assembly import AssemblyNode
from machinome.node.frames import Frame
from machinome.node.declarative import declared_children
from machinome.motion.joints import Prismatic, declared_joints
from machinome.motion.mates import declared_mates
from machinome.motion.ports import Time
from machinome.simulation import Driver, Sim
from simulation.higher_lockout_parts import ContactTens
from simulation.result_bank_lockout_parts import contact_result_channel
from simulation.counter_bank_lockout_parts import contact_counter_channel
from simulation.counter_lockout_parts import ContactCounterOnes
from simulation.reverser_operating_parts import (
    ProtectedOnesInput, ReverserContactTransmission,
)
from simulation.running_parts import CHANNEL_NAMES
from simulation.standard import channels
from simulation.test_mate_refactor import placed_basis


class FramedTensProbe(ContactTens):
    spindle = Frame(at=ContactTens.turn.at)


class LegacyTensBench(AssemblyNode):
    time = Time.running()
    angle = Driver(default=0, unit='deg')
    setting = Driver(default=0)
    carry = Driver(default=0)
    channel = ContactTens()
    angle.drives(channel.turn)
    setting.drives(channel.setting)
    carry.drives(channel.carry)


class MatedTensProbe(LegacyTensBench):
    bearing = Frame(at=ContactTens.turn.at)
    channel = FramedTensProbe()
    channel_mount = channel.spindle.on(bearing, channel.turn)


class LegacyResultBank(AssemblyNode):
    ones = channels.ResultOnes()
    tens = ContactTens()
    for _station in range(3, 12):
        locals()[CHANNEL_NAMES[_station - 1]] = contact_result_channel(_station)()
    del _station

    def simulate(self):
        from simulation.fit import INPUT_CLOCKING
        for index, name in enumerate(CHANNEL_NAMES[1:], 1):
            shaft = getattr(self, name)
            if shaft.turn.value is None:
                shaft.turn = INPUT_CLOCKING - 20 * index


class LegacyCounterOnes(ContactCounterOnes):
    p_10218_1 = ProtectedOnesInput(travel=Prismatic(axis=(0, 0, -1)))


class LegacyTurnsBank(AssemblyNode):
    ones = LegacyCounterOnes()
    for _station in range(2, 7):
        locals()[CHANNEL_NAMES[_station - 1]] = contact_counter_channel(_station)()
    del _station

    def simulate(self):
        from simulation.fit import INPUT_CLOCKING
        for index, name in enumerate(CHANNEL_NAMES[1:6], 1):
            shaft = getattr(self, name)
            if shaft.turn.value is None:
                shaft.turn = 130 + INPUT_CLOCKING - 20 * index


class LegacyTransmission(AssemblyNode):
    result = LegacyResultBank()
    turns = LegacyTurnsBank()


class LegacyTransmissionBench(AssemblyNode):
    time = Time.running()
    angle = Driver(default=0, unit='deg')
    setting = Driver(default=0)
    carry = Driver(default=0)
    transmission = LegacyTransmission()
    for _index, _name in enumerate(CHANNEL_NAMES, 1):
        angle.drives(getattr(transmission.result, _name).turn, ratio=_index)
        setting.drives(getattr(transmission.result, _name).setting, ratio=1 / _index)
        carry.drives(getattr(transmission.result, _name).carry, ratio=1 / _index)
    for _index, _name in enumerate(CHANNEL_NAMES[:6], 1):
        angle.drives(getattr(transmission.turns, _name).turn, ratio=_index)
        setting.drives(getattr(transmission.turns, _name).setting, ratio=1 / _index)
        carry.drives(getattr(transmission.turns, _name).carry, ratio=1 / _index)
    del _index, _name


class MatedTransmissionBench(LegacyTransmissionBench):
    transmission = ReverserContactTransmission()


class TransmissionMateProbeTest(unittest.TestCase):
    def test_all_seventeen_channel_attachments_reference_their_original_turns(self):
        transmission = ReverserContactTransmission()
        for owner, count in ((type(transmission.result), 11), (type(transmission.turns), 6)):
            with self.subTest(bank=owner.__name__):
                mates = declared_mates(owner)
                self.assertEqual(len(mates), count)
                self.assertEqual({mate.freedom.written for mate in mates.values()},
                                 {f'{name}.turn' for name in CHANNEL_NAMES[:count]})

    def test_historical_fit_trials_keep_their_independent_unmated_banks(self):
        from simulation.result_bank_operating_trial import TrialResultShafts
        from simulation.counter_bank_operating_trial import TrialCounterShafts
        self.assertEqual(declared_mates(TrialResultShafts), {})
        self.assertEqual(declared_mates(TrialCounterShafts), {})

    def test_both_banks_preserve_leaf_poses_state_and_replay(self):
        sims = tuple(Sim(cls(), dt=.1) for cls in
                     (LegacyTransmissionBench, MatedTransmissionBench))
        for request in ((), (('angle', 12),), (('setting', 9), ('carry', 1)),
                        (('angle', -36),), (('carry', .25), ('setting', 4.5)),
                        (('angle', 0), ('setting', 0), ('carry', 0))):
            for sim in sims:
                saved = sim.snapshot()
                for name, value in request:
                    self.assertEqual(sim.move(name, to=value).status, 'completed')
                expected = sim.snapshot()
                sim.restore(saved)
                for name, value in request:
                    self.assertEqual(sim.move(name, to=value).status, 'completed')
                self.assertEqual(sim.snapshot(), expected)
            self.assertEqual(list(sims[0].state), list(sims[1].state))
            self.assertEqual(dict(sims[0].state), dict(sims[1].state))
            before, after = (placed_basis(sim.node) for sim in sims)
            self.assertEqual(before.keys(), after.keys())
            tips = [path for path in before if path.endswith('.transmission_gear_tip')]
            self.assertEqual(len(tips), 17)
            sliding_paths = []
            legacy = sims[0].node.transmission
            for bank_name, count in (('result', 11), ('turns', 6)):
                bank = getattr(legacy, bank_name)
                for name in CHANNEL_NAMES[:count]:
                    channel = getattr(bank, name)
                    for child_name in declared_children(type(channel)):
                        child = getattr(channel, child_name)
                        if 'travel' in declared_joints(type(child)):
                            path = f'.transmission.{bank_name}.{name}.{child_name}'
                            sliding_paths.append(path)
                            self.assertIn(path, before)
                            self.assertTrue(any(leaf.startswith(path + '.') and
                                ('.transmission_gear_' in leaf or
                                 leaf.endswith('.pentagonal_lockout'))
                                for leaf in before), path)
            self.assertEqual(len(sliding_paths), 34)
            for path in before:
                for first, second in zip(before[path], after[path]):
                    for a, b in zip(first, second):
                        self.assertAlmostEqual(a, b, places=8, msg=path)

    def test_tens_source_self_placement_survives_parent_attachment(self):
        sims = tuple(Sim(cls(), dt=.1) for cls in (LegacyTensBench, MatedTensProbe))
        for name, value in (('angle', 36), ('setting', 5), ('carry', .5),
                            ('angle', -72), ('setting', 0), ('carry', 0)):
            for sim in sims:
                self.assertEqual(sim.move(name, to=value).status, 'completed')
            self.assertEqual(dict(sims[0].state), dict(sims[1].state))
            before, after = (placed_basis(sim.node) for sim in sims)
            self.assertEqual(before.keys(), after.keys())
            self.assertIn('.channel.p_10207_1_419228.transmission_gear_tip', before)
            for path in before:
                for first, second in zip(before[path], after[path]):
                    for a, b in zip(first, second):
                        self.assertAlmostEqual(a, b, places=8, msg=path)
