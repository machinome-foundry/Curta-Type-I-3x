"""Neutral action corpus from clocked-spike commit bcf2017 (2026-09-16)."""

SCENARIOS = {
    # test_running.py::test_manual_calibration_carries, and the page-53
    # sequence simulation/tools/running_probe.py replays.
    'calibration_page_53': [
        ('digits', {1: 0, 2: 0}), ('crank', 360, 2), ('read', 'after 0'),
        ('digits', {1: 1, 2: 0}), ('crank', 360, 2), ('read', 'after 1'),
        ('digits', {1: 9, 2: 0}), ('crank', 360, 2), ('read', 'after 9'),
        ('digits', {1: 0, 2: 9}), ('crank', 360, 2), ('read', 'after 90'),
    ],
    # test_running.py::test_subtraction_borrows_through_both_registers...
    'subtraction_borrow_and_undo': [
        ('digits', {1: 1}), ('crank_lift', 9, 0), ('crank', 360, 2),
        ('read', 'borrowed'),
        ('crank_lift', 0, 0), ('crank', 360, 2), ('read', 'undone'),
    ],
    # test_running.py::test_shift_reassociates_actual_dials...
    'shift_reassociates': [
        ('digits', {1: 9}), ('crank', 360, 2), ('read', 'nine'),
        ('carriage_lift', 6, .2), ('carriage_turn', 40, .2), ('read', 'shifted'),
        ('carriage_lift', 0, .2), ('digits', {1: 3}), ('crank', 360, 2),
        ('read', 'three hundred'),
    ],
    # test_running.py::test_independent_inputs_and_two_successive_additions
    'two_additions_and_selective_clearing': [
        ('digits', {1: 3}), ('crank', 360, 2), ('read', 'three'),
        ('digits', {1: 2}), ('read', 'selector only'),
        ('crank', 360, 2), ('read', 'five'),
        ('carriage_lift', 6, .2), ('read', 'lifted'),
        ('ring', 180, .2), ('read', 'result cleared'),
        ('ring', 180, .2), ('read', 'counter cleared'),
        ('ring', -360, .2), ('read', 'reverse sweep'),
    ],
    # test_running.py::test_partial_crank_release_and_snapshot_replay
    'partial_crank_release_and_resume': [
        ('digits', {1: 9}), ('crank', 90, .5), ('read', 'quarter turn'),
        ('crank', 270, 1.5), ('read', 'completed'),
    ],
    # test_running_clearing.py::test_seated_carriage_does_not_clear
    'seated_carriage_does_not_clear': [
        ('digits', {1: 5}), ('crank', 360, 2), ('read', 'five'),
        ('ring', 360, .4), ('read', 'seated sweep'),
    ],
    # test_running_clearing.py::test_opposite_half_sweeps_reach_different...,
    # at the whole machine rather than the one-wheel bench.
    'half_sweeps_reach_different_banks': [
        ('digits', {1: 5}), ('crank', 360, 2), ('read', 'five'),
        ('carriage_lift', 6, .2),
        ('ring', -180, .2), ('read', 'counter half sweep'),
        ('ring', 180, .2), ('read', 'back to rest'),
        ('ring', 180, .2), ('read', 'result half sweep'),
    ],
    # The interlock audit: actions the running model admits mid-stroke.
    'mid_stroke_selector_change': [
        ('digits', {1: 3}), ('crank', 180, 1), ('read', 'half stroke'),
        ('digits', {1: 7}), ('crank', 180, 1), ('read', 'completed'),
    ],
    'mid_stroke_carriage_shift': [
        ('digits', {1: 9}), ('crank', 180, 1),
        ('carriage_turn', 20, .2), ('read', 'shifted mid stroke'),
        ('crank', 180, 1), ('read', 'completed'),
    ],
    'mid_stroke_reversing_lever': [
        ('digits', {1: 4}), ('crank', 180, 1),
        ('crank_lift', 9, .2), ('read', 'lifted mid stroke'),
        ('crank', 180, 1), ('read', 'completed'),
    ],
    'mid_stroke_carriage_lift_and_sweep': [
        ('digits', {1: 9}), ('crank', 180, 1),
        ('carriage_lift', 6, .2), ('ring', 360, .4), ('read', 'cleared mid stroke'),
        ('carriage_lift', 0, .2), ('crank', 180, 1), ('read', 'completed'),
    ],
    'crank_reversal': [
        ('digits', {1: 9}), ('crank', 360, 2), ('read', 'nine'),
        ('crank', -360, 2), ('read', 'reversed'),
    ],
    # test_running_limits.py::test_crank_cannot_lift_past_subtraction_stroke
    'blocked_crank_lift': [
        ('digits', {1: 1}), ('crank_lift', 12, .2), ('read', 'overlifted'),
        ('crank', 360, 2), ('read', 'subtracted'),
    ],
    'between_detent_carriage': [
        ('digits', {1: 1}), ('carriage_lift', 6, .2), ('carriage_turn', 12, .2),
        ('carriage_lift', 0, .2), ('crank', 360, 2), ('read', 'snapped detent'),
    ],
    # The fold probe: a rack stopped between two teeth.
    'sweep_stopped_between_teeth': [
        ('digits', {1: 5}), ('crank', 360, 2), ('read', 'five'),
        ('carriage_lift', 6, .2), ('ring', 20.08, .2),
        ('read', 'rack between teeth'),
    ],
}

SCENARIOS.update({
    f'subtract_at_carriage_{position}': [
        ('digits', {1: 7}), ('carriage_lift', 6, .2),
        ('carriage_turn', 20 * position, .2), ('carriage_lift', 0, .2),
        ('crank_lift', 9, .2), ('crank', 360, 2), ('read', 'subtracted'),
    ] for position in (0, 2, 5)
})
