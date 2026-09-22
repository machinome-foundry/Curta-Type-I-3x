"""A browser restraint report must prove both requests, replay and retained state."""

from copy import deepcopy
import unittest

from simulation.tools.counter_operating_browser import validate_report


def fixture():
    state = {'crank_rotation': 174.78, 'main_drive.crank.turn': -174.78,
             'transmission.turns.ones.turn': 167.6}
    idle = dict(state, crank_rotation=174.73, **{'main_drive.crank.turn': -174.73})
    return {'errors': [], 'coordinate_ids': list(state), 'prepared': dict(state, crank_rotation=170,
                                          **{'main_drive.crank.turn': -170}),
            'cases': [{'target': target, 'status': 'blocked', 'replay': True,
                       'relief_status': 'completed', 'retry_status': 'blocked',
                       'stopped': dict(state), 'idle': dict(idle), 'retry': dict(state)}
                      for target in (180, 900)]}


class CounterBrowserReportTest(unittest.TestCase):
    def test_counter_tens_uses_its_own_preparation_and_request_bounds(self):
        report = fixture()
        report['coordinate_ids'][-1] = 'transmission.turns.tens.turn'
        for bank in [report['prepared'], *[case[name] for case in report['cases']
                                          for name in ('stopped', 'idle', 'retry')]]:
            bank['transmission.turns.tens.turn'] = bank.pop('transmission.turns.ones.turn')-20
            bank['crank_rotation'] += 20
            bank['main_drive.crank.turn'] -= 20
        for case in report['cases']:
            case['target'] += 20
        validate_report(report, deepcopy(report['cases']), station=2)
        report['prepared']['transmission.turns.tens.turn'] += .1
        with self.assertRaises(AssertionError):
            validate_report(report, station=2)

    def test_every_exported_coordinate_is_required_without_a_python_report(self):
        report = fixture()
        report['coordinate_ids'].append('unrelated_dial')
        with self.assertRaises(AssertionError):
            validate_report(report)

    def test_complete_report_and_full_bank_comparison(self):
        report = fixture()
        validate_report(report, deepcopy(report['cases']))

    def test_completed_or_missing_request_is_not_a_stop(self):
        report = fixture()
        report['cases'][0]['status'] = 'completed'
        with self.assertRaises(AssertionError):
            validate_report(report)
        report = fixture()
        report['cases'].pop()
        with self.assertRaises(AssertionError):
            validate_report(report)

    def test_replay_relief_and_page_errors_are_not_ignored(self):
        for field, value in (('replay', False), ('relief_status', 'blocked'),
                             ('retry_status', 'completed')):
            report = fixture()
            report['cases'][0][field] = value
            with self.subTest(field=field), self.assertRaises(AssertionError):
                validate_report(report)
        report = fixture()
        report['errors'] = ['worker failed']
        with self.assertRaises(AssertionError):
            validate_report(report)

    def test_bank_comparison_checks_unrelated_coordinates_and_missing_keys(self):
        for missing in (False, True):
            report = fixture()
            expected = deepcopy(report['cases'])
            expected[0]['stopped']['unrelated_dial'] = 0
            if not missing:
                report['cases'][0]['stopped']['unrelated_dial'] = 1
            with self.subTest(missing=missing), self.assertRaises(AssertionError):
                validate_report(report, expected)


if __name__ == '__main__':
    unittest.main()
