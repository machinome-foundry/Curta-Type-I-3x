## Why

Status: alignment revision ratified by the pilot on 2026-09-13
("ratify, go o"). The original planning commit `aec7ca4` remains unchanged;
this revision separately authorizes the bounded geometry work below.

Checkpoint, 2026-09-13: revision committed as `da432fb`; subsequent diagnostic
work is now paused at the pilot's request to steer project direction. Tasks
1.1 and 1.3 are complete (2/22); no operating selector fit is installed. The
[handoff](../../../simulation/docs/open-run-handoff-2026-09-13.md) records the
unfinished work. The proposal below retains its ratified scope, not an
instruction to continue automatically or a claim of completed acceptance.

The selected Curta input cannot yet traverse its required 0–9 range without
entering its housing, detent and helical-follower parts. The installed-home
audit at `dd981041ff41108727abc9ae02db0c291d0126cd` supplies nine native
counterexamples, so this local prerequisite must be resolved before calling
the input ready for the planned history-dependent running slice.

The first implementation measurements also reject a seating assumption in
that plan: the 5 mm ball on the source guide has its sampled seat near setting
0.825, not numbered one. The guide is 1.090999642 mm below the source pocket
center. This is an alignment problem as well as an interference problem;
holding the ball on the flank does not establish a detent. See the retained
[implementation evidence](../../../simulation/docs/selector-fit-implementation-2026-09-13.md#3-design-conflict-numbered-coordinates-are-not-the-source-guides-seats).

## What Changes

- Fit **one physical input**, the ones selector and its local housing
  interfaces, for complete travel in both directions at the initial and
  post-cascade stationary home configurations. Keep the pending second carry
  and all non-input fixture coordinates unchanged.
- Use the manual's nominal 5 mm ball as the ratified operating hardware,
  replacing only this occurrence of the source's 5.4 mm ball. Establish its
  guide/cam seating and the selector spring's installed compression from
  measured geometry; a smaller ball alone is not an accepted remedy.
- Preserve the ten numbered detents, full 54 mm knob stroke, source shaft
  axes and keyed-input capture. Derive the between-detent ball/spring and
  helical-follower paths from their working surfaces, not cosmetic blending.
- Realign the selected knob's ball/spring guide, its local shaft-facing mouth
  and spring back seat as one occurrence-specific correction. A straight guide
  parallel to the source guide, through the measured seated-ball centers, is
  the first design to prove; preserve the source axial back-seat plane.
- Authorize a narrow **local fill-and-rebore exception** inside that knob's
  original outboard guide/seat cavity and independently mapped guide-mouth
  region. It permits closing obsolete guide space as well as opening the
  corrected guide; cutting a wider void alone must not substitute for guidance.
  Preserve the knob's outer shape apart from the relocated guide opening,
  all shaft-support lands outside that mapped mouth, threads, fork capture
  and the remaining source body. No separate insert or added physical body.
- Keep the screw's optional non-threaded follower-tip fit and housing
  slot/window relief removal-only. Protect the shaft's detent/groove surfaces,
  bearings, other supports, keyed input, other selectors and completed frame fit.
  The local knob reconstruction does not grant a general right to add material.
- Treat only the existing co-moving screw/knob threaded engagement and
  bottom/top shaft join as candidates for an explicit fixed-seat inventory.
  No moving ball, spring, follower or housing penetration is exempted.
- Prove the local fit with red-first contracts, full installed-neighbour
  checks, continuous-path bounds, independent coupling/support checks,
  negative controls, native/faceted regression and inspected source/fit views.
  Numbered settings must be actual geometric seats with bounded working play,
  not merely non-intersecting held poses. Record remaining guide walls and
  supporting lands before any production reconstruction.

## Capabilities

### New Capabilities

- `selected-input-selector-fit`: supported travel, detent/follower contact,
  fixed-seat classification and local-fit preservation for the selected ones
  input at the two stationary home fixtures.

### Modified Capabilities

None. The existing `result-carry-frame-clearance` requirements remain intact.
The active `simulate-the-curta` change and its remaining whole-machine
requirements are not replaced or completed by this prerequisite.

## Impact

Work stays in this project's `WTs/open-run-simulation`, under `simulation/`
and this project-owned OpenSpec record. New selector fit/profile/inspection
helpers and contracts may be added; selected occurrence wiring may change in
the operating selector and lower housing. Preserve raw imports, upstream
STEP/STLs/manual, source attribution and all non-selected occurrences.
No new package dependency, framework/viewer feature code, UI, input command
contract, causal run or migration of the old calculator controls is included.

The original plan was ratified on 2026-09-13 ("ratify, go on") and committed
as `aec7ca4877c58820c6c02a32c44d8c6c206c9e9b`. At revision ratification
task 1.1 was complete; no operating geometry has changed. The pilot subsequently approved preparing,
then ratified, this bounded alignment revision. Its final fit dimensions
and geometric adequacy still require the implementation gates below.
The revised planning state was validated and committed separately as `da432fb`
before measurements resumed. A failed wall/support/capture/continuous-path gate
returns specific evidence and choice, not a silently broader repair.

Out of scope: the other seven selectors, unrelated housing/thread defects,
general force/friction/dynamics, offset/bent-spring guidance as a substitute
design, external knob enlargement, changed spring hardware, print qualification,
the complete home-angle
window and setup/outgoing-carry proof, and all solid-node/viewer running
implementation. Release 0.7 versus 0.8 remains undecided. Integration and
publication are not authorized by this proposal.
