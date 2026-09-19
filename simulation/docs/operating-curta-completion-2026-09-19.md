# Operating Curta completion

The pilot resumed the direct-operation roadmap on 2026-09-19 and requested
completion task by task. Work belongs to the existing project-owned
`simulate-the-curta` change. The clocked model remains a separate sibling;
its successful requests do not complete running-model acceptance.

Starting project: `a6e6a9f`, `direct-operation`, clean. The current manifest
already selects `operating_curta`; older records calling it an unpublished
development root are historical, not the current model selection. Selection
does not certify the outstanding mechanics.

## Order of work

1. Retained anti-reversal pawl and measured crank backlash.
2. Counter reversing lever: establish engagement before adopting a stroke.
3. Measured crank, selector, carriage and clearing restraints.
4. Printed clearing-loop deployment and retention.
5. Complete retained arithmetic, shifting, clearing and action-order matrix.
6. Hosted and standalone pointer operation, replay and performance evidence.
7. Remaining whole-machine interfaces, mutation checks, demonstration sweeps,
   both geometry kernels, snapshots, documentation and OpenSpec completion.

## Ratchet, in progress

The initial rerun reproduced both original red diagnostics. Repeated reverse
requests returned the crank from -10 degrees to zero instead of stopping at
-9.342758620689654 degrees. Reverse backlash reopened the pawl to
3.7428274021352315 degrees rather than retaining its 1.006-degree seat.
The other six contact-law and lift-limit tests passed.

The candidate uses the measured release stations, including the shortened
closing interval, and the native probe's `release - 0.2` free-side stop.
It compares and returns each same represented stop to avoid losing a captured
tooth through floating-point angle/pitch reconstruction. The bound also reads
the actual pawl: a not-yet-released tooth must not capture the crank early.

The pawl retains its own angle. Its finite return crosses the measured seating
angle; a gated, unused continuation below that angle makes seating a crossing
rather than a tangential touch. No physical motion below the seat is intended.
Backward travel through the release interval cannot reopen a seated pawl.
The ordinary pose bench is preserved separately for its existing contracts.

Both original diagnostics and the four contact-law tests now pass (6/6).
The wider sweep then found a shortened-tooth error: reverse travel past its
release lowered the pawl to 0.932935053381 degrees. Applying the regular tooth's
free window to the shortened interval resumed the preceding ramp too early.
The shortened interval now uses its own 3-degree span. Its return-height
selection also switches only where the return contribution is zero.

The retained-path native geometry check passes (1/1, 89.70 s): sampled forward
return and reverse seating at seven regular/closing stations, with clearance
at the admitted stop and contact another .001 degree into the tooth. The
earlier faceted and exact failure at the shortened interval was a real law
error, not a tessellation disagreement. The all-tooth repetition/replay and
contact-law/lift-limit suite now passes (10 tests, 869.662 s), including all
117 teeth across two revolutions. The integrated partial-crank and exact
snapshot/replay test passes (175.968 s), and `machinome build operating_curta`
succeeds. The complete `running_pawl.py` geometry regression now passes on both
kernels: 8/8 faceted (74.98 s), 8/8 native (121.09 s), including the original
pose/mount/spring regressions and the retained return/reverse checks. Logs are
`_build_running/ratchet-{faceted,native}-resumption.log`. Visual inspection and
the whole-machine regression remain outstanding.

## Mutation verification — task 2.3 complete

Both `drive.py` contracts and both `input_mesh.py` contracts passed before
mutation. Mutating the drum's joint axis from Z to Y failed its world-vertex
quarter-turn check (92.550209 mm maximum error). Changing the first selector's
relation from 6 to 5 mm per digit failed the independent 54 mm travel check
(9 mm error). These independent changes affected separate contracts. Adding
10° to the input-pinion phase failed both full passage and the .1° free-play
check (.059257 mm³ overlap at the latter).

All three implementation mutations were reverted with no changes left in
either implementation file. Both modules then passed again: 4/4 faceted and
4/4 native. Evidence logs are `_build_running/drive-mutation-{baseline,red,restored}.log`,
`input-mutation-{baseline,red,restored}.log`, and `{drive,input}-native-resumption.log`.
The geometric tests are not claims about whole-machine integrity or reverser
engagement. Task 2.3 alone is complete.

## Carry and calibration — task 3.3 complete

The retained `OperatingCurta` passes the manual's successive 0, 1, 9, 90
entries: results 0, 1, 10, 100 and counters 1, 2, 3, 4. The second scenario
subtracts one from zero, yielding eleven result nines and six counter nines,
then adds one to overflow both complete banks back to zero. Both tests pass
in 515.872 s (`_build_running/carry-running-resumption.log`). They issue actual
physical requests; neither initializes a register nor uses the pose calculator.

Multiplying the production `lever_motion` drop by zero makes the actual-slider
latch test fail by 4.2 mm. After restoring the law, all four running contact
tests pass in 3.254 s. Separately, changing the first bevel dial's offset from
3° to 13° fails both geometry contracts, including 1.776938 mm³ interference
at the .1° free-play check. Restoring the phase gives 2/2 faceted and 2/2 exact
passes. Logs: `carry-latch-mutation-{red,restored}.log` and
`bevel-phase-{baseline,red,restored,native}.log`, under `_build_running/`.
Neither temporary mutation remains in implementation. The bevel mutation is
an isolated physical-phase proof, not a new whole-bank clearance certification.

## Counter-reversal decision

The unchanged 12 mm source-stroke diagnostic was rerun on the faceted kernel:
full-turn clearance passes, but driving engagement fails at crank 101.25
degrees (1/2). The same native failure is recorded in the earlier checkpoints.

The diagnostic bench now exposes its pinion relief as a structural parameter,
without changing either sibling's geometry or adopting a new operating stroke.
At **9 mm stroke and .37 mm flank relief**, its complete nominal passage and
three one-sided driving-contact checks both pass:

- Faceted: 2/2, 20.31 s.
- Native: 2/2, 4.66 s; log `_build_running/reverser-9mm-037-exact.log`.

This proves the isolated higher-counter interface, not the first counter's
complete stack, all six channels, both crank modes or the yoke/shaft fit.
The source reversing shaft's two detents are 12 mm apart. The earlier proposal
to correct those detents was withdrawn after the pilot pointed out the working
physical build. It is **not authorized and not justified by this bench**:
the bench starts from the existing +4.5 mm normal-counter assembly assumption,
not a validated lever/ball/spacer/frame assembly. No detent geometry is changed.

### Assembly-video investigation

The pilot supplied the author's assembly video (`zh2Z11miQ0w`, uploaded
2017-07-24). Local frames at 17:05–18:35 and 22:45–26:30 show the shaft,
ball, knob/yoke and two sliding spacers being assembled, and the yoke capturing
the counter gears. The inspected arithmetic sequence near 44:35–46:29 shows
ordinary addition, not a measured counter-reversal stroke. Automatic captions
are supporting evidence only. The user's MP4 stays untracked. External video
analysis was abandoned at the pilot's direction; no Bailian analysis resulted.

The present STEP/STL export is from 2022-03-31 (`d9d3491`). Its parent has no
CAD files, so local history cannot identify the geometry used in the filmed
2017 build. The date difference is a provenance gap, not proof of a revision.

Independent source STL vertex checks agree with the STEP's 12 mm detent spacing,
15 mm upper spacer and 42.4998 mm lower spacer. The upper drum's nine-tooth
band is Z -49.7..-48.2 mm in the unchanged source frame. The 1.685 mm yoke slot
captures a 1.5 mm pinion, leaving .185 mm total axial play.

Exact solid contact checks with the current source placements give upper and
lower spacer/frame stops at knob displacements +3.9575 and -7.6927 mm from the
exported pose (11.6502 mm apart). Displacement .0001 mm through the lower stop
produces .0058630967 mm³ interference; +.0025 mm through the upper stop produces
.1632842782 mm³. These are spacer-envelope limits, not a validated operating
stroke; other neighbours and ball seating must also be checked. The source
upper detent centre would require +5.1575 mm, beyond the upper frame stop by
1.2 mm. At the lower centre (-6.8425 mm), even the most favourable slot play
leaves the higher pinion .3075 mm below the nine-tooth band. Neither result
establishes that the physical build is defective. They show why a complete
assembly bench is required before selecting positions or changing geometry.

The new `reverser_assembly.py` diagnostic includes all six counter-input stacks,
both drum halves, the source lever/shaft/ball/spring and both frame stops.
Its independent gear and knob heights deliberately expose the current model's
disconnected placements; they are not a proposed operating control. Three
acceptance checks fail on both kernels: the current +4.5 mm gear position is
not captured by the unmoved higher-counter yoke, moving the complete knob to
+4.5 mm intersects the seated upper spacer (21.846211 mm³ exact), and a pinion
at the lower detent does not meet the complement row's driving flank. The last
check rotates the tooth ingredient about its own shaft, not the world-framed
fused stack. The native tests all fail on geometric assertions, not exceptions
from asking an assembly for a single exact solid. Logs:
`_build_running/reverser-assembly-red-{faceted,native}.log`.

The current operating root's exact integrity rerun passes connected-material
and one-solid checks but still fails housing-thread interference at
224.327505 mm³ (1/2, 36.94 s; `_build_running/operating-root-native.log`). No
epsilon, exclusion or accepted-overlap inventory has been added.

Continuation: preserve the red reversal engagement contract, establish the
complete moving assembly and its contacts, and continue independent roadmap
tasks while this source/assembly discrepancy remains unresolved.

## Retained pose binding — prerequisite corrected and integrated

The new `running_motion.py` bench uses the complete operating model and fresh
`Sim(..., meshes=True)` runs. Its subtraction test passes: both crank and drum
move 9 mm while the bell stays fixed. Its carriage and clearing tests fail
even though the command outcomes and run-bank coordinates are correct:

- After a 20° lifted carriage shift, the result dial's bank remains −146°,
  but its bound node coordinate becomes 20°. World vertices differ by up to
  3.274559 mm from rigid carriage transport.
- After a 90° clockwise ring request, its bank is −90° and the command is
  completed, but the bound clearing-ring coordinate is 0°. The plate does not
  rotate; its vertices differ by up to 86.967443 mm from the expected position.

The stronger coordinate assertions reproduce the mismatch without relying on
mesh tolerances (`_build_running/running-motion-binding-red.log`, 1/3 passing).
The original world-coordinate failures remain in `running-motion-baseline.log`.
No motion law or source part was changed to conceal these failures.

`simulation/tools/retained_pose_probe.py --minimal` reduces the problem to
three nested empty assemblies, two drivers and ordinary public revolute joints.
It imports no Curta geometry or laws. With the outer joint at 20°, the inner
joint's bank is 0° but its bound value is 20°; after commanding the inner joint
to −90°, its bank is −90° while the bound value remains 20°. The two acceptance
tests fail in 0.684 s:

```sh
python -m simulation.tools.retained_pose_probe --minimal
python -m unittest simulation.tools.test_retained_pose_probe
```

This is a framework prerequisite for trustworthy operating geometry, not a
request to redesign the Curta. The framework-only reproduction establishes
the violated public contract without inspecting or changing framework source.
A separate framework correction was required under the shop's
`framework-change` procedure. Its acceptance requires agreement between each
retained bank coordinate, bound joint and rendered pose after parent/child
movement and snapshot restore, with these Curta tests passing unchanged.

The other agent completed `bind-retained-coordinates-by-owner` at
`b9b64ddaf0bc1d51d715d3d971b77b6ee58880bf`. Independent verification reproduced
both minimal failures on framework `c62319e`, then passed both unchanged tests
against the candidate. The full Curta `running_motion.py` bench passed 3/3
faceted (22.69 s) and 3/3 exact (22.95 s). Its actual-world-mesh before/after
images were inspected: the dial preserves its local angle while its carriage
moves, and the clearing plate rotates with its retained joint. Restored poses
agree. Logs: `_build_running/owner-fix-verification-{faceted,exact}.log`.

With explicit pilot approval, clean framework `main` was fast-forwarded from
`c62319e1974b88d8cfd2dd13fd205c7bf2533991` to `b9b64dd`. Both minimal tests
then passed in the normal workspace environment (0.743 s), without a worktree
import override. No framework source was changed by this project, no project
workaround was added, and nothing was pushed. The retained-pose prerequisite is
resolved; the independent reverser, mechanical-restraint, full-clearance and
pointer-acceptance findings remain open.

All eight selectors also pass a new independent-input test, changing them in
nonsequential order while checking every shaft angle and both unchanged
registers (1/1, 11.227 s; `_build_running/all-selectors-running.log`). The legacy
calculator page and its README instructions are now explicitly limited to
`fast_curta`; the default remains the incompletely validated operating model.
Tasks 4.2, 4.3 and 6.1 are now complete as recorded below. Tasks 1.3, 5.x and
6.2–6.6 remain open. The change is not archived.

## Operating-motion mutations — task 4.3 complete

With the integrated framework, deliberately changing the subtraction drive
ratio from 1/9 to 1/10 produces 8.1 mm travel and fails the independent 9 mm
world-vertex contract by .9 mm. Changing the carriage drive ratio to .9 yields
18° instead of the requested 20° and fails the joint-angle assertion. Reversing
the clearing relation from −1 to +1 yields +90° instead of −90° and fails its
angle assertion. These affect independent test poses; all three fail (0/3,
23.44 s), rather than being hidden by the former binding defect.

All three mutations were restored without changing the tests. The unchanged
production relations pass 3/3 faceted (22.88 s) and 3/3 exact (22.82 s), using
the normal workspace interpreter. Logs are
`_build_running/operating-motion-mutations-red.log` and
`operating-motion-mutations-restored-{faceted,exact}.log`. No temporary mutation
remains in `running.py`. This proves these motion contracts, not interference,
flexible-part regression or mechanical interlocks.

## Retained flexible-part motion — task 4.2 complete

Two additional full operating-model tests follow the actual world geometry.
The carriage spring's lower cap and thrust ring rise through 1.5, 3, 4.5 and
6 mm, while its upper cap and sleeve stay fixed; a subsequent 20° carriage
shift leaves the positioning spring on its shaft. The clearing follower and
its spring are checked through a forward sweep and return: the upper cap
follows the pin, the lower cap and sleeve remain fixed, and pin/cover,
spring/pin and spring/sleeve stay clear at the sampled cam stations.

Disconnecting the carriage-to-positioning relation fails the first test at
1.5 mm. Disconnecting the pin-to-spring relation fails the second on an actual
5.917006 mm³ spring/pin collision. The other three motion tests still pass
(3/5, 33.57 s). Both mutations were restored; no production change is needed
beyond the integrated owner-binding correction. The full five-test module then
passes faceted (41.12 s) and exact (58.20 s). Logs:
`_build_running/operating-flex-motion-red.log` and
`operating-flex-motion-restored-{faceted,exact}.log`.

The independent positioning-spring module also passes 2/2 faceted (.83 s)
and 2/2 exact (.94 s), including valid compression geometry and both seats;
logs `operating-positioning-{faceted,exact}.log`. These augment the existing
full bell-spring subtraction/contact and clearing-stop cam regressions; those
geometries and laws are unchanged. The final all-node regression remains a
separate obligation. Task 4.2 covers measured motion and flexible seats, not
the source assembly's unresolved contacts, interlocks or pointer acceptance.

## Carriage stop pin — assembly fit and native-representation finding

The pin/frame bench separates this interface from unrelated root overlaps.
At the original insertion, rest clearance fails against both the STEP main
body (2.835309 mm³ native) and the author's printable main body (2.569035 mm³
faceted). A 6 mm lift clears it at every degree from 0° through 100° (2/4
checks pass, 3.47 s; `_build_running/carriage-stop-native.log`). This is a
source-assembly contact, not evidence for freezing carriage rotation at rest.

Manual page 39 specifies about 4 mm of bottom-pin exposure. The recentered
carrier's bottom is Z24.9 and the original pin tip is Z20.544410518, giving
4.355589482 mm exposure. The source contact probe brackets first clearance at
an upward seating adjustment of .455579281–.455579758 mm. The operating
carrier seats the unchanged pin .51 mm deeper, leaving 3.845589482 mm exposed
and at least .05 mm axial clearance. This is an insertion-depth fit, not a
new pin, a bored-out frame, or a new shift-lock law. Neither source file changes.

The bore-retention check exposed a separate native STEP limitation. Its bore
is R2.293 and the pin's cylindrical land is R2.195: .098 mm radial play. The
faceted check correctly blocks a .15 mm displacement; the native boolean
returns zero intersection even at 1 mm displacement. Independent world-solid
and unrotated source-pair probes reproduce this outside the running simulation.
For a .15 mm shift, points (-21.330728,16.553416,Z), Z=26,30,34, classify
inside both solids, while the common volume is zero. Both inputs and the
empty result report valid. Swapping operands and cleaning redundant faces
do not resolve it. The reproduction is `simulation.tools.carriage_pin_fit`;
this is not attributed to the corrected retained-coordinate binding.

The operating pin therefore uses the author's **unchanged printable STL**:
`STLs/39 - Clearing Stop Pin & Digit Axles/carriage body stop pin.stl`.
It is watertight, one body, R2.195 × 15 mm, volume 218.222802 mm³ versus the
STEP's 218.300286 mm³. `print_parts.CounterBodyStopPin` records this provenance.
This follows the existing source-print handling for the covers/collar; the
older pose and clocked carriers are not changed. **Pin-contact assertions are
faceted even under the exact runner. No native-solid acceptance is claimed
for this pin.** No intersection-volume epsilon or skipped contact is introduced.

The eight pin contracts pass with both frame representations: .05 mm axial
seat clearance; every degree 0–100° at lifts 0,3,6 mm; both out-of-range
barriers at −20° and 120°; unchanged pin height/connectivity; and .05 mm
radial freedom / .15 mm blocking along both horizontal axes. The initial
.05 mm blocking trial was an incorrect bore-clearance assumption, corrected
from the measured radii rather than a volume tolerance. Logs:
`_build_running/carriage-stop-print-{faceted,exact}.log` (8/8, 20.98 s and
2.36 s respectively; both use source-STL pin contacts).

Removing the .51 mm seating adjustment while retaining the source STL fails
six of eight checks (1.28 s), including real frame interference and the
independent tip-height assertion. Restoring it gives 8/8 again (2.79 s).
Logs: `carriage-stop-seat-mutation-{red,restored}.log`. No fit mutation remains.

The inspection-only pin/frame view omits surrounding carrier parts without
changing the test bench. The fitted rest snapshot was inspected; it shows the
pin within the annular frame channel. Task 1.3 remains open for the other
source/frame interfaces. The pin is an angular end stop, not by itself the
seated-carriage shift interlock. No new operating restraint is claimed.

After integration into the operating carrier, the five retained world-motion
and spring-seat checks still pass (5/5 faceted, 57.42 s), and a fresh
`machinome build operating_curta` succeeds. Logs:
`operating-motion-after-pin-fit.log` and `operating-build-after-pin-fit.log`.
The rebuilt source-STL pin/frame snapshot was inspected separately from the
earlier native-pin trial (`carriage-stop-fitted-print-rest.png`).

## Browser prerequisites — task 6.1 complete

The fresh operating build is a version-7 document. It mounts through the public
`MachinomeViewer.mount()` API with framework content
`b9b64ddaf0bc1d51d715d3d971b77b6ee58880bf` and viewer content
`2912006dd4864bc25aa4b7c0e11cd2e457dd5836` (API 21, unreleased 0.2.0).
The tested bundle SHA-256 is
`a5a5542762c3326aa53fa68875f7d3da698ae0253681366ba325528446afa614`.
The viewer's README still says Slide is absent; the installed bundle actually
loads all 24 declared controls, supplies projected/raycast gesture locations,
and exposes distinct lift/turn targets when the crank is hovered.

`python -m simulation.tools.operating_browser_probe` serves local artifacts
through Playwright routing, mounts the actual model in an ordinary host page,
then uses real mouse events at those public gesture locations. No state is
assigned to a register or driver. During the selected crank-lift drag, both
the input and actual crank lift read 1.3333333333333333 mm, while crank input
and joint rotation remain zero. After a public run reset **as independent test
setup**, dragging the first selector produces digit 1 = 3.3333333333333335 and
its actual shaft = 120°, with the other seven digits and crank at zero. These
are in-motion readbacks, not claims that a fractional digit is a seated detent.
All assertions pass and no page errors occur. The browser screenshot was
inspected. The first attempt's delay was an incorrect accessible-name lookup
for the test's Reset button, not a demonstrated mechanism-performance failure.

Logs: `_build_running/operating-browser-prerequisite.log` (mount/hover) and
`operating-browser-pointer-prerequisite.log` (the two gestures). The script
records bundle identity, public control descriptors, readback and screenshot;
it uploads nothing and leaves no server running. Task 6.1 alone is complete:
this is not the full all-controls matrix, wrong-order verification, standalone
export-page acceptance, sustained performance measurement or task 6.5.

## Earlier environment history

Framework content `df0bee4c7a5c727becf9ea33b7409ef796256a3d`; viewer content
`26c86df4557dae6392de1e2237acdf25328fe963`. The installed viewer reports API 21
and document versions 1–8. This removes the old version-support warning as a
current prerequisite, but does not establish actual operating-model pointer
acceptance. No framework or viewer source was edited.

At the retained-pose checkpoint, the framework still has that content HEAD;
its primary checkout reports pre-existing modified `docs/examples/metamaquina2`
and `docs/examples/v8-engine` entries. They were not changed or cleaned here.
The independently advancing viewer is now at
`2912006dd4864bc25aa4b7c0e11cd2e457dd5836`; no pointer or paired acceptance is
claimed for that newer content. The OpenSpec change validates strictly and
the legacy calculator's five JavaScript tests still pass. Those checks do not
waive any of the red mechanical or retained-pose contracts.
