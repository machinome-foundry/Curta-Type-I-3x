## Context

This is the next Curta-owned prerequisite after the completed two-station
carry/frame fit, not the running-engine implementation. Preparation scope was
approved on 2026-09-13; the pilot then ratified the original design
("ratify, go on"), planning commit `aec7ca4`. Task 1.1 is now complete;
measurements paused implementation at the detent/guide alignment conflict.
The pilot approved revising the plan ("yes, go on"), then ratified this
alignment revision ("ratify, go o") on 2026-09-13, including its explicit local
reconstruction exception. Record it separately before resuming implementation;
ratification has not changed operating geometry or proved the fit. The pilot
retains the explicit solid-node feature-start gate.

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

The later [implementation record](../../../simulation/docs/selector-fit-implementation-2026-09-13.md)
and `simulation/docs/evidence/selector-fit-measurements-2026-09-13.json`
retain 115 native support measurements and the new independent retention
failure. Twenty-one native contracts now produce three passing guards and
18 expected red failures, including the source guide's misindexed seat.
The original source/fixture evidence and completed task remain historical
evidence, not passing acceptance for the proposed alignment.

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
qualify a print, enlarge the knob's outer shape, add a guide insert or physical
body, substitute an offset/bent-spring guidance model, select a finite-time
snap model, expose running controls,
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
6 mm / 36 degrees apart. Preserve the knob, shaft, number-roll, keyed-group
and housing occurrence transforms, including the different top/bottom shaft
axial offsets. Only the selected ball/spring internal mounting offsets and
knob guide/seat geometry may change as explicitly described below; do not
translate the entire knob or redefine the digit zero to conceal the mismatch.
Between-detent shaft phase may follow the measured groove instead of the old
straight interpolation;
it must meet those seated coordinates without changing the numbering.

Alternative rejected: re-clock the entire bank or housing to fix a local
edge, which risks every other selector and support.

### 2. Use the documented ball and model its installed spring

Use the ratified nominal **5.0 mm sphere for this occurrence only**, preserving
hardware attribution. Derive its seated centers from the unchanged native
shaft pockets at the unchanged numbered coordinates. The source guide is not
a valid seating datum: at numbered one its required radial ball-center X is
63.675127589 mm, but 0.15 mm of knob motion toward the preceding digit permits
an inward displacement of at least 0.125420108 mm. The sampled trough is near
setting 0.825. These are ideal geometric support measurements, not force or
friction predictions, and the sampled trough is not a certified exact minimum.

**Ratified candidate guide alignment.** Start with a straight guide parallel to
the source X direction, located from the cone-centered nominal sphere at
digit zero. The native cone has semi-angle 55 degrees; its apex plus
`axis * (2.5 / sin(55 degrees))` gives the ball-center witness
`(62.834124973, 0.333492741, -54.695)` mm in the assembled setting-zero frame.
The Y/Z guide shift relative to the source is approximately
`(+0.333492741, +1.090999642)` mm. Each corresponding seat must be independently
verified at the other nine unchanged 6 mm / 36 degree settings. This formula
establishes a candidate nominal seat, not clearance or the final moving path.
Do not substitute rounding these numbers, a source-law offset, or a shared
coordinate constant for independent native surface agreement.

Retain the back-seat plane at source X=72.6000000002046 mm and its axial
orientation, relocating its supporting footprint with the new straight guide.
Begin with the measured source guide radius 2.6185 mm, not an enlarged union
of the old and new bores. This leaves nominal radial ball-center play of
0.1185 mm and coil-envelope radial clearance of 0.0685 mm before accounting
for actual end geometry and numerical approximation. Those are dimensional
witnesses, not accepted working-play or clearance bounds. Measure the complete
installed guide, mouth, travel and back-seat support before finalizing them.
No different guide direction, axial back-seat depth, ball size or spring
hardware is silently substituted if this alignment fails.

The uninstalled cone-centered witness clears the native shaft but intersects
the source knob by 9.389392720 mm³. Relocating the guide and back seat therefore
requires the explicit local reconstruction in decision 3, not just placing a
new ball in the old knob. Size and centered endpoints alone are not acceptance:
prove actual guidance, bounded lateral/axial play, all ten geometric seats and
the complete between-detent path. The ball's displacement must be supported by
the resulting physical guide and cam, not held on a prescribed centerline that
the actual cavity does not constrain.

Replace this rigid imported spring's operating representation with a
source/manual-grounded analytic flexible spring using the already available
Molejo integration. Preserve the measured 0.51 mm wire diameter, 2.295 mm
centerline radius and 6.5 turns with the source hand and plain cut ends.
The source has an 11.1 mm axial centerline span and its rear extent passes
1.755 mm beyond the source back-seat plane; it is not installed compression.
The sampled native seam's linear-phase residual is about 0.009704294 rad,
so a constant-pitch helix is not already proved equivalent to the source end
geometry. Complete and record that measurement and both installed seats before
authoring the spring. Keep those source/manual dimensions, except for the
measured installed compression
and seating needed to represent the assembled spring. The ball drives its
moving end; the corrected knob seat retains its back end. The back seat's
function remains mandatory although this revision allows its guide-aligned
footprint to move. Do not uniformly scale a coil, shrink its wire or park the
ball to make clearance tests pass.

This remains ideal quasi-static geometry. A held knob has a supported ball
position; each numbered detent has geometric retention after measured working
play is accounted for. Escape from a seat in either direction must require
additional spring compression; a lower-compression neighbouring position or
unbounded ball drift rejects a supposed seat. At range endpoints distinguish
legal travel from local geometric perturbations outside the admitted stroke.
Check both guide play and the shaft/follower constraint; testing only a chosen
ball centerline or a single pair of samples is insufficient. Any selected
same-instant settlement branch must have its entire transition checked, not
just its endpoints. No spring rate, force margin, snap duration or frictional
hold is inferred. If a supported path requires a different fidelity, stop.

Alternative rejected: leave the rigid source spring/ball interpenetrating
and label their moving contacts as fixed assembly seats.

Alternatives not adopted: relabel setting 0.825 as digit one, re-clock the
shaft's numbered endpoints, or move the complete knob/keyed group; these would
change protected transmission datums. Retaining the old back seat with an
offset/bent spring is not proved impossible, but would need a different
guidance/seating design. It is not the selected straight-guide correction.

### 3. Reconstruct only the selected guide/seat; preserve transmission

First locate the helical groove and follower tip, knob fork and captured lower
gear independently of a proposed cutter. Measure relative play/contact in
both directions at the ten detents, intervening extrema and segment boundaries.
Use the existing independent perturbations as red witnesses, not as preset
allowances: ±1 degree shaft offsets meet the screw; opposite axial gear shifts
meet opposite fork faces. Fit/contact proof must still detect disconnection.

The expanded exception is **only the selected knob's outboard ball/spring
guide, its localized shaft-facing mouth and its aligned spring-seat footprint**.
Derive one source-backed corrected knob occurrence, not an upstream edit,
whole-knob redesign, added insert or new physical body. Preserve its external
shape except the relocated guide opening. All shaft-support lands outside
the independently mapped mouth, screw threads/retention, fork fingers and
capture cavities retain their source geometry and function. The unchanged
shaft itself, its detent/groove surfaces, input gear/keying, bearings, other
supports and other seven selectors remain protected.

Unlike the original removal-only plan, this revision **authorizes local material
restoration as well as removal**. Filling obsolete space may be necessary to
make a relocated guide: the union of two bores can leave a larger sideways
escape path rather than the claimed straight guide. Added material is limited
to the old outboard guide/seat cavity and its obsolete mouth, excluding the
shaft-clearance bore, fork cavities, thread voids and exterior air. Removal is
limited to the independently mapped corrected guide/mouth/seat region. A
bounding box around the knob is not a permissible restoration envelope.
Quantify additions and removals separately; a net volume comparison can hide
damage and is not sufficient. All remaining knob geometry must match source.

The screw's non-threaded follower tip, if needed, and the housing's local
selector-slot/number-window edges remain **removal-only**. Prefer correct
installed positioning and the measured follower path before removing material.
There is no general additive-material exception for these or other parts.

Before any production reconstruction, map the old guide cavity, proposed
restoration/removal regions, both guide mouths, supporting seat disk, remaining
shaft-support lands and nearby fastening/capture features independently of
construction tools. Fix every fill and cutter in the knob's own frame; none
may chase the current pose. Record actual dimensions, additions/removals,
remaining lands/walls and resulting clearance or working play. The new mouth
is not permission to trim away an otherwise obstructing shaft support.

The candidate guide's upper wall is a specific open risk: a simple shift of
the current-radius bore to Z=-54.695 leaves about **0.3515 mm** to the source
top plane locally. Do not treat this number, a positive volume, or one connected
solid as proof of adequate retention/support. Before choosing geometry, measure
the complete residual wall and seat lands, their continuity and contact
footprints over guide play and the entire stroke, and set explicit geometric
acceptance bounds with red damage/loss-of-support witnesses. Disclose thinning
relative to the source and keep print/strength qualification out of the claim.
If continuous containment and retained mechanical support cannot be established
inside the unchanged outer shape and mapped exception, stop. Do not grow the
knob, shrink the spring, move another support, or erase the source comparison
to make that gate pass.

There is no automatic inherited 0.05 mm frame-gap requirement: each interface's numerical
fit must be measured and documented before use. Measurement choices within
these protected bounds are routine; a need to cross them is a stop condition.

Free-running surfaces need a positive, defensible clearance bound. Working
contacts instead need a non-penetrating supported contact envelope and bounded
play; opening a universal gap around them would disconnect the mechanism.
No interference epsilon substitutes for either proof.

Alternatives rejected: machine a full swept void around the selector, leave
both guide bores open without proving constrained play, or replace the whole
knob with a convenient generic solid. Each can remove the very support,
guidance or capture interface under test.

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

Negative controls must catch at least: source oversized ball; restored old
guide/back-seat alignment; frozen spring or ball follower; unclosed obsolete
guide space with lost guidance; misplaced back seat or weakened/broken retaining
wall; reversed/missing keyed travel; wrong shaft axis/phase; disconnected
gear/fork or screw/groove; ineffective housing relief; addition or removal
outside permitted regions; and an early release of the second carry in the
diagnostic fixture. Source comparisons must separately detect additions and
removals, including a reconstruction with unchanged net volume but damaged
protected material. A mouth exemption that masks shaft-support loss must fail.

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
- Corrected alignment leaves a thin wall or a wide obsolete passage → prove
  wall/seat continuity, remaining support and bounded guide play before any
  reconstruction; do not call the 0.3515 mm witness adequate by assumption.
- A cone-centered endpoint might still have an unsupported intermediate path
  or a shifted retention basin under guide play → prove the physical coupled
  path and all ten seats independently of the placement formula.
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

The original planning-only commit is `aec7ca4`, based on `dd98104`.
The pilot ratified this complete alignment revision on 2026-09-13.
Validate and commit the revised
planning artifacts separately before resuming implementation. Keep the existing
red probes and evidence uncommitted with the implementation; do not absorb
them into a planning-only commit or check off their unfinished acceptance work.
The earlier planning commit/evidence remain traceable rather than being silently
relabelled as approval of the reconstruction exception.

Resume at task 1.2: complete source measurements, then map/protect the corrected
guide, mouth and back-seat region and prove the geometric wall/support bounds.
Reuse the retained red contracts, add the new alignment/guidance/restoration
mutations, prove the installed detent and then local housing/follower fits,
and only then wire selected occurrences and run the full acceptance matrix.
If a trial fails, retain its evidence and keep the previous operating wiring;
do not merge partial fits into the primary checkout.

Completion includes synced accepted specs, archive, validation records and a
focused implementation commit in this project. No integration, push or worktree
cleanup is implied. The original `simulate-the-curta` stays separately active.
Then resume home-window/setup/outgoing-boundary evidence and coordinated running
proposals; ask the pilot before actual solid-node feature development.

## Open Questions

The pilot ratified the original 5 mm hardware choice, installed quasi-static
spring/ball representation and two conditional fixed-seat candidates, and now
the bounded local fill-and-rebore exception and moved guide-mouth/back-seat
footprint. Final dimensions and their adequacy remain to be proved, not
accepted by ratification alone.

Routine implementation must determine spring dimensions/seating, actual follower
path and play, all ten retention basins, fixed-seat regions, separate permitted
restoration/removal coordinates, residual wall/seat/support bounds, numerical
fit values and complete continuous-path bounds. The ratified source-parallel
guide and source axial seat plane are the bounded alignment to evaluate, not
a blanket allowance for any convenient offset or spring path. Any need for
external knob growth, different guide direction or axial seat depth, changed
ball/spring hardware, shaft detents/groove, protected thread/support/fork
modification, another station, a broader inventory or different fidelity
requires a specific revised proposal.
