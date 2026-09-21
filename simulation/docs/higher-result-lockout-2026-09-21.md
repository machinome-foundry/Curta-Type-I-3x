# Higher result locking — first measured missing stop

This is the next tasks 6.2/6.3 investigation, not an adopted new restraint.
The fixed-height ones profile must not be copied onto the higher sliding
stacks. All upstream geometry remains unchanged.

`python -m simulation.tools.higher_lockout_probe --channel 2` runs the actual
OperatingCurta, sets digit 2 to 3, turns to 140°, withdraws that selector to
zero, and requests 170°. The complete installed tens upper stack retains
shaft angle 169.59999999999994° and travel −4.2 mm.

| Admitted crank | Native overlap | Published-mesh overlap |
| --- | --- | --- |
| 140° | 0 mm³ | 0 mm³ |
| 170° | 0.30868623127003425 mm³ | 0.21392486170149 mm³ |

Both requests currently complete. Both native commons are valid and both
Manifold results report NoError. This proves a missing restraint in this
action order, not a defect in the author's printed part or a need to trim it.

The focused source-backed two-channel test
`simulation.test_higher_result_locking` reproduces the same retained phase
and actual stack travel. Its expected blocked request fails red with
`completed != blocked` (36.058 s). The test consumes the current ones-only
ResultLocking bench; it does not invent a new contact limit.

Next measurements use `--locate` to bracket closing contact with the complete
solids and their published meshes. At the measured retained phase and −4.2 mm
stack travel, that probe now brackets the closing boundary at:

- Native: 145.33065795898438° free / 145.33068656921387° contact.
- Published mesh: 145.32258987426758° free / 145.32261848449707° contact.

These local brackets do not certify the complete phase/axial envelope.
The separate `--carry` preparation enters
9 then 1 through ordinary requests to latch the real first carry and test its
other axial position; no joint bank is manually seeded. This actual-root case
now completes both requests, and reports:

| Crank | Shaft | Upper travel | Native overlap | Published-mesh overlap |
| --- | --- | --- | --- | --- |
| 500° | 169.60000000000002° | −8.88e−16 mm (lower seat) | 0 mm³ | 0 mm³ |
| 530° | 241.60000000000002° | −8.88e−16 mm | 0.9496263373477174 mm³ | 0.7603711547340599 mm³ |

The carry adds a real 72-degree passage while this request moves. Thus the
second case is not a fixed-shaft bisection and cannot inherit the raised-seat
145-degree stop. Both shaft rotation and axial seating must enter any proposed
higher-channel restraint. The tiny residual in the admitted axial coordinate
is recorded, not converted into an overlap tolerance.

The new `HigherLockoutBench` exposes measurement-only shaft, crank and carry
coordinates on the unchanged source `ResultTens` and complete bell. Its
geometry parity tests compare both actual-root contact poses; its new
`higher_locking_envelope` tool surveys complete revolutions at a chosen shaft
phase and carry position. These are diagnostic instruments, not operating
controls or an adopted restraint. Both native and published-mesh parity tests
now pass (2 tests, 1.215 s). A preliminary comparison rotated an already
float32-rounded mesh from 140° to 170°, differing from the root's mesh published
at 170° by 6.95e−7 mm³. Publishing at the same contact pose resolves that
measurement-method discrepancy; the final comparison is stricter (nine decimal
places), not a relaxed clearance threshold. All positive contacts remain
positive; the clear reference is still required to be exactly zero.

The geometry helper imports now load their whole-machine entry points lazily:
using `world_solids`, `rigid_leaves` or `mesh_solid` no longer compiles an
unrequested operating machine. Measurement and placement algorithms are
unchanged. Wider phase/axial coverage remains open.

A first full-revolution survey (10-degree samples with 18 bisection rounds
where contact changes sign) finds these complete-bell opening/closing brackets:

| Carry | Shaft | Kernel | Opening bracket | Closing bracket |
| --- | --- | --- | --- | --- |
| 0 | 169.6° | native | 30.716820–30.716858° | 145.330658–145.330696° |
| 0 | 169.6° | mesh | 30.792465–30.792503° | 145.322609–145.322647° |
| 1 | 169.6° | native | 32.716827–32.716866° | 145.052605–145.052643° |
| 1 | 169.6° | mesh | 32.792473–32.792511° | 145.052605–145.052643° |
| 1 | 241.6° | native | 32.755356–32.755394° | 145.052605–145.052643° |
| 1 | 241.6° | mesh | 32.827377–32.827415° | 145.052605–145.052643° |

For an opening the right endpoint is free; for a closing the left endpoint
is free. The survey rotates meshes published at the 140-degree reference;
actual-root pose parity is separately checked with meshes published at each
actual contact pose. This finite survey can miss narrow unsampled islands and
does not certify interpolation, other shaft phases or intermediate carry
heights. In particular, the lowered closing boundary is earlier than the
raised boundary, disproving a carry-independent reuse of the measured stop.

## Indexed-position finding and isolated T07 trial

The unchanged tens stack then failed native clearance at the ordinary indexed
shaft position 200°, crank 180°. Across carry positions 0, .25, .5, .75 and 1,
the positive native volumes are respectively 0.0000170565657,
0.0000767545455, 0.0000852828307, 0.0000852828308 and 0.0000511696995 mm³.
All published-mesh commons there are zero. The other four indexed flats
(−16°, 56°, 128°, 272°) clear at those five heights in both kernels.
Reproduce with `python -m simulation.tools.higher_locking_envelope --indexed`.

This is a native-solid fit finding, not evidence that physical prints jam.
As with ones F18, adopting a contact law over the currently intersecting
normal indexed pose would encode an incorrect normal-operation stop.
`higher_lockout_trial.py` isolates **T07**, a proposed additional .01 mm outer
skin on this tens lockout only (.15 → .16 mm). Its contracts require unchanged
keyway/core and axial extent, no added material, bounded removal, connected
complete upper print, clearance at every indexed flat and sampled axial
position, and retained locking four degrees to either side. The trial is not
selected by the operating model; all other lockouts and upstream CAD remain
unchanged. The unchanged .15 mm trial fails the intended native clearance at
0.000017056565662916912 mm³ and the positive-removal check; both flank locking
and complete-print integrity pass (2/4, 27.57 s). The .16 mm candidate then
passes all four native checks (14.63 s), but its faceted run passes only 3/4
(20.18 s): the lower-angle locking flank is absent from the coarse mesh.

An independent comparison reproduces that mesh blind spot **before T07**:
all five lower-angle offsets (−4°) at carry positions 0, .75 and 1 have
positive native contact but zero faceted contact. For example, shaft −20°
at carry 0 gives 0.0032965019 mm³ native before the fit, 0.0030037110 mm³
after it, and zero coarse-mesh common in either case. This is not a reason
to weaken the negative control or increase its offset.

`TrialContactBell` refines only the diagnostic bell to .01 mm linear and
.1 rad angular deflection. The native solid is unchanged (zero material
removed or added in both difference directions). The unchanged locking
checks now pass: **5/5 faceted, 30.35 s; 5/5 native, 19.23 s**, including
the added native-fidelity contract. No contact-volume epsilon is used.
The source-like production bell and all operating geometry remain untouched.

The first native/mesh coarse phase survey of this complete trial pair covers
shaft −16°..344° every 12°, at carry positions 0, .5 and 1. It is being used
to locate the axial/phase boundaries, not as an interpolated-law certificate.
The original `.15` measurements above remain evidence for the original
production stack, not profile knots for the changed trial.

That survey completes in **619.713 s**, producing 186 kernel/shaft/height
records. Its [retained boundary evidence](evidence/higher-t07-coarse-envelope-2026-09-21.json)
includes the raw-log SHA-256 and maximum positive sampled volumes. A lowered,
indexed shaft is not free for a complete frozen revolution: the carry-tooth
contact at shaft −16° enters near 148.5353° and releases near 154.8604°.
Consequently the ones law's fully free indexed-angle branch cannot be copied
onto the lowered tens stack. No generated coarse curve has been adopted.

The inspected browser captures `_build_checks/higher-lockout-raised.png`
(original raised stack near closing) and `higher-t07-indexed.png` (trial,
shaft 200°, crank 180°, half carry) show the complete stack alongside the
bell's actual locking lands, with the refined bell's smoother circular mesh.
The .01 mm fit is established by the native contracts, not discernible pixels.

`HigherResultActionOrder` adds a separate retained diagnostic with the actual
T07 source stack and a carry-height instrument. That input moves the real
upper print through its existing 4.2 mm stroke and feeds the unchanged source
tooth-passage law. It is not a substitute for the operating lever bank and
does not set a register or directly seed the shaft. Both raised and lowered
withdrawal cases require a stop and a matching long-request stop; their
contact restraint is deliberately still absent while measurement continues.
The two-test action-order run fails all three expected assertions with
`completed != blocked` (29.772 s): original source bench, raised T07 stack
and lowered T07 stack. Both trial fixtures reach the measured 169.6-degree
shaft phase and their correct axial seats before failing the missing stop.

Expanding the fit test from five crank orientations to a full ten-degree
revolution first failed at carry .75, shaft −16°, crank 150°: 1.6770822181 mm³
native and 1.6496895882 mm³ published-mesh contact. That fixture incorrectly
held an **engaged carry gear stationary through its driving tooth**. Applying
the existing source tooth passage gives shaft 7.2° at that same crank and
height, and both complete-part commons become zero. No geometry is removed
to fix this fixture, and neither part is excluded.

The full 925-pose contract now follows the unchanged carry passage and latch
threshold while checking all five starting flats and five sampled heights.
A separate negative control deliberately freezes the engaged gear and must
detect the contact before releasing it to its proper driven angle. The
expanded six-contract suite passes **6/6 faceted (10.25 s) and 6/6 native
(99.71 s)**, with no volume epsilon. This is a sampled fit/trajectory result,
not yet a higher-channel restraint or its actual-root adoption.

Ingredient-height inspection identifies the expected axial transitions. The
printed pentagon spans source Z −26.1..−24.6 mm, rising by 4.2(1−carry) mm;
the upper results locking disc spans −23.1..−21.6 mm and the lower disc
−25.5..−23.1 mm. Their axial overlap intervals change separately, explaining
why interpolating whole-contact endpoints is not adequate. The complete
upper print also contains the carry pinion at source Z −33.6..−31.8 mm;
its tooth contact must remain part of the admitted-motion checks.

## Contact ownership, before compiling a restraint

The new `--components` diagnostic follows the same native placement operations
into the ingredients of each print. It identifies contact; all acceptance
checks continue to use the complete fused prints. At shaft 169.6°, crank
146°, the raised and half-carried contacts are pentagon/upper-results-disc
(0.0316946210 and 0.0633892420 mm³). At full carry the first contact is instead
carry-pinion/results-carry-ring (0.1604892313 mm³). At crank 170° the lowered
pentagon then meets the lower locking disc (0.8862395230 mm³).
The frozen-gear negative control at carry .75 / crank 150° is likewise
pinion/ring contact; the properly driven 7.2° shaft pose has no component
contacts. These measurements explain the different contact windows without
changing source motion or cutting away a drive tooth.

Three native ingredient-pair surveys (`--pair upper_lock`, `lower_lock`,
`carry_tooth`) now locate their independent angular boundaries. Their future
combination must be checked against complete native and published-mesh
geometry, including intermediate axial positions. Ingredient separation is a
measurement technique, not permission to omit any part from certification.

From the measured axial faces, the potential overlap gates in the actual
upper-stack travel coordinate q are upper disc q < −1.5 mm, lower disc
q > −3 mm, and the ring's driving-tooth height q > −2.1 mm. These are working
geometric hypotheses: box overlap is necessary, not a sufficient contact
proof, and any profile's axial invariance still needs direct measurement.

The native/mesh intermediate-height survey at shaft 169.6° also shows that
opening switches from the raised boundary at carry .25 to the later boundary
at .5; closing switches to the earlier lowered boundary between .5 and .75.
Linear interpolation between two endpoint envelopes would therefore need its
own geometry proof. No such interpolation is adopted.

An arbitrary one-turn cap, an assumed
20-degree copy of the ones envelope, and a silent swept clearance cut are not
acceptable substitutes for those measurements.

## Separating the three contact regions

The completed axial-invariance survey takes 129.552 s. At shaft phases 32°
and 169.6°, upper-disc boundaries agree through carry .64 and disappear at
.65; lower-disc boundaries are absent at .28 and agree from .3 through 1;
carry-tooth boundaries are absent at .5 and agree from .51 through 1.
The brackets agree within one 0.00000763-degree measurement interval.
This supports the three axial gates above at the sampled phases; it is not
a global continuous-contact proof.

The native upper and lower indexed-band measurements agree at all five
source flats. Applying the 20° station transform to the existing upper-disc
profile is now checked against the **complete raised T07 prints**:
1,888/1,888 faceted and 1,888/1,888 native boundary samples pass, with zero
positive common volume. This validates that particular reuse, not the
lowered stack or the other result/counter stations.

The new axial action-order test prepares the retained 169.6° shaft at crank
145.1°, then requests full lowering. Before the restraint it fails because
the request completes instead of stopping at carry-latch travel 2.1 mm.
In the same run all eight ordinary three-turn cases pass (raised/lowered,
digits 0/3/9 and lifted zero): two tests, one expected failure, 5.739 s.
The future constrained diagnostic is `HigherResultLocking`; its source
fixture remains `HigherResultActionOrder`. The original two-channel red
fixture established the missing behavior, but its ones-only restraint is
not silently relabeled as a higher-stack implementation.

`compile_higher_locking_profiles` produces a **candidate**, never acceptance:
native lower-disc boundaries and the two adjacent carry-tooth contact strips
are measured separately for all five source flats. Charts overlap at indexed
seams to avoid admitting contact there. The compiler asserts contiguous
measured support and records every unresolved strip birth/death bracket;
between-knot admission and complete native/mesh contact remain mandatory.
Neither T07 nor this candidate restraint is adopted in `OperatingCurta`.

## Candidate restraint and independent rejection checks

The dense native survey completes 181 shaft phases per ingredient pair
(−16..344° at 2° spacing), plus 20 local lower-disc refinements, in
1,491.005 s for the two main pairs. The first generated candidate passes
the four action-order tests in 85.413 s, including both short/long stops,
axial entry and eight ordinary three-turn cases. Adding exact replay,
reverse relief/idle/retry and complete-print stop/overtravel commons gives
five passing tests in 142.070 s. The physical negative controls force an
additional .2° bell rotation and require positive volume in both kernels.

This behavioral success does **not** adopt the first table. Its initial
complete-print coarse admission check passes 374 native samples but fails
six mesh samples at lower-disc opening. The `higher_lower_openings` tool
therefore brackets release using the actual complete published prints at
all 190 measured non-indexed/refinement phases; the compiler takes the later
of the native and mesh release, preserving the .1° free-side stand-off.
The resulting table passes 5,203 faceted knot/midpoint/support-edge checks
at full lowering and 2,052 more across carry .28/.3/.5/.51/.64/.65.

The denser native check of the **first**, native-only opening table also
finds an isolated Boolean blind spot at shaft 160°, crank exactly 30°:
both native ingredient and complete-print commons report zero, while the
published mesh reports 0.5034500144 mm³. Native contact is 0.4837292908 mm³
at 29.999° and 0.4828411747 mm³ at 30.001°. Thus the sampling/bisection had
mistaken that isolated zero for release and admitted neighboring contact
at shafts 159–161°. Component inspection confirms the same lower-disc /
pentagon pair, not a missing fourth restraint. The measured mesh release
31.0016745329° already corrects this knot in the combined table. Native
verification of the combined table remains a separate gate; no Boolean
zero, passing action-order test, or single kernel certifies it by itself.

The unchanged ordinary source trajectories also pass 79,310 half-degree
admission samples (five flats, eleven tooth counts, both carry seats) in
130.595 s. This checks against false jams; it is not collision acceptance.

An isolated full-tree `HigherOperatingTrial` now carries T07 and the refined
bell mesh while retaining all production inputs, carry levers, paths and
restraints. Its actual raised and carry-lowered stop tests are run red before
adding the candidate bound. The manifest and `OperatingCurta` are unchanged.

## Completed diagnostic acceptance and actual-carry blocker

The combined release table completes **5,203/5,203 native and 5,203/5,203
faceted** full-lowering admission checks, including knots, midpoints and
support seams. Both representations also pass **2,052/2,052** intermediate-
height checks. Ten retained raised/lowered cases covering all five source
flats on later revolutions pass short and unsplit long requests (198.045 s).
These finite checks do not settle the carry-tooth support-edge interpolation:
separate birth/death measurements now refine each original 2° support bracket
to less than .0001°, with near-edge curves still being checked before adoption.

The isolated browser matches Python stops **145.22323837279146°** raised and
**144.9514572141925°** lowered. Both short/long requests, exact replay,
relief/idle/retry and all eight legal three-turn cases pass, with no page
errors. Export SHA-256 is
`3415ba04e5ca46ea8efeed9f8f46c16af426dff79eaf80dcacf6821fc5292938`,
viewer bundle `8acaf5989e5fa99bb5f3314c2080016603893ca8e665569a4d707ff24f8de751`.
The stopped screenshot was inspected with the drum hidden. Two earlier
invocations passed motion checks but failed screenshot setup because the
test used the wrong visibility-path form; the corrected complete invocation
passes. This was a test-script error, not a viewer fix.

The full-tree T07 tests first fail **2/2 red** (264.029 s): raised withdrawal
and actual carry then withdrawal both complete instead of stopping. Adding
the candidate constraint gives **one pass and one error** (618.351 s), not
a green operating adoption. Raised withdrawal, replay, long request and
relief pass. The carried case fails earlier, on normal preparation of input
9 followed by a single 360° request: the engine raises `LandingInvariantError`
while evaluating the first real carry lever inside constraint observation.
No completed turn, geometry acceptance or whole-machine completion is claimed.

`carry_constraint_repro.py` removes CAD while retaining the actual source
shaft, dial and self-reading lever laws. The unrestricted 360° request passes
in .866 s; adding the measured restraint reproduces the same error in 16.497 s.
An initial reduction using linear dial bindings failed even without the
observer, so it was rejected as insufficiently faithful; the current fixture
uses the real dial laws and distinguishes the two cases.

Read-only traceback inspection identifies a mixed moving threshold: the lever
changes from −3.0518676393442643 to −3.051867639344261 mm at the cut, but the
comparison crosses in the opposite relative direction. The current landing
walk chooses its search direction from the lever's positive displacement and
cannot find the previous branch even after 200 doublings. This is an engine
finding, not clearance, source-print interference or permission to change the
carry law. `test_carry_constraint_repro` keeps the expected-completion test red;
the actual-root test remains the empirical acceptance gate. Upstream CAD,
production geometry, production constraints and the manifest are unchanged.

The full-tree export reproduces the same failure in the isolated Chromium
worker using viewer main `e82b521` (bundle hash above). Input 9 completes;
the single 360° request raises the landing invariant and leaves the entire
snapshot unchanged, with crank still at 0°. No page errors occur. The exported
assembly screenshot was inspected; it shows the requested input and unchanged
crank, not a completed carry. Evidence is
`_build_higher_operating_trial/carry-browser-acceptance.json` and
`_build_checks/higher-t07-operating-browser-red.log`. Thus both executors need
the scoped correction; a Python-only pass cannot close this gate. The proposed
framework cycle is `mixed-threshold-landing`, based on `e63700e`. The pilot
subsequently ratified the explained direction correction and local integration
after acceptance; its planning commit is `3a51345`. It is not integrated.

The first direction correction passes 163 selected framework tests and 653
subtests, including prior running and clocked conformance. Both the faithful
reduction (one pass, one error, 24.042 s) and the complete source-backed trial
(one error, 259.694 s) get past the original landing failure but then raise
`UnsupportedLaw` during the same ordinary carry preparation. On a pin-following
branch the contact level should stay zero; round-off produces
+2.220446049250313e−16, leading the branch decision to mistake following contact
for a sliding mode. An independent affine reproduction fails on unmodified
framework main as well, so this second fault was not introduced by the first
fix. No tolerance, carry law or geometry is changed to bypass it. An extension
of the correction was explicitly approved by the pilot on 2026-09-21.
The amended framework planning commit is `5673d1f`; the matching viewer's
planning commit is `f77dab4`. Acceptance, archival and integration remain
gated on passing the complete Curta and browser checks.

The precision correction uses an exact algebraic zero-motion certificate,
not a clearance epsilon: a contact whose relative position is provably
constant cannot depart just because a point evaluation rounds differently.
Continuous profile knots are split at their exact algebraic crossings;
uncertain/curved cases retain the existing execution and refusal rules.
The faithful unchanged-law reduction now passes both tests (54.046 s).
The full exported trial also completes the input-9/single-360° request in
the corrected browser worker with no page error. The inspected screenshot
shows crank 360°, the original complete tree and its visible number rolls.
Full withdrawal/relief/replay and final repository regressions are still
being validated. No physical-print modification follows from this software
finding; T07 and the other mechanical trials retain their separate gates.

## Near-edge sampling tool correction

Both native and faceted measurements bracket all ten carry-tooth support
edges to less than .0001°; the native flat-0 birth bracket is
22.2406494140625–22.24072265625°, and death is
49.1064453125–49.10650634765625°. Repeated source flats retain their own
measurements, not a symmetry assumption.

The first dual near-edge curve run stops at shaft 49.1044453125° because the
complete mesh has **four** disconnected grazing-contact intervals within
158.9680519104–160.1480800629°. The tool incorrectly assumed at most one.
Four focused tests give three failures before correction and four passes
afterward: preserve disjoint contacts/free gaps, union overlapping brackets,
retain mesh-only islands, and retain native coverage where it really exists.
The corrected tool unions measured intervals rather than taking their convex
envelope. It keeps both kernels' raw boundary lists in every record. The
downstream two-tooth compiler still refuses unsupported extra branches; it
does not silently collapse them. This is a measurement-tool fix, not a change
to collision tolerances or print geometry. Actual near-edge remeasurement and
candidate-profile regeneration/acceptance remain open.

## Software gate closed

The [integrated engine acceptance](mixed-contact-engine-2026-09-21.md) records
the completed correction in both executors. The final full-tree Python tests
pass **2/2 (1145.059 s)**; actual browser carry, raised/carried stops, replay,
long requests and relief also pass. All 213 bank coordinates match exactly
in four stopped/relieved states. The measured geometry and carry laws are
unchanged by the fix. T07 and the near-edge profile work above are still
provisional; this result is not production higher-bank adoption.
