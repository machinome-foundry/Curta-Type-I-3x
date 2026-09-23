# Simulation-only clearing-loop mounting

Status: isolated replacement under verification, not adopted in `OperatingCurta`.
The pilot explicitly chose "Design a simulation-only replacement mounting";
planning commit `1152d81` records the exception in the existing project change.
This does not explain or reproduce the original elastic clip's motion, certify
a printable modification, or change the author's STEP/STL assets. The
[source investigation](clearing-loop-investigation-2026-09-19.md) and its
unadopted T05/T06 trials remain evidence in their original form.

## Mounting and provenance

The new mounting uses the first source rivet's axis and both unchanged cover
holes. The source finger loop and every part of the loop outside an R8 mm
cylinder centred at source (40.5, 0) are unchanged. Within that cylinder, a
closed R3.85 mm bearing replaces the open clip, with a full R8 mm boss over
the original 5.46 mm thickness. A .05 mm loop/cover seating gap preserves the
source first-rivet head clearance.

The first rivet retains its original shaft and head. Its lower stud keeps its
source material but moves to the cover-hole axis as described below. A new R8 mm
flange at local Z12.6..13.6 carries a radius .6 mm stop pin on a 6 mm pitch
radius, extending from local Z11.1..12.7. It enters a round-ended arc recess
in the loop's upper face: .7 mm half-width, 6 mm pitch radius, centreline
angles −89.5..−.5 degrees, and 1.4 mm finished depth. The original second
rivet becomes a flush plug ending at local Z6.5; its remaining lower
stem likewise moves to the cover-hole axis. The unused second clip remains source geometry, not a
claimed active detent or retaining feature.

The closed bearing and headed pivot provide radial and axial capture. The
pin/recess walls provide angular end stops. Assembly over the pivot's lower
stud before seating it in the cover is fixture setup, not an extra operating
release button. These are new simulation design dimensions, not recovered
source tolerances, print-strength calculations or force/friction predictions.

The nominal swivel is −90..0 degrees. Native and published-mesh tests also
establish free positions at −90.4 and +.4 and blocked positions at −90.6 and
+.6. The intended running limits retain that measured free-side play; their
continuous verification and operating adoption remain separate below.

Occurrence mapping is explicit and one-for-one: the original `clearing_ring`
becomes the locally adapted loop; `clearing_ring_rivet_1` becomes the headed
stop pivot; `clearing_ring_rivet_2` becomes the flush plug. No source occurrence
is silently omitted and no cover, collar, crank or clearing tooth is modified.

## Red-first geometry and inspected pixels

The first two new contracts ran against the old `LoopSeatTrial` before the
replacement existed. Both fail: the −84-degree second-rivet common is
3.034345402686586 mm³, and the original first rivet supplies no angular end
stop. `simulation-loop-mount-red-01.log` SHA-256:
`07b0144488c4d177ae85ce0d0e49b1a56210d0a5dd426d379c09ce874d67fcd0`.
The same two tests pass after the replacement (native-01, 17.48 s).

The expanded native-02 invocation passes five tests but fails its sweep
because the probe passed a non-rigid crank assembly to a solid assertion.
It is not a green run. Enumerating all rigid crank leaves corrects that
test fixture, without changing mounting geometry. Native-03 passes all six
tests in 17.23 s; faceted-01 passes six in 6.75 s with zero volume epsilon.

The latest seven-test gate adds the free/blocked end-play check. Native-04
passes 7/7 in 16.59 s; faceted-02 passes 7/7 in 7.98 s. They cover connected
valid solids, original lower studs and finger-loop preservation, every degree
of the nominal stroke against mounted neighbours, radial/axial capture at
five poses, the former second-post obstruction and both end stops.

- Native-04 log SHA-256: `a397d01ea0e5baabdc478f89bcc5af0f2437a6b5f799742d08b44a43eb82ff1d`.
- Faceted-02 log SHA-256: `684b184e2aa1f342cfb88d16b2f0f1354df850eaa01704648058414cd74101aa`.
- Inspected stowed PNG SHA-256: `a8899f4ed0735bef80ca2d9a1297cc3fadf5a0ee3ab216bce327455d15d5b9bf`.
- Inspected deployed PNG SHA-256: `925d94d090281bee96dab4c7907b5390d3cfbc2af8c62e9b0d5e37c4f099256c`.
- Inspected exploded detail 02 PNG SHA-256: `df42633a586cc27c9e590602fdfaf47f3c663a9e1881dfb899a04030c60c99d1`.

The first exploded viewing angle hid the arc recess. Detail 02 exposes it;
both images are preserved. Inspection classes deliberately omit surrounding
assemblies, and the exploded class raises the pivot 6 mm for viewing only.
These are not installed-clearance or browser-control evidence.

## Between-pose clearance

`tools/clearing_loop_sweep.py` checks all 12 mounted neighbours. At each
accepted angular interval, its midpoint surface separation must exceed
`2 R sin(span / 4)` plus a positive 0.00001 mm computational separation guard.
`R` conservatively bounds every moving native point and published vertex
(84.31993500167974 mm here); this encloses motion from the midpoint to any
point in the interval. Intervals subdivide until proved, or fail. Strict
vertical separation is invariant under the independently calibrated Z-axis
rotation and can prove a whole interval directly. Initial valid zero commons
prevent containment from being mistaken for boundary separation. No positive
common is ignored or compared against a volume tolerance.

The native pass uses BREP distances for native neighbours and explicitly named
published Mesh64 geometry for the collar and source-STL covers. The mesh pass
uses full-precision placed vertices without a float32 world cast. Four helper
tests prove complete interval coverage and rejection of inter-sample contact,
non-finite/zero distances and exhausted subdivision.

The initial source-trial diagnostic was interrupted while doing unnecessarily
broad mesh distance searches (exit 130); its partial report is not acceptance.
The optimized probe caps distance searches at the needed separation bound.
Source-red-02 then fails genuinely at −62.5 degrees with zero separation,
between the old whole-degree samples. The replacement passes the complete
nominal −90..0 path in both representations, including 726 certified intervals
at the captive pivot and 90 each at collar, washer and main crank.

- Source-red-02 JSON SHA-256: `1d9702545ce29772d56a3697be5478dd24deda6b0e9732b625ffa644fff5f54e`.
- Mesh64-01 JSON SHA-256: `9cbc9bac8db9fb61048d0c3be843ca07a8c050000f9e34f978613c85504c8499`.
- Native-01 JSON SHA-256: `e666e8ab852c828cbdd2c76d6b35b2571d5bd44b293051565a6b9d5be10f8dfa`.

The wider −90.4..+.4 stroke also passes the full Mesh64 certificate, with
772 pivot intervals and 91 each at collar, washer and main crank. Report
`simulation-loop-sweep-mesh64-play-01.json` SHA-256:
`ced91c26d3a0e3b59e07ddb92c02c8efb94a67465403ad7cfc8cb77ffe508e4a`.
The native counterpart also passes, using the same interval counts and the
explicit source-STL fallbacks above. Report
`simulation-loop-sweep-native-play-01.json` SHA-256:
`139ed8bb39a6cb7b3a3b9372e7e2ede0e30ae663f4aead2612166bdca7ecbccc`.
All raw reports, logs and images are under the worktree's ignored `_build_checks/`.

The shared-shape refactor separates the diagnostic unbounded swivel/rise from
the prospective operating part's bounded swivel; it does not change the
mounting solid. The expanded eight-test gates pass natively (17.58 s) and
again under the default exact policy (17.37 s; its filename incorrectly says
`faceted`). The new negative check removes only the new pin from the
native placed pivot: both previously positive overtravel commons become zero,
while the remaining pivot stays one valid solid. This particular causal check
uses native geometry in both invocations; the other free/blocked assertions
use each runner's selected representation.

- Shared-shape native-02 log SHA-256: `ef0f5e6a42d503bbbc52be1b163c2f360c232aefabe6c5f3fbb22f81788d82ee`.
- Shared-shape mislabeled faceted-01 (actually exact) log SHA-256: `2b8debba4fb7027066c4bb7f0e46ed079956bf01902240c9d81e228658f224f5`.

## Operating adoption still owed

The first complete-root native diagnostic rejects the unchanged lower-stem
placements at every sampled loop angle (0, 30, 60, 90, 90.4, −.4, 0).
Among all 389 rigid leaves, the only positive mounting pairs are pivot/cover
5.471422321620056 mm³ and plug/cover 5.375431934944294 mm³; no intersections
are refused. The loop itself has no sampled positive common. Report
`operating-loop-installed-native-01.json` SHA-256:
`24dce43889807de5458d714b81c3977bbe52589be835f50b499d8d32b43cf36b`.
This is a failed candidate, not a whole-path pass.

The cover's native R3.107 bores have world centres
(38.9856130574289, 10.971416250258184) and
(36.96220621954035, −16.554313981079687). Both differ from the source rivet
axes by approximately (−.38651158, .02841236) mm, a .38755447 mm offset.
The lower R2.9375 stems therefore collide despite nominal radial clearance.
Diagnostic 01 omitted required pose-input binding; diagnostic 02 printed the
first common before a probe-only unsupported face accessor failed. Corrected
diagnostic 03 reads native circle edges and records both contacts and bores.
Neither earlier diagnostic is counted as a passing gate.

The revised mounting offsets only the source material below local Z6.6 by
(−.132055617, −.364362148, 0) in the rivet frame. The upper pivot, pin,
loop, cover holes and all other parts remain unchanged. The first mount is
now explicitly eccentric; the second is a flush seated plug. This is part of
the authorized simulation replacement, not an assertion about original glue
or manufacturing tolerances. The preserved lower-stem check now verifies
material after this declared translation rather than claiming unchanged
placement. The new cover-clearance test first fails at 5.471422321620056 mm³
(8/9 pass), then all nine native tests pass in 36.24 s after the correction.

- Stud-red-01 log SHA-256: `928e3a1ad37f11cc328215efb4c9c6b0dc8e40be496dcc580701670e61089911`.
- Seated-native-01 log SHA-256: `a9513bce90436c7c3567662a1625b32d64f67f81c4b2d22d0970c04bb2aff013`.

That eccentric candidate passes 9/9 default-policy tests too (18.87 s;
again exact, despite the log filename),
but the full placed Mesh64 transport diagnostic rejects its nominally flush
pivot shoulder. Its common is 0.0000013204290563404605 mm³, with a positive
height interval 57.09999990463257..57.099999999999994 mm; this is not a
zero-thickness contact. The separate Mesh64 regression reproduces the failure
while the ordinary exact assertion passes in the same invocation (9/10
pass, 35.83 s). A Sol-led read-only investigation catches this reporting
error: the CLI defaults to exact, and the explicit faceted policy correctly
reports a positive 0.000000054096993002357345 mm³ at the same old pose.
It is a representation difference near the flush plane, not an assertion
false negative. No framework correction or volume allowance is warranted.

Both replacement mounts now have a named .01 mm upward seat. Their source
material is unchanged by that placement, the loop still has its .05 mm seat,
and the flush plug remains .14 mm below the loop. The final ten-test gate
passes natively (35.95 s) and under the same default exact policy (36.57 s), including the explicit
published-world64 check, capture, both stops, and pin-removal negative.

- World64-red log SHA-256: `48c2d0622e5818a8584987a2dd818dbcc0225e000ea50ae4825526a4b4c008b9`.
- Seated-gap native log SHA-256: `ec3376a4bd13fa7521aea7f5b7613ef2bd821bf89bcf521c181be56189e60990`.
- Seated-gap mislabeled faceted (actually exact) log SHA-256: `b74dd8736f45839f6709b44a4e0b15a7843b23041e8331b7180821e862ef7517`.
- Explicit `--faceted` rerun: 10/10 pass, 27.02 s, zero volume epsilon;
  log SHA-256 `c1c2ef8700f8117371210814bd4ab72f405a0c7252094eb6b43ee55330599468`.
- Rejected full-root Mesh64 transport report SHA-256: `6d13ffde0e56aecac5b5d5743558108074a5396e5c5ebab1bb2878414e05ff22`.
- Corrected full-root Mesh64 transport report SHA-256: `1205340014d4b539af651501c2a7599108451f949b6687251f6980b8157345d3`.

The corrected report has 24 independently requested states: full loop travel,
raised crank at 90 and 360 degrees, six carriage positions, clearing at 90,
180, 230 and 360 degrees, and reseating. All three adapted leaves are compared
with all 389 rigid occurrences at each sample, with no positive commons or
refused intersections. Their vertices independently match the expected
deployment, carriage and clearing transforms at every state. This remains
sampled installed evidence, not a whole-machine or continuous-motion claim.

`tools/operating_loop_envelope.py` separately certifies the complete loop
deployment interval against ten central upper neighbours. Their entire
potentially intersecting height bands fit inside an R28.6 mm cylinder:
the native portions leave zero material outside, and all published triangle
vertices lie inside (largest radius 28.500001723 mm, the source-STL collar).
The height bands include 0..9 mm crank/drum rise and 0..6 mm carriage rise.
The full loop path clears that cylinder natively and a slightly larger
circumscribed 128-sided prism in Mesh64, with 91 certified intervals each.
Because those bounds are rotationally symmetric, the result covers every
relative Z-axis phase and permitted lift of the named neighbours. It does
not claim clearance for unnamed parts or the mounting studs; their tests
remain separate. Report SHA-256:
`835733ef6f78083d1c629c352d14e9340d09066392f0d0c45febfd43a6dc40b4`.

The revised local mounting's Mesh64 full-path certificate also passes again
over −90.4..+.4 degrees, with 772 pivot intervals and 91 at each other
distance-tested neighbour. Report SHA-256:
`113249f8920c78facb07a9cb009852c0144ee5bc007141b7aa066c23f8d4c21c`.
The native counterpart passes too, report SHA-256:
`8ba0797e1472fa58035943ed9272ec39ac9d6d4bb41073641c9b94329f5ec69e`.
The native installed transport gate likewise passes all 24 states with no
positive common/refusal, report SHA-256:
`e0c418a3397738d1bbb95fed2125b6ea85b937c659b66d2ecb672b295b67efa2`.

The default root still has no `loop_deployment` input. Two production-facing
tests prove that red baseline: the labeled control is missing, and a physical
loop request is rejected as undeclared (2 tests, one failure and one error,
4.742 s). The test is not weakened to accept missing operation.
Log `operating-loop-adoption-red-01.log` SHA-256:
`7af8df02ede24a057be6f6d99a33bbf07a247391429342a3a7928f9488b8b60c`.

The unchanged `LoopOperatingTrial` then exposes a framework declaration gap:
copied inherited controls hold the ancestor carriage declaration by identity,
so the compatible replacement carriage fails class construction. The separate
framework cycle `inherit-controls-through-replaced-child` fixes only validated
ancestor-control provenance and effective-path resolution. On its final
runtime source (`control.py` SHA-256
`6994068fb2c8a5d53930c230eb30bdc1972e395de420a33b8662fa62566f448c`,
`program.py` SHA-256
`101ac4f22e2c45fa7deb8da6b922d55f89f899683f72ffd3dae449a45d8cc9d2`),
both trial operation tests pass in 11.018 s: partial motion, both bounded
stops, repeated requests, relief and exact restore/replay. Every old coordinate
stays unchanged during loop requests. Log SHA-256:
`fbd70b453040941d222849ee66fa4c8e806f8c1aae65c05a9da451f893dcd32b`.

The preservation gate additionally compares the trial with the unchanged
default at rest and after crank, carriage and clearing requests. Only the
loop driver and swivel are added (214→216 coordinates); all old bank values,
all 386 unmodified rigid meshes and every flexible mesh match exactly. The
same 389 rigid occurrences remain, with 25→26 controls. That gate and both
operation tests pass 3/3 in 154.076 s, log SHA-256:
`8e8e0430b11a61d0cec1d68a6d0bacdfc510a3531d3121b13736311f3feea3e3`.

The normal standalone export succeeds with document version 13 and program
identity `2b6b59dbb135bd0c0ced9ba87fcc8df9dc36588138d1b0294ce7b8543588df1b`.
The installed API-26 viewer refuses it at load: deployment and clearing are
both Turns on the same visible loop, though they explicitly select different
joints. No pointer executes. Failed report SHA-256:
`e2228ef9848f7dd3dc9813b920154961911813c500c27a58f48ec68eef5f2355`.
Its generic harness retains `validation: pending` when it writes the exception;
the failure and nonzero exit are the authoritative result, not acceptance.
The separate viewer cycle `distinguish-same-part-joint-controls` must provide
independent named handles before operating adoption. It declares API 27 with
the same document schema; this does not claim a published package.

The final local exploded-detail snapshot was visually inspected: it shows
the captive head lifted 6 mm for inspection and the arc slot underneath.
It is not a full installed-machine image and does not expose every underside
feature. Image SHA-256:
`0c7e6af08d2d0d1e30437173b8d185b20b4e87fe33c8f258ef4da4714712b706`.

Next: exercise actual hosted and standalone gestures with the compatible
viewer, finish the unchanged arithmetic and clearing contracts on the trial,
then adopt and verify the production root. No task closes from the isolated
mounting alone.
