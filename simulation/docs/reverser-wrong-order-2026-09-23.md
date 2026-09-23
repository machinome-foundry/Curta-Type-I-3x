# Mid-cycle counter reversal: confirmed missing restraint

The operating root is **not finished**. A physical reversing request at crank
90° admits a positive gear/drum common. This is a project-law gap, not evidence
of a framework admission failure: `RunningReverser` declares only the fixed
housing/spacer range, with no drum-dependent bound. No production law, print,
placement, source asset or accepted requirement changes in this checkpoint.

## Pinned reproduction

Project content `e4ef8755e80e25e677aa40072d06c97dda21746b`, framework main
`82bf530cacae1fd7b841a47a35c961eb438b79f8`; viewer main remains `a92541d` and is
not used by this native/Python diagnostic. Framework CI commits `a87abc5` and
`e05d9c5` were independently reconfirmed as ancestors of framework main.

An untouched `Sim(OperatingCurta(), dt=.1, meshes=True)` receives an ordinary
crank request to 90°, duration .5 s, followed by .5 s of running. The command
completes. The counter-ones shaft remains 134°, crank lift is zero. Subsequent
requests move only the reverser and its connected axial/follower coordinates;
the probe never seeds a register, poses a gear independently or prepares the
crank for the reverser.

The complete printed pair is:

- `Curta.transmission.turns.ones.p_10218_1`
- `Curta.main_drive.stepped_drum.main_axle_step_drum_1.main_axle_step_drum_top_1`

Native checks use `machinome.exact.intersect_shapes`, including the resolved
interior-witness guard. Faceted checks use the published local meshes with
their retained world placements in `Manifold.Mesh64`. No positive volume is
waived by an epsilon.

## Observed contact

The native nine-tooth drum band's top is world Z = −48.2 mm. The descending
ones pinion's bottom reaches it when the knob is at 1.0575 mm. This is a
fixture-specific first-contact height, **not a universal reverser bound**.

| Requested knob height (mm) | Native common (mm³) | World64 common (mm³) |
| --- | ---: | ---: |
| 1.0675 | 0 | 0 |
| 1.0575 | 0 | 0 |
| 1.0475 | 0.02353507611251452 | 0.023458419217706056 |
| 1 | 0.1353266876469794 | 0.13491142006933782 |
| 0 | 2.4888342988989 | 2.481290385366863 |
| −4.9425 | 3.530261416877793 | 3.519563077511023 |

Every request currently reports `completed`, including the penetrating ones.
At 1.0475 mm the positive native common spans Z = −48.21…−48.2 mm,
X = −24.4627565819035…−22.957519635462795 mm and
Y = 25.19387598931957…27.489809721425278 mm. The reviewed native section at
Y = 26.3 shows the .01 mm gap and .01 mm penetration on opposite sides of
the same contact. Its axial scale is explicitly expanded.

An earlier exploratory probe checked only the ones pair at crank 171.25°
and 180° and six lever heights; its zero faceted samples do not certify a
clear path. The subsequent 90° probe checked all six counter inputs against
both complete drum prints at nine heights. Only the pair above was positive
at those samples. These terminal observations narrow the finding; they are
not an all-angle, continuous-path or whole-machine certificate.

## Red-first regression and retained evidence

`simulation.test_running_reverser_wrong_order` runs **two tests in 47.697 s**:
the free-play test passes; the penetration test fails in both geometry checks
and its terminal-status assertion (**three failures, exit 1**). This is an
intentionally open acceptance regression, not a passing implementation.
The test checks actual material before asserting `blocked`, so its failure
does not depend solely on an assumed command status.

Reproduce from the project with the workspace Python:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=. \
  /home/asa/devel/machinome-studio/.venv/bin/python -m unittest -v \
  simulation.test_running_reverser_wrong_order
```

The separate section tool completes with exit 0; that means its diagnostic
ran, not that the operating mechanism passed:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=. \
  /home/asa/devel/machinome-studio/.venv/bin/python \
  -m simulation.tools.reverser_wrong_order_sections \
  --image _build_checks/reverser-wrong-order-e4ef875.png \
  --report _build_checks/reverser-wrong-order-e4ef875.json
```

Use new filenames on a rerun; the tool refuses to overwrite evidence. The
report retains both full 214-coordinate banks, independently restored from
the prepared 90° snapshot before each request.

- JSON SHA-256: `826727a408247be94b008d598f39fc2d403f04141f64af6b131c63623ca4dda0`.
- Inspected PNG SHA-256: `a1b79ff2c82c37305c24ce1deef0b26f4c601e5fdcd754ab3a4918b532b3d2f7`.

The table and test outcome above are reconstructed from completed terminal
calls, not claimed to be a raw saved transcript. The two-pose JSON is emitted
directly by the checked-in tool. Exploratory volumes are not silently promoted
to a regression matrix.

## Phase-envelope continuation

On project `8ca74d5`, `tools/reverser_tooth_envelope.py` adds an independent
pose instrument from the **complete installed prints** in an untouched
production root. It rotates each input about its declared shaft axis, rotates
both complete drums about their installed main axis, and applies the lever
and drum axial displacements. It does not mutate the run, change print material
or normalize the source to an assumed ideal gear. Each report names its station,
crank, shaft, lever height, drum lift and kernel. All five shaft sectors are
measured over a full 360°; no sector is silently repeated.

Two fixture tests pass in **91.604 s**. They compare the instrument with real
requests at the near-contact heights, at crank 171.25° with a nonzero retained
shaft phase, and at crank 90° after raising the drum 9 mm. Native and mesh
world bounds match within coordinate-rounding precision (1e−10 mm); contact
classification must match exactly, and every zero common must remain exactly
zero. Comparing the final digits of two positive volumes is not an overlap
tolerance. The initial tool attempt mistakenly read the axis off the bound
value instead of the class joint declaration and stopped before measurement;
that local diagnostic error is corrected, not a framework limitation.

An additional real-history test passes in **25.530 s**: lower the reverser at
home, then turn to 90°. The ones shaft is now 231.6°, instead of the red
fixture's 134°. Requests to −3, 0, 1.0675 and 3.9075 mm all complete with zero
native/world64 common in the ones pair and without changing crank or shaft
phase. This is a sampled withdrawal counterexample to a home-only lock, not a
whole-bank continuous-clearance certificate. The original penetrating-history
test remains red; this passing test does not replace it.

The first world64 survey samples nine crank angles (0, 75, 90, 100, 120, 150,
170, 180, 270°), two lever heights (0 and −3 mm), and 181 shaft angles from
134° through 494° at 2° spacing. All **3,258 rows** complete; 790 have a positive
common and none has a negative volume. At crank 90° / lever 0, the first shaft
sector's free samples are 154…174°; at lever −3 the whole sampled sector is
clear. At crank 170°, both heights have free samples 160…178°. These are
observations, not interpolated bounds or evidence of all intervening points.

The boundary instrument retains every observed transition and both its free
and positive endpoints. It performs 16 bisections within each observed bracket;
it explicitly does **not** claim to exclude unsampled islands. Three unit tests
pass, including two disconnected contact islands, preservation of a positive
1e−30 mm³ common, and refusal of unordered, negative or nonfinite measurements.
The nine-angle survey yields 18 records and 70 boundary brackets; each active
row has ten boundaries across the five shaft sectors.

Native checks at crank 90°, lever 0 confirm the first sector's angular gap:
shaft 152° overlaps by 0.008850995541473169 mm³, 153°, 154° and 174° are clear,
175° overlaps by 0.004657491704910437 mm³ and 176° by 0.018376175081854292 mm³.
Refinement gives these **clear-side endpoints**, with positive commons retained
on the other side of each bracket:

| Kernel | Lower clear shaft angle | Upper clear shaft angle |
| --- | ---: | ---: |
| Native | 152.23562622070312° | 174.0721435546875° |
| Published world64 mesh | 152.22329711914062° | 174.07217407226562° |

Thus mesh-only admission would be too permissive at the lower boundary.
The limiting native positive samples are 3.7497067733704725e−9 and
8.213639765078992e−13 mm³; neither is waived. Combining measured bounds must
use the stricter free side of both kernels, then validate interpolation and
the full retained path. No runtime table is adopted from this coarse survey.

Raw generated JSONL under `_build_checks/` (all producer processes exit 0):

- `reverser-angular-survey-8ca74d5.jsonl` — SHA-256
  `355c2885cca1151c1bef1d1018979a1e08b3fcf7eb6f1e73da23ceb7e8726c8c`.
- `reverser-angular-boundaries-8ca74d5.jsonl` — SHA-256
  `d011c41ca6f75738e7e2f12c5c15409533914d33a05d8c52142e23c501d4799e`.
- `reverser-angular-native-brackets-8ca74d5.jsonl` — SHA-256
  `933cedc3f462c7d16588018bbea8b864615fed26e0626e3d70e9122edc185816`.
- `reverser-angular-native-boundaries-8ca74d5.jsonl` — SHA-256
  `9787162f1ba0e0413939ca49860cb60f50f8db8ae74d3bf3ad236350c260fe37`.

For example, reproduce native refinement with the workspace Python, from this
project, setting `PYTHONPATH=.` and one BLAS/OpenMP thread as above:

```sh
python -m simulation.tools.reverser_tooth_envelope --crank 90 --height 0 \
  --shaft 152 --shaft 153 --shaft 174 --shaft 175 --boundaries --kernel native \
  --output _build_checks/reverser-angular-native-boundaries-rerun.jsonl
```

For the faceted survey, supply the nine `--crank` values above,
`--shaft-step 2 --height 0 --height -3`, and a new output path. Adding
`--boundaries` retains/refines the observed transitions. Every existing evidence
file is preserved. The instrument supports stations 1…6, but the current
fixture and phase evidence are explicitly **station 1**, not proof of the
five different higher-counter prints.

## Local admission experiment and full-revolution survey

`reverser_contact_trial.LocalReverserContactTrial` is an **unadopted, deliberately
local experiment**. It is not selected by the manifest. It constrains only the
measured crank-90°, zero-drum-lift fixture and uses the measured free angular
interval 152.3…174° with a .01 mm axial free-side stand-off. The temporary
72° phase chart is checked only by the two retained histories below; it is
not an assertion of exact source symmetry across the five sectors. Outside
that fixture the added bound falls through to the existing physical window.
This experiment cannot complete the operating restraint requirement.

The first draft incorrectly expressed a signed contact level relative to the
bound's `own` argument. The framework deliberately holds that argument at the
start of a segment (including for `Bound` with reads), preserving ratchet
semantics. The erroneous fallback `own-1` therefore stopped a normal parked
lever after 1 mm and allowed retry drift. Four tests ran in 100.073 s with two
failures. An earlier draft also stopped at construction because the project's
expression `max` is binary, not variadic (four errors in 5.753 s). Both are
local implementation errors, not framework limitations or passing results.

The corrected trial selects **absolute axial stop planes** from the held
position and reads the live angular state. Its four tests pass in **97.838 s**:

- The original native/world64 penetration request stops clear of the tooth.
- The .01 mm pre-contact free request remains admitted.
- The different retained phase still permits the sampled withdrawal sequence.
- A long request to −3 mm cannot cross the obstructing band even though that
  endpoint is clear. Repeating it leaves the complete snapshot unchanged;
  restore/replay is exact, and explicit relief returns to the saved snapshot.

The production test was rerun **after importing the trial** to verify that
the subclass declaration did not mutate the default model. It still fails
the same native/world64/status assertions (one test, three failures, 24.364 s).
The production defect remains open rather than being hidden by a test-only
class or an accidental global constraint.

The inspected native trial section shows zero common for both requests. The
1.0475 mm request is blocked at 1.0674999999999986 mm; the 1.0675 mm request
completes. The .01 mm gap is a declared placement stand-off, not an accepted
positive overlap. Both full 214-coordinate banks are retained in:

- `_build_checks/reverser-local-trial-2590f38.json`, SHA-256
  `08584f25ff8ead420007e14ae81b6384776bd8b93d95563777cfd8fc373f54f7`.
- `_build_checks/reverser-local-trial-2590f38.png`, SHA-256
  `a20ac7db61974bea40033eeb10af0fc462780a63ee734f730f16c9878d21d123`.

The section command above accepts `--local-trial` and requires fresh output
names. Without that flag it continues to inspect the unchanged production root.

The independent complete-print world64 survey now spans **both full angular
revolutions**: crank 0…360° and shaft 134…494°, each at 2° spacing, with lever
heights 0 and −3 mm. It completes with exit 0: 362 rows, 65,522 coarse pair
samples, and 610 refined observed transition brackets in 61 active rows.
The active sampled crank angles are 74…178° at height 0 and 164…178° at height
−3; the other sampled rows have no observed transitions. This still does not
exclude unsampled islands or prove native clearance between angular knots.

Raw file: `_build_checks/reverser-angular-full-world64-2590f38.jsonl`, SHA-256
`ae56f0c5f0fa896ca61168061ed4e84d0dff93b6475368e70d01a52bf83e347e`.
Reproduce with `--crank-step 2 --shaft-step 2 --height 0 --height -3 --boundaries`
and a new `--output` path on `simulation.tools.reverser_tooth_envelope`.

`simulation.tools.refine_reverser_native` independently brackets and refines
each observed transition in native geometry. It retains both endpoint
classifications, expansion attempts and the input file's SHA-256. Rows without
a faceted transition are explicitly `not_checked_no_world64_transition`, never
copied as a native clearance pass. The full refinement has been launched at
this checkpoint and is **pending**, not counted as completed acceptance:

```sh
python -m simulation.tools.refine_reverser_native \
  --input _build_checks/reverser-angular-full-world64-2590f38.jsonl \
  --output _build_checks/reverser-angular-full-native-2590f38.jsonl
```

That was the state at commit `3d26928`; the completed continuation is recorded
below. Neither the local trial nor this survey changes any umbrella task
checkbox, source print, production law or control.

## Completed native knots and rejected interpolation

The original serial refinement was intentionally interrupted after 90 complete
records (eight active rows, 80 boundaries). Its exit 130 is not a completed
survey. The complete records were preserved, validated against the input hash,
and resumed into a **different** file using four independent spawned readers.
The resumed process completed with exit 0 and 272 additional records. Combined,
the two files cover all 362 input poses with no duplicates or missing poses:
61 active rows retain all **610 native brackets**; the other 301 rows remain
explicitly unchecked in native geometry.

The resume validator rejects mismatched input hashes, unknown/duplicate poses,
missing transitions, incomplete endpoints and positive volumes relabelled zero.
Parallel workers own separate geometry; only the parent writes the output, in
input order. No native Boolean, false-empty guard or positivity rule changed.

- Serial prefix: `_build_checks/reverser-angular-full-native-2590f38.jsonl`,
  SHA-256 `34fa2e360718ed70d6e604ab0874d0c3f39717cbc85875f2bec4df4fd2c26660`.
- Completed continuation:
  `_build_checks/reverser-angular-native-parallel-3d26928.jsonl`, SHA-256
  `d967af30b5bb44391b4fbd4f75bf7358cd0766c4f5624d040bba6d2ded1e5af0`.

`simulation.tools.compile_reverser_phase` joins the stricter boundary from
each kernel: enter contact when either kernel does, and leave only after both
are clear. All five measured source sectors are retained independently, not
averaged or replicated. Subtracting `6.4*crank` merely unwraps their coordinate
chart; it imposes no shaft motion. Missing native rows remain unmeasured.
The narrowest measured free interval is about 13.292053° at crank 80°, height
0, chart sector 2. These are **candidate knots, not an adopted restraint**.

Candidate: `_build_checks/reverser-phase-candidate-3d26928.json`, SHA-256
`f9827262773dba8f9f7c597e06af7333b2a8e51fd4dfd7064bc0e659b631a678`.

An independent challenge linearly interpolated chart sector 0 between adjacent
2° knots at crank 79°, 89°, 99°, 109° and 139°, height/lift zero. Each predicted
free edge was inset by .01°. Of 20 complete-print probes (two edges, five
cranks, two kernels), **eight overlap**: four physical poses rejected by both
kernels. The probe command correctly exits 1. This rules out adoption of that
coarse interpolation; a stand-off is not permission to accept positive common.

| Crank | Edge | World64 common, mm³ | Native common, mm³ |
| --- | --- | --- | --- |
| 79° | upper | .004573496588 | .004596454622 |
| 89° | upper | .002199620784 | .002220950961 |
| 109° | upper | .013203428927 | .013203098173 |
| 139° | lower | .001751155498 | .003005561564 |

Raw rejection: `_build_checks/reverser-phase-interpolation-rejection-3d26928.json`,
SHA-256 `28b08cee9dc9188857ef984e5d3a118761e64666e6ad8e8504704669d60aad0d`.
The exact shaft angles and both drum volumes are retained there. Reproduce with:

```sh
python -m simulation.tools.probe_reverser_phase \
  --input _build_checks/reverser-phase-candidate-3d26928.json \
  --output _build_checks/reverser-phase-interpolation-rerun.json \
  --crank 79 --crank 89 --crank 99 --crank 109 --crank 139 \
  --sector 0 --kernel world64 --kernel native
```

The boundary/resume/compiler/probe unit gate passes **16 tests**. It proves the
evidence plumbing, not a green production reverser regression. Interpolation
cannot skip an unmeasured row, extrapolate, collapse a free interval or silently
replace the selected source sector.

A bounded Sol investigation on framework `82bf530` found no framework defect
behind the native survey cost: four station-1 queries at crank 90°, height/lift
zero and shafts 152.23°/174.07° took .36–.43 CPU seconds apiece. Approximately
51% was OCCT Boolean work, 28% project-tool rigid placement, and 19% strict
false-empty verification. The bottom drum was separated in Z by over 4.44 mm
at those sampled poses, but the top pair's boxes overlap. A possible local
placement cache or conservative cull needs separate paired proof; none was
implemented, no guard was weakened, and no framework cycle was opened.

## Midpoint refinement and project-tool placement reuse

A trial retained just one pair of posed drum bodies, keyed by kernel, crank
angle and drum lift. Changing the shaft or reverser height still built the gear
pose independently; changing any drum-pose key invalidated the cache. It did
not cache intersections, alter either geometry kernel, or remove the
invalid/false-empty common checks. The reuse unit test failed before the change
and passed afterward, including invalidation checks. **Native reuse was then
withdrawn** after the sequence-dependent failure below: the current tool reuses
only world64 drum placements and always constructs fresh native drum poses.

Both ten-probe rejection sequences were rerun, grouped by kernel so adjacent
queries actually reuse the drum placement. **Every recorded field is exactly
equal** to the corresponding uncached record, including the four positive
commons in each kernel. These probe commands still correctly exit 1:

- `_build_checks/reverser-phase-cached-native-48d71c9.json`, SHA-256
  `e8731e0d8c20b3dac91b1b9e50cebcda544dda3be1202921b8f16d5b06e5b9de`.
- `_build_checks/reverser-phase-cached-world64-48d71c9.json`, SHA-256
  `3f9215b489c5e3dd24f2eb532f403359adfdf1f63f91321e2e7fdd311d6a7074`.

The actual-root pose/contact fixture also passes both tests in **96.187 s**.
A bounded placement-only timing (16 native shaft poses at crank 90°, height/lift
zero, alternating uncached/cached passes) measured 1.00252/.14957 and
.95809/.15613 CPU seconds. That is evidence about placement cost only, not
whole-machine runtime or total native survey speed. The native speedup is an
unsuccessful trial, not an accepted optimization.

`simulation.tools.refine_reverser_intervals` uses interpolated angles only as
search seeds, expanding a local interval until it independently measures the
expected clear/positive transition. It refuses a wrong transition or an
unbracketed seed. All five sectors remain separate. The completed four-worker
world64 run adds **59 midpoint rows and 590 observed brackets**: 75…177° at
height zero, and 165…177° at height −3, both in 2° steps. It does not measure
native clearance or exclude additional unsampled islands.

Raw midpoint file: `_build_checks/reverser-phase-midpoints-world64-48d71c9.jsonl`,
SHA-256 `a6955cab207cf1a6dbd24f1beaf73bd49db2750b115d3611d004026a12f7f00a`.
Compared against the old linear predictions, 375 of the 590 edges move inward;
360 differ inward by more than .1°. The largest measured inward difference is
about 2.357056° at crank 81°, height zero, on each upper sector edge. This is
further evidence for refinement, not for enlarging an arbitrary angular guard.

The native midpoint run **failed**, exit 1, on an invalid native common during
bisection. It preserves four complete rows (cranks 165/167/169/171°, height −3)
in `_build_checks/reverser-phase-midpoints-native-48d71c9.jsonl`, SHA-256
`4c465085fe8c711dc7857d9266fa2ebecf271042432c29b53bd497c9d0c1f441`.
It is neither a completed native survey nor a passing geometry result. The
invalid result is not relabelled empty; diagnostics now include the exact
crank, shaft, axial positions and body pair.

The independent Sol check reproduced the failure on query 40 at crank 173°,
shaft 207.5123519897461°, height −3 and lift zero against the top drum. The last
valid bracket was clear at shaft 207.51234436035156° and positive at
207.51235961914062° (1.767487067998046e−11 mm³). Reusing the swept drum gave an
invalid two-solid common with a bogus volume of 1241.4637972376165 mm³, although
both operands still reported valid. At the same query, forcing a fresh drum
pose gave a valid positive common of 2.8890132738894073e−12 mm³; a fresh reader
agreed. Thus the earlier twenty paired queries were insufficient evidence for
native reuse. No positive value is waived. With fresh native placements, the
complete crank-173° refinement now succeeds at both heights −3 and 0: twenty
boundaries, exit 0. Raw file
`_build_checks/reverser-phase-native-fresh173-48d71c9.jsonl`, SHA-256
`159206126174a74c828493f2a3850f49514229c867c06453c26aa5ebb9f02878`.
The framework investigation of input mutation is continuing separately.

**Do not resume from the four cached-native rows.** They are diagnostic
evidence only: detecting an invalid common late in the sequence does not prove
that earlier, nominally valid results were unaffected by mutated input
tolerances. The 610-bracket native survey in the preceding section predates
this cache experiment and used fresh native placements.

The compiler now joins multiple measurement files while checking each native
record against its own world64 source hash. Unknown sources, duplicate poses
and missing native records are rejected. The focused boundary, resume, cache,
midpoint, compiler and probe gate passes **23 tests**, including refusal to
reuse a native drum even with an identical pose key. These tools still do not
change the production law, controls, or umbrella completion state.

## Higher-counter independent surveys

The five higher input prints each have a separate completed world64 survey:
crank 0…360° and one complete shaft revolution, both in 2° steps, at heights
0 and −4 with zero drum lift. Each command terminated with exit 0 and records
362 rows, 65,522 coarse pair poses and 610 refined transition brackets.
Every active row has ten observed transitions; this does not exclude islands
between samples. No native result or operating restraint follows from these
world64-only files.

The higher print has one pinion and a different fitted tooth relief from the
ones print. Its height-zero samples meet the one-tooth row; height −4 meets
the nine-tooth row. Copying the ones height/phase profile would therefore be
wrong. The observed crank ranges are:

| Counter station | Height 0: 8 active rows | Height −4: 53 active rows |
| --- | --- | --- |
| 2 | 184…198° | 94…198° |
| 3 | 204…218° | 114…218° |
| 4 | 224…238° | 134…238° |
| 5 | 244…258° | 154…258° |
| 6 | 264…278° | 174…278° |

These are independently measured files, not shifted copies. Their common
row counts and 20° offsets do not establish identical tooth profiles or
identical clear-window edges.

- `_build_checks/reverser-station2-world64-48d71c9.jsonl`, SHA-256
  `1b2ff9a95e73100680c074f469b410cc0bfa207ec8f2ffceecc78d4f6afba087`.
- `_build_checks/reverser-station3-world64-48d71c9.jsonl`, SHA-256
  `36f167eac0b9214dc348a56b4b6ea4cabe5687d116636219e10c7440c0940d53`.
- `_build_checks/reverser-station4-world64-0cb681a.jsonl`, SHA-256
  `97c8a332fe0036276a5ad64f29fec55f4dcf74c8826563c9ea539f0b582a87a8`.
- `_build_checks/reverser-station5-world64-0cb681a.jsonl`, SHA-256
  `e58d5438a19c41d1b269c5583f06efcf66b1fe3d2c51dc09ab40e1f4fea8259d`.
- `_build_checks/reverser-station6-world64-0cb681a.jsonl`, SHA-256
  `c626e46f0c55ba53688684b8d7246d86f7225bd2f658ca8db7ed5fe2efee8073`.

`test_higher_station_surveys_match_actual_retained_requests` passes in
435.661 s on framework `82bf530` (exit 0). Its fifteen retained poses cover
all five higher inputs: height −4 during nine-tooth passage, height zero
during one-tooth passage, and height zero with a raised drum. Both kernels'
independent placements match the actual complete-print bounds, and both
gear/drum commons match their actual-root classification and measured volume.
This validates the survey instrument's placement, not clearance of those
poses, an operating restraint, or the complete action-order matrix. The
production model remains unchanged.

## Remaining implementation

Measure the axial admission envelope against **actual retained shaft phase**,
crank rotation and crank elevation for all six inputs and both request
directions. An input may be free in the same crank pose after a different
physical history. Neither a global `crank == 0` lock nor a universal 1.0575 mm
floor follows from this witness. Crossing a blocked band must stop even when
the requested endpoint lies in another clear band.

Express the measured restraint on the existing connected reverser joint;
preserve available play, register history and ordinary parked-crank reversal.
Require red-to-green actual-root contact, long/short requests, relief, repeat,
snapshot/replay and viewer parity before adoption. Tasks 6.2–6.5 remain open;
this finding does not waive the clearing loop or whole-assembly contacts.
