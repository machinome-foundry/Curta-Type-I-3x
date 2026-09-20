## Current continuation — finish operating Curta, 2026-09-19

The pilot requested completion of the operating model task by task after the
clocked sibling. The work order and new red/green evidence are recorded in
`simulation/docs/operating-curta-completion-2026-09-19.md`. The manifest now
selects `operating_curta`; the earlier development-root descriptions below are
historical. No task is completed by that selection or by clocked-model tests.

Tasks 2.3, 3.3, 4.2, 4.3 and 6.1 are now complete (12/23 overall). The framework
bank/pose disagreement is corrected and, with explicit pilot approval,
framework main is fast-forwarded to `b9b64dd`. The unchanged minimal reproduction
and full retained world-motion checks pass. Subtraction, shift and clearing
mutations then failed their intended contracts, with both kernels green after
restoration. Additional retained-model spring-seat/follower checks pass both
kernels after detecting their disconnected-drive mutations. The reverser assembly,
measured restraints, source overlap findings and complete viewer pointer
acceptance remain unresolved. The tested framework/viewer pair loads all 24
controls, and actual selected crank-lift and first-selector drags pass with
retained readback. The operating stop pin also has a tested source-print seating
fit; that partial frame work does not complete the whole overlap inventory.
The marker-track mesh discrepancy is also resolved without changing the native
housing or marker seating: all four marker geometry checks pass both kernels.
The retained-motion suite now passes six checks, including every marker's own
motion and upper-bank carriage/clearing transport. Task 6.4 remains open for
the reverser, clearing-loop and complete operating matrix.

The carriage/clearing restraint increment now passes its source-fidelity,
free/blocked contact and installed-world checks on both kernels. Eleven
running tests cover measured play, all six slots, repeated attempts, separate
release and replay; a negative-sweep follower error is corrected. Real hosted
pointer drags now stop seated shift and clearing without auto-lifting. The
bounded fits and evidence are in
`simulation/docs/carriage-interlocks-2026-09-19.md`. Tasks 1.3 and 6.2–6.5 remain
open for the rest of their stated matrices; this does not certify crank and
selector mid-cycle restraints, counter reversal or the printed loop.

The housing-thread fitting increment clears the covers at their already
verified datum and preserves their axial capture. Its generated-STL defect
was caught by the neighbouring regressions and corrected without repairing
the source prints. The seven cover contracts pass again under both runners;
see `simulation/docs/housing-thread-fit-2026-09-20.md`. The rest inventory is
still open. Separate calibrated loop and reverser-seat investigations retain
their unresolved findings rather than inventing working endpoints.

The next enclosure increment recenters the source lower group on the sleeve's
native circular datum, carries its five markers and lower fittings, and names
a .05 mm base seat. Five scoped geometry/fidelity contracts pass both runners;
see `simulation/docs/enclosure-seats-2026-09-20.md`. This does not close the
whole-machine rest inventory or the final control matrix.

The initial operating rest inventory is now measured and committed separately:
390 rigid occurrences, 268 positive faceted pairs and 166 positive native/STL
pairs, with no refused commons. These remain findings, not exclusions; task
1.3 is still open because the rest/frame contracts are red. The reverser-seat
record now also checks the actual knob print, ball bore, shaft fastening
shoulder and housing window. A functional mounting-seat correction is a pilot
decision, not an adopted workaround for the remaining lower-detent mismatch.

Pilot-guided inspection on 2026-09-20 adds the separate `reverser_inspection`
model with measured-pose buttons, independent gear/drum rotation and a short
navigation tree. Its source-equivalence and control checks do not resolve the
reverser fit or complete tasks 5.1/6.4. See
`simulation/docs/reverser-inspection-2026-09-20.md`; operating controls, geometry
and the manifest default remain unchanged.

The pilot authorized testing a bounded reversing-shaft mounting-seat change on
2026-09-20, with all fits documented for author review. The separate trial
raises the unchanged detent-bearing body 1.9 mm while shortening the upper
profile to preserve its installed fastening-end height. It restores sampled
lower-row reach but leaves sixth-channel fork interference and upper detent
retention unresolved. See `simulation/docs/reverser-seat-trial-2026-09-20.md`
and the consolidated `simulation/docs/author-review.md`. No operating geometry,
upstream CAD, task checkbox or acceptance requirement is changed by this trial.

The subsequent fork/follower continuation fits the sixth fork seat, represents
the manual's finished M4 end, and differentiates the five higher counter tooth
profiles from the ones stack. Both original shaft pockets remain unchanged.
The six-input working bank passes 15/15 under each kernel; the source-sized
radial follower and housing overtravel pass independently. `OperatingCurta` now
has a physical `reverser_height` input, all six gears follow the actual knob,
and engagement reads source tooth-row overlap rather than a midpoint mode.
The first four-turn retained-operation sequence, physical overtravel and replay
tests pass. All 24 shifted-operation cases also pass, as do installed-world
motion checks on both kernels and scoped hosted down/up gestures. Evidence is
in `simulation/docs/reverser-fork-and-follower-2026-09-20.md`.
Task 6.4 still includes clearing-loop deployment, and the
remaining action-order and whole-machine obligations are not waived.

The clearing-loop continuation now proves the original first clip's captive
bearing and a bounded second-seat candidate (T05/T06) on both kernels.
The candidate's endpoint and rivet-head capture pass, but a 111-pose sweep
still finds two second-rivet passage contacts on the body-side mouth wall.
It remains a diagnostic, not an adopted deploy/stow control or task completion.
See `simulation/docs/clearing-loop-investigation-2026-09-19.md`.

## Previous continuation — Python direct operation, 2026-09-16

The retained-angle and live source-selection prerequisites have merged. Python
implementation is active, without waiting for viewer work. The source-backed
`simulation.running:OperatingCurta` development root implements retained
arithmetic/clearing and independent physical inputs; it does not yet replace
the manifest's pose model. All ten decimal markers now move on their measured
tracks with cyclic neighbour stops. See the
`simulation/docs/direct-operation-implementation-2026-09-15.md` checkpoint and
`simulation/docs/direct-operation-markers-2026-09-16.md` for passing evidence,
the faceted/native discrepancy and explicitly open reverse-operation tests.
Counter reversal, loop deployment, interlocks and final matrices remain open.
The pilot requested a performance wart and continued implementation, not a
Python handoff. Tasks 6.1–6.6 remain open; no earlier geometry task is waived.

## Historical continuation — Python direct-operation prerequisite, 2026-09-15

The pilot accepted the markings visually and authorized Python implementation
without waiting for the viewer's retained-angle implementation. ADR-121 is now
available and the repeated/bidirectional clearing prerequisite passes. A second
reduced probe exposes a changing-carry-association cycle: both fixed carriage
positions construct, but live selection is refused as a cyclic running program.
See `simulation/docs/direct-operation-running-checkpoint-2026-09-15.md` for
the tested framework identity, reproduction and representation decision needed.
The production migration is paused; the existing model is unchanged. Tasks
6.1 and 6.5 still owe paired viewer/pointer evidence, not a gate on Python-only
work under the pilot's current direction. No older task is marked complete.

## Previous continuation — markings, 2026-09-15

The pilot directed a framework handoff for retained-angle clearing, then
project markings. The handoff is committed in the framework as
`workflow/docs/curta-retained-angle-clearing.md` (`3045600`), a pre-spec
requirement for another agent. The scoped markings record is
`simulation/docs/markings.md`. The flat/cylindrical API supports 25 number
rolls and three housing sheets; the conical upper-housing index sheet remains
outside that API, and viewer rendering remains a separate pending capability.
This continuation does not complete the direct-operation or older geometry tasks.

## Paused continuation — direct operation, 2026-09-15

The pilot approved direct interaction with every physical input, retained
Time.running state and user-chosen ordering. No production code for this
migration has been changed yet. The approved command inventory is in
`simulation/docs/direct-operation-2026-09-15.md`. The required framework and
viewer capabilities were developed separately as `direct-part-motion` and
`slide-and-turn-parts`; see the dated prerequisite probe for their tested state
and the additional retained-angle clearing requirement.
The new work below does not complete or waive any older mechanical task.

## Previous continuation — 2026-09-11

The pilot resumed this change after machinome's `expression-graphs` cycle
merged into main at `5e59147` (planning `446bc22`, ADR-101). The complete
post-fit export succeeds in 41.43 s at 817216 KiB peak process RSS with the
existing CAD cache. All six
calculator examples, page-53 calibration, retained operations, lift/shift
guards, selector controls and layers pass against that export; its screenshot
was inspected. The cover/ring and seventeen axle-seat interfaces now have
seven passing contracts on both runners and three separately failing fit
mutations, restored and green. All 37 tested node modules were rerun: 142/144
faceted and 143/144 native checks pass. The root's thread contact remains red;
the additional faceted bearing contact passes natively. Remaining thread/frame
interfaces and final acceptance tasks below are still open. The schema is
`spec-driven`, with 7/17 tasks complete. The full matrix is recorded in
`simulation/docs/resumption-validation-2026-09-11.md`.

## Historical pause checkpoint — 2026-09-11

Paused by the pilot for the machinome construction-time expression-sharing
follow-up. See `simulation/docs/pause-report-2026-09-11.md` for the initial
10h Astra/xhigh sprint, memory evidence, cycle handoff and ordered restart.
At that checkpoint no formal framework memory-fix change existed; this project stays
active and unarchived. Checked tasks below record scoped incremental evidence,
not a final full-machine regression. No outstanding task is waived by the pause.

## 1. Source assembly and frame

- [x] 1.1 Add the manifest, an initial renderable root and build exclusions; write and run source and integrity contracts red. Frame build passed; inventory failed with 1 != 547 (faceted, 2026-09-11).
- [x] 1.2 Import the STEP hierarchy, identify the invalid solid and resolve ambiguous hardware with reproducible probes and measurements. All 547 occurrences imported; native invalid product is zero positioning spring (#419219). Repeated names retain their distinct source entity identities; see simulation/docs/measurements.md.
- [ ] 1.3 Verify the complete rest assembly, rigid groups and source overlap inventory; make source and frame contracts green.

## 2. Crank and one selectable digit

- [x] 2.1 Measure the drum, selector and transmission interfaces; write travel, seating and engagement contracts red. Measurements and red evidence are recorded in simulation/docs/measurements.md.
- [x] 2.2 Declare crank, drum, selector and shaft joints and drive relations; make the single-channel contracts green. The complete result/counter drum sweeps also pass faceted and exact (20 result settings/modes, both counter modes).
- [x] 2.3 Prove mutations of drum axis, selector travel and gear phase fail their intended contracts. On 2026-09-19, a Y-axis drum, 5 mm selector pitch and +10° pinion-phase mutation each failed the intended geometry contracts; all were restored, then both modules passed faceted and exact (4/4 per kernel). See the operating completion record.

## 3. Carry and registers

- [x] 3.1 Write adjacent-digit carry and reset contracts red, including the manual's geometric checks. Dial-pin, fork and reset-shoe contracts failed; native probes identified the contacts. Timing tests rejected an early reset, and the installed bank exposed a nine-degree half-pin mounting discrepancy plus shifted-neighbour contact.
- [x] 3.2 Implement the carry mechanism, expand to all digit channels and register dials, and make the contracts green. All fifteen carries pass both kernels through two revolutions and all carriage shifts; the complete bell spring's mounting and subtraction sweep now pass native as well.
- [x] 3.3 Verify the page-53 arithmetic sequence and complete overflow; prove carry and dial-phase mutations fail. The retained model passes the 0, 1, 9, 90 sequence with counter readings 1–4 and subtraction from zero followed by full-bank overflow back to zero (both registers). Disabling the production carry latch and shifting the bevel dial phase +10° each fail their intended contracts; restored checks pass, including exact bevel geometry. See the 2026-09-19 completion record.

## 4. Subtraction, carriage and clearing

- [x] 4.1 Write subtraction-lift, carriage alignment and clearing contracts red. World-vertex tests exposed missing 9 mm subtraction, 6 mm carriage lift, 20° shift, plate rotation and spring-seat motion.
- [x] 4.2 Implement the measured joints and relations, including affected flexible parts, and make the contracts green. The existing subtraction/carriage/clearing relations now pass the retained world-motion checks after framework b9b64dd. Added operating-model carriage-spring and clearing-follower/spring contracts pass with the motion checks (5/5 faceted and exact); disconnected-drive mutations fail. The isolated positioning spring is also rerun green on both kernels. Earlier bell-spring full-travel geometry evidence is unchanged. This closes the measured motion/flexible-seat task, not task 1.3 clearance or 6.x restraints and operation acceptance.
- [x] 4.3 Prove subtraction, shift and clearing mutations fail their intended contracts. On 2026-09-19, 8.1 mm subtraction travel, 18° instead of 20° shift and reversed clearing direction each failed its retained-model motion contract. All three mutations were restored; 3/3 contracts pass faceted and exact on integrated framework b9b64dd. See the operating completion record.

## 5. Complete machine and evidence

- [ ] 5.1 Finish direct mechanical controls, educational show/hide assembly layers and the small separate demonstration set; assert retained outcomes, layer membership and sample interference through every demonstration.
- [ ] 5.2 Run every node's faceted regression, build the root and inspect its viewer document and all referenced artifacts.
- [ ] 5.3 Render and inspect rest, moving, isometric and alignment snapshots; record measured findings and fidelity limits.
- [ ] 5.4 Run every node's exact regression and write the final simulation README from the verified implementation.
- [ ] 5.5 Validate and sync the accepted specifications, archive the completed change and commit implementation and evidence.

## Current evidence and continuation

The following records the earlier pose-driven implementation. It is retained
as evidence, not a claim that the newly approved direct-operation controls
are already implemented.

The source assembly builds and its complete 547-occurrence world placement check
passes. A +1 mm main-crank placement mutation fails that check with measured
1.00000000007 mm drift at occurrence 0:1:1:18:1; the mutation is reverted.

Task 1.3 remains open. The initial red root tests exposed the invalid spring
and an invalid digits-cover/upper-housing boolean.
The pilot explicitly authorized replacing the spring from the manual's winding
dimensions and measured mounts, and delegated routine engineering decisions.
The documented spring's validity, wire-size and mounting tests now pass, including
the exact mount test. Crank/drum and selector-travel contracts passed after their
red runs. The educational layer test accounts for all 547 source occurrences and
preserves their placements. Six arithmetic tests pass, but do not yet prove
complete register geometry or drive engagement. The single-row input passage
and first bevel pair now pass exact and faceted engagement contracts, after
documented fitting corrections. Seventeen dial joints are connected to the
settled register ports and sub-turn cycle relations. Three register geometry
tests pass both kernels, including every result dial's independent radial axis
and visible input preceding carry. The browser check passed the manual's full
0, 1, 9, 90 sequence with retained registers, eight digit sliders and recursive
layer visibility/focus. The drum/tens-bell printed groups are reconciled; their
inventory, connectivity and native validity pass exact. The 9 mm subtraction
lift passed after its red world-vertex test. Keyed input travel and 72° shaft
rotation passed after red; all seventeen source-specific stacks are integrated.
The complete result/counter drum sweeps now pass both kernels after the documented
input-sleeve fits and .36 mm counter-tooth relief. Sliding carry levers, rotating
tens bell, 6 mm carriage lift, 20° shift and rotating clearing plate pass their
motion checks. Carriage spring compression passes its faceted seat and validity
tests and its two exact tests. Lower/upper decimal-marker ownership passes
while all 547 source placements remain accounted for. A material-connectivity
contract verifies the fitted print's enclosed cavities without mistaking them
for detached material. The axial bevel fit's newly exposed frame interference
is corrected by shortening the protruding stem, verified exact.
The installed bevel bank now passes both kernels across all six shift positions,
lifted intermediate positions and all seventeen ±12° flank engagement checks,
after centering dial clocking by -3°. Six worked examples pass arithmetic and
model replay tests; seven instruction endpoints and a routed carriage scenario
pass. The first carry pairs pass complete bell contact sweeps and both ±12°
locking / active-tooth engagement limits in both kernels after centered profiles
and measured passage timing. A spring tessellation-budget
test exposed 7,968,048 triangles; four samples per spline span preserve geometry
while making the viewer mesh manageable. The updated browser run passed every
example, retained-operation checks, lift/shift guards and layer controls.
The zero-cam/follower has six passing contracts in both kernels, including the
drive pin's axial travel, seated roller contact and moving spring mounts. The
anti-reversal pawl follows the measured ratchet, including its shorter closing
interval; forward contact, reverse blocking, release clearance and moving spring
mounts pass exact. Its collar/plate and spring-anchor fits are recorded explicitly.
The fifteen carry U-wires now follow the measured detents with fixed closed folds;
twelve wire/travel/contact contracts pass both kernels. The manual's two clearing
tooth strips and spacer were missing from the STEP but present as flat STLs. Their
formed groove fit passes faceted. The integrated root now keeps all 547 original
leaves plus these three prints, with twelve passing checks; the source housing
overlap remains the one failing ordinary interference assertion.
The clearing gear's missing-tooth gap fixes the absolute zero, previously
undetermined by bevel phase alone. Four whole dial pitches correct all seventeen
dials without changing bevel engagement; that bank's exact regression passes.
After the documented groove-depth and clearing-flank fits, both racks reset the
dials sequentially. Five clearing contracts pass both runners, including every
digit/station, eighth-tooth passages and paired free/blocked engagement checks.
Reversing the clearing law fails three geometry contracts; it is restored.
The new first-carry contact bench exposed dial-pin and reset-bell collisions;
native probes confirmed fixed fork/sleeve and reset-shoe contacts. Documented
local fits, measured pin approach and real reset-cam timing now pass six native
checks over two turns, including one-sided driving contacts. Carry remains
latched across the cycle boundary where its cam requires it. The complete
fifteen-station cascade passes both kernels after aligning the half-pin flats
with the manual's 36 degrees and choosing the cutaway side that clears parked
neighbouring digits. All six carriage positions are covered, as are two-turn
cascades. The twelve carry-wire checks remain green after the slider fits.
The bell's positioning leaf spring now preserves its native plate and tapered
hooks while measured ribbed arms bend through the subtraction stroke. Its
source-fidelity, one-body, mounting and full-travel contracts pass; the whole
bell and its two spring screws share one revolute joint. The restoring screw
also clears the three formed clearing strips after a strictly bounded back
relief that leaves every tooth face unchanged. All seventeen register balls and
tapered spider fingers now pass native source-fidelity, continuity, seating,
carry/subtraction and progressive-clearing checks. The spring-loaded clearing
stop also passes seven contracts in both kernels, including native cam contact
through a half-degree sweep and both spring endpoints. A whole-machine relative-
placement audit identifies the remaining cover/window, frame-guide and retained-
seat interfaces; these are not silently treated as fixed source overlaps.
Inter-system contact, the whole-machine overlap inventory and demonstration sweeps keep
their tasks open. These results are checkpoints, not final delivery evidence.

## 6. Direct mechanical operation

- [x] 6.1 Verify the ratified framework/viewer prerequisites are available as a tested content pair before relying on Slide or selected-joint controls. Framework b9b64dd and viewer 2912006 (API 21, bundle SHA-256 a5a5542762c3326aa53fa68875f7d3da698ae0253681366ba325528446afa614) load the actual version-7 operating build with all 24 controls. Real pointer drags use the distinct selected crank-lift target and the first selector; retained readback proves lift without crank turn and independent selector/shaft motion. Public run reset is test setup between cases. Full standalone/hosted interaction and wrong-order coverage remain task 6.5.
- [ ] 6.2 Write red run tests for independent selector changes, retained arithmetic across operand/mode changes, partial crank travel, direction reversal attempts, carriage interlocks and repeatable snapshot/replay.
- [ ] 6.3 Migrate the mechanism to Time.running with run-owned state and independent physical inputs; make those tests green without a page-local calculator, direct register setters or automatic operation preparation.
- [ ] 6.4 Add and prove the reversing lever, selective bidirectional clearing, clearing-loop deployment and each decimal marker's independent movement and mechanical limits; preserve source provenance and existing geometric evidence.
- [ ] 6.5 Bind every input to its actual visible part; test real pointer interactions in standalone and ordinary hosted viewers, including wrong-order attempts and partial motion, and inspect rest/moving/interlock snapshots.
- [ ] 6.6 Replace obsolete calculator-page instructions and demos, update the simulation README and acceptance evidence, and report remaining whole-machine geometric gaps separately from the control migration.
