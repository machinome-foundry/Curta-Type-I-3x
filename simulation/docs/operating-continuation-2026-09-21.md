# Operating Curta continuation after the fresh-agent handoff

The active objective remains completion of the operating Curta under
`simulate-the-curta`. This is incremental evidence, not delivery or a waiver
of any of the eleven unchecked tasks. The chronological entries below start
before production tens adoption; the later adoption and final arithmetic
results are recorded explicitly in their own section.

Environment: framework `c5ca365616251bd4649dc344cb7f00f97afdf832`, viewer
`a1ae12dc3ca7c09638898c22501542b123b78acc`. The framework head has advanced
through manual work since the handoff; its `machinome/` runtime tree is
unchanged from `9016f00`. No dependency is modified in this continuation.

## Arithmetic acceptance

The handoff's interrupted trial arithmetic gate is rerunning as
`_build_checks/higher-t07-trial-arithmetic-resumed.log`, against
`HigherOperatingTrial` through a temporary `unittest.mock.patch.object` of
the test module's `OperatingCurta`. The original interrupted log is preserved.
The complete arithmetic gate is not passed until all three cases complete.

The manual-calibration and subtraction/borrow with addition-undo cases have
now completed successfully. The independent-input and successive-addition
case is running. Two passed cases are not the three-case adoption gate.

A separate bounded diagnostic queues an empty 360° turn over two seconds
on `Sim(HigherOperatingTrial(), dt=.1)` and runs only its first .1 second.
Initialization takes 11.216 s and that first step takes approximately
53.330 s: the physical crank reaches −18° (driver +18°), with the longer
request still active. Log: `_build_checks/higher-timed-first-step-diagnostic.log`.
This establishes substantial per-step execution cost, not an arithmetic
pass or proof that every later step terminates. The original three-case
acceptance process is left uninterrupted. An optional debugger attachment
was unavailable in the host and did not alter the process.

The corresponding existing-production step was also measured: initialization
8.745 s, step 17.214 s, driver +18° / physical crank −18°, both registers still
zero and the longer command active. Log:
`_build_checks/operating-timed-first-step-baseline.log`. These are individual
observations under concurrent load, not a controlled benchmark or a diagnosed
framework defect. No framework change follows from them without its separate
authorization and cycle.

The pilot subsequently requested a separate framework performance
investigation. Read-only probes on framework `e6a42c80e6dcc686c180b8a6d94037301c4213a5`
(runtime tree still unchanged) reproduce a 57.752-second lightly instrumented
tens first step. About 97% is spent in the two moving crank restraint checks;
the lower constraint's dependency program includes a 31-member carry block
and is replayed at 65 sample points. The profiled existing/tens runs and the
lightly instrumented tens run produce exactly equal 213-coordinate banks.
Raw profiles and the external investigation report are retained under
`/tmp/curta-runner-profile-kkvxOQoU/`. This is attribution, not a speed fix or
an operating acceptance result. The dirty framework-primary gate prevents
opening a framework change without a separate decision; no executor,
sample count, contact law or project declaration was changed for the probe.

## Result-bank measuring fixture correction

The first bank-wide .16 mm trial revealed an error in the diagnostic factory,
not a new machine contact. `station_bench` generated every trial upper print
under the same class name and parameter identity. The ten source fusions
have different local placements, but reused the tens station's cached print.
At stations 2 and 3 the public `uniq_id`, artifact path and native bounds were
identical: X32.217137784..44.544997304, Z−39.0000001..−20.0999999 mm.

A new geometry contract compares each trial's complete upper solid against
that station's source upper. Before correction it fails at all nine later
stations (1 test, 9 failures, 3.845 s), including 478.006090863 mm³ of material
outside the source solid. The diagnostic now includes `source_station` in
its declared artifact parameters. The placement/material contract then passes
at all ten stations (9.623 s). No production part or upstream source changed.

The expanded contract also verifies one valid connected print, no added
material, positive removal bounded by the lockout's area times .01 mm,
removal confined to the locking ingredient, an untouched R4 keyed core and
preserved axial extent. It passes at all ten stations (14.163 s).

The initial trial contact batch was interrupted after this fixture defect
was isolated; `_build_checks/result-bank-trial-indexed-flanks.log` is invalid
machine evidence. Do not confuse it with the earlier **source** survey, which
uses distinct original classes and is unaffected. The corrected trial batch
passes 2/2 in 156.767 s:

- 100 indexed poses, ten stations × two seats × five flats, each checked
  natively and on the published mesh;
- 500 locking-flank poses, ten stations × five carry heights × five flats ×
  two directions, each checked natively and on the published mesh.

The source-fit indexed test deliberately remains red with `trial = False`;
the candidate is selected only by a temporary patch during acceptance.
`check_higher_locking_profile --station N` now permits the same dense profile
check against each station's own complete source-backed candidate. Its angles
are normalized by the existing measuring fixture, not by moving source pivots.
Dense profile admission and operating-bank adoption remain pending.

Logs under `_build_checks/`:

- `result-bank-fixture-identity-red.log`
- `result-bank-fixture-identity-green.log`
- `result-bank-fixture-material-green.log`
- `result-bank-trial-indexed-flanks-corrected.log`

## Intermediate-height mesh finding

The first dense hundreds-station admission sweep checks 23,556 poses across
carry fractions 0, .5 and 1. Both end seats pass; the intermediate seat has
199 positive mesh commons, all retained as failures. The largest is
1.823780742e−7 mm³ at normalized shaft 131°, crank 25.3366216485°. The original
handoff's 8,063-point dense check covered the lowered seat, while its other
intermediate checks sampled different poses. This is additional coverage.

The same opening reproduces on the tens fixture: native volume zero, mesh
volume 1.826214581e−7 mm³ when freshly posed at the contact angle. Varying the
measurement's reference angle and carry fraction (.49999, .5, .50001) retains
the discrepancy. The contact occupies X34.137151106..34.139354706,
Y−9.368464895..−9.360690970, Z−24..−23.930098002 mm. A new regression fails
all three carry cases on the mesh while their native checks pass (1.054 s).

Refining the **upper printed stack** to .01 mm linear / .1 rad angular
deflection, like the already refined bell, clears all three cases (19.706 s
including rebuilding). This changes no native solid, mechanical law or
contact threshold. Two other sampled residual commons also become empty.
The trial and bank measuring fixture use that refinement; it is not yet
production adoption. Six original fit contracts pass faceted (9.79 s) and
native (75.87 s). The expanded support/material suite passes 5/5 (65.928 s).
The complete hundreds-station profile passes on both kernels as recorded
below.

Additional logs:

- `result-station-3-profile-faceted.log` — pre-refinement, 199 failures;
- `result-bank-midseat-disagreement.log`;
- `higher-midseat-reference-probe.log`;
- `higher-midseat-opening-red.log`;
- `higher-midseat-opening-refined-upper.log`;
- `higher-midseat-common-dimensions.log`;
- `higher-refined-upper-fit-faceted.log`;
- `higher-refined-upper-fit-exact.log`;
- `higher-refined-upper-support-material.log`.

## Exactly planar common geometry

The refined hundreds-station sweep retains residual signed volume sums near
1e−15 mm³ at carry .5. Independent inspection finds an exactly planar common:
both Z bounds are **−31.5 mm**, with nonzero X/Y extents. For example,
normalized shaft −17.999°, crank 150° reports 1.262878691e−15 mm³ despite
having exactly zero thickness. Tens produces an empty common at that pose.

The contact measuring helper now recognizes zero spatial measure using exact
bounding extents: if an extent is zero, the intersection has zero 3D volume.
Empty intersections are recognized by their inverted bounds. There is no
length or volume tolerance, and all positive-thickness commons retain the
Boolean's volume. A new source-backed regression fails before this correction
(0.739 s); it then passes alongside a finite solid of approximately **1e−18
mm³** that must remain positive, both original full-root contact fixtures and
the generalized tens fixture comparison (5/5, 6.281 s).

This is a correction to the project's measuring instrument, not an exclusion
of a pair, an overlap allowance, a changed contact law or a framework change.
Raw values and geometric bounds are retained in
`result-bank-planar-common-probe.log`; red/green logs are
`result-bank-planar-common-{red,green}.log`. The independent recheck passes
all **230/230** residual poses, with exactly zero
native and measured mesh volume at every one; see
`result-bank-planar-common-native-recheck.log`. The clean complete faceted
sweep now passes **23,556/23,556** admitted poses, across carry 0, .5 and 1.
Its native counterpart has also completed with **23,556/23,556** passing;
the two logs are
`result-station-3-profile-certified-{faceted,native}.log`.

Fresh isometric and axial views of the refined tens trial at shaft 131°,
crank 25.3366216485°, carry .5 were rendered and inspected:
`_build_checks/higher-refined-upper-{iso,top}.png`. The complete bell,
source shaft and upper/lower printed stacks remain in their source frames.
These views establish assembly and pose; the contacts above are too small
for pixels to decide.

The final focused regression run passes **7/7 in 75.476 s**: all three
`ResultBankFixtureTest` contracts and all four `HigherSupportAdmissionTest`
contracts. Log: `_build_checks/continuation-fixture-support-suite.log`.
The original production bank clearance test remains red and is not included
in this scoped green claim.

The counter investigation then exposed a second factory identity issue:
non-rigid generated roots/channels shared SCAD artifact names despite their
distinct rigid children. The result factory's regression reproduces it
with three failures (2.414 s). Explicit station/fit identities now distinguish
all twenty source/trial roots and ten trial channels. The expanded fixture,
material, planar-common and original-tens parity checks pass **5/5 in
34.554 s**; logs are `result-bank-export-identities-{red,green}.log`.
No part, placement or law changed. The completed hundreds measurements use
the already corrected rigid children and are unaffected by this export fix.

A sequential batch has completed the refined tens station's faceted check:
**23,556/23,556** admitted poses pass. Its native check is running, followed
by faceted admission at stations 4–11. Logs use
`result-station-N-profile-certified-KERNEL.log`; only completed terminal
records count as passes. This is not bank-wide adoption.

## Further clearing-loop observation

Frames from the supplied assembly video were inspected over 36:00–38:50
(10-second samples), 38:20–38:58 (2-second samples), and 39:00–46:00
(30-second samples). They show the loop mounted during final carriage
assembly and later clearing use. They do not establish the intervening
clip/release motion or elastic deformation. The sampled evidence therefore
does not resolve the contact intervals in the existing loop investigation,
and no deployment control or geometry change follows from it.

Reproducible contact sheets are retained under `_build_checks/` as
`clearing-loop-assembly-video-overview.png`,
`clearing-loop-clip-sequence.png`, and
`clearing-loop-late-video-overview.png`. Their observations are not a claim
to have examined every frame of the video.

## Counter-side continuation

The [counter investigation](counter-lockout-investigation-2026-09-21.md)
adds independently calibrated source instruments for all six counter
stations. It records a new parked-indexed clearance failure on every station,
and a bounded T08 outer-skin candidate that passes indexed clearance,
protected-material and two-sided engagement checks. That candidate remains
isolated; no counter restraint or operating fit has been adopted.

## T07 arithmetic gate and default-root adoption work

The resumed `HigherOperatingTrial` arithmetic gate completes **3/3 in
8666.232 s**: page-53 calibration/carries, subtraction through both registers
followed by addition undo, and independent inputs with successive additions.
Log: `_build_checks/higher-t07-trial-arithmetic-resumed.log`. This replaces
neither the earlier interrupted log nor its recorded status.

The refined tens native admission check has also completed **23,556/23,556**
with zero failures, matching its completed faceted run. The sequential
remaining-result-bank batch has moved on to station 4; later stations are not
yet certified by this result.

Station 4's faceted check subsequently passes **23,556/23,556**. The mesh
queue continues through stations 5–11. Two native queues now independently
cover stations 4/6/8/10 and 5/7/9/11, aborting their own queue on any failure
and refusing to overwrite existing logs. They use the same
`result-station-N-profile-certified-native.log` naming. No remaining-bank
pass is inferred from a running queue or from the tens/hundreds results.

The handoff's production gate is therefore satisfied. The tested parts now
live in `higher_lockout_parts.py`; historical trial names alias those same
classes. `ResultShafts.tens` and `RetainedCarries.tens_bell` use the fitted
tens and refined bell. `OperatingCurta` owns the existing `higher_closing_limit`
bound, reading actual bell rotation, retained tens rotation and upper-stack
travel. The ones/pawl restraints, inputs, control paths and motion laws are
preserved. `HigherOperatingTrial` only inherits the default root; it no
longer redeclares the bound or substitutes a separate subtree.

The prior production red is still retained as `higher-t07-production-red.log`
(completed instead of blocked, 66.318 s). Production acceptance results:

- `tens-production-operating.log`: all three stop/free-support cases, with
  stopped/idle banks in `tens-production-python-acceptance.json` on completion.
  all three pass **3/3 in 2119.774 s**;
- `tens-production-arithmetic.log`: the same three arithmetic cases on the
  actual default root pass **3/3 in 10042.779 s**;
- `tens-production-ones-regression.log`: the unchanged ones/pawl stop,
  geometry, relief and replay test against the default root with the new bell
  passes **1/1 in 1403.527 s**;
- `tens-production-fit-{faceted,native}.log`: the six complete-print fit
  contracts; faceted has passed **6/6 in 34.87 s**, native **6/6 in 132.32 s**;
- `tens-production-build.log`: fresh default-root build to the isolated
  `_build_tens_production/` directory has passed, not the pilot's live Studio
  build. The standalone export to `_export_tens_production/` also passes
  (`tens-production-export.log`). The fresh browser run passes against the
  earlier trial's Python banks in `tens-production-browser-vs-trial.log`;
  all four new production Python banks also match exactly.

The fresh build's [document comparison](evidence/tens-production-document-comparison-2026-09-21.json)
preserves all 213 coordinates, 24 inputs, 25 controls and 608 descendant
paths from the previously accepted trial export. All 155 distinct referenced
model/marking assets exist and are nonempty. Drivers, instructions, controls,
bindings and the program's clock, coordinates, intermediates, spans, sources
and limits are exactly equal. All 273 edges are equal except their
`stated_by` class names (historical trial names become production names).
Program identity and geometry-piece identities change with those names;
neither is claimed byte-identical. This is a structural comparison, not
runtime or contact acceptance.

The [fresh browser evidence](evidence/tens-production-browser-acceptance-2026-09-21.json)
records completed carry preparation, raised/carried short and long stops,
exact replay, relief/idle and the free-support request to 506.3°. There are
no page errors. All 213 coordinates are **exactly equal** to the earlier
trial's Python banks at all four stopped/idle states; this is stronger than
the probe's threshold assertions and was checked independently on the saved
JSON values. The three fresh full-model screenshots were inspected:
`carry-preparation.png`, `carry-withdrawal-relieved.png`, and
`carry-free-support.png`, under `_export_tens_production/`. They establish
the rendered assembly, crank/selector poses and control readback, not Boolean
contact clearance or every physical-pointer interaction.

The viewer checkout has independently advanced since the handoff. This fresh
run uses viewer commit `1995aa1f58d44dfeea7bfa62502d71349891327a`, bundle
SHA-256 `5f3ec29aede4934106bb0cbbdaa7454dcec39d2ba04a233f431a4ce279fef610`,
and framework `e6a42c80e6dcc686c180b8a6d94037301c4213a5`. The exported document
SHA-256 is `fdd2442d49ec978556169fec8300f42f6d4f52924114ed686d0332aa552e384b`.
No viewer or framework mutation was performed for this adoption.

The [production Python banks](evidence/tens-production-python-acceptance-2026-09-21.json)
are now complete. All four 213-coordinate stopped/idle banks match both the
old trial and the fresh production browser **exactly**, checked independently
from the saved values. Production neighbouring arithmetic now passes all
three cases, including successive addition/selective clearing, in
**10042.779 s**. The [production arithmetic record](evidence/tens-production-arithmetic-2026-09-21.json)
pins the completed log and distinguishes it from the previously completed
three-case trial gate. This implementation step does not close any
whole-project task or adopt higher-result-bank/counter restraints.

Additional supplied-video samples at 42:30–43:30 and 43:30–44:30 (two-second
intervals), and 0:00–2:00 (five-second intervals), were rendered and inspected.
They show carriage/crank assembly and the opening drum assembly, respectively,
not a justified clearing-loop clip/release path. The source and unadopted
T05/T06 diagnostics are unchanged. Contact sheets are
`clearing-loop-crank-install-42m30-43m30.png`,
`clearing-loop-crank-install-43m30-44m30.png` and
`clearing-loop-video-intro-0m-2m.png` under `_build_checks/`.

## Isolated counter-ones operating checkpoint

The independent cusp-refined counter-ones law now passes both dense geometry
checks: **11,858 admitted poses per kernel**, zero positive commons. The
full-machine `CounterOperatingTrial` installs that measured upper print and
restraint without changing the manifest-selected `OperatingCurta`. Its
short/long withdrawal test passes in **1665.484 s**, including native/faceted
stop clearance, positive .2° overtravel contact, retained shaft, exact replay
and relief/retry. See the [counter investigation](counter-lockout-investigation-2026-09-21.md)
and [numeric checkpoint](evidence/counter-ones-trial-acceptance-2026-09-21.json).

Its first browser run timed out during the prepared-state screenshot before
either stop request; that incomplete report is preserved and not accepted.
A retry with a finite 60 s capture deadline passes both requests, replay,
relief/idle and retry with zero page errors; both screenshots were inspected.
The full 213-coordinate browser banks are preserved in the investigation's
linked evidence. The fresh Python report/idle test now passes in 1500.407 s;
all four stopped/idle banks match the saved browser values **exactly**.
The separate three-case arithmetic run is active. No ordinary-arithmetic
acceptance is claimed for this
isolated counter trial. Higher-counter coarse measurement completes three
sampled heights, but reveals height-dependent contact windows; higher-counter
operation remains unimplemented. No whole-project task is closed here.

## Remaining result-bank operating trial

The production hundreds-channel withdrawal now has a full-machine failing
test: a physically prepared partial shaft is left behind by its selector,
then the crank completes 190° through **.308686 mm³ native / .323536 mm³
faceted upper/bell overlap**, instead of stopping. The measured red and the
unadopted nine-station bound/print trial are recorded in the
[result-bank operating investigation](result-bank-operating-trial-2026-09-21.md).
Numeric station-frame/intersection tests pass and a wrong-sign mutation
fails. The full-root fixture exposed a missing axial normalization at the
five source stations whose raised raw travel is zero rather than −4.2 mm.
The corrected law and fixture now pass; all ten complete higher prints match
their independent benches and all initial bank values match production.
The trial's hundreds short/long test passes in 1112.808 s: both stops clear
in both kernels, .2° overtravel contacts, the shaft is retained, replay is
exact and relief/retry pass. The trial's eighth-input test also passes in
1166.542 s, preserving four complete 213-coordinate stopped/relieved banks.
The isolated export completes, but its browser mount fails before any
requests: loading 30,159 expression bindings resets the viewer's expression
pool while the validator holds an older root. The result-bank investigation
preserves the unmodified failure and bounded in-memory diagnostic. No package
source was changed; a separate viewer-owned change is requested but not yet
authorized. Faceted dense admission now passes at every result station 2..11;
native 2..7 have passed and 8..11 checks continue. The production
eighth-input test now fails as intended at 290°, with the positive common
preserved in the new evidence file. The manifest
and production restraint declarations remain unchanged.

Counter-tens component diagnostics now identify the distinct upper-disc,
lower-disc and carry-tooth contacts. A 40-pose complete-print survey and six
native/faceted axial brackets are retained in the counter investigation.
They show why neither a fixed-height ones law nor a single higher closing
curve covers the counter. No higher-counter operating law is adopted.
The combined component/axial/indexed-band/browser-validator/result-frame
regression passes **14/14 in 41.333 s**
(`counter-support-regression.log`).

The higher-counter lower-disc/carry-tooth split now has independent angular
measurements: 122 native component curves over all five shaft flats, plus
12 curves at intermediate heights. Their full-carry contact classification
agrees with both complete-print kernels at all 8,906 sampled positions.
Component records are explicitly rejected by the fixed-height whole-print
compiler; no operating law or geometric acceptance is inferred from them.
The combined probe/compiler/support regression passes 21/21. The counter
investigation retains the curves, endpoint volumes and finite-sampling limits.

The new higher-counter compiler and law remain isolated. Their first candidate
refuses known contacts but incorrectly blocks ordinary carry at five source
flat poses that both complete-print kernels prove clear. A finer scan reveals
the missed free interval behind those false stops. The
[candidate record](higher-counter-restraint-2026-09-21.md) preserves the rejection
and refinement. The completed 181-shaft fine scan now clears all four
numerical gates, including those five false stops, but the expanded faceted
complete-print check finds admitted collisions. Geometry acceptance remains
failed for that candidate and no operating restraint is adopted. Its faceted
sweep finishes with 40 failures in 15,519 poses, all preserved as regression
evidence. Complete-print boundary measurements identify a held lower-disc
endpoint; ten added edge curves now refuse those collisions without blocking
the five earlier free poses. The new isolated profile is under fresh geometry
verification. The old native sweep independently confirmed 16 collisions
before intentional interruption, with all partial evidence retained; a full
native sweep of the revised profile replaces it. Targeted native edge checks
pass 175 admitted poses. Intermediate carry-height checks now run in both
kernels, including the measured axial-support brackets on all five flats.
The revised counter-tens faceted sweep passes 15,714 poses and its separate
support-height sweep passes 7,094 in both kernels. The full native angular
sweep remains open. The first faceted transfer diagnostic passes 787/787/839/839 admitted
poses on counter stations 3/4/5/6; full station sweeps are queued. These
remain finite geometric checks, not bank-wide operating adoption.

The physical counter-tens withdrawal diagnostic now exposes an earlier
preparation stop: a 90°→180° crank request stops at 163.42595046793576° while
the counter-tens shaft remains at 114°, before the intended half-tooth pose.
Its native counter upper/bell pair is clear there. Attribution to the other
existing restraints remains open; a fresh full-bank/stop-report trace is
running without splitting the request or altering any law. The candidate
record preserves this finding separately from the passing geometry samples.

At the pilot's request, viewer-owned OpenSpec change
`keep-expression-references-valid` is prepared for approval, with proposal,
design, behavioral delta, tasks and pinned Curta mount evidence. Strict
OpenSpec validation passes. This is planning only: no viewer implementation
or framework mutation is authorized by that preparation request.

## Independent collar/rest-contact continuation

While viewer implementation awaits approval, task 1.3's collar contact was
measured against every other current rigid occurrence at nine diagnostic
heights. The unchanged operating model's 213-coordinate bank is preserved.
A .7 mm rise clears the spider mount but worsens thrust-ring interference
and retains nut/pin contacts; none of the tested rises clears all neighbours.
Full-stack and local-source sections were inspected, along with manual pages
44 and 48. The STEP and print sections agree visually at the suspect seats;
the STEP mesh remains non-watertight and is not used as contact evidence.
The [reproducible survey](collar-seating-investigation-2026-09-21.md) records
the rejected placement change and the source-fidelity/retention checks owed
by any subsequent local fit. No geometry, operating law, dependency or task
checkbox changed; this is not a replacement whole-machine inventory.
