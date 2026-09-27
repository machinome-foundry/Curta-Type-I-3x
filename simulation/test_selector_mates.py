"""Independent pre-mate selector declarations and all-eight-channel witnesses.

The reference below retains the old site joints and inherited STEP placements;
it must not import attachment datums from the migrated implementation.
"""

import unittest

from machinome.node import AssemblyNode
from machinome.motion.mates import declared_mates
from machinome.motion.ports import Time
from machinome.simulation import Sim
from simulation.selectors import IndependentSelectors as MatedSelectors
from simulation.test_mate_refactor import placed_basis

from machinome.motion.joints import Revolute, Prismatic
from machinome.motion.ports import Port
from machinome.math import floor
from machinome.simulation import Driver
from simulation.standard.assembly import *
from simulation.standard.layers import InputSelectors

def digit_at(place):
    return lambda source, target: lambda value: (
        floor(value / 10 ** place) - 10 * floor(value / 10 ** (place + 1)))

class LegacySelector1(DigitSelectorAxle1):
    setting = Port()
    selector_shaft_bottom = SelectorShaftBottom(turn=Revolute(axis=(0, 0, 1), at=(58.5, 0.0, 0)))
    selector_shaft_top_1_419054 = SelectorShaftTop1_419054(turn=Revolute(axis=(0, 0, 1), at=(58.5, 0.0, 0)))
    selector_knob_1_419057 = SelectorKnob1_419057(travel=Prismatic(axis=(0, 0, -1), range=(0, 54)))
    setting.drives(selector_knob_1_419057.travel, ratio=6)
    setting.drives(selector_shaft_bottom.turn, ratio=36)
    selector_shaft_bottom.turn.drives(selector_shaft_top_1_419054.turn)


class LegacySelector2(DigitSelectorAxle2):
    setting = Port()
    selector_shaft_bottom = SelectorShaftBottom(turn=Revolute(axis=(0, 0, 1), at=(54.972018316, -20.008178385, 0)))
    selector_shaft_top_1_419153 = SelectorShaftTop1_419153(turn=Revolute(axis=(0, 0, 1), at=(54.972018316, -20.008178385, 0)))
    selector_knob_1_419152 = SelectorKnob1_419152(travel=Prismatic(axis=(0, 0, -1), range=(0, 54)))
    setting.drives(selector_knob_1_419152.travel, ratio=6)
    setting.drives(selector_shaft_bottom.turn, ratio=36)
    selector_shaft_bottom.turn.drives(selector_shaft_top_1_419153.turn)


class LegacySelector3(DigitSelectorAxle3):
    setting = Port()
    selector_shaft_bottom = SelectorShaftBottom(turn=Revolute(axis=(0, 0, 1), at=(44.813599922, -37.603075167, 0)))
    selector_shaft_top_1_419224 = SelectorShaftTop1_419224(turn=Revolute(axis=(0, 0, 1), at=(44.813599922, -37.603075167, 0)))
    selector_knob_1_419225 = SelectorKnob1_419225(travel=Prismatic(axis=(0, 0, -1), range=(0, 54)))
    setting.drives(selector_knob_1_419225.travel, ratio=6)
    setting.drives(selector_shaft_bottom.turn, ratio=36)
    selector_shaft_bottom.turn.drives(selector_shaft_top_1_419224.turn)


class LegacySelector4(DigitSelectorAxle4):
    setting = Port()
    selector_shaft_bottom = SelectorShaftBottom(turn=Revolute(axis=(0, 0, 1), at=(29.25, -50.662486121, 0)))
    selector_shaft_top_1_419083 = SelectorShaftTop1_419083(turn=Revolute(axis=(0, 0, 1), at=(29.25, -50.662486121, 0)))
    selector_knob_1_419084 = SelectorKnob1_419084(travel=Prismatic(axis=(0, 0, -1), range=(0, 54)))
    setting.drives(selector_knob_1_419084.travel, ratio=6)
    setting.drives(selector_shaft_bottom.turn, ratio=36)
    selector_shaft_bottom.turn.drives(selector_shaft_top_1_419083.turn)


class LegacySelector5(DigitSelectorAxle5):
    setting = Port()
    selector_shaft_bottom = SelectorShaftBottom(turn=Revolute(axis=(0, 0, 1), at=(10.158418394, -57.611253551, 0)))
    selector_shaft_top_1_419178 = SelectorShaftTop1_419178(turn=Revolute(axis=(0, 0, 1), at=(10.158418394, -57.611253551, 0)))
    selector_knob_1_419177 = SelectorKnob1_419177(travel=Prismatic(axis=(0, 0, -1), range=(0, 54)))
    setting.drives(selector_knob_1_419177.travel, ratio=6)
    setting.drives(selector_shaft_bottom.turn, ratio=36)
    selector_shaft_bottom.turn.drives(selector_shaft_top_1_419178.turn)


class LegacySelector6(DigitSelectorAxle6):
    setting = Port()
    selector_shaft_bottom = SelectorShaftBottom(turn=Revolute(axis=(0, 0, 1), at=(-10.158418394, -57.611253551, 0)))
    selector_shaft_top_1_419142 = SelectorShaftTop1_419142(turn=Revolute(axis=(0, 0, 1), at=(-10.158418394, -57.611253551, 0)))
    selector_knob_1_419141 = SelectorKnob1_419141(travel=Prismatic(axis=(0, 0, -1), range=(0, 54)))
    setting.drives(selector_knob_1_419141.travel, ratio=6)
    setting.drives(selector_shaft_bottom.turn, ratio=36)
    selector_shaft_bottom.turn.drives(selector_shaft_top_1_419142.turn)


class LegacySelector7(DigitSelectorAxle7):
    setting = Port()
    selector_shaft_bottom = SelectorShaftBottom(turn=Revolute(axis=(0, 0, 1), at=(-29.25, -50.662486121, 0)))
    selector_shaft_top_1_419103 = SelectorShaftTop1_419103(turn=Revolute(axis=(0, 0, 1), at=(-29.25, -50.662486121, 0)))
    selector_knob_1_419102 = SelectorKnob1_419102(travel=Prismatic(axis=(0, 0, -1), range=(0, 54)))
    setting.drives(selector_knob_1_419102.travel, ratio=6)
    setting.drives(selector_shaft_bottom.turn, ratio=36)
    selector_shaft_bottom.turn.drives(selector_shaft_top_1_419103.turn)


class LegacySelector8(DigitSelectorAxle8):
    setting = Port()
    selector_shaft_bottom = SelectorShaftBottom(turn=Revolute(axis=(0, 0, 1), at=(-44.813599922, -37.603075167, 0)))
    selector_shaft_top_1_419156 = SelectorShaftTop1_419156(turn=Revolute(axis=(0, 0, 1), at=(-44.813599922, -37.603075167, 0)))
    selector_knob_1_419155 = SelectorKnob1_419155(travel=Prismatic(axis=(0, 0, -1), range=(0, 54)))
    setting.drives(selector_knob_1_419155.travel, ratio=6)
    setting.drives(selector_shaft_bottom.turn, ratio=36)
    selector_shaft_bottom.turn.drives(selector_shaft_top_1_419156.turn)


class LegacySelectors(InputSelectors):
    """The physical channels; each setting is independently wired by its owner."""
    digit_selector_axle_1 = LegacySelector1()
    digit_selector_axle_2 = LegacySelector2()
    digit_selector_axle_3 = LegacySelector3()
    digit_selector_axle_4 = LegacySelector4()
    digit_selector_axle_5 = LegacySelector5()
    digit_selector_axle_6 = LegacySelector6()
    digit_selector_axle_7 = LegacySelector7()
    digit_selector_axle_8 = LegacySelector8()



class LegacySelectorBench(AssemblyNode):
    time = Time.running()
    bank = LegacySelectors()
    digit_1 = Driver(default=0)
    digit_2 = Driver(default=0)
    digit_3 = Driver(default=0)
    digit_4 = Driver(default=0)
    digit_5 = Driver(default=0)
    digit_6 = Driver(default=0)
    digit_7 = Driver(default=0)
    digit_8 = Driver(default=0)
    for _index, _driver in enumerate((digit_1, digit_2, digit_3, digit_4,
                                     digit_5, digit_6, digit_7, digit_8), 1):
        _driver.drives(getattr(bank, f'digit_selector_axle_{_index}').setting)
        del _driver
    del _index


class MatedSelectorBench(LegacySelectorBench):
    bank = MatedSelectors()


class SelectorMateTest(unittest.TestCase):
    def test_each_selector_attaches_both_shafts_and_its_sliding_knob(self):
        for index in range(1, 9):
            selector = getattr(MatedSelectors, f'digit_selector_axle_{index}')
            mates = declared_mates(selector.node_class)
            with self.subTest(channel=index):
                self.assertEqual(len(mates), 3)
                ends = {mate.freedom.written for mate in mates.values()}
                self.assertIn('selector_shaft_bottom.turn', ends)
                self.assertEqual(sum(end.endswith('.turn') for end in ends), 2)
                self.assertEqual(sum(end.endswith('.travel') for end in ends), 1)

    def test_old_and_mated_channels_preserve_leaf_poses_state_and_replay(self):
        sims = (Sim(LegacySelectorBench(), dt=.1),
                Sim(MatedSelectorBench(), dt=.1))
        for digits in ((0,) * 8, (1, 2, 3, 4, 5, 6, 7, 8),
                       (9,) * 8, (.5,) * 8, (0,) * 8):
            for index, value in enumerate(digits, 1):
                for sim in sims:
                    before = sim.snapshot()
                    self.assertEqual(sim.move(f'digit_{index}', to=value).status,
                                     'completed')
                    after = sim.snapshot()
                    sim.restore(before)
                    self.assertEqual(sim.move(f'digit_{index}', to=value).status,
                                     'completed')
                    self.assertEqual(sim.snapshot(), after)
            self.assertEqual(list(sims[0].state), list(sims[1].state))
            self.assertEqual(dict(sims[0].state), dict(sims[1].state))
            poses = [placed_basis(sim.node) for sim in sims]
            self.assertEqual(poses[0].keys(), poses[1].keys())
            for index in range(1, 9):
                prefix = f'.bank.digit_selector_axle_{index}.'
                self.assertIn(prefix + 'selector_shaft_bottom', poses[0])
                for leaf in ('selector_shaft_top', 'number_roll', 'selector_knob',
                             'selector_knob_spring', 'digit_selector_screw', 'p_5mm_ball'):
                    self.assertEqual(sum(path.startswith(prefix) and
                                         path.endswith('.' + leaf)
                                         for path in poses[0]), 1, (index, leaf))
            for path, points in poses[0].items():
                for before, after in zip(points, poses[1][path]):
                    for a, b in zip(before, after):
                        self.assertAlmostEqual(a, b, places=8, msg=path)

