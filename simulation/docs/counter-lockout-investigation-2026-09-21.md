# Counter lockout investigation

Tasks 6.2/6.3 require actual counter-side restraints as well as result-side
ones. This investigation does not adopt a counter restraint or fit in
`OperatingCurta`, and does not reuse the result-side contact table.

## Source-backed instrument

`tools/counter_lockout_probe.py` constructs each of the six existing counter
channels, retaining its source shaft pivot, upper-print placement and carry
stroke. Angles are actual machine shaft/crank angles, not normalized result
angles. The initial shaft positions are 134°, 114°, 94°, 74°, 54° and 34°.
The ones lockout is fixed; the five higher upper stacks have travel
−1.8..2.4 mm along their source downward axes. The normal lower input position
is retained at −4 mm, though it is not part of this upper-contact measurement.
The bell uses the already measured finer tessellation; its native material
is unchanged.

The fixture contract compares every upper print with the **actual retained
operating root**, using `Sim(..., meshes=True)`, and verifies identical native
material with zero native difference in both directions. The same comparison proves the
complete bell native-equivalent. Independent intermediate/full carry checks
prove the five upper stacks move down by 2.1/4.2 mm and the ones stays fixed.

The initial missing-instrument test is red. A first implementation check
also exposed an unassembled test oracle: mesh-free `Sim` does not prepare the
geometry tree. That test setup was corrected, not accepted as geometry evidence.
The first three geometry/selection contracts then pass (30.194 s).

The dynamic fixture factory initially gave all six root exports the same
artifact identity. Its regression fails **1 != 6** (0.641 s). The declared
`source_station` parameter now distinguishes them, and `trial_fit` additionally
distinguishes the unmodified and candidate instruments. No original printed
class or upstream file was changed. With complete-bell equivalence added,
the four-contract source fixture suite passes (121.106 s).

Logs under `_build_checks/`:

- `counter-lockout-fixture-red.log` — missing instrument;
- `counter-lockout-fixture-first.log` — unassembled oracle, not a machine defect;
- `counter-lockout-fixture-posed.log` — three contracts pass;
- `counter-lockout-export-identity-red.log` — export identity collision;
- `counter-lockout-fixture-green.log` — four source-instrument contracts pass.

Snapshot publication additionally exposed a shared identity on the trial's
enclosing channel, despite distinct roots and upper prints. An expanded
identity test fails **1 != 6** (1.656 s); the channel now declares its source
station too, and the test passes (1.667 s). Logs:
`counter-lockout-channel-identity-{red,green}.log`. Native/memory measurements
use each actual placed child and are unaffected by this SCAD-reference issue.
The analogous generated result-bank enclosing/root identity issue was then
reproduced and corrected separately; its dense measurements use the already
corrected rigid children. See the operating continuation record.

## Indexed contact before a candidate fit

The source-fit survey covers 120 poses: six stations, both carry seats,
five indexed flats and crank 0°/180°, measured natively and on the published
mesh. Fourteen poses have positive commons. At the parked crank, flat 3
contacts on every station:

| Station | Shaft | Raised native common, mm³ | Carried native common, mm³ |
| --- | --- | --- | --- |
| ones | 350° | 0.00004264142218 | unchanged fixed lockout |
| tens | 330° | 0.00001705656544 | 0.00005116969883 |
| hundreds | 310° | 0.00001705656680 | 0.00005116970292 |
| fourth | 290° | 0.00001705656566 | 0.00005116969952 |
| fifth | 270° | 0.00001705656885 | 0.00005116970906 |
| sixth | 250° | 0.00001705656783 | 0.00005116970601 |

The mesh misses several native contacts, including all five raised higher
stacks. The ones also contacts at crank 180° natively; its mesh reports zero
there. These findings concern the existing rigid simulation fits, not a claim
that the author's working printed calculator jams.

`CounterBankContactTest` pins parked-crank clearance over 60 poses and fails
with **19 kernel/pose failures in 15.715 s**. It deliberately defaults to
the installed fit and remains red until candidate adoption is justified.
Logs: `counter-lockout-indexed-source.log` and `counter-bank-indexed-red.log`.

## T08 candidate — not adopted

The isolated `--trial` substitutes only a .16 mm outer-profile relief for
the existing .15 mm counter lockouts and refines each complete upper print
to .01 mm linear / .1 rad angular tessellation. All six source class
identities, frames and carry relations remain explicit. This is a candidate
simulation fitting allowance, not a manufacturing recommendation.

The same 60-pose indexed-clearance test passes natively and faceted with the
candidate selected by a temporary test patch (**1/1, 41.645 s**). Log:
`counter-bank-indexed-trial.log`.

The candidate's material/identity/engagement suite passes **3/3 in 136.076 s**.
Every complete upper is one connected print and one valid native solid;
there is no added material, removal is confined to the original lockout and
bounded by its surface area times .01 mm, its R4 keyed core is untouched,
and the complete upper's axial extent is retained. Both locking flanks remain
present at all six stations, all five indexed flats and five carry heights:
**300 complete-print contact poses**, measured natively and on the mesh.
Log: `counter-bank-trial-material-flanks.log`.

Whole-profile
admission, wrong-order retained stops and actual-root
Python/browser acceptance remain unproved; no counter contact law is proposed
from indexed clearance alone.

Fresh snapshots of counter ones at shaft 350° / carry 0 and counter tens at
330° / carry 1, both with the bell parked, were rendered and inspected.
The initial default views hid the upper interfaces behind the bell, so a
front-facing oblique view was rendered instead. The inspected final images
are `_build_checks/counter-ones-t08-contact-view.png` and
`_build_checks/counter-tens-t08-carried-contact-view.png`. They show the source
shaft, complete upper and lower prints, and bell in their separate installed
frames. Their pixels establish the assembly view, not clearance of the tiny
contacts quantified above.

## Ordinary passage and independent contact timing

Freezing an engaged carry gear is a negative control, not ordinary motion.
At each higher counter's tooth midpoint (crank 204°, 224°, 244°, 264°, 284°),
the frozen initial shaft has approximately **2.9283 mm³** native contact;
advancing it by the source passage's 36° makes both complete-print kernels
clear. All five stations reproduce this contrast. Log:
`counter-carry-motion-control-probe.log`.

`test_counter_bank_lockout.py` now samples ordinary source tooth trajectories
for counts 0, 1 and 9, five starting flats and carry fractions 0, .5 and 1.
It includes input/carry entry, midpoint and exit angles as well as a 10° grid.
An initial candidate run is scoped to ones and tens through temporary test
patches, not production edits, in
`counter-trial-ordinary-motion-ones-tens.log`. It passes **2/2 tests in
1112.536 s**: the negative control and **4,125 complete-print poses** in both
kernels (90 flat/count/height cases). The corresponding run for stations
3–6 has now passed **2/2 tests in 2525.137 s**, covering **8,520 poses**
in both kernels (180 flat/count/height cases), in
`counter-trial-ordinary-motion-stations-3-6.log`. Together these runs cover
12,645 ordinary source-path poses over all six candidate stations. This
does not establish admission of arbitrary interrupted/wrong-order paths.

The counter's bell ingredients are not rigid copies of the result-side ones.
`tools/compare_counter_profiles.py` reads the original native parts and
compares candidate registrations without altering them:

| Native ingredient | Result volume, mm³ | Counter volume, mm³ |
| --- | --- | --- |
| upper locking disc | 2849.553368 | 2891.484231 |
| lower locking disc | 4511.217197 | 4572.692667 |
| carry ring | 2033.363220 | 2033.075111 |

The tested 0°, 180°, 181.25° and 182° registrations all retain material
differences. Some working surfaces could nevertheless coincide; whole-solid
non-equivalence does not establish every contact curve's shape. It means
rigid congruence cannot justify simply copying a result contact table. The
committed probe reproduces the initial readings byte-for-byte in
`counter-result-profile-shape-comparison-tool.log`.

`tools/counter_locking_envelope.py` therefore measures complete counter
prints independently. At ones shaft **167.6°**, the native closing bracket is
**174.885711670..174.885749817°**, while the mesh closes slightly earlier at
**174.884986877..174.885025024°**. At raised tens shaft **147.6°**, the sampled
opening and closing brackets are exactly 20° later in both kernels. This
single-pose agreement does not establish a shared profile. Logs:
`counter-ones-partial-envelope.log` and
`counter-tens-raised-partial-envelope.log`.

A coarse ones profile collection has completed over shaft 134..494° in 6°
steps, with a 5° crank grid and bracket refinement in both kernels, in
`counter-ones-upper-envelopes-coarse.log`. Each kernel has 61 shaft records:
55 have two boundaries and six indexed records have none. The terminal
completion record is present. This finite grid can miss narrow islands;
refined/between-knot checks and retained operating action-order evidence are
still required. No counter law is adopted or proposed as settled by this
collection. A 2° shaft-grid refinement, excluding the already measured 6°
knots, subsequently completed in `counter-ones-upper-envelopes-refine-2deg.log`;
see the refinement checks below.

## Indexed free-band measurement

The measuring tool now accepts `--bands` instead of `--shaft`, with an
explicit parked `--crank` (default 0). It brackets both complete-print
locking flanks around each of the station's five actual shaft indices in
both kernels. A blocked centre or a missing outer contact fails the probe;
every reported bracket retains its measured zero/positive endpoint volumes.
The 18 bisections give an angular bracket no wider than 5/2^18 degrees,
not a tolerated intersection volume. The instrument's missing-function
test failed first; all three bracketing/negative-control tests then pass
(0.003 s), including contact as small as 1e-20 mm³.

The complete ones run has ten verified records. The intersection of the two
kernels' measured free intervals at crank 0 is:

| Shaft index | Last free on lower side | Last free on upper side |
| --- | ---: | ---: |
| 134° | 131.304992676° | 134.311031342° |
| 206° | 203.303943634° | 206.311031342° |
| 278° | 275.303962708° | 278.307903290° |
| 350° | 347.310714722° | 350.063819885° |
| 422° | 419.518196106° | 422.308094025° |

These bands are asymmetric and differ among source flats. They are local
parked-crank measurements, not a continuous all-crank clearance certificate
or a reason to use identical repeated sectors. Logs:
`counter-indexed-band-tool-{red,green}.log` and
`counter-ones-indexed-bands.log`. The full bracket/volume records are also
committed as [numeric evidence](evidence/counter-ones-indexed-bands-2026-09-21.json).
The corresponding tens measurement at carry 0, .5 and 1 has completed:
30 bracket records plus its terminal completion record are in
`counter-tens-indexed-bands.log` and the committed
[tens numeric evidence](evidence/counter-tens-indexed-bands-2026-09-21.json).
All three heights have the same combined parked bands in that measurement:
111.304992676..114.311031342°, 183.303943634..186.311031342°,
255.303943634..258.307903290°, 327.310714722..330.063819885°,
399.518196106..402.308113098°. No all-crank or higher-station law is inferred
from that agreement. Independent tens envelope measurements at those three
heights are running in `counter-tens-upper-envelopes-coarse.log`.

The first actual-root diagnostic reaches crank 170° and counter shaft
167.6°, but fails its measurement setup: its drum path omitted the enclosing
`main_axle_step_drum_1` node. This is not a geometry result. The failed log is
preserved as `counter-ones-wrong-order-root-probe.log`.

The durable `tools/counter_wrong_order.py` corrects that path and additionally
checks **all six** complete lower counter prints against both drum halves.
Its actual operating requests are crank lift to 9 mm, reverser to −4.9425 mm,
partial crank movement to 170°, ten separate −.2 mm lever withdrawals toward
the lower housing stop at −6.9425 mm, and a further crank request to 180°.
The corrected run completes in `counter-ones-wrong-order-root-corrected.log`.
The retained counter shaft stays at 167.6°. At all eleven pre-final poses,
all thirteen measured pairs have zero native and faceted common volume.
The final request incorrectly reports **completed**: the upper/bell common
is **0.8056968920 mm³ native / 0.8044790921 mm³ faceted**, while all twelve
lower/drum pairs remain clear. The compact full readings and log hashes are
committed as [withdrawal evidence](evidence/counter-ones-withdrawal-2026-09-21.json).
This establishes the missing stop for these interfaces, not whole-machine
clearance of the preparation path.

`OperatingCounterLockoutTest` now uses that actual preparation and requires
short/long requests, a physically clear installed stop, positive overtravel
contact, exact replay and pawl relief. It fails at the first missing stop
(**completed instead of blocked**, 128.385 s), before the later assertions
can run. Log: `counter-ones-operating-restraint-red.log`. Production remains
unchanged; no assertion is skipped or marked expected-failure.

## Provisional ones law and rejected coarse interpolation

`compile_counter_locking_profile.py` combines independent native/faceted
free-side brackets and all five independently measured indexed bands. It
refuses missing kernel/flat records, unexpected contact islands and the
wrong candidate geometry. Its initial missing-module test was red; the
four compiler tests pass. The provisional `counter_locking_laws.py` retains
the existing .1° free-side stand-off and .002° shaft-support guard, with
unbounded shaft/crank revolution normalization. It is not connected to the
operating root. Higher counter stacks are outside this fixed-height law.

The initial numeric law checks pass: known withdrawal timing, five indexed
flats, and 21,615 ordinary source-path samples. Geometry independently
**rejects** the 6°-shaft-grid profile: each kernel checks 1,154 admitted
poses and finds ten positive commons between knots, including shaft 143°,
crank 171.500600647° (native common 0.005447758910 mm³). Both terminal records
are present in `counter-ones-profile-coarse-{native,faceted}.log`.
The complete rejection coordinates/volumes and profile hash are committed in
[rejection evidence](evidence/counter-ones-coarse-profile-rejection-2026-09-21.json).
Those twenty kernel/pose failures are now pinned by a numeric regression,
red with all twenty failures in 0.011 s; log
`counter-profile-between-knots-red.log`. The previously green numeric checks
are not a clearance certificate.

The verifier retains these discovered poses even when later profiles change
their knots. Its `--dense` mode additionally checks a 1° shaft / 5° crank
grid, plus profile knots, midpoints and support edges. Missing sampling-helper
tests failed first; all three sampling and four compiler tests pass in
0.007 s (`counter-profile-sampling-{red,green}.log`). This tests the measuring
instrument, not clearance. The 2° profile refinement has completed all 120
additional shaft rows in both kernels. Recompiling with those records makes
all eleven compiler, sampling and law tests pass (**30.969 s**), including
the twenty pinned coarse failures; log `counter-profile-refined-regression.log`.
Neither the contact stand-off nor any positive-volume rule changed. Dense
complete-print checks are now running against profile SHA-256
`59487d13eb37fd4e86947eb7661b86b5816a3325f457c52efd04e61c9b6051de`
in `counter-ones-profile-refined-dense-{native,faceted}.log`.
Numeric success is not geometry acceptance or operating adoption.

The dense checks reject that 2° interpolation near
a contact-curve minimum: shaft 141°, crank 171.2062967529297° has positive
common **0.000028125040 mm³ native / 0.000029810830 mm³ faceted**. The faceted
sweep completes **11,138 admitted poses with five failures**. Once rejected,
the native sweep was intentionally interrupted (exit 130): its last completed
shaft is 187°, with 1,510 poses and one confirmed failure. It is neither a
pass nor a full native sweep. Coordinates and profile hashes are retained in
[refined rejection evidence](evidence/counter-ones-refined-profile-rejection-2026-09-21.json).
The expanded numeric regression reproduces all six retained kernel/pose
failures in 0.037 s (`counter-profile-cusp-red.log`). A focused
independent measurement at offsets 6.5°, 7° and 7.5° from each of the five
shaft indices completes all fifteen rows in both kernels in
`counter-ones-envelope-cusp-refinement.log`. It measures each actual source
flat rather than copying one flat's curve. The rebuilt curve passes all
eleven compiler/sampling/law tests in **36.244 s**, including both sets of
discovered collision poses (`counter-profile-cusp-regression.log`).
Its SHA-256 is
`eaa3bd7dfbdb58e20a32549a748e11745737b8d2598d4d37ff7496c46ce4f367`.
The fresh dense checks each pass **11,858/11,858 admitted poses**, in both
faceted and native kernels, including the retained failures and independently
sampled interiors. Their terminal results are recorded in
`counter-ones-profile-cusp-dense-{faceted,native}.log`. These are finite
geometry checks, not a proof of every continuous intermediate pose.
No default operating counter fit/bound or changed stand-off follows from
this unfinished acceptance.

## Isolated retained counter-ones trial

`CounterOperatingTrial` now adds the measured T08 ones upper print and the
independent fixed-height counter law to the complete operating tree. It
inherits the current result ones/tens and pawl restraints and all actual
inputs. There is no new register setter or preparation macro in the model,
and higher counter stacks are unchanged. The manifest still selects
`OperatingCurta`, which has no counter restraint or T08 counter fit.

The full-root fixture compares the installed complete upper and bell against
the measured station-one candidate in both native-difference directions,
and compares the complete initial state bank against `OperatingCurta`.
It passes **1/1 in 77.328 s** (`counter-operating-fixture-green.log`). The same
test with the unmodified production counter selected as its subject rejects
it: **0.404301831873 mm³** of extra material relative to the measured upper
print, 76.590 s (`counter-operating-fixture-baseline-red.log`). The original
production wrong-order stop failure remains the behavioral red evidence.

An earlier attempt to check for the missing trial module was still importing
when the module was written, so it cannot establish a red result. That
invalidated, redundant attempt was intentionally interrupted (exit 130) and
retained as `counter-operating-fixture-import-attempt-interrupted.log`. It is
not counted as a test pass or failure.

The production withdrawal test now has an explicit model class so the exact
same assertions can run against the isolated trial. Its short/long request,
installed-stop/overtravel geometry, retained shaft, replay and relief checks
pass **1/1 in 1665.484 s** (`counter-operating-trial-stops.log`). The short
request to 180° stops at **174.7853836059494°**; the long request to 900° stops
at **174.78538360544917°**. Both installed stop poses have zero common in
both kernels, and .2° overtravel has positive common. This isolated stop
test is not ordinary arithmetic, browser or whole-counter-bank acceptance.

`tools/counter_operating_browser.py` prepares the same actual inputs on a
separate full-machine export and tests short/long stops, snapshot replay,
relief/idle and retry. It can compare every retained coordinate exactly with
an optional Python report. Without that report it explicitly records no
Python comparison. Its report-validator module failed as missing first;
all four positive/negative validator tests then pass (0.001 s), including
missing requests, failed replay/relief, page errors and an unrelated changed
or missing bank coordinate. Logs: `counter-browser-validator-{red,green}.log`.
The isolated export passes (`counter-operating-trial-export.log`). The first
browser check reaches the prepared crank 170° / counter shaft 167.6° but
times out taking its first screenshot, before either stop request
(`counter-operating-trial-browser.log`). Its incomplete report is preserved
as `_build_counter_ones_trial/counter-browser-capture-timeout.json`; it is not
acceptance. A retry with a finite 60 s capture deadline **passes**, exit 0
(`counter-operating-trial-browser-retry.log`). Both short/long requests stop
at exactly the Python stop angles above, replay exactly, admit .05° relief,
retain the relieved state during an idle step, and stop again on retry. Its
[complete browser report](evidence/counter-ones-browser-acceptance-2026-09-21.json)
contains all 213 coordinates per state and zero page errors. Both fresh
prepared/stopped screenshots were inspected: the complete assembly renders,
the crank is lifted and readback advances from 170° to 174.7854°. These images
do not expose or prove the internal contact clearances. The tested document
SHA-256 is `0ab407640bcda4aee8f0e79e264a4bbd7d6857939fb1149c896e53faf719f648`;
viewer bundle SHA-256 is
`5f3ec29aede4934106bb0cbbdaa7454dcec39d2ba04a233f431a4ce279fef610`.

The completed original Python stop test did not record full banks or idle
steps. Its extended invocation now adds those assertions and optional report
capture (`CURTA_COUNTER_ACCEPTANCE_REPORT`). That separate invocation passes
**1/1 in 1500.407 s** (`counter-operating-trial-idle-banks.log`). All four
stopped/idle banks in the [complete Python report](evidence/counter-ones-python-acceptance-2026-09-21.json)
match the saved browser banks **exactly**, all **213 coordinates** at both
targets. The existing strict browser-report validator performs this comparison
on the saved values; the browser report's original `python_report: null`
is retained because no Python report existed during that earlier invocation.
The Python report SHA-256 is
`113d241d40144a4384de16b7ecd544553b9b3023e7ebee94ba752551b897874b`;
its log SHA-256 is
`0e3631bb95c3f7b4141184f0e2d76d175f469e5fc501f31c54a9f814d77d549f`.
The three-case page-53/subtraction/successive-addition-and-clearing arithmetic
suite ran against the isolated trial through a temporary test-class patch,
with production tests unchanged (`counter-operating-trial-arithmetic.log`).
Page-53 calibration and subtraction/overflow undo both passed. The process
then disappeared during successive-addition/selective-clearing without a
terminal summary, so the batch is incomplete and adoption remains gated.
The [interruption record](evidence/geometry-worker-terminations-second-2026-09-21.json)
preserves the log hash; the process is not still running.
This is a browser request/render probe, not physical-pointer or mesh-clearance
acceptance. Its Playwright Promise evaluation and local-file interception
follow the official Python API documentation fetched through Context7.

Higher counter measurement is also independent of this fixed-height trial.
At tens shaft 120°, carry 0's native opening bracket is
86.666355133..86.666374207°, while carry .5 opens at
88.666362762..88.666381836°. Both close at
191.422691345..191.422710419° in that measurement. The approximately two-degree
opening change rules out treating this sampled axial motion as a fixed curve.
The coarse tens collection now completes all **183 shaft/height rows**:
61 shaft positions at each of carry 0, .5 and 1, in both kernels
(`counter-tens-upper-envelopes-coarse.log`). Fully carried poses can have
four contact boundaries rather than two; for example shaft 156° has a
second short free interval near crank 203.49°..205.79°. This rules out
feeding all heights to the fixed-height ones compiler unchanged. These are
sampled heights and angles, not a continuous axial interpolation law or
an operating higher-counter restraint.

The native component reader now accepts the counter's source stack path,
with a test proving its ingredients cover exactly the complete bell and upper
prints at carry 0, .5 and 1: no missing or extra native material. Its existing
result-tens path is unchanged in both difference directions. Both tests fail
first on the unsupported counter path, then pass **2/2 in 61.885 s**
(`counter-components-{red,first}.log`). The new
`tools/counter_component_contacts.py` always reports complete native/faceted
commons alongside ingredient labels, never replaces the complete print by
selected collision surfaces. A five-height, eight-crank-pose measurement at
tens shaft 156° completes all **40 poses** in
`counter-tens-contact-components.log`. The upper locking disc is the only
contact at carry 0/.25. At carry .5 the lower disc also contacts the pentagon
near the opening, while the upper disc still causes the earlier closing.
At carry .75/1 the upper disc is clear; the lower disc controls the opening
and the carry-ring teeth create the late contact intervals. At full carry,
crank 198° and 202° contact the transmission gear, 204° clears in both kernels,
and 206° contacts that gear again. A single closing boundary would lose this
measured free interval. The source prints remain unchanged.

The [complete contact/support evidence](evidence/counter-tens-contact-support-2026-09-21.json)
retains those rows and all six independent axial brackets. The new
`tools/counter_axial_support.py` measures complete prints at independently
posed carry heights, screens a 17-height grid for a unique transition and
bisects it without a volume tolerance. Its tests fail on the missing module
first, then pass **3/3 in .003 s**, including tiny positive commons,
non-finite measurements, absent/multiple transitions and rejection of the
fixed ones stack (`counter-axial-support-{red,green}.log`).

Three isolated tens poses complete in both kernels:

| Transition | Shaft / crank | Native raw-travel bracket, mm | Faceted raw-travel bracket, mm |
| --- | --- | --- | --- |
| Upper disc releases | 156° / 204° | .899999463558 .. .899999713898 | .899998962879 .. .899999213219 |
| Lower disc enters | 156° / 94° | −.599999570847 .. −.599999320507 | −.600000071526 .. −.599999821186 |
| Carry teeth enter | 114° / 205° | .300000500679 .. .300000751019 | .300000000000 .. .300000250340 |

Each bracket retains the zero and positive endpoint common; the kernel
differences are not suppressed or replaced by a contact-volume epsilon.
Logs are `counter-tens-{upper,lower,tooth}-axial.log`. These finite readings
identify separate axial supports, not a continuous admission proof or a
complete higher-counter restraint. Lower-disc and carry-tooth angular
profiles, intermediate-height admission and actual operating acceptance
remain to be established.

The combined component/axial/indexed-band/browser-report/result-frame
regression passes **14/14 in 41.333 s** (`counter-support-regression.log`).

A separate read-only comparison of the coarse carry-zero envelopes supplies
a possible upper-disc reuse lead, not a new law. Matching tens shaft +20° to
ones shaft and subtracting 20° from the tens crank brackets gives identical
transition topology across all 122 kernel/shaft rows. All 110 native brackets
overlap; 108/110 faceted brackets overlap. The faceted brackets at tens shafts
120° and 264° are separated by **.000019073486328125°**, retained rather than
rounded away. The [normalization evidence](evidence/counter-upper-normalization-2026-09-21.json)
pins both source logs and the comparison. This neither certifies interpolation
between those coarse samples nor supplies the lower-disc/carry-tooth fields.

## Independent lower-disc and carry-tooth angular fields

The native pair reader now accepts explicit counter ingredient names and the
source-specific stack path. A new check compares its rotated reference shapes
against independently posed ingredients at seven upper/lower/tooth contact and
clear positions. Zero common must stay exactly zero; positive/zero classification
must agree before numerical-volume parity is checked. The whole-print counter
profile compiler now refuses any row or band marked `component`, so diagnostic
curves cannot accidentally become complete-print acceptance.

Those two tests fail first (unsupported `stack_path`, and two missing refusal
assertions), then the complete component/compiler group passes **8/8 in
67.305 s**. Logs: `counter-pair-envelope-{red,green}.log`. The new
`tools/counter_component_envelope.py` preserves every observed contact interval,
its free/contact endpoint volumes and its component identity. Three tests fail
on the absent module first and then pass **3/3 in .002 s**, covering multiple
intervals, a positive common of 1e−20 mm³, non-finite results and invalid scopes
(`counter-component-envelope-{red,green}.log`). No intersection epsilon or
whole-print replacement is introduced.

The first measured six native curves cover tens shafts 114°, 120° and 156° at
full carry, for each lower-disc and carry-tooth pair. The
[curve evidence](evidence/counter-tens-component-curves-2026-09-21.json)
retains all boundary brackets, endpoint volumes and source-log hashes. At
shaft 156°, the lower disc opens near **95.25585°** and closes near
**209.16744°**. The carry teeth contact in **197.05272°..203.48665°** and
**205.78767°..212.12027°**, explaining the independently measured intervening
complete-print free interval. At the indexed shaft 114° the lower disc has no
sampled contact, but the carry teeth contact near **200.53528°..206.87382°**.
An indexed shaft therefore does not make this carried upper print universally
free. The lower closing boundary is not an upper-disc curve shifted by the
roughly two-degree opening difference.

At all 73 sampled crank angles for those three shafts, the native component
union's positive/zero classification agrees with the previously measured
complete print in both kernels: **438/438 comparisons**, no mismatch. This
does not equate the component volume sum with a fused-print common, certify
unsampled angles or intermediate heights, or adopt a restraint. The remaining
58 shaft samples at six-degree spacing now complete for both pairs in
`counter-tens-lower-tooth-component-coarse-remaining.log`: **122 native curves**
total across 61 actual shaft angles from 114° to 474°. Each lower-disc curve
has zero or two boundaries; each carry-tooth curve has two or four. Their
union's classification matches the prior full-carry complete-print sweep at
all **8,906 kernel/pose samples**, zero mismatches. The
[complete coarse and intermediate-height boundary evidence](evidence/counter-tens-component-coarse-2026-09-21.json)
retains endpoint volumes and all four source-log hashes. The upper-disc
and axial-support evidence remain separate; no result-side curves are copied.

The combined component/envelope/compiler/axial/indexed-band/support-interval
regression passes **21/21 in 46.168 s**
(`counter-angular-support-regression.log`). Twelve additional native curves
at carry .5 and .75 complete for the same three shafts. The carry-tooth pair
has no sampled contact at .5; at .75 its brackets equal the full-carry
brackets. Lower-disc openings differ by up to one final bisection bracket
between these heights, while lower closings match. These observations retain
the endpoint volumes and do not assert exact continuous height invariance.
Log: `counter-tens-component-intermediate-heights.log`.

The next [higher-counter candidate](higher-counter-restraint-2026-09-21.md)
compiles these independent fields but fails ordinary carry admission. Both
complete-print kernels clear five falsely blocked source-flat poses. Finer
angles expose a real free interval missed by the five-degree scan; the
rejection is pinned and a two-degree shaft/quarter-degree tooth-window
refinement is running. This is not an operating adoption.
