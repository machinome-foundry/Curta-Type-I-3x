"""Crank pointers need arithmetic-aware acceptance, not noncrank invariance."""

from copy import deepcopy
import unittest
from simulation.tools.operating_crank_pointers import validate_case, bank_sha256, COUNTER_ONES


class CrankPointerReportTest(unittest.TestCase):
    def test_browser_bit_hash_preserves_negative_zero_lost_by_json_numbers(self):
        bits = {'value': '0000000000000080'}
        self.assertEqual(bank_sha256({'value': 0}, bits), bank_sha256({'value': -0.0}))
        self.assertNotEqual(bank_sha256({'value': 0}, bits), bank_sha256({'value': 0}))

    def case(self, full=True):
        before = {'crank_rotation': 0, 'loop_deployment': 0,
                  **{f'digit_{n}': 0 for n in range(1, 9)},
                  **{f'carriage.registers.result_register.r{n}.turn': 0 for n in range(11)},
                  **{f'carriage.registers.turns_register.c{n}.turn': 0 for n in range(5)},
                  COUNTER_ONES: 0}
        after = dict(before, crank_rotation=360 if full else 2)
        if full:
            after[COUNTER_ONES] = -36
        return dict(control='one revolution' if full else 'turn crank', before=before,
                    after=after, drivers=['crank_rotation', 'loop_deployment']+
                    [f'digit_{n}' for n in range(1, 9)], commands=[], errors=[],
                    release_observed=True, hit_verified=True,
                    outcomes=[dict(input='crank_rotation', status='completed')])

    def test_accepts_partial_turn_and_complete_zero_entry_turn(self):
        validate_case(self.case(False))
        validate_case(self.case(True))

    def test_rejects_partial_button_and_wrong_counter_or_unrelated_input(self):
        for mutate in (
            lambda c: c['after'].update(crank_rotation=359.9999),
            lambda c: c['after'].update({COUNTER_ONES: 0}),
            lambda c: c['after'].update(loop_deployment=1),
            lambda c: c['after'].update({'carriage.registers.result_register.r0.turn': -36}),
        ):
            case = self.case()
            mutate(case)
            with self.subTest(mutation=mutate), self.assertRaises(AssertionError):
                validate_case(case)

    def test_rejects_missing_release_hit_outcome_retirement_or_page_error(self):
        for changes in (dict(release_observed=False), dict(hit_verified=False),
                        dict(outcomes=[]), dict(commands=[{'active': True}]),
                        dict(errors=['page error']),
                        dict(outcomes=[dict(input='crank_rotation', status='refused')])):
            case = deepcopy(self.case())
            case.update(changes)
            with self.subTest(changes=changes), self.assertRaises(AssertionError):
                validate_case(case)

    def test_rejects_nonpositive_or_full_turn_in_partial_case(self):
        for rotation in (-1, 0, 360):
            case = self.case(False)
            case['after']['crank_rotation'] = rotation
            with self.subTest(rotation=rotation), self.assertRaises(AssertionError):
                validate_case(case)
