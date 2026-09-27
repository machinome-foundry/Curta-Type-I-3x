"""Adoption gate for the two original sliding groups in each channel."""

import unittest

from machinome.node import declared_children
from machinome.motion.joints import declared_joints
from machinome.motion.mates import declared_mates
from simulation.reverser_operating_parts import ReverserContactTransmission
from simulation.running_parts import CHANNEL_NAMES


class TransmissionSliderMateTest(unittest.TestCase):
    def test_all_thirty_four_sliding_groups_keep_their_original_travel_joints(self):
        transmission = ReverserContactTransmission()
        for bank_name, count in (('result', 11), ('turns', 6)):
            bank = getattr(transmission, bank_name)
            for name in CHANNEL_NAMES[:count]:
                channel = getattr(bank, name)
                with self.subTest(channel=f'{bank_name}.{name}'):
                    sliders = {child_name for child_name in declared_children(type(channel))
                               if 'travel' in declared_joints(type(getattr(channel, child_name)))}
                    self.assertEqual(len(sliders), 2)
                    mates = declared_mates(type(channel))
                    self.assertEqual(len(mates), 2)
                    self.assertEqual({mate.freedom.written for mate in mates.values()},
                                     {f'{child}.travel' for child in sliders})
