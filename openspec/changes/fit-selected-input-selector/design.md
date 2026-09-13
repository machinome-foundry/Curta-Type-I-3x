## Context

This is the next Curta-owned prerequisite after the completed two-station
carry/frame fit, not the running-engine implementation. Preparation scope was
approved on 2026-09-13; the pilot then ratified this complete design
("ratify, go on"). No implementation task was complete at ratification.
The pilot retains the explicit solid-node feature-start gate.

Working branch/worktree: `open-run-simulation` in this project. Planning
starts at `dd981041ff41108727abc9ae02db0c291d0126cd`. The framework bench is
`solid-node/WTs/open-run-simulation` at `6e41f2da132a8604f9b68895967247fb8876fc4d`.
Neither primary checkout is an editing target. This is not sprint work.

Read [the project evidence](../../../simulation/docs/open-run-selector-evidence-2026-09-13.md)
and its retained JSON for all nine pair names, volumes, source hashes and
inspected sections. Eight native intersections occur at all ten seated
settings; the shaft/screw pair adds a ninth at the half-detents. The source
ball is 5.4 mm, while manual page 32 specifies 5 mm and installed spring
compression. Page 33 shows the ones input's lower gear between the knob fingers.
The source shaft join overlaps axially by 0.025 mm. Those facts have not
already established a corrected assembly or a continuous safe path.

The existing public project model is prescribed: `Selectors.operand` selects
the digits, `Selector1.setting` moves the first knob and shafts, and the
result transmission slides its keyed input group. Re-evaluating the complete
root operand also reconstructs carry state. The readiness fixture must remain
independent of that law; it is not a new public operating control.

## Goals / Non-Goals

**Goals:** support all ten selected detents and continuous travel in both
directions; preserve numbering, keyed-input/follower capture and stationary
output/carry state; retain source-derived geometry with local, measured fits;
classify only the two named fixed joints; prove installed clearance without
discarding neighbours or treating a sample grid as a continuous proof.

**Non-Goals:** repair all eight selectors, remodel unrelated covers/threads,
change carry timing or the completed frame fit, predict force/friction/rate,
qualify a print, select a finite-time snap model, expose running controls,
implement the causal mechanism, establish the full angular home window, or
close whole-machine setup/outgoing-carry obligations. No dependencies are added.

## Decisions

### 1. Modify occurrences, not shared source products

The selected selector is
`Curta.input_selectors.selectors.digit_selector_axle_1`; its keyed gear is
`Curta.transmission.result.ones.p_10219_410002_1`. The housing target is
`Curta.enclosure.lower_housing_1.bottom_housing`.

Use dedicated adapters in `simulation/` and explicit selected-occurrence
wiring, not edits to shared `standard/` imports. `Selector2` through
`Selector8`, their hardware and their source poses remain unchanged. Keep the
unmodified source assembly available as the placement reference. If a spring
representation changes its leaf structure, record an explicit source-to-body
mapping; every physical body from the 428-body inventory must still be accounted
for, not discarded to preserve a convenient count.

Preserve the ones selector's source axis `(58.5, 0, Z)`, the keyed shaft axis
`(40.5, 0, Z)`, the -Z knob/input stroke of 54 mm and the ten seated settings
6 mm / 36 degrees apart. Preserve the existing source placement transforms,
including their different top/bottom axial offsets. Between-detent shaft
phase may follow the measured groove instead of the old straight interpolation;
it must meet those seated coordinates without changing the numbering.

Alternative rejected: re-clock the entire bank or housing to fix a local
edge, which risks every other selector and support.

### 2. Use the documented ball and model its installed spring

Use the ratified nominal **5.0 mm sphere for this occurrence only**, preserving
hardware attribution. Derive its guide axis, seated center and cam-following
displacement from the actual knob, shaft and spring seats. Size alone is not
acceptance: prove guide retention, ten supported detents and the complete
between-detent travel. Failure of that nominal hardware to seat within the
protected geometry returns the diameter/interface decision to the pilot.

Replace this rigid imported spring's operating representation with a
source/manual-grounded analytic flexible spring using the already available
Molejo integration. Measure and record wire diameter, winding count/hand,
coil geometry, end forms and both installed seats before authoring it. Keep
those source/manual dimensions, except for the measured installed compression
and seating needed to represent the assembled spring. The ball drives its
moving end; the knob retains its back end. Do not uniformly scale a coil,
shrink its wire or park the ball to make clearance tests pass.

This remains ideal quasi-static geometry. A held knob has a supported ball
position; each numbered detent has geometric retention. Any selected
same-instant settlement branch must have its entire transition checked, not
just its endpoints. No spring rate, force margin, snap duration or frictional
hold is inferred. If a supported path requires a different fidelity, stop.

Alternative rejected: leave the rigid source spring/ball interpenetrating
and label their moving contacts as fixed assembly seats.

### 3. Preserve transmission while fitting only non-protected regions

First locate the helical groove and follower tip, knob fork and captured lower
gear independently of a proposed cutter. Measure relative play/contact in
both directions at the ten detents, intervening extrema and segment boundaries.
Use the existing independent perturbations as red witnesses, not as preset
allowances: ±1 degree shaft offsets meet the screw; opposite axial gear shifts
meet opposite fork faces. Fit/contact proof must still detect disconnection.

The allowed source-derived rigid fitting surfaces are **only** the selected
knob's ball-guide wall, the screw's non-threaded follower tip if necessary,
and the housing's local selector-slot/number-window edges. Prefer correct
installed positioning and the measured follower path before removing material.
Do not alter the shaft's detent/groove working surfaces, screw threads, spring
back seat, knob fork fingers, input gear or its keying, bearings or supports.

Before any production cut, map the complete proposed removal region and
nearby support/fastening features independently. Fix each cutter in the part's
own frame; it must not chase the current pose. Record actual removal dimensions,
remaining lands/walls and resulting clearance or working play. There is no
automatic inherited 0.05 mm frame-gap requirement: each interface's numerical
fit must be measured and documented before use. Measurement choices within
these protected bounds are routine; a need to cross them is a stop condition.

Free-running surfaces need a positive, defensible clearance bound. Working
contacts instead need a non-penetrating supported contact envelope and bounded
play; opening a universal gap around them would disconnect the mechanism.
No interference epsilon substitutes for either proof.

Alternative rejected: machine a full swept void around the selector, which
would remove the very guide/follower/capture interfaces under test.

### 4. Allow only two explicit, unchanged fixed-seat candidates

The ratified local inventory can contain only:

| Pair within the selected selector | Source finding | Required classification proof |
| --- | --- | --- |
| `digit_selector_screw` / `selector_knob` | 13.141988148 mm³ overlap; manual M4 tap/die joint | Constant relative pose, retained thread/retention region, no contact region reaching the moving follower interface |
| Bottom / top selector shaft | 0.025 mm axial overlap, about 0.533679777 mm³ | Constant relative pose and unchanged supported source joint; not a moving axial obstruction |

Record exact occurrence identities, canonical relative transforms, measured
intersection region/volume and the source references. Compare in that canonical
frame rather than interpreting floating-point variation after world rotation
as physical motion. New, removed or changed inventory contacts fail; a broad
maximum volume is not an acceptable inventory. No ball, spring, shaft/screw
follower, gear/fork or housing interface is eligible.

This explicitly classifies existing source fits; it does not certify thread
engagement strength or interference-fit manufacturing. If either pair fails
the fixed-joint/support proof, return that specific interface to the pilot.
Do not move its parts or silently extend the inventory. Preserve the old
whole-root integrity findings and tests; this is a selected-input inventory,
not a replacement whole-machine waiver table.

### 5. Validate the fitted path in independently frozen home fixtures

Retain the initial `099`, operand-one, zero-turn fixture and the post-cascade
`100`, one-turn fixture. In the second fixture carry fractions remain exactly
`[0, 1]`; in the first they retain the measured preloads. Hold all root drivers,
output shaft/dial coordinates, other selector settings, drum and carry geometry
fixed while evaluating the independently moved selected input. Check both 0→9
and 9→0. This proves the fixture does not manufacture a reset, not that the
future runtime already implements persistence.

The old eight rigid transforms are a red baseline, not the fitted ball/spring
law. Adapt the diagnostic explicitly to the new flexible/relative movements;
verify source-frame bindings and invariants independently, and enumerate every
installed neighbour, including covers, supports and source-mesh exceptions.
Physical input motion must retain its unchanged keyed-shaft rotation at each
fixture and must not back-drive the drum or any output there.

Use dense/adaptive native and faceted checks for localization and regression,
including every measured extremum and branch boundary. For unsampled intervals,
use conservative swept enclosures or analytic/interval bounds containing the
actual rigid and flexible paths, with independently bounded approximation
error. Prove free-space exclusion against all possible neighbours and supported
contact/play separately. A sample grid, interpolation residual at its training
points or a copy of the fitting cutter is not a continuous certificate. If
that proof cannot be completed, leave the affected acceptance item open.

Negative controls must catch at least: source oversized ball; frozen spring or
ball follower; reversed/missing keyed travel; wrong shaft axis/phase; disconnected
gear/fork or screw/groove; ineffective housing relief; damage outside permitted
regions; and an early release of the second carry in the diagnostic fixture.

### 6. Preserve the old product while preparing the future one

After focused tests pass, wire the adapters only into the selected operating
occurrences. Preserve the root's existing calculator controls, instructions,
reproducibility and non-selected geometry. Do not advertise that old root as
history-dependent or use its arithmetic as the new clearance oracle.

Rerun all 39 previously recorded node modules plus every new/affected module,
in both kernels. The old frame baseline is 159/161 faceted and 160/161 native;
its named bearing-facet and housing/thread findings must remain explicit.
New tests must pass and no unexplained regression is accepted. Rerun the
lightweight Python and calculator JavaScript tests, build the complete root,
inspect its actual publication and capture OpenSCAD views at seated and
between-detent poses. Keep source/fit sections and an assembled context view;
restore the complete root publication after any inspection-only build.

## Risks / Trade-offs

- Nominal ball or source spring dimensions may disagree with the installed
  guide → measure before replacement; return conflicts with protected geometry
  or hardware/fidelity choices instead of improvising new dimensions.
- Tiny shaft/screw overlap may expose a profile or phase error → investigate
  native working surfaces and both-direction capture; do not waive its volume.
- Local housing cuts may reach threads or guide/support lands → independent
  protection map and source-difference checks gate every cut.
- Dense tests can miss an intermediate obstruction → continuous enclosures
  and approximation bounds are required in addition to snapshots/samples.
- Exact moving contact is numerically delicate → distinguish kernel failure,
  actual overlap and bounded contact; retain both kernels and negative witnesses.
- CAD work can consume large resources → run heavy jobs sequentially with an
  8 GiB address-space cap, numerical thread counts one and bounded timeouts;
  retain process wall time, maximum RSS, commands and source fingerprints.

## Migration Plan

After full plan ratification, validate and commit the planning-only record
before implementation. Establish red contracts, measure/protect the source
interfaces, prove the installed detent and then local housing/follower fits,
and only then wire selected occurrences and run the full acceptance matrix.
If a trial fails, retain its evidence and keep the previous operating wiring;
do not merge partial fits into the primary checkout.

Completion includes synced accepted specs, archive, validation records and a
focused implementation commit in this project. No integration, push or worktree
cleanup is implied. The original `simulate-the-curta` stays separately active.
Then resume home-window/setup/outgoing-boundary evidence and coordinated running
proposals; ask the pilot before actual solid-node feature development.

## Open Questions

The pilot ratified the 5 mm hardware choice, installed quasi-static
spring/ball representation, two fixed-seat candidates and bounded fitting
authority above. Their adequacy is still to be measured, not assumed.

Routine implementation must determine spring dimensions/seating, actual follower
path and play, fixed-seat regions, permitted-removal coordinates, numerical fit
values and complete continuous-path bounds. Any need for a different ball size,
changed shaft detents/groove, thread/support/fork modification, another station,
a broader inventory or different fidelity requires a specific revised proposal.
