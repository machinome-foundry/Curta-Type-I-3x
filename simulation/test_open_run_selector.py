"""The evidence probe must move only the intended source-frame coordinates."""

import unittest
from types import SimpleNamespace as Object


class ShapeSpy:
    def translate(self, vector):
        return ('translation', vector)

    def rotate(self, start, end, angle):
        return ('rotation', start, end, angle)


class SelectorProbeTest(unittest.TestCase):
    def test_knob_and_input_group_have_six_mm_negative_z_travel(self):
        from simulation.tools.open_run_selector import move_shape
        knob = 'Curta.input_selectors.selectors.digit_selector_axle_1.selector_knob_1_419057.selector_knob'
        group = 'Curta.transmission.result.ones.p_10219_410002_1'
        self.assertEqual(move_shape(knob, ShapeSpy(), 0, 1), ('translation', (0, 0, 6)))
        self.assertEqual(move_shape(group, ShapeSpy(), 9, 1), ('translation', (0, 0, -48)))

    def test_shafts_rotate_about_the_source_axis_not_the_machine_origin(self):
        from simulation.tools.open_run_selector import move_shape
        shaft = 'Curta.input_selectors.selectors.digit_selector_axle_1.selector_shaft_bottom'
        self.assertEqual(move_shape(shaft, ShapeSpy(), 9, 1),
                         ('rotation', (58.5, 0, 0), (58.5, 0, 1), 288))

    def test_unlisted_body_cannot_become_a_mover(self):
        from simulation.tools.open_run_selector import move_shape
        with self.assertRaisesRegex(ValueError, 'Unlisted'):
            move_shape('Curta.frame.upper_frame.main_body', ShapeSpy(), 9, 1)

    def test_retained_state_reads_numeric_drivers_and_bound_ports_separately(self):
        from simulation.tools.open_run_selector import retained_state
        root = Object(**dict.fromkeys(('initial_result', 'initial_turns', 'operand',
                      'crank_turns', 'subtract', 'carriage_position', 'carriage_lift', 'clear'), 0))
        root.crank_turns = 1
        root.result = Object(value=100)
        root.input_selectors = Object(selectors=Object(digit_selector_axle_1=Object(setting=Object(value=1))))
        root.transmission = Object(result=Object(**{
            name: Object(turn=Object(value=angle)) for name, angle in
            zip(('ones', 'tens', 'hundreds'), (4, -16, 36))}))
        root.carriage = Object(registers=Object(result_register=Object(**{
            name: Object(turn=Object(value=angle)) for name, angle in
            zip(('p_10203_1', 'p_10203_2', 'p_10205_1'), (0, 0, -36))})))
        root.carry_mechanism = Object(result_carries=Object(
            results_tens_lever_assembly_1=Object(engage=Object(value=0)),
            results_tens_lever_assembly_2=Object(engage=Object(value=1))))
        snapshot = retained_state(root)
        self.assertEqual(snapshot['drivers']['crank_turns'], 1)
        self.assertEqual(snapshot['result'], 100)
        self.assertEqual(snapshot['carry_fractions'], [0, 1])
        self.assertEqual(snapshot['shaft_degrees'], [4, -16, 36])


if __name__ == '__main__':
    unittest.main()
