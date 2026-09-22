"""A pointer readback is not accepted while its command is still running."""

from copy import deepcopy
import unittest

from simulation.tools.operating_pointer_matrix import validate_case, validate_attempt, wait_for_gesture


class PointerReportTest(unittest.TestCase):
    def setUp(self):
        self.case = {
            'input': 'digit_1', 'before': {'digit_1': 0, 'digit_2': 0, 'dial.turn': 0},
            'after': {'digit_1': 1, 'digit_2': 0, 'dial.turn': 0},
            'commands': [], 'outcomes': [{'input': 'digit_1', 'status': 'completed'}],
            'release': {'observed': True},
            'drivers': ['digit_1', 'digit_2'], 'register_coordinates': ['dial.turn'],
        }

    def test_accepts_only_retired_independent_motion(self):
        validate_case(self.case)

    def test_rejects_intermediate_readback(self):
        self.case['commands'] = [{'input': 'digit_1'}]
        with self.assertRaises(AssertionError):
            validate_case(self.case)

    def test_rejects_a_missing_pointer_release(self):
        self.case['release']['observed'] = False
        with self.assertRaises(AssertionError):
            validate_case(self.case)

    def test_noop_direction_is_not_coverage_and_cannot_hide_unrelated_motion(self):
        self.case['after'] = dict(self.case['before'])
        self.case['outcomes'] = []
        validate_attempt(self.case)
        with self.assertRaises(AssertionError):
            validate_case(self.case)
        self.case['after']['digit_2'] = 1
        with self.assertRaises(AssertionError):
            validate_attempt(self.case)

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


class PointerAsyncBarrierTest(unittest.TestCase):
    def test_async_snapshot_is_resolved_before_its_command_bank_is_tested(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.evaluate('''() => {
                    window.pointerRelease={observed:true}; window.calls=0;
                    window.pointerOutcomes=[{input:'digit_1',status:'completed'}];
                    window.curta={run:()=>({snapshot:async()=>{
                        await new Promise(resolve=>setTimeout(resolve,10));
                        calls++;
                        return {commands:calls<3?[{status:'active'}]:[]};
                    }})};
                }''')
                snapshot = wait_for_gesture(page, 'digit_1')
                self.assertEqual(snapshot['commands'], [])
                self.assertEqual(page.evaluate('calls'), 3)
                page.evaluate('pointerOutcomes=[]')
                self.assertEqual(wait_for_gesture(page, 'digit_1')['commands'], [])
                self.assertEqual(page.evaluate('calls'), 4)
            finally:
                browser.close()
