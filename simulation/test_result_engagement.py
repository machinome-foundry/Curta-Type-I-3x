"""Actual source teeth, including positions between the two crank seats."""

from machinome.test import TestCase
from simulation.result_engagement import ResultEngagement
from simulation.result_modes import ROWS, result_count
from simulation.cycle import RESULT_INPUT_END, TOOTH_PITCH


class ResultEngagementTest(TestCase):
    node = ResultEngagement

    def test_band_table_matches_original_source_parts(self):
        self.node.set_state(crank_angle=0, crank_height=0)
        words = ('zero', 'one', 'two', 'three', 'four', 'five',
                 'six', 'seven', 'eight', 'nine', 'ten')
        measured = {}
        for part in self.node.drum.main_axle_step_drum_bottom_1.children:
            if '_tooth_step_drum_segment' not in part.name:
                continue
            count = words.index(part.name.split('_')[0])
            bottom, top = part.mesh.bounds[:, 2]
            self.assertAlmostEqual(top-bottom, 1.5, delta=.00001)
            height = round(float(bottom), 4)
            measured[height] = max(measured.get(height, 0), count)
        self.assertEqual(measured, dict(ROWS))

    def test_partial_selector_settings_follow_whole_source_teeth(self):
        for digit, height in ((.25, 0), (.5, 0), (3.3, 0), (4.5, 9),
                              (8.75, 4.5), (7.8, 3)):
            self.check_sweep(digit, height)

    def test_mapped_passages_have_actual_driving_contact(self):
        drum = self.node.drum.main_axle_step_drum_bottom_1
        for digit, height in ((3, 1.5), (3, 4.5), (.25, 0), (4.5, 9)):
            self.node.set_state(digit=digit, crank_height=height)
            for index, gear in enumerate((self.node.ones.p_10219_410002_1,
                                           self.node.tens.p_10230_410008_1_419229)):
                count = int(result_count(index, digit, height))
                for tooth_index in range(count):
                    angle = (RESULT_INPUT_END + 20*index - TOOTH_PITCH*count
                             + 6.5 + TOOTH_PITCH*tooth_index)
                    self.node.set_state(crank_angle=angle)
                    self.assertNotIntersecting(gear, drum)
                    engaged = []
                    for tooth in gear.children:
                        if not tooth.name.startswith('transmission_gear_0_5'):
                            continue
                        try:
                            self.assertBlockedBeyond(tooth, 12, against=drum,
                                                     axis=(0, 0, -1), directions='forward')
                            engaged.append(tooth.name)
                        except AssertionError:
                            pass
                    self.assertTrue(engaged, (digit, height, index, tooth_index))

    def test_partial_crank_height_follows_the_teeth_it_actually_reaches(self):
        for height in (1.5, 3, 4.5, 6, 7.5):
            self.check_sweep(3, height)

    def check_sweep(self, digit, height):
        drum = self.node.drum.main_axle_step_drum_bottom_1
        self.node.set_state(digit=digit, crank_height=height)
        for angle in range(0, 361, 3):
            self.node.set_state(crank_angle=angle)
            for gear in (self.node.ones.p_10219_410002_1,
                         self.node.tens.p_10230_410008_1_419229):
                try:
                    self.assertNotIntersecting(gear, drum)
                except AssertionError as error:
                    raise AssertionError(f'digit={digit}, height={height}, angle={angle}, '
                                         f'{gear.name}: {error}') from error
