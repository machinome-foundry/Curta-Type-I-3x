"""Clocked-machine spike: the fast Curta plus committed memory, in Python.

Project-level evidence for `solid-node/workflow/docs/clocked-machine.md`,
section "Before the proposal: a project-level spike". Nothing here is a
framework API, and no framework code is changed: the harness emulates the
note's candidate clocked semantics OUTSIDE solid-node, around the fast
model `simulation/curta.py:Curta` and its public drivers and ports.

Vocabulary, from the note:

* a REQUEST moves one or more inputs along a straight path to a new value;
* an EVENT is a unit step of an integer-valued expression of the inputs and
  the committed state, located exactly on that path;
* a COMMIT writes the state at an event, reading the inputs at the crossing
  and every state at its pre-event value;
* between events nothing is retained: the pose is the fast model's existing
  closed form evaluated at the current inputs and the current state.

The two committing relations emulated here are

    (crank & result & turns & operand & subtract & shift).commits(
        (result, turns), at=floor(crank / 360), law=<the fast model's ports>)

and, per decimal place of each register, the note's comparison event

    (ring & digit_p).commits(digit_p, at=ring >= rack_end(p, digit_p),
                             law=digit_p * (ring < rack_end(p, digit_p)))

`rack_end` is the ring angle at which that place's nine-tooth rack has
carried the dial round to its zero; it reads the digit because how far the
rack must travel depends on the digit standing there. The rack geometry is
the project's own measured phases, taken from `simulation/running_laws.py`
(`clearing_travel`) and `simulation/cycle.py` (`cleared_position`), which
agree on one digit per rack pitch.

Run `python -m simulation.tools.clocked_spike --help` from the project.
"""

import argparse
import json
from dataclasses import dataclass, asdict
from math import ceil, degrees, floor
from pathlib import Path
from time import monotonic

from simulation.arithmetic import calculate, digit

RESULT_PLACES = 11
TURNS_PLACES = 6
RESULT_MODULUS = 10 ** RESULT_PLACES
TURNS_MODULUS = 10 ** TURNS_PLACES

# The anti-reversal ratchet, from simulation/pawl.py.
RATCHET_PITCH = 357 / 116
RATCHET_RELEASE = .31

# Gates that are part of the closed form, not interlocks: the dials leave
# their bevel tips at 3 mm of carriage lift (running_laws.dial_motion) and
# the clearing racks only reach them at the full 6 mm (clearing_travel).
DIAL_ENGAGED_LIFT = 3.0
CLEARING_LIFT = 6.0
SUBTRACT_LIFT = 4.5           # running_laws.shaft_motion: elevation >= 4.5

EPS = 1e-9
FIXTURE = Path(__file__).resolve().parent / 'clocked_spike_oracle.json'


def rack(place, counter=False):
    """(start angle, degrees per digit) of one dial's nine-tooth rack.

    Identical constants to `clearing_travel` and `cleared_position`; the
    sweep coordinate is the clearing-ring DRIVER angle, which is minus the
    ring joint's angle (`clearing_rotation.drives(..., ratio=-1)`).
    """
    outer = place < 2
    station = (130 if counter else 0) - 20 * place
    datum = 0 if outer else -40
    start = (9.75 if outer else 10.5) + (datum - station) % 360
    pitch = degrees(3.75 / (52 if outer else 49.55))
    return start, pitch


def rack_reach(sweep, place, counter=False):
    """Digits this place's dial has been carried by the ring at `sweep`.

    A continuous, monotone, piecewise-linear function of the unbounded ring
    angle: flat outside the rack, one digit per pitch across its nine teeth,
    and nine digits per full ring revolution. The travel a path produces is
    the difference of this function at its ends, which is exactly what the
    running law contributes (`f(end) - f(start)`, jumps subtracted).
    """
    start, pitch = rack(place, counter)
    offset = sweep - start
    whole, part = divmod(offset, 360)
    return 9 * whole + min(part, 9 * pitch) / pitch


def rack_sweep(reach, place, counter=False, forward=True):
    """Inverse of `rack_reach`, which is flat between one rack and the next.

    A reach that is a whole multiple of nine is held over a whole dwell, so
    the inverse needs a side: a sweep running FORWARD reaches it first at the
    dwell's low end, one running backward at its high end.
    """
    start, pitch = rack(place, counter)
    whole, part = divmod(reach, 9)
    if forward and not part:
        whole, part = whole - 1, 9
    return start + 360 * whole + part * pitch


def solve_reach(sweep_from, sweep_to, travel):
    """The ring angle on a straight path at which `travel` digits are made.

    `travel` is signed and measured from `sweep_from`; returns None when the
    path does not deliver it. Only the rack's own geometry is used, so this
    is the exact crossing, not a search.
    """
    def locate(place, counter):
        base = rack_reach(sweep_from, place, counter)
        target = base + travel
        end = rack_reach(sweep_to, place, counter)
        if (travel > 0 and end < target - EPS) or (travel < 0 and end > target + EPS):
            return None
        return rack_sweep(target, place, counter, forward=travel > 0)
    return locate


@dataclass
class Interlocks:
    """Every lock starts open; the spike closes one only when a scenario asks."""
    crank_ratchet: bool = False
    selectors_off_rest: bool = False
    carriage_off_rest: bool = False
    crank_lift_off_rest: bool = False
    ring_off_rest: bool = False
    crank_lift_stroke: bool = False
    carriage_lift_travel: bool = False
    carriage_turn_needs_lift: bool = False
    crank_needs_seated_carriage: bool = False
    ring_rest_checks: bool = False


# The clearing lever's two stop positions A and B, in the sweep coordinate.
# The booklet puts them "at the two points where the black and the white dials
# meet"; the project's measured rack stations put the result bank in
# 9.75..209.5 degrees of sweep and the counter bank in 239.75..339.5, so the
# two checks bracket each bank and the existing running tests sweep 180 at a
# time between them.
RING_CHECKS = 180.0


INPUTS = tuple(f'digit_{index}' for index in range(1, 9)) + (
    'crank_rotation', 'crank_elevation', 'carriage_rotation',
    'carriage_elevation', 'clearing_rotation')


class ClockedCurta:
    """The note's clocked semantics over the fast Curta's public surface.

    `result` and `turns` are the state variables; `dial` keeps each place's
    ACTUAL position in digits, including a fraction left by a rack stopped
    between teeth. The two are separate on purpose: `result`/`turns` are the
    committed state the candidate spelling declares, `dial` is the held value
    (`fold`) the note asks the spike to decide about. Both are reported, so
    the corpus shows where a state committed only at events is enough.
    """

    def __init__(self, interlocks=None, fast=None, commit_through_fast=False):
        self.inputs = {name: 0.0 for name in INPUTS}
        self.result = 0
        self.turns = 0
        self.dial = {False: [0.0] * RESULT_PLACES, True: [0.0] * TURNS_PLACES}
        self.locks = interlocks if interlocks is not None else Interlocks()
        self.fast = fast
        self.commit_through_fast = commit_through_fast
        self.events = []
        self.refusals = []
        self.notes = []
        self.commits = 0
        self.commit_seconds = 0.0

    # ---------------------------------------------------------------- reading

    @property
    def shift(self):
        """The engaged carriage detent: `aligned()` partitions every angle."""
        return int(floor(self.inputs['carriage_rotation'] / 20 + .5))

    @property
    def subtracting(self):
        return 1 if self.inputs['crank_elevation'] >= SUBTRACT_LIFT else 0

    @property
    def operand(self):
        return sum(int(round(self.inputs[f'digit_{index}'])) * 10 ** (index - 1)
                   for index in range(1, 9))

    def set_registers(self, result=None, turns=None):
        """Session setup: a snapshot writes the state, the maker never does."""
        if result is not None:
            self.result = int(result)
        if turns is not None:
            self.turns = int(turns)
        self._reseat_dials()

    def reading(self, counter=False):
        """The committed state: what the clocked model says the register is."""
        return self.turns if counter else self.result

    def dial_reading(self, counter=False):
        """The held dials, read the way `running_laws.reading` reads angles."""
        return sum(int(floor(position + .5)) % 10 * 10 ** place
                   for place, position in enumerate(self.dial[counter]))

    def fractional_dials(self):
        return [(counter, place, position)
                for counter in (False, True)
                for place, position in enumerate(self.dial[counter])
                if abs(position - round(position)) > 1e-6]

    # ----------------------------------------------------------------- posing

    def pose_state(self):
        """Fast-Curta drivers for the CURRENT inputs and committed state."""
        crank = self.inputs['crank_rotation']
        return dict(initial_result=self.result, initial_turns=self.turns,
                    operand=self.operand,
                    crank_turns=(crank - 360 * floor(crank / 360)) / 360,
                    subtract=self.subtracting,
                    carriage_position=self.shift,
                    carriage_lift=self.inputs['carriage_elevation'] / 6,
                    clear=0)

    def pose(self):
        """Bind the fast model at the current pose and read its ports."""
        self.fast.set_state(**self.pose_state())
        return self.fast.result.value, self.fast.turns_counter.value

    def pose_dials(self, counter=False):
        """Where the fast model puts each dial at the current pose, in digits.

        `simulation/cycle.py:dial_positions` is the closed form the fast Curta
        already prescribes for motion inside one stroke. Under the clocked
        reading it is fed from the committed state instead of a slider, and
        the corpus checks it against the running model's actual dial angles.
        """
        from simulation.cycle import dial_positions
        places = TURNS_PLACES if counter else RESULT_PLACES
        return [position % 10 for position in dial_positions(
            self.turns if counter else self.result, self.operand,
            self.inputs['crank_rotation'] / 360, self.subtracting, self.shift,
            0, places, counter)]

    # --------------------------------------------------------------- requests

    def request(self, **targets):
        """One straight path from the current inputs to the requested ones."""
        unknown = set(targets) - set(INPUTS)
        if unknown:
            raise KeyError(f'not an input: {sorted(unknown)}')
        start = dict(self.inputs)
        end = dict(start)
        end.update({name: float(value) for name, value in targets.items()})
        end = self._apply_interlocks(start, end)
        self._walk(start, end)
        self.inputs = end
        return end

    def _rest_phase(self, crank):
        return crank - 360 * floor(crank / 360)

    def _apply_interlocks(self, start, end):
        """Clip or refuse the request; every clip is recorded as a refusal."""
        locks = self.locks
        off_rest = self._rest_phase(start['crank_rotation']) > EPS
        held = []
        if locks.crank_ratchet:
            seat = (RATCHET_RELEASE + RATCHET_PITCH *
                    floor((start['crank_rotation'] - RATCHET_RELEASE) / RATCHET_PITCH))
            if end['crank_rotation'] < seat - EPS:
                held.append(('crank_ratchet', 'crank_rotation',
                             end['crank_rotation'], seat))
                end['crank_rotation'] = seat
        if locks.crank_lift_stroke:
            clipped = min(9.0, max(0.0, end['crank_elevation']))
            if abs(clipped - end['crank_elevation']) > EPS:
                held.append(('crank_lift_stroke', 'crank_elevation',
                             end['crank_elevation'], clipped))
                end['crank_elevation'] = clipped
        if locks.carriage_lift_travel:
            clipped = min(6.0, max(0.0, end['carriage_elevation']))
            if abs(clipped - end['carriage_elevation']) > EPS:
                held.append(('carriage_lift_travel', 'carriage_elevation',
                             end['carriage_elevation'], clipped))
                end['carriage_elevation'] = clipped
        if locks.carriage_turn_needs_lift and \
                abs(end['carriage_rotation'] - start['carriage_rotation']) > EPS and \
                max(start['carriage_elevation'], end['carriage_elevation']) < CLEARING_LIFT - EPS:
            held.append(('carriage_turn_needs_lift', 'carriage_rotation',
                         end['carriage_rotation'], start['carriage_rotation']))
            end['carriage_rotation'] = start['carriage_rotation']
        if locks.crank_needs_seated_carriage and \
                abs(end['crank_rotation'] - start['crank_rotation']) > EPS and (
                    start['carriage_elevation'] > EPS or
                    abs(start['carriage_rotation'] -
                        20 * round(start['carriage_rotation'] / 20)) > EPS):
            held.append(('crank_needs_seated_carriage', 'crank_rotation',
                         end['crank_rotation'], start['crank_rotation']))
            end['crank_rotation'] = start['crank_rotation']
        if locks.ring_rest_checks and \
                abs(end['clearing_rotation'] - start['clearing_rotation']) > EPS:
            span = end['clearing_rotation'] - start['clearing_rotation']
            checks = end['clearing_rotation'] / RING_CHECKS
            seated = RING_CHECKS * (ceil(checks) if span > 0 else floor(checks))
            if abs(seated - end['clearing_rotation']) > EPS:
                held.append(('ring_rest_checks', 'clearing_rotation',
                             end['clearing_rotation'], seated))
                end['clearing_rotation'] = seated
        if off_rest:
            groups = (
                (locks.selectors_off_rest,
                 tuple(f'digit_{index}' for index in range(1, 9))),
                (locks.carriage_off_rest, ('carriage_rotation', 'carriage_elevation')),
                (locks.crank_lift_off_rest, ('crank_elevation',)),
                (locks.ring_off_rest, ('clearing_rotation',)),
            )
            for closed, names in groups:
                if not closed:
                    continue
                for name in names:
                    if abs(end[name] - start[name]) > EPS:
                        held.append(('off_rest', name, end[name], start[name]))
                        end[name] = start[name]
        self.refusals.extend(held)
        return end

    def _walk(self, start, end):
        """Locate every event on the path in order, committing each in turn.

        Between events the held dials are carried by the rack exactly as the
        running law carries them (the difference of `rack_reach` over the
        sub-segment), so the event is reached with the dial ON its zero.
        """
        at = 0.0
        for _ in range(4096):
            found = self._next_event(start, end, at)
            if found is None:
                break
            position, commit = found
            self._carry_dials(start, end, at, position)
            at = position
            commit(self._values(start, end, at))
        else:
            raise RuntimeError('more than 4096 events in one request')
        self._carry_dials(start, end, at, 1.0)

    def _values(self, start, end, at):
        return {name: start[name] + (end[name] - start[name]) * at
                for name in INPUTS}

    def _next_event(self, start, end, at):
        candidates = []
        crank = self._next_crank_event(start, end, at)
        if crank is not None:
            candidates.append(crank)
        candidates.extend(self._next_clearing_events(start, end, at))
        if not candidates:
            return None
        return min(candidates, key=lambda item: item[0])

    # ------------------------------------------------------------ crank event

    def _next_crank_event(self, start, end, at):
        """`at = floor(crank / 360)`: every multiple of 360 on the path."""
        first, last = start['crank_rotation'], end['crank_rotation']
        span = last - first
        if abs(span) < EPS:
            return None
        here = first + span * at
        rising = span > 0
        index = floor(here / 360) + 1 if rising else ceil(here / 360) - 1
        position = (360 * index - first) / span
        if position <= at + EPS or position > 1 + EPS:
            return None
        return min(position, 1.0), self._commit_registers

    def _commit_registers(self, values):
        """The stroke's end: the fast model's settled registers, at once."""
        operand = sum(int(round(values[f'digit_{index}'])) * 10 ** (index - 1)
                      for index in range(1, 9))
        subtract = 1 if values['crank_elevation'] >= SUBTRACT_LIFT else 0
        shift = int(floor(values['carriage_rotation'] / 20 + .5))
        engaged = values['carriage_elevation'] < DIAL_ENGAGED_LIFT
        before = (self.result, self.turns)
        if engaged:
            started = monotonic()
            if self.commit_through_fast:
                self.fast.set_state(initial_result=self.result,
                                    initial_turns=self.turns, operand=operand,
                                    crank_turns=1, subtract=subtract,
                                    carriage_position=shift,
                                    carriage_lift=values['carriage_elevation'] / 6,
                                    clear=0)
                result = int(self.fast.result.value)
                turns = int(self.fast.turns_counter.value)
            else:
                result, turns = calculate(self.result, self.turns, operand, 1,
                                          subtract, shift)
                result, turns = int(result), int(turns)
            self.commit_seconds += monotonic() - started
            self.commits += 1
            self.result, self.turns = result, turns
            self._reseat_dials()
        self.events.append(dict(kind='stroke', crank=values['crank_rotation'],
                                operand=operand, subtract=subtract, shift=shift,
                                engaged=engaged, before=before,
                                after=(self.result, self.turns)))

    def _reseat_dials(self):
        """Arithmetic turns whole teeth: it re-seats every dial on its detent.

        A dial left between teeth by a stopped rack keeps its fraction in the
        real machine, and a whole-tooth advance preserves it. The corpus does
        no arithmetic on a fractional dial (`fractional_dials()` reports one),
        so re-seating is exact here; the report says where it would not be.
        """
        for place in range(RESULT_PLACES):
            self.dial[False][place] = float(digit(self.result, place))
        for place in range(TURNS_PLACES):
            self.dial[True][place] = float(digit(self.turns, place))

    # --------------------------------------------------------- clearing event

    def _clearing_active(self, start, end):
        """The racks reach the dials only with the carriage fully raised."""
        low = min(start['carriage_elevation'], end['carriage_elevation'])
        high = max(start['carriage_elevation'], end['carriage_elevation'])
        if low >= CLEARING_LIFT - EPS:
            return True
        if high >= CLEARING_LIFT - EPS and abs(
                end['clearing_rotation'] - start['clearing_rotation']) > EPS:
            self.notes.append('a request moved the ring while the carriage lift '
                              'crossed the clearing height; the spike does not '
                              'model a combined lift-and-sweep request')
        return False

    def _next_clearing_events(self, start, end, at):
        """Per-digit comparison events: the rack carries a dial to its zero."""
        first, last = start['clearing_rotation'], end['clearing_rotation']
        span = last - first
        if abs(span) < EPS or not self._clearing_active(start, end):
            return []
        here = first + span * at
        found = []
        for counter, places in ((False, RESULT_PLACES), (True, TURNS_PLACES)):
            for place in range(places):
                standing = self.dial[counter][place]
                if standing <= EPS:
                    continue            # the missing tooth holds a zero dial
                travel = (10 - standing) if span > 0 else -standing
                sweep = solve_reach(here, last, travel)(place, counter)
                if sweep is None:
                    continue
                position = (sweep - first) / span
                if position <= at + EPS or position > 1 + EPS:
                    continue
                found.append((min(position, 1.0),
                              self._clearing_commit(counter, place)))
        return found

    def _carry_dials(self, start, end, at_from, at_to):
        """Move every engaged dial by the rack travel over one sub-segment."""
        first, last = start['clearing_rotation'], end['clearing_rotation']
        span = last - first
        if abs(span) < EPS or at_to <= at_from or not self._clearing_active(start, end):
            return
        was, now = first + span * at_from, first + span * at_to
        for counter, places in ((False, RESULT_PLACES), (True, TURNS_PLACES)):
            for place in range(places):
                standing = self.dial[counter][place]
                if standing <= EPS:
                    continue
                travel = (rack_reach(now, place, counter) -
                          rack_reach(was, place, counter))
                room = (10 - standing) if travel > 0 else -standing
                moved = min(travel, room) if travel > 0 else max(travel, room)
                position = standing + moved
                self.dial[counter][place] = 0.0 if (
                    position <= EPS or position >= 10 - EPS) else position

    def _clearing_commit(self, counter, place):
        def commit(values):
            before = self.dial[counter][place]
            self.dial[counter][place] = 0.0
            if counter:
                self.turns -= digit(self.turns, place) * 10 ** place
            else:
                self.result -= digit(self.result, place) * 10 ** place
            self.events.append(dict(kind='clear', counter=counter, place=place,
                                    before=before,
                                    sweep=values['clearing_rotation'],
                                    after=(self.result, self.turns)))
        return commit


# --------------------------------------------------------------- the corpus

# One neutral action vocabulary, replayed through both models. Durations are
# the ones the existing running tests use, so the oracle side costs what those
# tests cost. `read` records both registers and every dial's actual position.
#
#   ('digits', {1: 3})          set selectors, as the user's fingers do
#   ('crank', degrees, seconds) turn the crank, signed
#   ('crank_lift', mm, seconds) the reversing/subtraction stroke
#   ('carriage_lift', mm, s)    lift the carriage off its bevel tips
#   ('carriage_turn', deg, s)   shift the carriage, 20 degrees per decimal
#   ('ring', degrees, seconds)  sweep the clearing ring, signed
#   ('read', label)             record both readouts

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


# ------------------------------------------------------------- the two sides

def replay_clocked(actions, harness):
    readings = []
    for action in actions:
        head = action[0]
        if head == 'read':
            readings.append(dict(
                label=action[1],
                result=harness.reading(), turns=harness.reading(True),
                dial_result=harness.dial_reading(),
                dial_turns=harness.dial_reading(True),
                posed=[round(value, 6) for value in harness.pose_dials()] +
                      [round(value, 6) for value in harness.pose_dials(True)],
                fractional=[[bool(c), p, round(v, 6)]
                            for c, p, v in harness.fractional_dials()]))
            continue
        if head == 'digits':
            harness.request(**{f'digit_{index}': value
                               for index, value in action[1].items()})
        elif head == 'crank':
            harness.request(crank_rotation=harness.inputs['crank_rotation'] + action[1])
        elif head == 'crank_lift':
            harness.request(crank_elevation=action[1])
        elif head == 'carriage_lift':
            harness.request(carriage_elevation=action[1])
        elif head == 'carriage_turn':
            harness.request(carriage_rotation=action[1])
        elif head == 'ring':
            harness.request(clearing_rotation=harness.inputs['clearing_rotation'] + action[1])
        else:
            raise KeyError(head)
    return readings


def running_dials(sim, counter=False):
    from simulation.running_parts import RESULT_DIALS, TURNS_DIALS
    table = TURNS_DIALS if counter else RESULT_DIALS
    bank = 'turns' if counter else 'result'
    state = sim.state
    return [((zero - state[f'carriage.registers.{bank}_register.{name}.turn'])
             / 36) % 10 for name, zero in table]


def replay_running(actions, sim):
    from simulation.running import register_reading
    readings = []
    for action in actions:
        head = action[0]
        if head == 'read':
            dials = running_dials(sim), running_dials(sim, True)
            readings.append(dict(
                label=action[1],
                result=register_reading(sim), turns=register_reading(sim, True),
                dial_result=[round(value, 6) for value in dials[0]],
                dial_turns=[round(value, 6) for value in dials[1]]))
            continue
        if head == 'digits':
            for index, value in action[1].items():
                sim.move(f'digit_{index}', to=value)
            continue
        target, duration = action[1], action[2]
        if head == 'crank':
            handle = sim.move('crank_rotation', by=target, duration=duration)
        elif head == 'crank_lift':
            handle = sim.move('crank_elevation', to=target, duration=duration)
        elif head == 'carriage_lift':
            handle = sim.move('carriage_elevation', to=target, duration=duration)
        elif head == 'carriage_turn':
            handle = sim.move('carriage_rotation', to=target, duration=duration)
        elif head == 'ring':
            handle = sim.move('clearing_rotation', by=target, duration=duration)
        else:
            raise KeyError(head)
        if duration:
            sim.run(duration)
        readings.append(dict(command=head, status=handle.status,
                             requested=handle.requested, admitted=handle.admitted))
    return readings


def record_oracle(names=None, path=FIXTURE):
    """Run the operating Curta ONCE over the corpus and keep its readouts."""
    from solid_node.simulation import Sim
    from simulation.running import OperatingCurta

    started = monotonic()
    sim = Sim(OperatingCurta(), dt=.1)
    built = monotonic() - started
    record = dict(framework=framework_commit(), dt=.1, construct_seconds=built,
                  scenarios={})
    for name, actions in SCENARIOS.items():
        if names and name not in names:
            continue
        sim.reset()
        began, ticks = monotonic(), sim.tick
        readings = replay_running(actions, sim)
        record['scenarios'][name] = dict(
            readings=readings, seconds=monotonic() - began,
            ticks=sim.tick - ticks)
        print(f'{name}: {monotonic() - began:.1f} s, '
              f'{sim.tick - ticks} ticks', flush=True)
    path.write_text(json.dumps(record, indent=1))
    return record


def framework_commit():
    import subprocess
    import solid_node
    root = Path(solid_node.__file__).resolve().parents[1]
    try:
        return subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'],
                              capture_output=True, text=True,
                              check=True).stdout.strip()
    except Exception:                                   # pragma: no cover
        return 'unknown'


def compare(names=None, interlocks=None, fast=None, commit_through_fast=False,
            path=FIXTURE):
    """Replay the corpus through the harness and diff it against the oracle."""
    oracle = json.loads(path.read_text())
    report = {}
    for name, actions in SCENARIOS.items():
        if names and name not in names:
            continue
        if name not in oracle['scenarios']:
            continue
        harness = ClockedCurta(interlocks=interlocks, fast=fast,
                               commit_through_fast=commit_through_fast)
        began = monotonic()
        clocked = replay_clocked(actions, harness)
        expected = [item for item in oracle['scenarios'][name]['readings']
                    if 'label' in item]
        rows = []
        for want, got in zip(expected, clocked):
            rows.append(dict(
                label=want['label'],
                running=(want['result'], want['turns']),
                clocked=(got['result'], got['turns']),
                held=(got['dial_result'], got['dial_turns']),
                agree=(want['result'], want['turns']) == (got['result'], got['turns']),
                held_agree=(want['result'], want['turns']) ==
                           (got['dial_result'], got['dial_turns']),
                running_dials=want['dial_result'] + want['dial_turns'],
                pose_error=max(abs(((posed - ran + 5) % 10) - 5) for posed, ran
                               in zip(got['posed'],
                                      want['dial_result'] + want['dial_turns'])),
                fractional=got['fractional']))
        report[name] = dict(rows=rows, seconds=monotonic() - began,
                            events=harness.events, refusals=harness.refusals,
                            notes=harness.notes, commits=harness.commits,
                            commit_seconds=harness.commit_seconds,
                            running_seconds=oracle['scenarios'][name]['seconds'],
                            running_ticks=oracle['scenarios'][name]['ticks'])
    return report


ALL_LOCKS = Interlocks(**{field: True for field in Interlocks().__dict__})

# What the spike settles on for the Curta: every lock the corpus demanded, plus
# the two the operating model already declares as joint ranges. `selectors_off_rest`
# and `crank_needs_seated_carriage` are documented by the manufacturer's booklet
# but no scenario demands them, and closing either makes the clocked model
# disagree with the operating model, which has neither. See
# simulation/docs/clocked-spike-2026-09-16.md.
CURTA_LOCKS = Interlocks(
    crank_ratchet=True,
    carriage_off_rest=True,
    crank_lift_off_rest=True,
    ring_off_rest=True,
    crank_lift_stroke=True,
    carriage_lift_travel=True,
    carriage_turn_needs_lift=True,
    ring_rest_checks=True,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('record', 'compare', 'time'))
    parser.add_argument('--scenario', action='append')
    parser.add_argument('--locks', default='none',
                        help="'none', 'all', or comma-separated lock names")
    parser.add_argument('--through-fast', action='store_true',
                        help='commit through the fast model instead of calculate()')
    arguments = parser.parse_args()
    if arguments.command == 'record':
        record_oracle(arguments.scenario)
        return
    if arguments.locks == 'none':
        locks = Interlocks()
    elif arguments.locks == 'all':
        locks = ALL_LOCKS
    else:
        locks = Interlocks(**{name: True for name in arguments.locks.split(',')})
    fast = None
    if arguments.through_fast or arguments.command == 'time':
        from simulation.curta import Curta
        started = monotonic()
        fast = Curta()
        print(f'fast model constructed in {monotonic() - started:.2f} s', flush=True)
    if arguments.command == 'time':
        timings(fast)
        return
    report = compare(arguments.scenario, locks, fast, arguments.through_fast)
    print(json.dumps(report, indent=1, default=str))


def timings(fast):
    harness = ClockedCurta(fast=fast, commit_through_fast=True)
    started = monotonic()
    harness.pose()
    cold = monotonic() - started
    started = monotonic()
    for index in range(50):
        harness.inputs['crank_rotation'] = index * 7.2
        harness.pose()
    warm = (monotonic() - started) / 50
    harness.inputs['crank_rotation'] = 0.0
    harness.request(**{'digit_1': 3})
    started = monotonic()
    for index in range(20):
        harness.request(crank_rotation=360 * (index + 1))
    through_fast = (monotonic() - started) / 20
    plain = ClockedCurta()
    plain.request(**{'digit_1': 3})
    started = monotonic()
    for index in range(20):
        plain.request(crank_rotation=360 * (index + 1))
    direct = (monotonic() - started) / 20
    print(json.dumps(dict(
        framework=framework_commit(),
        pose_cold_seconds=cold, pose_warm_seconds=warm,
        commit_through_fast_seconds=through_fast,
        commit_direct_seconds=direct,
        commits=harness.commits,
        commit_only_seconds=harness.commit_seconds / max(1, harness.commits),
    ), indent=1))


if __name__ == '__main__':
    main()
