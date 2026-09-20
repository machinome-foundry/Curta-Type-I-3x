"""Geometric check of actual lever-height engagement between retained seats."""

from machinome.test import TestCase
from simulation.reverser_mapped import MappedReverserTrial
from simulation.test_reverser_assembly import INPUTS
from simulation.reverser_modes import ROW_STARTS, THICKNESS, counter_count


class MappedReverserTest(TestCase):
    node = MappedReverserTrial

    def test_band_table_matches_source_geometry(self):
        self.node.set_state(subtract=0, crank_angle=0)
        rows = [part for part in self.node.drum.main_axle_step_drum_top_1.children
                if 'tooth_turns_step_drum_segment' in part.name]
        self.assertEqual(len(rows), 7)
        bounds = sorted((part.mesh.bounds[0, 2], part.mesh.bounds[1, 2]) for part in rows)
        for (bottom, top), expected in zip(bounds, ROW_STARTS):
            self.assertAlmostEqual(bottom, expected, delta=.00001)
            self.assertAlmostEqual(top-bottom, THICKNESS, delta=.00001)

    def test_partial_engagement_has_driving_contact_not_just_clearance(self):
        drum = self.node.drum.main_axle_step_drum_top_1
        for height in (-3, 0, 2):
            for subtract in (0, 1):
                self.node.set_state(knob_height=height, gear_height=height+.0925,
                                    subtract=subtract, reversed_counter=0)
                for index, (name, member) in enumerate(INPUTS):
                    count = int(counter_count(index, height+.0925, 9*subtract))
                    if not count:
                        continue
                    gear = getattr(getattr(self.node, name), member)
                    for passage in ((0, 4, 8) if count == 9 else (0,)):
                        angle = 176+20*index-11.25*count+6.5+11.25*passage
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
                        self.assertTrue(engaged, f'height={height}, subtract={subtract}, {name}, angle={angle}')

    def test_partial_lever_positions_clear_drum_through_a_revolution(self):
        self.check_heights((-4.9425, -3.5, -3, -2, -1, 0, 1, 2, 3, 3.9075))

    def test_overtravel_below_lower_working_pocket_clears_a_revolution(self):
        self.check_heights((-6.9425, -6.8, -6, -5.5))

    def check_heights(self, heights):
        for height in heights:
            for subtract in (0, 1):
                self.node.set_state(knob_height=height, gear_height=height+.0925,
                                    subtract=subtract, reversed_counter=0)
                for angle in range(0, 361, 6):
                    self.node.set_state(crank_angle=angle)
                    for name, member in INPUTS:
                        gear = getattr(getattr(self.node, name), member)
                        for drum in (self.node.drum.main_axle_step_drum_top_1,
                                     self.node.drum.main_axle_step_drum_bottom_1):
                            try:
                                self.assertNotIntersecting(gear, drum)
                            except AssertionError as error:
                                raise AssertionError(f'height={height}, subtract={subtract}, angle={angle}, {name}: {error}') from error
