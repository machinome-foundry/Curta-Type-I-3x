# Higher-counter restraint candidate

Status: isolated candidate, **lower-edge refinement under verification**.
The preceding fine-tooth candidate failed complete-print geometry. Not
installed in `OperatingCurta`, not a geometry certificate and not an adopted
counter fit. Tasks 6.2/6.3 remain open.

## Independent fields, not copied result-side profiles

The preceding [counter investigation](counter-lockout-investigation-2026-09-21.md)
records the complete-print contacts, separate axial supports and 122 native
component curves. `tools/compile_higher_counter_profiles.py` processes those
counter measurements, intersects both kernels' full-carry indexed bands and
keeps the complete faceted lower-disc release. It does not infer the lower
closing from a complete-print curve containing intervening teeth.

The existing contour-processing routines use a −16° shaft datum and 152° carry
centre. Counter readings are registered into that calculation chart by shaft
−130° and crank −52°, then returned to their original 114° / 204° frame.
Those shifts label measured branches; no result geometry, boundary coordinate
or contact volume is reused. All five source flats retain separate curves.
The resulting `higher_counter_locking_profiles.py` has five lower-disc sectors
and ten provisional tooth strips. Its source logs and hashes are embedded.

Three compiler tests fail first on the absent module, then pass in .006 s
(`higher-counter-compiler-{red,green}.log`). They check coordinate round trips,
source identity, missing mesh/band evidence and duplicate rows. A later test
exposes an unnecessary same-grid requirement between the two independent
fields. It fails before the compiler admits different tooth and lower-disc
sampling grids (`higher-counter-independent-knots-red.log`). Explicit
`--refined` inputs supersede named component/shaft readings and retain their
source hashes. The compiler/envelope/whole-print-compiler/interval regression
then passes **17/17 in .018 s** (`higher-counter-compiler-regression.log`).

`higher_counter_locking_laws.py` combines the counter upper-disc chart in the
tens frame with these independent lower/tooth fields. The measured nominal
raw-travel support planes are .9, −.6 and .3 mm, respectively; the independent
native/faceted brackets remain in the earlier evidence and are not claimed
identical or continuously certified. The explicit .1° angular stand-off is
unchanged. No collision-volume epsilon is added.

## Coarse compilation fails an ordinary carry

The law tests first fail on the absent module (`higher-counter-law-red.log`).
The first implemented run passes the measured positive-endpoint refusals and
distinct-support/free-interval checks, but **fails ordinary source-path
admission** at crank **206.5°**, shaft **166°**, full carry, first flat, zero
direct-input teeth. The candidate reports a positive gap (about 2.1), blocking
a legal carry (`higher-counter-law-first.log`, 3.404 s). This result is not
described as passing just because it refuses known contacts.

Independent complete-print probes find **exactly zero common in both kernels**
at that pose, and at shaft phases **238°, 310°, 382° and 454°**. All five are
false stops. The [rejection evidence](evidence/higher-counter-coarse-profile-rejection-2026-09-21.json)
pins the profile/law hashes, complete-print readings and source logs. A dedicated
numeric regression retains all five free poses and fails five assertions on
this candidate (`higher-counter-measured-free-poses-red.log`).

At shaft 168°, the original five-degree grid sees contact at both 205° and
210° and misses the real free interval **205.4273996°..207.4433498°**. Its
single recorded contact interval becomes a false bridge in the interpolated
candidate. At shaft 166°, independent native ingredient brackets place the
free interval at **205.2221816°..207.1262279°**, consistent with both complete
prints clearing 206.5°. These are finite measurements, not continuous proofs.

The component probe now accepts extra angles while keeping its base grid.
A test fails first on the unsupported argument, then all four sampler tests
pass in .005 s (`counter-extra-angles-{red,green}.log`). The new tests retain
both a narrow positive island and a narrow free gap, and reject invalid extra
angles. Four diagnostic curves use quarter-degree samples over 190°..220°
(`higher-counter-tooth-fine-angle-diagnostic.log`); their boundary records are
preserved with the rejection evidence.

A broader refinement completed in `higher-counter-tooth-fine-grid.log`:
shaft 114°..474° every 2°, with the same quarter-degree tooth-window samples
and five-degree whole-revolution grid. The four completed diagnostic shafts
were omitted from that job and merged explicitly at compilation: 181 unique
shaft readings cover the complete two-degree grid. The resulting profile
SHA-256 is `ad255b61cc1c6b3ea252ff13c0f7357c4e6c727e4c63576a4bff2fc1615afffd`.
The law is unchanged. All four numerical gates now pass in 31.477 s
(`higher-counter-law-fine-grid.log`): the five measured false stops,
positive component endpoints, separate supports and 21,630 ordinary
source-path samples. This does not certify complete-print clearance.

The new `tools/check_higher_counter_locking_profile.py` checks admitted poses
against complete counter-tens bell/upper prints, not ingredients. It includes
knots, midpoints, support edges and the recorded rejected poses, with optional
independent one-degree shaft/five-degree crank grids. Its three tests fail on
the missing module first, then pass **3/3 in .024 s**, including a 1e−20 mm³
positive common and non-finite/negative measurement refusal
(`higher-counter-sampling-{red,green}.log`). The first bounded check covers
shafts 116°, 166° and 168° at half/full carry: **41 admitted poses per kernel**,
zero positive commons (`higher-counter-coarse-admission-{native,faceted}.log`).
This does not clear the known false stops: rejecting safe travel can pass an
admission-only test, which is why the separate free-path gate was required.
The combined sampling/compiler/envelope/interval tool regression passes
**20/20 in .034 s** (`higher-counter-validation-tools-regression.log`). It
does not include the separately reported candidate law tests.

The fine-tooth candidate's expanded faceted check completed **15,519 poses
with 40 admitted collisions** in `higher-counter-fine-admission-faceted.log`.
Its native sweep was later interrupted after independently confirming 16
collisions under that original profile identity; it is not a completed pass.
The [rejection record](evidence/higher-counter-fine-profile-rejection-2026-09-21.json)
retains all 40 poses and source/log hashes. A dedicated numerical regression
fails all 40 assertions before further profile changes
(`higher-counter-complete-collisions-red.log`, .091 s). Neither an incomplete
native run nor the earlier bounded check overrides these failures.

## Lower-disc edge refinement

The failures lie at shaft 182°/183° and the corresponding positions on all
five flats, near crank 98°, at half and full carry. The coarse lower-disc
table's last knot is 180°, held constant through the sector end at 183.3059°.
Complete-print bisection shows that the release continues moving: the first
flat's faceted free-side bracket is 98.1383247° at shaft 180°, 98.2961426° at
182° and 98.3692245° at 183°. The .1° stand-off on the held endpoint therefore
does not cover the omitted curve. Both kernels confirm that direction;
[30 complete-print brackets](evidence/higher-counter-lower-release-2026-09-21.json)
retain the positive/free endpoints across all five flats. No common-volume
epsilon or geometry change is introduced.

Ten native lower-disc component curves and ten complete-print faceted curves
at shafts 182, 183, 254, 255, 326, 327, 398, 399, 470 and 471 are now measured
and retained in the [edge evidence](evidence/higher-counter-lower-edge-curves-2026-09-21.json).
The tools are `counter_component_envelope --station 2 --carry 1 --trial
--component lower_lock` with repeated `--shaft`, and
`counter_locking_envelope --station 2 --carry 1 --trial --kernel faceted
--step 5 --shaft <value>` for each shaft. The native diagnostic uses its
default five-degree crank grid; the earlier quarter-degree tooth curves stay.

The compiler's `--refined` input now includes
`higher-counter-lower-edge-component-curves.log`. Its complete-mesh input
`higher-counter-lower-complete-merged.jsonl` concatenates the 61 existing
full-carry faceted rows with the ten new complete curves, retaining station,
shaft, carry, trial, kernel and boundaries. Both original logs and the new
measurements remain preserved; the merged input does not invent a boundary.
The emitted profile SHA-256 is
`c24f22af55a86e7419ca417e03a829c6287934566d75f18de52891e4103f5816`.

All 40 recorded collision refusals and the five earlier free poses pass on
this profile; the full law regression passes **5/5 in 43.147 s**, including
21,630 ordinary source-path samples
(`higher-counter-law-lower-edge-refined.log`). The revised candidate's complete
configured faceted sweep passes **15,714 admitted poses with zero common**
in `higher-counter-lower-edge-admission-faceted.log`. This finite check is
not native or operating acceptance. The checker now retains collision evidence even if
later profile knots move: its new retention test fails first, then the
sampling/compiler/component group passes **12/12 in .063 s**
(`higher-counter-failure-retention-{red,green}.log`).

The new native edge-only check completes **175 admitted poses, zero positive
commons**, at those ten shafts and half/full carry
(`higher-counter-lower-edge-admission-native-targeted.log`). This is targeted
validation, not the full native matrix. The old native sweep used the
earlier fine-tooth profile and independently reproduced 16 collisions. It
was intentionally interrupted after rejection was established; its
[partial evidence](evidence/higher-counter-fine-native-profile-rejection-2026-09-21.json)
preserves all observed failures, the last progress row and interrupted log
hash. A full native sweep of the revised profile now runs as
`higher-counter-lower-edge-admission-native.log`. Neither run's results may
be attributed to the other's profile.

## Axial-support admission checks

The checker's optional `--support-heights` matrix retains quarter/three-quarter
carry, both sides and the midpoint of each independently measured native and
faceted axial bracket, and the nominal −.6/.3/.9 mm support planes with
±.001 mm samples. The former default 0/.5/1 heights remain unchanged; explicit
`--carry` cannot be combined with this option. A missing-helper test fails
first, then all **13 sampling/compiler/component tests pass in .047 s**
(`higher-counter-support-sampling-{red,green}.log`). The header now also pins
the checker and support-evidence hashes.

Both kernels are checking these heights at twenty actual counter-tens shaft
positions: 114, 156, 166 and 182 degrees, repeated at each of the five flats
with 72-degree offsets. These include the indexed flat, the mixed-contact
region, the earlier false-stop pose and the lower-disc edge. Each tests the
existing angular grid and all applicable profile boundaries. Logs are
`higher-counter-support-heights-{native,faceted}.log`. Faceted completes
**7,094 admitted poses, zero positive common**; native remains running.
The [scoped geometry record](evidence/higher-counter-lower-edge-admission-2026-09-21.json)
pins each completed run's actual header, summary, source identities and log
hash. These finite poses do not establish height-independent clearance or
prove the other four higher-counter stations.

## Other higher-counter station frames

The measuring CLI now accepts `--station 2..6`. It measures each complete
source-backed station, not a rotated tens surrogate. All five higher counter
channels declare the same raw axial law, −1.8 + 4.2 × carry, in
`standard/channels.py`. The measured input/carry timing advances 20° per
station while the indexed shaft phase retreats 20°. To ask the tens-frame
candidate at station N, only its numeric query is registered by
crank − 20(N−2), shaft + 20(N−2); the geometry reader receives the original
machine crank and shaft values. This is a transfer hypothesis to challenge,
not a declaration that the source bodies are identical.

The frame test fails first on the unsupported station argument, then all
**14 sampling/compiler/component tests pass in .115 s**
(`higher-counter-station-chart-{red,green}.log`). It checks all five offsets,
the unchanged geometry-query pose and rejection of ones/out-of-range
stations. The faceted diagnostic at stations 3..6 passes carry 0/.5/1 and
the same twenty chart positions per station: **787, 787, 839 and 839 admitted
poses**, respectively, with zero positive common. The
[station evidence](evidence/higher-counter-later-stations-faceted-2026-09-21.json)
pins the per-station headers and summaries of
`higher-counter-later-stations-faceted-diagnostic.log`. This does not replace
the per-station full matrix, other heights or native verification. Full
configured faceted sweeps are now queued in station order 3..6 as
`higher-counter-station-N-admission-faceted.log`; the queue stops if a station
fails rather than treating its successor's result as a substitute.

## Remaining acceptance

Complete the new candidate's whole-print checks and investigate every failure.
Retain the now-passing five pinned false stops, measured contact endpoints
and ordinary source tooth paths as regression gates. Challenge both
complete-print kernels between profile knots, at support edges and at
intermediate carry heights, retaining every discovered collision or false
stop. Only after those checks pass should an isolated retained-motion bench
and actual-root wrong-order/normal-operation tests use the candidate. Higher
counter stations still need their own source-frame admission checks. The
viewer cache-reset finding has a separate viewer-owned proposal,
`keep-expression-references-valid`, prepared at the pilot's request and
awaiting approval; no viewer fix has been implemented.

## Actual-root withdrawal diagnostic in progress

`tools/higher_counter_wrong_order.py` preserves the separate production-root
counter-tens experiment. It uses only these actual requests: crank elevation
9 mm, reverser −4.9425 mm, crank 90°, 180°, 190°, reverser −6.9425 mm, crank
200°. No register is seeded and no retained coordinate is assigned directly.
The intended question is whether withdrawing the counter input after partial
tooth passage leaves a displaced shaft that the next crank request must stop
against. This is a diagnostic question, not a passing stop claim.

The reusable tool records each actual status, retained shaft/crank, the full
bank and complete upper-print/bell contact in both kernels. It stops after an
unexpected preparation refusal without retrying or repairing state. Two trace
tests first fail on the absent module, then pass **2/2 in .001 s**
(`higher-counter-wrong-order-probe-red.log` and
`higher-counter-wrong-order-probe-light-green.log`). The fixture substitutes
contact readings and a request recorder; those two tests prove the diagnostic
sequence and refusal handling, not geometry or simulator performance.
CAD/model imports are deferred until real measurement so testing the trace
does not construct the complete machine.

An earlier equivalent seven-request native-only invocation remains live in
`higher-counter-tens-production-wrong-order-diagnostic.log`. It has completed
lift, reverser positioning and crank 90°, each with zero measured upper/bell
common. The remaining requests are pending. Do not conflate that preliminary
native-only run with a completed run of the dual-kernel, full-bank tool above.
It is not a whole-machine interference test; other contacts in its preparation
will still need checking before an operating restraint is accepted.
