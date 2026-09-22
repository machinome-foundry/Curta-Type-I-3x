"""Result-bank browser evidence must retain complete cases and coordinate banks."""

from copy import deepcopy
import unittest

from simulation.tools.result_bank_operating_browser import validate_report


def fixture():
    base = {'crank_rotation': 0, 'main_drive.crank.turn': 0,
            'transmission.result.hundreds.turn': -36,
            'transmission.result.digit_8.turn': -136,
            'digit_3': 0, 'digit_8': 0, 'unrelated_dial': 0}
    report = {'errors': [], 'coordinate_ids': list(base), 'prepared': [], 'cases': []}
    for station, channel in ((3, 'hundreds'), (8, 'digit_8')):
        shift = 20*(station-2)
        bank = dict(base, crank_rotation=140+shift,
                    **{'main_drive.crank.turn': -140-shift,
                       f'transmission.result.{channel}.turn': 169.6-shift})
        report['prepared'].append({'station': station, 'bank': bank})
        stop = dict(bank, crank_rotation=145.22+shift,
                    **{'main_drive.crank.turn': -145.22-shift})
        relief = dict(stop, crank_rotation=145.17+shift,
                      **{'main_drive.crank.turn': -145.17-shift})
        for target in (170+shift, 860+shift):
            report['cases'].append({'station': station, 'target': target,
                'status': 'blocked', 'replay': True, 'relief_status': 'completed',
                'retry_status': 'blocked', 'stopped': dict(stop),
                'relieved': dict(relief), 'retry': dict(stop)})
    return report


class ResultBankBrowserReportTest(unittest.TestCase):
    def test_idle_evidence_is_complete_and_unchanged(self):
        report = fixture()
        report['initial_bank'] = dict(report['prepared'][0]['bank'])
        report['idle_bank'] = dict(report['initial_bank'])
        validate_report(report)
        report['idle_bank']['unrelated_dial'] = 1
        with self.assertRaises(AssertionError):
            validate_report(report)
        report['idle_bank'] = dict(report['initial_bank'])
        for key in ('initial_bank', 'idle_bank'):
            report[key].pop('unrelated_dial')
        with self.assertRaises(AssertionError):
            validate_report(report)

    def test_complete_report_and_explicit_partial_python_comparison_scope(self):
        report = fixture()
        self.assertEqual(validate_report(report), [])
        expected = deepcopy(report['cases'][2:])
        self.assertEqual(validate_report(report, expected), [(8, 290), (8, 980)])

    def test_missing_or_repeated_requests_and_false_stops_are_rejected(self):
        for alter in (lambda r: r['cases'].pop(),
                      lambda r: r['cases'].append(r['cases'][0]),
                      lambda r: r['cases'][0].update(status='completed'),
                      lambda r: r['cases'][0].update(replay=False),
                      lambda r: r['cases'][0].update(relief_status='blocked'),
                      lambda r: r['cases'][0].update(retry_status='completed'),
                      lambda r: r['errors'].append('worker failed')):
            report = fixture()
            alter(report)
            with self.assertRaises(AssertionError):
                validate_report(report)

    def test_coordinate_coverage_and_exact_bank_values_are_required(self):
        report = fixture()
        report['cases'][0]['stopped'].pop('unrelated_dial')
        with self.assertRaises(AssertionError):
            validate_report(report)
        report = fixture()
        expected = deepcopy(report['cases'][2:])
        expected[0]['relieved']['unrelated_dial'] = 1
        with self.assertRaises(AssertionError):
            validate_report(report, expected)

    def test_partial_or_empty_python_station_evidence_is_not_accepted(self):
        report = fixture()
        for expected in ([], report['cases'][2:3]):
            with self.assertRaises(AssertionError):
                validate_report(report, expected)


if __name__ == '__main__':
    unittest.main()
