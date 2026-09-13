Status: original plan ratified on 2026-09-13 ("ratify, go on"), commit `aec7ca4`.
Alignment revision ratified on 2026-09-13 ("ratify, go o"); record its revised
planning commit before implementation resumes.
None of the implementation tasks below was complete at original ratification. The audit
at `dd98104` is red evidence, not a passing fit or a completed task in this cycle.

Implementation progress: 1/22 complete. Previously paused during task 1.2 after native
measurements found that the source guide places the ball on a detent flank at
the required numbered coordinates. The 5 mm hardware correction alone does
not fix that indexing. The revised source-parallel guide/back-seat alignment
preserves numbered datums and authorizes the explicitly bounded knob restoration
exception in the design; those complete revised choices are now ratified. See
`simulation/docs/selector-fit-implementation-2026-09-13.md` §3. No operating
geometry has changed; broader alignment/cutter scope remains unauthorized.

The original planning-only record preceded task 1.1. Validate and commit only
this ratified revision's planning artifacts before
resuming task 1.2; preserve `aec7ca4` and the existing red evidence/probes without
absorbing them into that planning-only commit. Work inside this project's existing
`WTs/open-run-simulation`. Source/support conflicts return to the pilot;
routine measurements and reversible trials within the ratified bounds do not
need another confirmation. No solid-node or viewer feature work is included.

## 1. Reproduce and bound the selected interfaces

- [x] 1.1 Add independent selected-input acceptance contracts and reproduce the initial/post-cascade native counterexamples red, including between-detent screw and ball contacts; retain the frozen states, complete physical inventory, source/framework hashes and exact failing interfaces. Evidence: `simulation/docs/selector-fit-implementation-2026-09-13.md` §1 (20 native contracts: 3 passing guards, 17 expected red failures).
- [ ] 1.2 Complete the nominal ball/shaft, source spring wire/coil/end, groove/follower and gear/fork measurements. Independently establish the source-parallel guide through the measured nominal seats and the relocated back-seat footprint on its unchanged axial plane; verify all ten unchanged numbered datums, retention basins, intermediate extrema and both-direction/lateral working play before changing operating geometry. Retain the original misindexing as a red witness, not a shifted digit-zero convention.
- [ ] 1.3 Prove or reject the two fixed-seat candidates in canonical relative coordinates; record only the supported, unchanged screw/knob and shaft-join regions, with inventory mutation tests and no moving-contact exemptions.
- [ ] 1.4 Map separate independent knob-restoration and removal regions for the outboard guide, old/new local mouth and shifted seat footprint; preserve shaft clearance and all support lands outside that mouth, threads, fork/capture cavities and other stations. Measure and set geometric wall/seat/support, guide-play and clearance bounds before reconstruction; explicitly resolve the approximately 0.3515 mm upper-wall warning. Keep screw/housing changes removal-only. Stop if the fixed guide direction, source axial seat plane, unchanged outer shape, protected features or source hardware cannot support the fit.
- [ ] 1.5 Add separate added/removed-material, connected/valid-part, residual wall/seat/support, bounded-guidance, unchanged-datum, source-to-body accounting and non-selected-occurrence guards. Establish negative witnesses including equal-net-volume protected damage, added material in a protected void, an overbroad mouth exception and an uncontrolled old guide opening before fitting; preserve the completed carry/frame comparison baseline.

## 2. Establish the installed detent and local fits

- [ ] 2.1 Reproduce ball diameter, numbered-seat retention, bounded guide play and transition-support failures red. Implement the mapped occurrence-local guide/mouth/back-seat correction (separately checked restoration and removal where needed), nominal 5 mm ball and actual guided displacement. Prove all ten seats green under working play, with wall/support guards, no changes to the shaft's working surfaces or numbered datums, and no clearance epsilon or arbitrary ball centerline.
- [ ] 2.2 Run installed spring seating, source wire/coil/end geometry, connectivity and deformation/clearance contracts red; implement the source/manual-grounded straight-guide flexible spring and measured compression. Prove support at the ball and corrected guide-aligned seat, retain the source axial seat plane and hardware dimensions, and make the contracts green without an offset/bent-spring substitute.
- [ ] 2.3 Run helical-follower and keyed-input capture contracts red for the relevant failure/disconnection witnesses; establish the measured between-detent path and, only if needed within the mapped bounds, the non-threaded follower-tip fit. Prove the ten numbered positions and both-direction contact/play without modifying fork, keying, threads or groove or changing the guide/support bounds already proved in 2.1.
- [ ] 2.4 Run housing slot/window clearance contracts red; implement the bounded, fixed local housing adapter and prove those interfaces green with measured clearances, no added material and all protected features intact.
- [ ] 2.5 Record final guide/mouth/seat alignment, additions and removals, fit dimensions, source/manual spring traceability, remaining walls/support and their thinning relative to source, working play and rejected trials. Verify fresh and built geometry agree and retain independent native source/fit sections; distinguish geometric containment/support from unproved manufacturing strength.

## 3. Prove complete installed travel without resetting the machine

- [ ] 3.1 Bind the fitted selector, ball/spring path and unchanged keyed input group into the independently frozen fixtures; verify actual world geometry and all non-input state invariants, explicitly replacing the old probe's insufficient rigid ball/spring transforms.
- [ ] 3.2 Sweep 0→9 and 9→0 in the initial `099` stationary-home fixture against the complete installed neighbour inventory on native and faceted paths; include every seated position, measured extremum and transition boundary and report source-mesh coverage explicitly.
- [ ] 3.3 Repeat complete bidirectional travel in the post-cascade `100` fixture, including one-to-zero selection; prove carry fractions `[0, 1]`, wheels, output shaft rotations and all other fixture coordinates stay unchanged.
- [ ] 3.4 Complete conservative continuous-path enclosures or analytic/interval bounds for rigid and flexible motion, separating free clearance from supported working contact, accounting for guide/capture play and numbered-seat escape, and covering all possible neighbours and settlement branches. Quantify approximation error independently of fitting; a centered endpoint or sparse compression comparison alone must not certify retention. Leave this open if only sampling succeeds.
- [ ] 3.5 Exercise and restore the oversized-ball, old guide/back-seat alignment, frozen follower/spring, uncontrolled obsolete guide opening, misplaced seat or lost wall/support, wrong-axis/phase, missing/reversed keyed travel, lost screw/groove or fork capture, ineffective relief, unauthorized addition/removal and premature second-carry release mutations. Identify the independent contract detecting each, then rerun the unmutated acceptance checks.

## 4. Wire, regress and hand off the bounded result

- [ ] 4.1 Wire only the selected operating selector/hardware and lower-housing occurrences; preserve raw imports, all non-selected instances, root controls/instructions and source-body provenance. Do not convert the old root into a running model.
- [ ] 4.2 Run the full recorded 39-module node regression plus all new/affected modules on both native and faceted runners, including the completed carry/frame contracts; retain commands, named historical failures, resource use and a stable final source fingerprint, accepting no unexplained new regression.
- [ ] 4.3 Rerun the applicable lightweight Python and calculator JavaScript tests, including the evidence-probe guards; retain complete results separately from mechanical acceptance.
- [ ] 4.4 Build the full Curta root and inspect the actual viewer document, selected fitted artifacts, unchanged controls/instructions and body accounting; confirm no stale errors or missing referenced artifacts.
- [ ] 4.5 Inspect actual OpenSCAD seated and between-detent snapshots, a surrounding-assembly view and native source/fit sections; record image hashes and restore the complete root publication after inspection-only builds.
- [ ] 4.6 Update project measurements, simulation README and running-acceptance handoff with the bounded verified result and remaining home-window/setup/outgoing-boundary obligations; preserve the original `simulate-the-curta` task state and do not claim causal running or whole-machine acceptance.
- [ ] 4.7 Validate the completed cycle, synchronize accepted delta requirements, archive under the project-owned workflow and commit the implementation with its tests/evidence/records; verify clean project state without integration, push or worktree removal, then return to readiness work and retain the explicit solid-node feature-start gate.
