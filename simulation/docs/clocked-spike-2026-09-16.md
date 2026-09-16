# Clocked-machine spike — 2026-09-16

The framework note `solid-node/workflow/docs/clocked-machine.md` asks, in its
section "Before the proposal: a project-level spike", whether this Curta is a
**clocked machine**: a few retained values, closed-form positions between
events, and a commit of the retained values at each event. This record is that
spike's result. It is project evidence, on branch `clocked-spike`. **No
framework change was made and none is proposed here**; the clocked semantics
are emulated in ordinary Python around the fast model's existing public
surface. Nothing in the note's candidate spelling is a framework API, and this
record does not make it one.

Framework at `81c53646f5bdf603a7c2b45d03203032be7dd366`
(`solid-node` primary `main`, read-only for this work); project branch
`clocked-spike` from `direct-operation` at `9fb725f`.

## What was built

[`simulation/tools/clocked_spike.py`](../tools/clocked_spike.py) is a harness,
not a model. It holds

* **inputs** — the eight setting selectors, the crank's unbounded rotation and
  its lift, the carriage's rotation and lift, and the clearing ring's unbounded
  rotation: exactly `simulation/running.py:OperatingCurta`'s drivers, minus the
  decimal markers, which change no register;
* **state** — `result` and `turns`, plus each dial's actual position in digits,
  kept separately so the spike can answer the fold question (below);
* **requests** — `request(**targets)` moves inputs along ONE straight path,
  locates every event on that path in path order, and commits each;
* **interlocks** — a `dataclass` of named locks, ALL OPEN by default.

Two committing relations are emulated, in the note's shape:

    (crank & result & turns & operand & subtract & shift).commits(
        (result, turns), at=floor(crank / 360), law=<the fast model's ports>)

    (ring & digit_p).commits(digit_p, at=ring >= rack_end(p, digit_p),
                             law=digit_p * (ring < rack_end(p, digit_p)))

The stroke commit evaluates `simulation/curta.py:Curta`'s own `result` and
`turns_counter` ports with `crank_turns=1`, the inputs read AT the crossing and
the state at its pre-event value; `--through-fast` runs it that way and the
default runs the same expression through `simulation/arithmetic.py:calculate`,
which the ports are built from. The clearing commit's `rack_end` is the ring
angle at which that place's nine-tooth rack has carried the dial round to its
zero. It READS the digit, because how far the rack must travel depends on the
digit standing there — the note's sketch writes a constant `RACK_END[3]`, and
the measured geometry does not allow one.

The rack constants are the project's own: `simulation/running_laws.py`
(`clearing_travel`) and `simulation/cycle.py` (`cleared_position`) agree that
the rack carries one digit per pitch, with the pitch and station of each of
the 17 dials. `rack_reach(sweep, place)` is that law written as a continuous
monotone function of the unbounded ring angle, so a path's travel is the
difference at its ends — which is exactly what the running law contributes.
Its inverse needs a side, because the function is flat between one rack and
the next: a forward sweep reaches a whole multiple of nine at the dwell's low
end, a backward one at its high end. Getting that wrong was the one harness
defect the corpus caught, and it failed red as
`ClearingTest::test_one_forward_sweep_clears_both_banks_with_no_held_value`
before the fix.

Between events nothing is retained. `pose_dials()` is
`simulation/cycle.py:dial_positions` fed from the committed state instead of
the `initial_result` / `initial_turns` sliders; `pose()` binds the whole fast
Curta and reads its ports.

`simulation/curta.py`, `simulation/running.py` and the laws were not modified.

## The corpus and the oracle

One neutral action vocabulary is replayed through both models:
[`simulation/tools/test_clocked_spike.py`](../tools/test_clocked_spike.py).
Eighteen scenarios, drawn from the running tests the note names — the page-53
calibration sequence (`Manual/Curta Build Manual.pdf` page 53, and
`simulation/tools/running_probe.py`), carries and borrows through both full
banks, the shift, selective clearing in both directions, partial crank release
and resume, the seated-carriage sweep, the blocked crank lift, subtraction at
three carriage positions — plus five scenarios that exist only for the
interlock audit, each performing an action mid-stroke.

The operating model was run ONCE over the whole corpus and its readouts kept in
`simulation/tools/clocked_spike_oracle.json`:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD" \
        /home/asa/devel/libresolid-studio/.venv/bin/python -m simulation.tools.clocked_spike record

439.2 s over 574 ticks at `dt = .1`, plus 5.4 s to construct the `Sim`. The
fixture records both registers AND every dial's actual angle at each read, so
the pose can be checked as well as the readout.

`test_running_markers.py` was NOT replayed: the markers are arithmetic-free,
the clocked model has no state for them, and they would only have added ticks.

## Question 1 — does the clocked model reproduce the readouts?

**Yes, at every stroke end, with every interlock still open**, across every
scenario in which the machine was operated the way the manufacturer's booklet
says it must be. `running` is the operating model's readout, `open` the clocked
model's committed state with no lock at all, `locked` with the locks the spike
settles on (`CURTA_LOCKS`), `pose` the largest difference in digits between
`dial_positions` fed from the clocked state and the operating model's actual
dial angles.

| scenario (source) | read | running | clocked, open | clocked, locked | agree | pose error |
| --- | --- | --- | --- | --- | --- | --- |
| calibration_page_53 (`test_manual_calibration_carries`, `running_probe`) | after 0 | (0, 1) | (0, 1) | (0, 1) | yes | 0 |
| | after 1 | (1, 2) | (1, 2) | (1, 2) | yes | 0 |
| | after 9 | (10, 3) | (10, 3) | (10, 3) | yes | 0 |
| | after 90 | (100, 4) | (100, 4) | (100, 4) | yes | 0 |
| subtraction_borrow_and_undo (`test_subtraction_borrows...`) | borrowed | (99999999999, 999999) | same | same | yes | 0 |
| | undone | (0, 0) | (0, 0) | (0, 0) | yes | 0 |
| shift_reassociates (`test_shift_reassociates...`) | nine | (9, 1) | (9, 1) | (9, 1) | yes | 0 |
| | shifted | (9, 1) | (9, 1) | (9, 1) | yes | 0 |
| | three hundred | (309, 101) | (309, 101) | (309, 101) | yes | 0 |
| two_additions_and_selective_clearing (`test_independent_inputs...`) | three | (3, 1) | (3, 1) | (3, 1) | yes | 0 |
| | selector only | (3, 1) | (3, 1) | (3, 1) | yes | 0 |
| | five | (5, 2) | (5, 2) | (5, 2) | yes | 0 |
| | lifted | (5, 2) | (5, 2) | (5, 2) | yes | 0 |
| | result cleared | (0, 2) | (0, 2) | (0, 2) | yes | 0.0139 |
| | counter cleared | (0, 0) | (0, 0) | (0, 0) | yes | 0.0139 |
| | reverse sweep | (0, 0) | (0, 0) | (0, 0) | yes | 0.0139 |
| partial_crank_release_and_resume (`test_partial_crank_release...`) | quarter turn | (6, 0) | (0, 0) | (0, 0) | **mid-stroke** | 0 |
| | completed | (9, 1) | (9, 1) | (9, 1) | yes | 0 |
| seated_carriage_does_not_clear (`test_seated_carriage_does_not_clear`) | five | (5, 1) | (5, 1) | (5, 1) | yes | 0 |
| | seated sweep | (5, 1) | (5, 1) | (5, 1) | yes | 0 |
| half_sweeps_reach_different_banks (`test_opposite_half_sweeps...`) | five | (5, 1) | (5, 1) | (5, 1) | yes | 0 |
| | counter half sweep | (5, 0) | (5, 0) | (5, 0) | yes | 0.0139 |
| | back to rest | (5, 0) | (5, 0) | (5, 0) | yes | 0.0139 |
| | result half sweep | (0, 0) | (0, 0) | (0, 0) | yes | 0.0139 |
| mid_stroke_selector_change (audit) | half stroke | (3, 1) | (0, 0) | (0, 0) | **mid-stroke** | 0 |
| | completed | (7, 1) | (7, 1) | (3, 1) with the selector lock | yes, open | 0 |
| mid_stroke_carriage_shift (audit) | shifted mid stroke | (9, 1) | (0, 0) | (0, 0) | **mid-stroke** | 1.0 |
| | completed | (9, 1) | **(90, 10)** | (9, 1) | **no, open; yes, locked** | 1.0 |
| mid_stroke_reversing_lever (audit) | lifted mid stroke | (4, 1) | (0, 0) | (0, 0) | **mid-stroke** | 4.98 |
| | completed | (99986420004, 975311) | (99999999996, 999999) | (4, 1) | **no** | 4.98 |
| mid_stroke_carriage_lift_and_sweep (audit) | cleared mid stroke | (0, 0) | (0, 0) | (0, 0) | yes | 1.01 |
| | completed | (0, 0) | (9, 1) | (9, 1) | **no** | 1.01 |
| crank_reversal (audit, `test_running_ratchet`) | nine | (9, 1) | (9, 1) | (9, 1) | yes | 0 |
| | reversed | (0, 0) | **(18, 2)** | (9, 1) | **no** | 2.0 |
| blocked_crank_lift (`test_crank_cannot_lift_past...`) | overlifted | (0, 0) | (0, 0) | (0, 0) | yes | 0 |
| | subtracted | (99999999999, 999999) | same | same | yes | 0 |
| between_detent_carriage (audit) | snapped detent | (10, 10) | (10, 10) | (10, 10) | yes | 0 |
| sweep_stopped_between_teeth (fold probe) | five | (5, 1) | (5, 1) | (5, 1) | yes | 0 |
| | rack between teeth | (8, 1) | (5, 1), held dial reads (8, 1) | (0, 1) | **no** | 2.5 |
| subtract_at_carriage_0 (audit) | subtracted | (99999999993, 999999) | same | same | yes | 0 |
| subtract_at_carriage_2 | subtracted | (99999999300, 999900) | same | same | yes | 0 |
| subtract_at_carriage_5 | subtracted | (99999300000, 900000) | same | same | yes | 0 |

**The pose result is as strong as the readout result.** At every read of every
scenario that stayed inside the machine's documented interlocks — mid-stroke
reads included — `dial_positions`, fed from the clocked state and the current
crank angle, reproduces the operating model's ACTUAL dial angles to
0.000000 digits, except after a clearing sweep, where the difference is
0.0139 digits: half a wheel degree, exactly the zero-capture band
`clearing_travel` prescribes and `test_running_clearing` asserts. A mid-stroke
read is therefore not a disagreement at all: the operating model is reading
moving dials, and the clocked model answers with the same moving dials from its
pose while its committed state has not moved yet. That is what "between events
nothing is retained" means, and it is measured here, not assumed.

## Question 2 — the interlocks

Every lock started open and one was closed only when a scenario demanded it.

| lock | demanded by | the manual's word |
| --- | --- | --- |
| **crank_ratchet** — the crank cannot turn back past the last seated ratchet tooth (357/116 degrees) | `crank_reversal`: with the lock open, `at = floor(crank / 360)` fires on the FALLING step and the note's additive law commits a SECOND addition, 9 → 18 | booklet p.4: "Turn the handle clockwise only – it is always locked against backward turns and any attempt to force the handle to turn backwards may damage the machine"; `Manual/Curta Build Manual.pdf` p.18: "The anti-reversal pawl spring should press the pawl against the teeth of the zero positioning disc and prevent counter-clockwise turns of the step drum" |
| **carriage_turn_needs_lift** — the carriage must be raised to rotate (and, equivalently here, **carriage_off_rest**) | `mid_stroke_carriage_shift`: with the lock open the clocked commit puts the whole operand at the shifted place, 90, where the operating model's dial kept the 9 it had already taken at place 0 | booklet p.5: "make sure the handle is in its zero stop position, raise the carriage straight upward, then turn it until the indicator arrow points to the required position and let the carriage snap down" |
| **crank_lift_off_rest** — the reversing/subtraction lift only at the zero stop | `mid_stroke_reversing_lever`: with the lock open, lifting at crank 180 degrees leaves the operating model's registers at 99986420004 / 975311, a number the machine cannot produce, and the clocked commit says -4 | booklet p.4: "In its zero stop position the handle can be pulled upward … for subtractive (minus) turns"; "The handle must always be brought into its zero stop position before manipulating any other parts of the machine" |
| **carriage_off_rest** — the carriage cannot be lifted off the crank's rest | `mid_stroke_carriage_lift_and_sweep`: with the lock open the operating model clears the dials mid-stroke and finishes at 0, the clocked commit at 9 | booklet p.4 (as above); trmm.net transcription: "the carriage cannot be lifted if the handle is not in its stop position" |
| **ring_off_rest** — the clearing ring cannot sweep off the crank's rest | same scenario | booklet p.4 (as above) |
| **ring_rest_checks** — the clearing lever comes to rest only at stop position A or B | `sweep_stopped_between_teeth`: a ring parked mid-rack leaves a dial between two teeth, which no committed integer digit can express | booklet p.8: "After clearing, the clearing lever must always be located in one of its two stop positions (A or B), otherwise the carriage will not snap down and the operating handle will remain locked" |
| **crank_lift_stroke** (0–9 mm) and **carriage_lift_travel** (0–6 mm) | `blocked_crank_lift`; both are already declared as joint ranges in `simulation/running_parts.py` and reproduced here so the harness stops where the machine does | the project's measured strokes |

Two locks the booklet documents and **no scenario demanded**, both of which move
the clocked model AWAY from the operating model, which has neither:

* **selectors_off_rest.** The booklet's "the handle must always be brought into
  its zero stop position before manipulating any other parts of the machine"
  covers the setting knobs. But `mid_stroke_selector_change` AGREES with the
  lock open — (7, 1) both sides — and DISAGREES with it closed. The note's
  point 5 says that "moving a selector at a crank phase of 180 degrees would
  retroactively move a tooth that had already passed". It does, in the pose,
  in BOTH models identically: `tooth_passage(angle, count, end)` reaches
  `count` before the stroke ends, so a changed count moves the dial at once,
  and `dial_positions` and `shaft_motion` are the same function of the same
  inputs. What the note infers from it — that the closed form is therefore
  wrong without the lock — does not hold for the REGISTER: a stroke's whole
  effect is the selector value at the stroke's END in both models, which is
  precisely what the commit reads at the crossing. Measured pose error at both
  reads of that scenario: 0.000000 digits.
* **crank_needs_seated_carriage.** "The handle cannot be operated when the
  carriage is not resting in a niche." `between_detent_carriage` puts the
  carriage at 12 degrees and turns the crank; the operating model's `aligned()`
  partitions every angle, so it snaps to detent 1 and answers (10, 10), and the
  clocked model's `floor(rotation / 20 + .5)` snaps the same way and agrees.
  Closing the lock would refuse the stroke and disagree. The Curta is a
  clocked machine here either way; which of the two is right is a question
  about the operating model, not about the clocked discipline.

**Is there an action the real Curta permits mid-stroke that the closed form
gets wrong?** On this corpus, no. Every mid-stroke action that breaks the
closed form — shifting the carriage, lifting the reversing lever, lifting the
carriage and sweeping the ring — is an action the manufacturer's booklet says
the machine mechanically forbids, and the one mid-stroke action that is merely
inadvisable rather than blocked (changing a selector) does not break it. The
one action the corpus found that the machine permits and the closed form gets
differently is not mid-stroke at all: it is parking the clearing ring between
its two checks, and the booklet forbids that rest too.

## Question 3 — does anything need a fold?

**No.** Per-digit comparison events cover partial clearing in both directions,
with no held value, over: the full forward sweep of both banks; a 180-degree
sweep that reaches the result bank and a -180-degree sweep that reaches the
counter bank (`half_sweeps_reach_different_banks`, the whole-machine form of
`test_opposite_half_sweeps_reach_different_registers`); a reversed sweep, which
does not un-clear a zeroed dial because a zero digit makes the event's
threshold its own standing position and the law commits zero again — the same
answer the operating model gets from its missing-tooth gate (ADR-121); and a
seated-carriage sweep, which clears nothing.

The note's point 4 worried that "reversing the ring un-clears the dials it
already zeroed". It does not, in either model, and no `max` over the sweep is
needed to prevent it.

What events alone cannot express is the READING of a dial the rack stopped
between two teeth. `sweep_stopped_between_teeth` parks the ring 2.5 pitches
into the result units rack with a 5 standing there: the operating model's dial
sits at 7.5 digits and `reading()` rounds it to 8; the clocked state is still
5, because no capture event has fired; the harness's held dial position, kept
only so this question could be answered, reads 8 and agrees. So a fold WOULD
close that last gap — and the machine forbids the state it closes. With
`ring_rest_checks` closed the sweep is carried to its check and the dial
clears, as it must.

The verdict for the proposal: leave the fold out, and declare the clearing
lever's two rest checks. If a later project wants to read a mechanism between
its detents, the fold is the shape that does it, and this is the evidence for
why the Curta does not need it.

## Speed

All figures on framework `81c5364`, Python 3.12 in the workspace venv, with
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`. Caveat: a `solid build` of another
project was running for part of the oracle recording, so the running figure
below is an upper bound; `running_probe --ticks 3` on a quiet machine
immediately before gave 0.698, 0.738 and 0.739 s per tick.

| measurement | command | seconds |
| --- | --- | --- |
| operating model, per 0.1 s tick | `clocked_spike record` (574 ticks, 439.2 s) | **0.765** |
| operating model, `Sim` construction | same | 5.4 |
| clocked pose: bind the fast Curta's eight drivers and read both ports, cold | `clocked_spike time` | **0.0306** |
| the same, warm (mean of 50) | | **0.0219** |
| one event commit through the fast model's ports (mean of 20) | | **0.0207** |
| one event commit through `calculate` (mean of 20) | | **0.000026** |
| fast Curta construction (`_build` caches warm) | | 1.8 |
| the whole 18-scenario corpus through the harness, registers only | `compare()` | 0.0103 total |

One clockwise revolution costs the operating model 20 ticks, 15.3 s. The same
revolution costs the clocked model one commit plus however many poses are
rendered: at the same 20 samples, 20 × 0.0219 + 0.000026 = **0.438 s**, a
factor of **35**. The commit is not the cost; the pose is, and the pose is the
fast Curta's existing per-pose cost, unchanged. The clocked discipline adds
26 microseconds per stroke.

## Disagreements, with their diagnosis

| read | diagnosis |
| --- | --- |
| five mid-stroke reads | Not stroke ends. At the two taken in scenarios that stayed inside the machine's interlocks the clocked model's POSE reproduces the operating model's dial angles to 0.000000 digits; the other three sit in scenarios that already diverge at their stroke end and their pose follows that divergence. Not a defect. |
| `mid_stroke_carriage_shift` completed | A missing interlock in the harness. Closing the carriage lock the booklet documents makes it agree. |
| `mid_stroke_reversing_lever` completed | The machine forbids the action; the operating model permits it and produces a number no Curta can show. The clocked model with the lock closed says (4, 1) — the lever could not move. The disagreement is the operating model's gap, and worth carrying into `simulation/running.py` as declared bounds. |
| `mid_stroke_carriage_lift_and_sweep` completed | The same: the booklet blocks both the lift and the sweep off the crank's rest. |
| `crank_reversal` reversed | The operating model has no anti-reversal pawl bound: `simulation/test_running_ratchet.py` is an OPEN RED diagnostic ("reverse operation is not yet accepted"), so it runs the passages backward and reads 0. The real machine cannot do either. Separately, this is where the note's spelling breaks: `at = floor(crank / 360)` fires on falling steps, and the additive law commits a second addition. |
| `sweep_stopped_between_teeth` | A rest the booklet forbids, and the only place the corpus found where a held value would be needed. See question 3. |

## What the framework proposal must therefore settle

1. **Direction on an event.** `at = floor(crank / 360)` fires on a falling step
   and the note's law neutralises nothing there: it adds a second revolution.
   Either `at` takes a direction, or a falling step is refused, or the
   declaration requires the bound that makes it unreachable. The Curta has the
   bound — the ratchet the note already sketches — but a proposal that leaves
   this to the project's bounds should say so explicitly.
2. **An event threshold may read the state.** The note's clearing sketch writes
   `ring >= RACK_END[3]`, a constant. The measured rack does not admit one: the
   sweep at which a dial reaches zero is `start_p + pitch_p * (10 - digit_p)`.
   The `at` expression must be allowed to read the state it commits, in the
   same way the `law` does, and its pre-event reading rule must cover both.
3. **The clocked pose must be fed by the state, and only by the state.** The
   whole speed result rests on it, and the measured evidence is here: the
   project's existing `dial_positions` reproduces the operating model's actual
   dial angles at every in-corpus pose to the width of its own capture band.
4. **A stop on a request path.** `blocked_crank_lift` and the ratchet both need
   a violated `Bound` to CLIP a request rather than reject a pose, with the
   events located on the clipped path. The harness does exactly that and
   records every clip; the note names this as the one thing the clocked mode
   borrows from the run.
5. **The interlock list is small, and it is the project's, not the
   framework's.** Eight locks, all expressible as `Bound(..., reads=...)` on
   joints (ADR-113); two more the booklet documents that this machine does not
   need. None of them required a new framework idea.
6. **No fold in the first cycle.** With the clearing lever's rest checks
   declared, per-digit comparison events cover partial clearing in both
   directions with no held value.
7. **The state is not a control.** Everything the corpus does, it does through
   physical inputs; `set_registers` exists only for session setup, which is
   what the note says `snapshot`/`restore` are for.

## What was not run

* No framework or viewer code was changed, built, or measured. No document
  version, no viewer execution, no browser figure: the spike is Python only.
* No geometry assertion, no interference test, no snapshot image. The harness
  needs no meshes, and the fast Curta was built only to time the pose and the
  commit through its ports.
* `simulation/test_running_markers.py` was not replayed (arithmetic-free).
* The build manual's cascading-carry test — set every dial to 9 by hand, add 1,
  watch them all return to zero — needs dials settable by hand, which neither
  model exposes as an input. `subtraction_borrow_and_undo` exercises the same
  cascade through both full banks by borrowing from zero instead.
* Only three of the six carriage positions were swept for subtraction (0, 2, 5),
  to bound the oracle's cost; the shift enters both models through the same
  `decimal_shift` / `aligned` pair, and all three agreed exactly.
* Arithmetic on a fractional dial was deliberately not exercised. A dial the
  rack left between teeth pre-trips its carry lever in `lever_motion`
  (`PIN_DROP` at 9.3), and the clocked commit has no way to express that. The
  clearing-lever rest checks forbid the state; if a later change admits it,
  this is the first thing to test.
* `Interlocks.selectors_off_rest` and `crank_needs_seated_carriage` are
  implemented but left open, because no scenario demanded them; the effect of
  closing them is measured above, not assumed.
