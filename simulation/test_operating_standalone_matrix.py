"""A partial standalone pointer run must never count as full coverage."""

import unittest
from simulation.tools.operating_standalone_matrix import validate_matrix


class StandaloneMatrixReportTest(unittest.TestCase):
    def test_requires_each_requested_control_exactly_once_and_no_errors(self):
        required = ['clear registers', 'deploy loop (simulation-only mounting)']
        rows = [{'control': name, 'validation': 'passed'} for name in required]
        validate_matrix(required, rows, [])
        for invalid in (rows[:1], rows + rows[:1],
                        [dict(rows[0], validation='failed'), rows[1]]):
            with self.subTest(rows=invalid), self.assertRaises(AssertionError):
                validate_matrix(required, invalid, [])
        with self.assertRaises(AssertionError):
            validate_matrix(required, rows, ['page error'])

    def test_empty_request_is_not_acceptance(self):
        with self.assertRaises(AssertionError):
            validate_matrix([], [], [])
