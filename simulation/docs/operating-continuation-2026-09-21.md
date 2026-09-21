# Operating Curta continuation after the fresh-agent handoff

The active objective remains completion of the operating Curta under
`simulate-the-curta`. This is incremental evidence, not delivery or a waiver
of any of the eleven unchecked tasks. The production tens restraint is not
yet adopted at this checkpoint.

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

The manual-calibration case has now completed successfully. The process has
advanced to subtraction/borrow and addition undo; the later independent-input
and successive-addition case is still queued. One passed case is not the
three-case adoption gate.

A separate bounded diagnostic queues an empty 360° turn over two seconds
on `Sim(HigherOperatingTrial(), dt=.1)` and runs only its first .1 second.
Initialization takes 11.216 s and that first step takes approximately
53.330 s: the physical crank reaches −18° (driver +18°), with the longer
request still active. Log: `_build_checks/higher-timed-first-step-diagnostic.log`.
This establishes substantial per-step execution cost, not an arithmetic
pass or proof that every later step terminates. The original three-case
acceptance process is left uninterrupted. An optional debugger attachment
was unavailable in the host and did not alter the process.

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
The complete hundreds-station mesh profile passes as recorded below; its
native counterpart remains pending.

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
Its native counterpart is still running, logged separately as
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
