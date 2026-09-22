"""A pointer readback is not accepted while its command is still running."""

from copy import deepcopy
import unittest

from simulation.tools.operating_pointer_matrix import validate_case


class PointerReportTest(unittest.TestCase):
    def setUp(self):
        self.case = {
            'input': 'digit_1', 'before': {'digit_1': 0, 'digit_2': 0, 'dial.turn': 0},
            'after': {'digit_1': 1, 'digit_2': 0, 'dial.turn': 0},
            'commands': [], 'outcomes': [{'input': 'digit_1', 'status': 'completed'}],
            'drivers': ['digit_1', 'digit_2'], 'register_coordinates': ['dial.turn'],
        }

    def test_accepts_only_retired_independent_motion(self):
        validate_case(self.case)

    def test_rejects_intermediate_readback(self):
        self.case['commands'] = [{'input': 'digit_1'}]
        with self.assertRaises(AssertionError):
            validate_case(self.case)

    def test_rejects_refusal_and_cancel_only(self):
        for status in ('refused', 'cancelled'):
            row = deepcopy(self.case)
            row['outcomes'][0]['status'] = status
            with self.subTest(status=status), self.assertRaises(AssertionError):
                validate_case(row)

    def test_rejects_motion_of_another_input_or_register(self):
        for key in ('digit_2', 'dial.turn'):
            row = deepcopy(self.case)
            row['after'][key] = 1
            with self.subTest(key=key), self.assertRaises(AssertionError):
                validate_case(row)

    def test_rejects_no_motion_and_missing_terminal_outcome(self):
        for field, value in (('after', self.case['before']), ('outcomes', [])):
            row = deepcopy(self.case)
            row[field] = value
            with self.subTest(field=field), self.assertRaises(AssertionError):
                validate_case(row)
