# Open-run Curta: first acceptance slice

**Current disposition, 2026-09-13:** paused by the pilot to steer project
direction. This document preserves the ratified scope and unfinished acceptance
obligations; it is not an instruction to continue the previous roadmap.
The [checkpoint handoff](open-run-handoff-2026-09-13.md) is the latest project
status. Neither the selected-input fit nor the running slice is delivered.

Status: first acceptance scope and initial fidelity ratified by the pilot,
2026-09-12; evidence audit and remaining detailed operating choices are still
open. This is a scoped planning decision, not ratification of a complete
OpenSpec cycle, a new working simulation or a claim that the existing
simulation is complete. No CAD sweeps, profile reproduction or simulation
tests were rerun for the initial audit or its subsequent ratification. The
later [evidence pass](open-run-evidence-2026-09-12.md) recovers the raw logs,
reproduces the profiles and reports fresh bounded mechanical checks; the
remaining geometric gate is still open.

Project base: `60979adbc795785fc51a28a386f85d1a49bfedf7`, branch/worktree
`open-run-simulation`. The coordinated roadmap belongs to solid-node at
`workflow/open-run-simulation/roadmap.md` on its same-name branch. Framework
and viewer have separate implementation cycles; this document and the actual
Curta geometry/acceptance belong to this project. Release 0.7 versus 0.8 is
still the pilot's later choice.

## Ratified scope and first observable result

Build a **quasi-static, forward-addition subassembly**: one physical selector,
the ones/tens/hundreds result transmissions and wheels, and the two intervening
carry stages. Start with one transmission, then one carry, then both carries.
Use fitted source parts and their actual joint frames, not the spike's
schematic wheels. Accept the selected input's full 0–9 travel before calling
the slice complete; zero/one is only bring-up.

The headline run starts from an explicitly initialized `099`, selects one,
and turns the crank. The visible wheels reach `100` through two successive
carry contacts. Stop at one revolution, preserve the second carry's still
latched state, and continue through its reset in the following revolution.
No calculator result, completed-turn count, or page Commit operation supplies
the wheel positions or decides a carry.

This is a test subassembly, not a complete Curta with its omitted mechanisms
silently frozen. Full-bank overflow, the turns counter, subtraction, carriage
movement and physical clearing are later increments.

The pilot ratified the one-input/three-wheel/two-carry scope, addition with a
fixed carriage, the mechanical `099 + 1 -> 100` result, pause/resume mid-carry
and retained carry state across revolutions. Selector changes are admitted
only while the crank is stopped in a verified home window. The initial
fidelity is ideal, quasi-static detent settlement with checked transition
clearance. Operations beyond this slice are explicitly refused, including
the outgoing carry boundary described below.

This approval settles those choices, not the truth of unverified measurements
or every additional recommendation in this audit. The exact home window,
admissible complete `099` setup, snap-path clearance, profile reproduction and
swept-neighbour inventory remain evidence obligations. Additional setup
presets, detailed command recovery rules and operating/resource budgets still
need proposal review. The coordinated proposal sequence is approved; complete
cycle ratification remains a separate gate before implementation.

## Actual parts and connections

Paths in the table are relative to `simulation/`. Names identify existing
classes/attributes to extract or rebind; reusing a class with its current
prescribed drives intact would not constitute the migration.

| Function | Selected source-backed components | Connection to establish |
| --- | --- | --- |
| Physical input | `selectors.py:Selector1`, including `selector_knob_1_419057`, bottom/top selector shafts; ones input group `p_10219_410002_1` in `standard/channels.py:ResultOnes` | Knob travel 0–54 mm along −Z, 6 mm per digit; existing selector-shaft rotation is 36° per digit. The keyed input group follows axial setting independently of its transmission rotation. Verify the intervening contact/guide, not just equal numerical targets. |
| Crank and tooth source | `mechanism.py:MainDrive`, `SteppedDrum`, `TensBellAssembly`; fitted printed drum and bell | Crank, drum and bell retain their common physical phase. In the existing model their +Z rotation is −360° per forward revolution. Subtraction lift stays at its addition position. |
| Ones transmission | `standard/channels.py:ResultOnes`; shaft `p_10208_1`, fitted input pinion, bevel tip and stationary axial stack parts | Selected drum-row contact advances the keyed shaft; its bevel moves the ones dial. Tooth disengagement does not reset either angle. |
| Tens/hundreds transmissions | `ResultTens` and `ResultHundreds`; shafts `p_10207_1_419228` / `p_10207_1_419087`; carry groups `p_10220_410003_1_419227` / `p_10220_410003_1_419086` | Two separately retained shaft angles; each carry sleeve slides on its shaft and admits its bell tooth only in the engaged position. Direct input rows for these stations stay at zero. |
| Three result wheels | `registers.py:ResultRegister.p_10203_1`, `.p_10203_2`, `.p_10205_1`, with fitted dial bodies and installed half pins from `dial_fits.py` / `pin_mounts.py` | Each fitted bevel pair transmits 72° shaft travel per 36° digit pitch. The first two pins trip the two selected carry sliders. Preserve source-specific radial axes and pin orientation. |
| Two carry stages | `standard/carry.py:ResultsLever1` / `ResultsLever2`; fitted `tens_slider_for_results`, `ResultsSpringSeat`, `MountedCarrySpring` | Pin → slider approach → retained detent → sleeve engagement → bell-driven next shaft; later bell-cam contact resets the slider. Each slider's full engagement stroke is 4.2 mm. |
| Dial retention | `register_detents.py:RegisterDetents`: balls `p_6mm_ball_419241_12`, `_1`, `_13`; `FlexibleSpider.result_1`, `_2`, `_3` | Ball/cam travel and spring-finger deformation follow each actual dial, with supported retention between tooth passages. Retain the common mounting ring and required seats. |
| Crank retention and support | `zero.py:ZeroPositioning`, `pawl.py:AntiReversal`, their documented springs, fitted bearing plates; relevant frame, carrier, guide and cover surfaces | Preserve the zero-cam/follower and ratchet contact paths. Forward-only UI admission is not itself proof that the pawl mechanically blocks reverse travel. |

Frame bookkeeping is an acceptance item. `fit.py` records a carriage recenter
of `(0.537721035, -0.038177283, 0)` and clocking `0.549916905°`, a
`−0.079764273 mm` tens-shaft X correction, input clocking `4°` and bevel
clocking `−3°`. `registers.py` also accounts for the clearing gear's absolute
zero. Carry stage 1 uses travel `4.2 × engage − 4.2`; stage 2 uses
`4.2 × engage`, both along their declared −Z axis. These source offsets are
not interchangeable zeros. Logical wheel advance must be bound explicitly
to each signed joint coordinate and static transform.

### Boundary closure still to prove

Keep the carriage seated at position zero, subtraction lift zero and clearing
at rest. Keep the two nonselected input rows at zero. These are fixture
conditions, not new claims about the machine's physical interlocks.

The component map above is a code/source inventory, not yet an exhaustive
swept-neighbour inventory. Before implementation, enumerate the moving bodies'
guides, bearings, spring seats, covers and adjacent obstacles against the
fitted assembled source. Record each as retained, independently clear of the
sweep, or an explicit subassembly cut. Hiding a body does not remove it from
contact validation. A body still driven by the common drum cannot simply be
parked: retain its necessary motion or explicitly cut that subsystem out of
the rig. In particular, do not represent the omitted turns counter as an
intact locked counter that the drum can rotate through.

The hundreds wheel has an outgoing carry interface. The two-carry slice does
not prove what happens beyond it. Accepted sequences must stay short of that
unmodelled interface's activation; an interactive run reaching the boundary
must stop with an explicit fixture-scope diagnostic, not wrap to `000`, lose
a carry, or claim full-machine overflow. Locate the boundary from the actual
pin/contact phase, not a calculator algorithm. Completing the result bank
removes this temporary acceptance boundary in a later increment.

## Mechanical state and event map

The run owns the crank phase/winding, physical selector travel, three shaft
and wheel angles, two slider positions and their local retained detent state.
It also owns any pawl/retention state required by the accepted contact laws.
Follower positions and flexible shapes may be evaluated from that committed
mechanical state where the laws make them dependent; they are not an
independent calculator state machine. Rendering never advances the run.

The spike supplies useful candidate event locations, not production geometry
certification. Its measured-profile inputs came from this same project commit:

| Cause | Candidate location in the reduced rig | Consequence |
| --- | --- | --- |
| Selected one-tooth passage | Forward crank 113.5–124.75° | Ones shaft advances 72°, wheel advances one 36° digit pitch. |
| Approaching dial pin passes carry detent crest | Logical driving wheel approximately 335.393407° modulo 360° | Retain that adjacent slider's lower detent; no output wheel increment is assigned by the event. |
| First/second carry tooth passages | Crank 146.375–157.625° / 166.375–177.625° | Advance the next shaft only when its sleeve is engaged. The second trip is caused by the tens wheel's resulting motion. |
| Reset cam releases first/second detent | Crank approximately 355.016° / 375.016° | Release each retained carry separately; the second crosses a revolution boundary. |

The trip threshold is `0.61 × 4.2 = 2.562 mm`, using the measured U-wire
spreading crest. The spike chooses `1.85 mm` reset lift; the current prescribed
reset law blends its snap between 1.65 and 1.85 mm. These are assumptions to
revalidate together with the moving geometry, not universal detent constants.
`PIN_DROP` is an envelope of fitted half/full-pin approaches with a 0.05 mm
gauge allowance; compression targets 0.001 mm error at the input samples.
That allowance is not a solver tolerance or permission for overlap.

The existing all-row law suggests input-train windows ending at 124.75° and
extending earlier by 11.25° per tooth. Compile each physical row's measured
tooth engagement, including entry/exit and selector-height compatibility;
do not promote this prescribed formula to proof of all nine rows. No new
nonlinear solving class should be assumed until these actual laws are mapped.

## Operating decisions: ratified choices and remaining recommendations

Items 1 and 2 state the approved ideal-detent and pause/persistence semantics.
Item 3's stationary-home selector restriction and refusal of operations beyond
the slice are approved; its detailed admission rules still need specification
and evidence. Items 4–6 remain recommendations for the coordinated proposals,
except that the headline `099` initialization is part of the ratified scope.

1. **Quasi-static ideal detents first.** Retain the measured approach/reset
   paths and model a spring snap as same-instant settlement between stable
   branches. Prove clearance along the slider and flexible-part transition
   path, not only its endpoints. Do not interpolate a cosmetic transition
   through obstacles or invent a spring rate. This does not prove force,
   friction, speed limits or impact behaviour. Finite-time spring motion is
   a different fidelity choice and must be explicitly scoped if desired.
2. **Pause means preserve.** Before the trip, a stopped crank holds its
   supported partial-contact pose. At a trip, finish same-instant settlement;
   then pause at the committed branch. There is no selectable intermediate
   instant inside an ideal instantaneous snap. Mid-tooth and mid-reset
   checkpoints retain all coordinates, local memory and pending command
   progress. Restart never reconstructs them from completed revolutions.
3. **Physical input, conservative admission.** Allow selector movement only
   with the crank stationary at its verified home window; allow cranking only
   at a seated selector detent. The selector still traverses its real travel,
   including between-detent poses. Start with forward crank commands only;
   reject reverse, subtraction, carriage movement and clearing by name.
   These command restrictions are declared scope, not invented physical stops.
4. **Explicit setups, not output controls.** Provide validated `000`, `009`
   and `099` setups with consistent shaft clocking, sleeve positions and
   supported detent state. Validate each setup geometrically before use.
   Reset restores a whole setup snapshot; it is not physical clearing.
   Checkpoint restore is distinct and preserves partially completed motion.
5. **Blocking must be observable.** Admit movement only to the first blocking
   contact or declared rig boundary, report the requested/admitted remainder,
   and stop that command. Keep the blocked remainder available for inspection
   but do not automatically restart it. A fresh command or explicit resumption
   must validate the current state. Incompatible simultaneous requests fail
   transactionally, including command progress, not just wheel coordinates.
6. **Use a modest test operating rate.** Start demonstrations at one crank
   revolution per six simulated seconds (the existing Turn crank instruction's
   duration), with slower/faster runs proving rate-independent quasi-static
   outcomes. This is a test setting, not a physical or performance rating.
   Fix numerical error and responsiveness/resource budgets in the package
   proposals after a measured slice baseline; the synthetic 240 Hz spike is
   not a promise for this model.

The principal scope/fidelity choices and outgoing-boundary policy are now
ratified. The exact home window, snap-path clearance and supported setup
states still need geometric evidence before the mechanical evidence gate
closes. In particular, scope ratification does not certify the candidate
thresholds, profile samples or source-frame bindings above.

## Evidence to reuse, and what it does not prove

The latest recorded run is [resumption validation](resumption-validation-2026-09-11.md),
against framework `5e591474b5cf…`, not a new run against the current framework
bench. It reports 142/144 faceted and 143/144 native checks across 37 modules.
The common housing/thread overlap and additional faceted bearing disagreement
remain open. The current audit changes no waivers or test expectations.

| Existing evidence | Reusable part | New running acceptance needed |
| --- | --- | --- |
| `test_selectors.py`, `test_transmission.py` | Source-frame 6 mm selector travel, keyed sliding and 72° shaft placement checks | Physical connection and between-detent admission; no decimal operand controls driving the mechanism. |
| `test_input_mesh.py`, `test_engagement.py` | Fitted tooth passage, flank perturbation tests and all-row prescribed clearance samples | The compiled contact laws produce every tested pose, and preserve disengaged state. All-row clearance alone does not prove transmitted motion. |
| `test_bevel.py`, `test_bevel_bank.py` | Fitted source axes, phase and independently perturbed flank engagement | Apply to the three runtime-produced shaft/wheel states, including interruption. |
| `test_carry_contact.py`, `test_carry_mesh.py`, `test_carry_bank.py` | Pin, fork, bell/reset contacts; installed half-pin orientation; neighbouring pin sweeps | Two causally tripped stages and persisted reset, without `enabled`, calculated carries or prescribed register values determining them. |
| `test_carry.py`, `test_dial_detents.py`, `test_dial_detent_bank.py`, `test_spider_bank.py` | Measured slider/spring paths, ball and spider seats, sampled clearances | Stable-branch retention and entire ideal-snap paths under actual running events; these tests do not establish spring forces. |
| `test_zero.py`, `test_pawl.py` | Crank follower, spring mounting and directional contact evidence | Home-window admission and any retained pawl constraint driven from committed state. |
| Arithmetic, calibration and demo tests | Independent expected displayed answers and useful operations | Observe the answer from wheel geometry/state; never feed the oracle back into the mechanism. Full page-53 calibration remains beyond this slice. |

The dependency to remove is explicit in `curta.py` (`arithmetic.calculate`),
`registers.py` (`dial_positions`), `transmission.py` (`dial_positions`,
`added_digits`, `carries`) and `carry_motion.py` (reconstructed previous carry).
The existing `CarryContactBench` also prescribes register values and engagement;
it is a reusable geometry test arrangement, not an already causal root.

### Reproducibility finding

During this audit, SHA-256 checks of `carry_profiles.py`, `carry_motion.py`,
`cycle.py` and `selectors.py` match the framework spike's
`evidence/provenance.json`. The profile file hash is
`b047f5f8f219e549485a3dfc6b8b6fed601573c36fae80c95d5caec8a097ff86`.

At the initial audit the fresh worktree had **no `_build_evidence/` directory**.
The three raw inputs
named by `tools/compile_carry_motion.py` — `carry-half-trigger-assembled.jsonl`,
`carry-full-trigger-final-tip.jsonl`, `carry-reset-profile.jsonl` — are ignored
historical artifacts, not tracked evidence originally carried by this checkout.

**Resolved for profile reproduction, 2026-09-12:** all three full-log hashes
and all six recorded source hashes match the spike provenance. The verified
logs were recovered from the unchanged primary checkout into this worktree;
compact measurement records and hashes are now project-owned under
`simulation/docs/evidence/open-run-profiles/`. Both input forms reproduce
`carry_profiles.py` byte for byte. See the [evidence pass](open-run-evidence-2026-09-12.md)
for the fresh error checks and scoped exact/faceted geometry results. This
closes the missing-input gap, not continuous-contact, snap-path, home-window
or full initial-setup acceptance.

## Acceptance sequence and negative controls

Run each sequence through the real Python producer and the viewer executing
that same published program, with inspected actual-part captures:

1. `000`, input zero: successive crank turns leave all three wheels unchanged.
   Inputs 1–9: a complete turn gives the corresponding ones-wheel advance;
   repeat without resetting, within the rig's outgoing boundary.
2. `009`, input one: the ones wheel trips exactly one carry into tens.
   `099`, input one: two successive carries produce `100`.
3. For the cascade, stop inside input contact, between the two carry stages,
   during reset approach, and at 360°. Checkpoint/replay must preserve the
   same mechanical state and event sequence. Continue through the second
   reset beyond 360°; no fresh arithmetic operation or reset is needed.
4. At a validated stationary home position, select zero after the cascade,
   preserving any pending carry reset. Further crank movement resets it
   without adding a digit. Refuse selector movement away from the admitted
   window and cranking between selector detents without moving outputs.
5. Exercise a blocked command, a conflicting command pair, explicit recovery,
   whole-run reset, checkpoint restore and the outgoing-slice diagnostic.
   Rendering and extra snapshots alone change nothing.
6. Repeat with coarse/fine numerical steps and different display cadences.
   Compare exact discrete state/events and tolerance-bounded coordinates and
   admitted progress. Measure real export size, build/step cost and retained
   memory without history recording; keep those results separate from CAD
   sampling resolution and geometric uncertainty.

Red-first mutations must remove an input contact, reverse a bevel relation,
disconnect a carry fork, suppress a pin trip, reset a latch early, erase the
second latch at the turn boundary, and corrupt a joint-frame binding. Name
which motion or independent geometric assertion detects each fault. Restore
and rerun after each mutation; endpoint arithmetic alone is not sufficient.

## Relationship to the existing OpenSpec change

`simulate-the-curta` remains active and unarchived, with 7/17 tasks complete at
this base. Its proposal explicitly promises prescribed kinematics with
arithmetic state. This new running rig must not silently rewrite that promise
or mark its remaining work complete.

The new project cycle should explicitly distinguish running physical controls,
history-dependent carry and checkpoint/replay from the old reproducible
starting-register/pose controls. Preserve the old path while it remains
supported, or ratify its replacement separately. Retain the existing assembly
requirements, source attribution, unresolved housing/frame findings and
full-machine calibration/overflow/clearing tasks in the original record.
Completing this slice closes none of those whole-machine tasks by implication.

The subsequent installed diagnostic finds native spring/frame and
slider/frame intersections at both selected trip/reset stations; see the
[evidence report](open-run-evidence-2026-09-12.md#installed-tripreset-transitions-native-counterexamples).
The frame was outside the earlier isolated carry and selected `099` checks.
No interface or geometry correction is implied by recording that finding.

**Follow-up, 2026-09-13:** source/manual comparison and the complete
[clear-result-carry-frame-contacts proposal](../../openspec/changes/archive/2026-09-13-clear-result-carry-frame-contacts/proposal.md)
are now recorded. The proposed correction is frame-only and limited to these
two stations. The pilot subsequently ratified it on 2026-09-13 ("ratify,
go on"), retaining its protected-feature stop conditions. The running cycles
are not thereby ratified.

The original plan is committed as `7d39306`; six native red tests reproduced
the contacts and three guards passed. The requested gap reached guide-seat
edges, triggering the [measured gate](carry-frame-gate-2026-09-13.md). The pilot
approved its bounded exception; revision `9c58255` records that approval.
The two-station frame fit now meets its focused acceptance: all 17 new
contracts pass both runners, with continuous slider/spring/sleeve frame
enclosures, four installed transition sweeps, dimensional/protected-feature
measurements, twelve negative controls and inspected native/OpenSCAD views.
Full regression is 159/161 faceted and 160/161 native, with only the named
pre-existing failures. See the [completed validation](carry-frame-validation-2026-09-13.md).

The verified correction is committed as `3afcac97a808aebf9d7019d6e43a6dc3086fea62`.
Integration remains pending. Readiness work has resumed with the selected-input
source-frame inventory and a pure-law counterexample: even with completed
result `100` held fixed at one turn, the old operand law changes the second
carry from latched to released when input changes from one to zero. The next
geometry probe must independently freeze that retained state, as detailed in
the completion record; it cannot use the old calculator control as evidence.

**Selected-input evidence, 2026-09-13:** independent native-copy sweeps now
hold the initial and post-cascade home states unchanged, including the latter's
still-latched second carry. Both fixtures show eight intersecting pairs at the
ten seated settings and nine with half-detents included. Housing-slot/window
and installed ball/spring/follower findings are separate from the completed
frame fit. See the [selector evidence and bounded next-step recommendation](open-run-selector-evidence-2026-09-13.md).
No selector geometry or running code is changed. The pilot subsequently
approved preparing the bounded selector correction; its complete
[fit-selected-input-selector plan](../../openspec/changes/fit-selected-input-selector/proposal.md)
now passes strict validation. The pilot ratified its complete fit/fidelity
choices on 2026-09-13 ("ratify, go on"); planning commit `aec7ca4`.
All 22 implementation tasks were open at ratification. Task 1.1 is now complete;
the [implementation evidence](selector-fit-implementation-2026-09-13.md)
records the independent native red tests and a subsequent source detent/guide
indexing conflict. The pilot ratified its bounded guide/back-seat alignment and
local fill-and-rebore revision, committed separately as `da432fb`. Measurements
resumed: two tasks are complete (red baseline and fixed-seat classification).
Native endpoint/local support witnesses support further trials, but no production
fit, full working-play retention or continuous travel is yet proved. These
remaining gates keep running readiness open.

The pilot subsequently requested a documented commit and pause to steer the
project direction. The latest retained measurements and 23-test result are in
implementation evidence §§6–7. Spring seating, full working-play/capture and
protected-geometry gates remain open, followed by any eventual fitted-part and
installed-travel acceptance. Home-window, continuous-neighbour, initial-setup
and outgoing-boundary obligations likewise remain unresolved; raw-data
reproduction is already verified. This checkpoint does not choose which work
to pursue next, abandon the recorded scope, or complete either active change.
Only the scoped Curta frame fit is implemented and verified in this readiness
campaign; framework and viewer feature code remain unchanged. Await the
pilot's project direction and retain the separate explicit go-ahead before
solid-node feature development.
