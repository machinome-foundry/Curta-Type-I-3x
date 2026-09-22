"""One corpus, two models: the clocked harness against the operating Curta.

The oracle side is recorded once, because `simulation/running.py` costs about
0.8 s per 0.1 s tick; `clocked_spike_oracle.json` beside this file holds the
readouts and the actual dial angles of every scenario in
`simulation.tools.clocked_spike.SCENARIOS`. Re-record it with

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD" \
        /home/asa/devel/machinome-studio/.venv/bin/python -m simulation.tools.clocked_spike record

which takes about seven and a half minutes. These tests replay the same
corpus through the harness, which needs no geometry and finishes in
milliseconds, and pin exactly which readouts agree and which do not.

`simulation/docs/clocked-spike-2026-09-16.md` explains every entry below.
"""

import json
import unittest

from simulation.tools.clocked_spike import (
    ALL_LOCKS, CURTA_LOCKS, FIXTURE, Interlocks, SCENARIOS, ClockedCurta,
    compare, rack, rack_reach, rack_sweep, replay_clocked)

# The running model's prescribed zero-capture band is half a wheel degree.
CAPTURE_BAND = .5 / 36 + 1e-6      # the fixture rounds to six places

# Reads taken with the crank off its rest. They are not stroke ends: the
# clocked model answers them from its POSE, and its committed state has not
# moved yet. `test_the_pose_reproduces_the_running_dial_angles` is the check
# that applies to them.
MID_STROKE = {
    ('partial_crank_release_and_resume', 'quarter turn'),
    ('mid_stroke_selector_change', 'half stroke'),
    ('mid_stroke_carriage_shift', 'shifted mid stroke'),
    ('mid_stroke_reversing_lever', 'lifted mid stroke'),
    ('mid_stroke_carriage_lift_and_sweep', 'cleared mid stroke'),
}

# Stroke ends the clocked model does NOT reproduce, with the diagnosis the
# spike settled on. Everything else in the corpus must agree.
DIVERGENT = {
    ('mid_stroke_carriage_shift', 'completed'):
        'needs the carriage interlock; closing it agrees',
    ('mid_stroke_reversing_lever', 'completed'):
        'the machine forbids the action and the operating model does not',
    ('mid_stroke_carriage_lift_and_sweep', 'completed'):
        'the machine forbids the action and the operating model does not',
    ('crank_reversal', 'reversed'):
        'the operating model has no anti-reversal pawl (open red diagnostic)',
    ('sweep_stopped_between_teeth', 'rack between teeth'):
        'a dial parked between two teeth; the clearing checks forbid the rest',
}


class RackGeometryTest(unittest.TestCase):
    """The clearing racks, read off the project's own measured phases."""

    def test_reach_is_continuous_monotone_and_invertible(self):
        for counter, places in ((False, 11), (True, 6)):
            for place in range(places):
                start, pitch = rack(place, counter)
                previous = rack_reach(start - 400, place, counter)
                for step in range(0, 8000):
                    sweep = start - 400 + step / 10
                    reach = rack_reach(sweep, place, counter)
                    self.assertGreaterEqual(reach + 1e-9, previous)
                    self.assertLessEqual(reach - previous, .1 / pitch + 1e-9)
                    previous = reach
                for reach in (-11.5, -9, -.5, 0, 4.5, 9, 13.5):
                    for forward in (True, False):
                        self.assertAlmostEqual(rack_reach(
                            rack_sweep(reach, place, counter, forward),
                            place, counter), reach)

    def test_one_ring_revolution_carries_nine_teeth_past_every_dial(self):
        for counter, places in ((False, 11), (True, 6)):
            for place in range(places):
                self.assertAlmostEqual(
                    rack_reach(360, place, counter) -
                    rack_reach(0, place, counter), 9)


class ClockedAgreementTest(unittest.TestCase):
    """Stroke-end readouts, against the recorded operating model."""

    @classmethod
    def setUpClass(cls):
        cls.open_locks = compare(interlocks=Interlocks())
        cls.curta_locks = compare(interlocks=CURTA_LOCKS)

    def rows(self, report):
        for name, item in report.items():
            for row in item['rows']:
                yield name, row

    def test_every_stroke_end_agrees_with_no_interlock_at_all(self):
        """Question 1: the clocked readout at each stroke end, locks open."""
        for name, row in self.rows(self.open_locks):
            key = (name, row['label'])
            if key in MID_STROKE or key in DIVERGENT:
                continue
            with self.subTest(scenario=name, read=row['label']):
                self.assertEqual(row['running'], row['clocked'])

    def test_the_recorded_divergences_are_still_exactly_these(self):
        found = {(name, row['label']) for name, row in self.rows(self.open_locks)
                 if not row['agree'] and (name, row['label']) not in MID_STROKE}
        self.assertEqual(found, set(DIVERGENT))

    def test_the_pose_reproduces_the_running_dial_angles(self):
        """Between events nothing is retained: the pose is the whole answer.

        Every read of every scenario that stayed inside the machine's
        documented interlocks, mid-stroke reads included, to within the
        running model's own half-degree zero-capture band.
        """
        for name, row in self.rows(self.open_locks):
            if name in {scenario for scenario, _ in DIVERGENT}:
                continue
            with self.subTest(scenario=name, read=row['label']):
                self.assertLessEqual(row['pose_error'], CAPTURE_BAND + 1e-9)

    def test_the_carriage_interlock_is_the_one_the_corpus_demands(self):
        row = next(row for name, row in self.rows(self.curta_locks)
                   if (name, row['label']) == ('mid_stroke_carriage_shift',
                                               'completed'))
        self.assertEqual(row['running'], row['clocked'])

    def test_closing_the_selector_interlock_would_break_agreement(self):
        """The register does not need the selectors held; the pose does not either."""
        locked = compare(['mid_stroke_selector_change'],
                         Interlocks(selectors_off_rest=True))
        open_row = next(row for row in
                        self.open_locks['mid_stroke_selector_change']['rows']
                        if row['label'] == 'completed')
        shut_row = next(row for row in
                        locked['mid_stroke_selector_change']['rows']
                        if row['label'] == 'completed')
        self.assertEqual(open_row['running'], open_row['clocked'])
        self.assertNotEqual(shut_row['running'], shut_row['clocked'])


class CommitSemanticsTest(unittest.TestCase):
    """The two committing relations, checked directly."""

    def test_an_open_ratchet_commits_a_reverse_revolution_as_an_addition(self):
        """Red first: `at = floor(crank / 360)` fires on a falling step too."""
        harness = ClockedCurta()
        harness.request(digit_1=9)
        harness.request(crank_rotation=360)
        self.assertEqual(harness.reading(), 9)
        harness.request(crank_rotation=0)
        self.assertEqual(harness.reading(), 18)     # not 9, and not 0

    def test_the_ratchet_leaves_the_register_where_the_stroke_left_it(self):
        harness = ClockedCurta(interlocks=Interlocks(crank_ratchet=True))
        harness.request(digit_1=9)
        harness.request(crank_rotation=360)
        harness.request(crank_rotation=0)
        self.assertEqual((harness.reading(), harness.reading(True)), (9, 1))
        self.assertEqual(harness.refusals[0][0], 'crank_ratchet')

    def test_several_crossings_in_one_request_commit_in_order(self):
        harness = ClockedCurta()
        harness.request(digit_1=7)
        harness.request(crank_rotation=3 * 360)
        self.assertEqual((harness.reading(), harness.reading(True)), (21, 3))
        self.assertEqual([event['kind'] for event in harness.events],
                         ['stroke'] * 3)

    def test_an_input_changed_along_the_path_is_read_at_the_crossing(self):
        harness = ClockedCurta()
        harness.request(digit_1=1)
        harness.request(crank_rotation=2 * 360, digit_1=5)
        self.assertEqual([event['operand'] for event in harness.events], [3, 5])


class ClearingTest(unittest.TestCase):
    """Question 3: do per-digit comparison events cover partial clearing?"""

    def prepared(self, result=1234567, **locks):
        harness = ClockedCurta(interlocks=Interlocks(**locks))
        harness.result = result
        harness.set_registers()
        harness.request(carriage_elevation=6)
        return harness

    def test_one_forward_sweep_clears_both_banks_with_no_held_value(self):
        harness = self.prepared()
        harness.turns = 987654
        harness.set_registers()
        harness.request(carriage_elevation=6)
        harness.request(clearing_rotation=360)
        self.assertEqual((harness.reading(), harness.reading(True)), (0, 0))
        self.assertEqual(harness.fractional_dials(), [])

    def test_half_sweeps_reach_one_bank_each_way(self):
        forward = self.prepared()
        forward.turns = 4
        forward.set_registers()
        forward.request(clearing_rotation=180)
        self.assertEqual((forward.reading(), forward.reading(True)), (0, 4))
        backward = self.prepared()
        backward.turns = 4
        backward.set_registers()
        backward.request(clearing_rotation=-180)
        self.assertEqual((backward.reading(), backward.reading(True)),
                         (1234567, 0))

    def test_a_reversed_sweep_does_not_un_clear_a_zeroed_dial(self):
        harness = self.prepared()
        harness.request(clearing_rotation=360)
        self.assertEqual(harness.reading(), 0)
        harness.request(clearing_rotation=0)
        self.assertEqual(harness.reading(), 0)
        harness.request(clearing_rotation=-360)
        self.assertEqual(harness.reading(), 0)

    def test_a_seated_carriage_does_not_clear(self):
        harness = self.prepared()
        harness.request(carriage_elevation=0)
        harness.request(clearing_rotation=360)
        self.assertEqual(harness.reading(), 1234567)

    def test_only_a_held_dial_reads_a_rack_stopped_between_teeth(self):
        harness = self.prepared(result=5)
        start, pitch = rack(0)
        harness.request(clearing_rotation=start + 2.5 * pitch)
        self.assertEqual(harness.reading(), 5)          # no event has fired
        self.assertEqual(harness.dial_reading(), 8)     # the held dial reads 8
        self.assertEqual([(place, round(value, 3)) for _, place, value
                          in harness.fractional_dials()], [(0, 7.5)])

    def test_the_clearing_checks_forbid_that_rest(self):
        harness = self.prepared(result=5, ring_rest_checks=True)
        start, pitch = rack(0)
        harness.request(clearing_rotation=start + 2.5 * pitch)
        self.assertEqual(harness.refusals[-1][0], 'ring_rest_checks')
        self.assertEqual(harness.inputs['clearing_rotation'], 180)
        self.assertEqual(harness.reading(), 0)
        self.assertEqual(harness.fractional_dials(), [])


class OracleFixtureTest(unittest.TestCase):
    def test_the_fixture_covers_the_whole_corpus(self):
        oracle = json.loads(FIXTURE.read_text())
        self.assertEqual(set(oracle['scenarios']), set(SCENARIOS))
        self.assertEqual(oracle['dt'], .1)


if __name__ == '__main__':
    unittest.main()
