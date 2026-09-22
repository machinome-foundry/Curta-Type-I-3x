# Counter-ones fit and operating restraint

The default operating root now selects the independently measured T08
counter-ones print and fixed-height restraint. This is scoped implementation,
not whole-counter-bank, whole-machine or final pointer acceptance. Higher
counter channels remain unchanged. Upstream STEP/STL files are untouched.

`counter_lockout_parts.py` separates the production part from diagnostic
tools: the locking outline's existing .15 mm relief becomes .16 mm, and the
complete upper print retains its refined .01/.1 tessellation. The source
keyed core, height, datum and other print features remain unchanged. The
original trial parts remain an independent shape oracle. Its wrapper inherits
the production restraint instead of declaring the same crank bound twice.

The crank reads the actual retained counter-ones shaft and bell coordinates
through the existing measured `counter_closing_limit`. No control, macro,
register seed, contact tolerance, sample count or angular stand-off changes.
The existing [trial acceptance](evidence/counter-ones-trial-acceptance-2026-09-21.json)
records candidate short/long stops and browser/full-bank parity. The earlier
ordinary arithmetic batch was incomplete; the missing successive-additions
and selective-clearing case now completes, 1/1 in 329.387 s, through unchanged
tests with the candidate model selected in-process. Other previously completed
candidate cases remain their own evidence, not a fabricated single full run.

## Production evidence

Before adoption, the actual-root withdrawal test fails because the crank
completes instead of blocking (`counter-ones-production-recheck-red.log`,
87.947 s). After adoption the unchanged test passes both requested targets:
180° stops at 174.7853836059494°, and 900° at 174.78538360544917°.
Each stopped complete print is clear in both native and published meshes;
.2° overtravel has positive common in both. Exact snapshot replay, .05°
reverse relief, idle retention and repeat approach also pass. The tiny
short/long numerical difference is retained rather than rounded away.

That three-test process finishes with **one pass and two errors**, not a
green batch (`counter-ones-production-adoption-green.log`, 936.854 s).
The parts-comparison test initially omitted assembly before asking a fusion
for its solid; this test setup was corrected. The next full-machine fixture
exposed a framework lifecycle defect: a stale exact BREP could use a SCAD
`_ArtifactImport` in place of native geometry. A fresh two-test rerun confirms
that independent framework error, while the corrected parts check passes.

Framework `4112d76` fixes the stale exact-leaf path after a minimal red
reproduction in its own worktree. Its 82 exact/currency and 72 STEP/build123d
tests pass, as does this actual Curta fixture in that worktree. It preserves
the existing cache and renders native geometry when the BREP is stale;
no project geometry or collision policy was changed to hide the error.
The production fixture/part pair passes again against integrated framework
main, 2/2 in 30.760 s with observed zero exit
(`counter-ones-production-fixtures-final.log`). The
[evidence index](evidence/counter-ones-production-2026-09-22.json) retains both
failed batches and the separate passing runs, not a rewritten batch verdict.

The station instrument now distinguishes the production station from an
explicit pre-adoption `source=True` station. Otherwise a preservation check
would incorrectly compare the adopted fit with itself. The missing source
selection fails first; the final fixture/source/part suite passes 6/6 in
114.060 s, covering every source station, bounded removal, connectivity,
independent shaft placement and the actual root's complete-print geometry.
The separately corrected part comparison passes 1/1 in 23.52 s.

Final real-pointer acceptance with a fresh current export remains open.
Current viewer timings are not acceptable merely because older candidate
Python/browser banks matched. All remaining counter/result-bank and
whole-machine obligations stay open in the project's task record.
