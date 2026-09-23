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

The first rivet retains its original lower stud, shaft and head. A new R8 mm
flange at local Z12.6..13.6 carries a radius .6 mm stop pin on a 6 mm pitch
radius, extending from local Z11.1..12.7. It enters a round-ended arc recess
in the loop's upper face: .7 mm half-width, 6 mm pitch radius, centreline
angles −89.5..−.5 degrees, and 1.4 mm finished depth. The original second
rivet becomes a flush plug ending at local Z6.5; the original seated lower
stud is preserved. The unused second clip remains source geometry, not a
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
faceted (17.37 s). The new negative check removes only the new pin from the
native placed pivot: both previously positive overtravel commons become zero,
while the remaining pivot stays one valid solid. This particular causal check
uses native geometry in both invocations; the other free/blocked assertions
use each runner's selected representation.

- Shared-shape native-02 log SHA-256: `ef0f5e6a42d503bbbc52be1b163c2f360c232aefabe6c5f3fbb22f81788d82ee`.
- Shared-shape faceted-01 log SHA-256: `2b8debba4fb7027066c4bb7f0e46ed079956bf01902240c9d81e228658f224f5`.

## Operating adoption still owed

The default root still has no `loop_deployment` input. Two production-facing
tests prove that red baseline: the labeled control is missing, and a physical
loop request is rejected as undeclared (2 tests, one failure and one error,
4.742 s). The test is not weakened to accept missing operation.
Log `operating-loop-adoption-red-01.log` SHA-256:
`7af8df02ede24a057be6f6d99a33bbf07a247391429342a3a7928f9488b8b60c`.

Next: bind independent bounded deployment
on the visible loop, prove partial motion, both stops/retry/relief and exact
restore/replay, check installed carriage/clearing transport and crank
neighbours, then exercise actual hosted and standalone gestures. Rerun
neighbouring retained arithmetic and clearing after adoption. No task closes
from the isolated mounting alone.
