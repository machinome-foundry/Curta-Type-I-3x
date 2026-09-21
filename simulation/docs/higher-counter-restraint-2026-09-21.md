# Higher-counter restraint candidate

Status: isolated numerical candidate, **rejected pending refinement**. Not
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

A broader refinement is running in `higher-counter-tooth-fine-grid.log`:
shaft 114°..474° every 2°, with the same quarter-degree tooth-window samples
and five-degree whole-revolution grid. The four completed diagnostic shafts
are omitted from that job and must be merged explicitly at compilation.
This job changes no law while running. The checked-in candidate remains the
known-rejected coarse version until refined evidence is complete.

## Remaining acceptance

Compile the completed readings, then rerun the five pinned false stops,
measured contact endpoints and ordinary source tooth paths. Challenge both
complete-print kernels between profile knots, at support edges and at
intermediate carry heights, retaining every discovered collision or false
stop. Only after those checks pass should an isolated retained-motion bench
and actual-root wrong-order/normal-operation tests use the candidate. Higher
counter stations still need their own source-frame admission checks. The
viewer cache-reset finding remains a separate, unapproved package change.
