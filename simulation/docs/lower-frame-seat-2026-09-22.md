# Lower shell / frame key-seat investigation

Status: adopted with scoped production verification. No upstream asset or operating datum
changes. This is a simulation-source finding, not a claim about the author's
working physical prints or a manufacturing recommendation.

At the current concentric lower-shell datum, the main-body common is
75.264065 mm³ faceted and 2.977763 mm³ native. The lower bearing plate is
native-clear but the coarse shell mesh intersects it by 5.653221 mm³.
Refining only the shell to .01 mm linear/.1 rad angular deflection changes
the main-body common to 2.971420 mm³ and clears the bearing in the direct
placed-mesh probe. This separates a mesh issue from the native key-seat issue.

The remaining native common is one small region at world X47.9273..49.4946,
Y39.6955..41.5536, Z-22.2..-18.45. Native face normals identify the shell key
flank at u=11.4 and the mating frame flank at u=11.01, where
u = cos(40°)X - sin(40°)Y. Their 0.39 mm crossing is visible in the inspected
horizontal section at Z-20. This is not an overall cylindrical interference.
The shell and frame remain on their established datums; rotating either to
solve this one contact would move unrelated seats and the reversing window.

The initial production wrapper fails both faceted clearance contracts
(2.87 s); native passes the bearing and fails the main body (3.09 s).
Adding bounded-removal and retained-key capture contracts gives 1/4 native
(3.42 s), as expected before a fit exists.

`SeatedBottomHousing` is an isolated bounded key-flank candidate. Its first
build attempted to invoke a nonexistent source `adjust()` superclass hook;
both failed process logs are retained. Removing that invalid call allows
the four native contracts to pass (21.84 s): both neighbours clear, the
source solid loses material only inside the declared upper-key zone, no
material is added, connectivity/extents remain, .02 mm lateral motion is
free and .1 mm toward the mating flank remains blocked.

The first four-contract faceted run is 3/4 (21.00 s), with a
0.000009558575 mm³ bearing common. The separate actual placed-mesh probe
reports zero for the same pair, so runner/probe comparison is in progress.
That positive result was not waived by size. The later contract also adds
the fixed pre-fit 213-coordinate initial-bank witness.

Evidence is retained under `_build_checks/`: `lower-frame-seat-red-*`,
`lower-frame-seat-contracts-red-exact.log`, `lower-frame-seat-trial-first-*`,
`lower-frame-seat-trial-{exact,faceted}.log`, and
`lower-frame-contact-{face-probe,trial}-2026-09-22.{json,png}`. The original
section's cropped viewport is superseded by the full-height, radial and
horizontal three-panel section; neither is a whole-machine render.

## Precision finding and final bounded fit

Independent review traced the bearing discrepancy to the standalone probe's
world-float32 cast, not a framework defect. The CLI preserves the local STL
face at Z20.100000381469727 through placement, yielding a real positive
3.8146972e-7 mm mesh thickness against the native-flush shoulder. Casting
already-placed vertices to float32 hides that thickness. The
[precision record](mesh-probe-precision-2026-09-22.md) keeps this limitation
explicit; the framework was not weakened.

An axial seat contract fails before correction: lifting the shell .02 mm
into the bearing yields 8.404151 mm³ native common. The final shell faces
its local Z12 shoulder to Z11.95 inside R64.111 (bearing's R64.061 plus
.05 radial gap). No part is moved. The key cutter is additionally capped at
R64.4805, the frame's R64.4305 plus .05, avoiding unnecessary removal in the
outer wall. Both removal regions are bounded independently in the test;
extents, connectivity, no material addition and the deeper original key remain.
Both directions of .02 mm key and axial motion are free; .1 mm toward each
seat remains blocked. All six isolated contracts pass, 23.35 s native and
21.96 s faceted.

## Production adoption

Returning the wrapper to the unmodified production root fails 4/6 native
contracts (4.99 s), retaining only the initial-bank and native bearing-clear
passes. `RunningEnclosure` then selects `SeatedLowerHousing` without a datum
change. The thin actual-root wrapper passes 6/6 native (23.61 s) and faceted
(22.06 s). The original five enclosure/marker/base-seat regressions pass on
both runners (25.28/17.53 s). Their placement reference uses the fitted local
bottom print only; the independent source-removal test supplies its fidelity
proof. Other enclosure references remain unchanged.

The production full-precision faceted rest inventory changes from 262 to 259
positive pairs, with no new pair and no refused common. Both intended frame
pairs disappear; a small lower-shell/bottom-shell raw common also disappears
with the changed tessellation. That third numerical change is not a claim of
new physical separation. The 259 remaining pairs are not waived. The earlier
252 count used different parts and world-float32 precision and is not a
paired baseline for this fit.

The final four-panel production image
`_build_checks/lower-frame-contact-production-2026-09-22.png` was inspected:
the key gap and shoulder at world Z-138.50 below the bearing's -138.45 face
are visible. Both complete native commons and world-float64 mesh commons are
zero, and all 213 coordinates remain unchanged during inspection. The
[evidence index](evidence/lower-frame-seat-2026-09-22.json) pins the actual
source, tests, image and inventory pair. No whole-machine or OpenSpec task
completion follows from this scoped fit.
