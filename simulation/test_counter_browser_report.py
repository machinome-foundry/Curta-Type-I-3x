"""A browser restraint report must prove both requests, replay and retained state."""

from copy import deepcopy
import math
import unittest

from simulation.tools.counter_operating_browser import validate_report, compare_banks, P9_DETENT


def fixture():
    state = {'crank_rotation': 174.78, 'main_drive.crank.turn': -174.78,
             'transmission.turns.ones.turn': 167.6}
    idle = dict(state, crank_rotation=174.73, **{'main_drive.crank.turn': -174.73})
    return {'station': 1, 'errors': [], 'coordinate_ids': list(state), 'prepared': dict(state, crank_rotation=170,
                                          **{'main_drive.crank.turn': -170}),
            'cases': [{'target': target, 'status': 'blocked', 'replay': True,
                       'relief_status': 'completed', 'retry_status': 'blocked',
                       'stopped': dict(state), 'idle': dict(idle), 'retry': dict(state)}
                      for target in (180, 900)]}


class CounterBrowserReportTest(unittest.TestCase):
    def test_measured_detent_rounding_is_explicit_and_reported(self):
        actual = {P9_DETENT: .08929057589867746, 'unrelated': 1.0}
        expected = {P9_DETENT: .0892905758986775, 'unrelated': 1.0}
        with self.assertRaises(AssertionError):
            compare_banks(actual, expected)
        differences = compare_banks(actual, expected, allow_measured_detent_rounding=True)
        self.assertEqual(len(differences), 1)
        self.assertEqual(differences[0]['coordinate'], P9_DETENT)
        self.assertEqual(differences[0]['ulps'], 3)

    def test_larger_detent_error_or_any_other_coordinate_drift_is_rejected(self):
        expected = {P9_DETENT: .08929057589867746, 'unrelated': 1.0}
        for key, delta in ((P9_DETENT, 4*math.ulp(expected[P9_DETENT])),
                           ('unrelated', math.ulp(1.0))):
            actual = dict(expected)
            actual[key] += delta
            with self.subTest(key=key), self.assertRaises(AssertionError):
                compare_banks(actual, expected, allow_measured_detent_rounding=True)

    def test_rounding_option_does_not_ignore_nonfinite_or_missing_state(self):
        expected = {P9_DETENT: .08929057589867746}
        for actual in ({}, {P9_DETENT: float('nan')}, {P9_DETENT: float('inf')}):
            with self.subTest(actual=actual), self.assertRaises(AssertionError):
                compare_banks(actual, expected, allow_measured_detent_rounding=True)

    def test_counter_tens_uses_its_own_preparation_and_request_bounds(self):
        report = fixture()
        report['station'] = 2
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

    def test_remaining_counters_keep_their_own_frames_and_request_targets(self):
        for station, channel in ((3, 'hundreds'), (4, 'digit_4'),
                                 (5, 'digit_5'), (6, 'digit_6')):
            report = fixture()
            report['station'] = station
            shift = 20*(station-1)
            shaft = f'transmission.turns.{channel}.turn'
            report['coordinate_ids'][-1] = shaft
            for bank in [report['prepared'], *[case[name] for case in report['cases']
                                              for name in ('stopped', 'idle', 'retry')]]:
                bank[shaft] = bank.pop('transmission.turns.ones.turn')-shift
                bank['crank_rotation'] += shift
                bank['main_drive.crank.turn'] -= shift
            for case in report['cases']:
                case['target'] += shift
            with self.subTest(station=station):
                validate_report(report, deepcopy(report['cases']), station=station)
                report['cases'][0]['stopped'][shaft] += .1
                with self.assertRaises(AssertionError):
                    validate_report(report, station=station)

    def test_report_cannot_claim_another_station(self):
        report = fixture()
        report['station'] = 2
        with self.assertRaises(AssertionError):
            validate_report(report, station=1)

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
