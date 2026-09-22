"""Standalone UI evidence is distinct from hosted full-bank acceptance."""

from copy import deepcopy
import unittest

from simulation.tools.operating_standalone_probe import validate_report


class StandaloneReportTest(unittest.TestCase):
    def setUp(self):
        self.report = dict(control='lift crank', input='crank_elevation',
            hover='turn crank · one revolution · lift crank', errors=[],
            declared_inputs=['crank_elevation', 'digit_1'],
            before={'crank_elevation': '0.0000', 'digit_1': '0.0000'},
            after={'crank_elevation': '2.0000', 'digit_1': '0.0000'},
            release_observed=True, outcome='completed')

    def test_accepts_terminal_visible_independent_movement(self):
        validate_report(self.report)

    def test_rejects_missing_hit_release_terminal_or_movement(self):
        for key, value in (('hover', 'turn crank'), ('release_observed', False),
                ('outcome', 'running…'), ('outcome', 'refused'),
                ('after', self.report['before']), ('errors', ['page error'])):
            row = deepcopy(self.report)
            row[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(AssertionError):
                validate_report(row)

    def test_rejects_missing_input_or_changed_other_readout(self):
        for after in ({'crank_elevation': '2.0000'},
                      {'crank_elevation': '2.0000', 'digit_1': '1.0000'}):
            row = deepcopy(self.report)
            row['after'] = after
            with self.subTest(after=after), self.assertRaises(AssertionError):
                validate_report(row)

    def test_named_full_revolution_requires_its_complete_visible_delta(self):
        self.report['expected_delta'] = 360
        self.report['after']['crank_elevation'] = '359.9999'
        with self.assertRaises(AssertionError):
            validate_report(self.report)
        self.report['after']['crank_elevation'] = '360.0000'
        validate_report(self.report)
