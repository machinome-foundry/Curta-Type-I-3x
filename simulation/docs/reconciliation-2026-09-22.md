# Operating Curta reconciliation and completion

The pilot requested that all prior Curta work be integrated into the owning
repositories' local main branches, followed by completion of the operating
calculator. The pilot also authorized autonomous framework/viewer corrections
through Sol subagents when project evidence exposes a limitation. Nothing in
this work authorizes pushing, publication or contacting the original author.

## Recovered branches

The project primary checkout was on `direct-operation` at `8333a6b`, 68
commits ahead of `main` (`60979ad`). Main was fast-forwarded to that complete
checkpoint. The two older project worktrees had stale Git metadata referring
to the former workspace location; `git worktree repair` restored their actual
project-owned paths. Both worktrees were clean. Their branches remain intact.

`clocked-spike` (`bcf2017`) supplied three additional commits containing the
original clocked experiment, recorded oracle and tests. Merge `763390f`
preserves them and updates executable imports for the package rename.
Its 18 tests pass against the historical oracle. This does not re-record that
oracle or substitute the clocked calculator for `OperatingCurta`.

`open-run-simulation` (`06bdfc5`) supplied ten additional commits: an archived,
accepted two-station carry/frame fit and a separate unfinished selected-input
investigation. The frame fit had never reached `direct-operation`. Its source
code is reconciled with the current `machinome` namespace; diagnostic records
retain their original dates and results. The README retains the current
operating status instead of reinstating the old pause. The selected-input
investigation's red contracts remain evidence, not completed fitting work.

The recovered frame fitter passes 7/7 preservation/seating contracts on each
kernel (56.31 s faceted, 60.52 s exact). The installed carry/frame bench passes
10/10 motion and clearance contracts on each kernel (57.51 s faceted,
103.02 s exact). The four lightweight selector-probe tests also pass.
Logs are in ignored `_build_checks/`, named
`reconcile-frame-*` and `reconcile-carry-frame-*`.

## Completion baseline

The active `simulate-the-curta` change reports 12/23 completed tasks. Existing
carry timing corrections are already on framework main `5d5ba18` and viewer
main `684c583`. The additional framework `harden-direct-part-motion` cycle is
now merged at `c81a585`; the viewer `draw-at-the-declared-tempo` cycle is merged
at `fcecb1a`. Their existing branches and records are preserved, with renamed
package paths reconciled against current main rather than reverted.

Framework verification includes 571 affected tests and 34 strict OpenSpec
specifications. The full run had 3,534 passes and two stale version assertions;
those assertions were corrected and included in the passing affected rerun.
Viewer verification includes type checking, bundle build, the actual browser
calculator gesture, 106 documentation tests and ten strict specifications.
Its loaded broad unit run passed 1,454/1,456 tests; the two throughput checks
passed in an isolated rerun. This is not a claim that the original loaded run
was green. The primary viewer bundle was rebuilt after integration.

The actual default remains `simulation.running:OperatingCurta`. The unchanged
six-test operating arithmetic batch completes with six passes in 1,883.841 s
(`_build_checks/reconcile-running-arithmetic.log`). It covers independent
selectors, successive additions/selective clearing, manual calibration,
partial-turn replay, carriage shifting and subtraction/overflow undo. This
job started before framework reconciliation; it does not certify later
performance changes or later physical adoptions. No partial run is counted
as a pass, and no task checkbox changes merely because commits are on main.

The outstanding native result-profile jobs for stations 10 and 11 now finish
with observed zero exits, each checking 23,556 admitted poses with no positive
common. The counter-tens candidate's four unchanged arithmetic tests also
finish, 4/4 in 1,729.122 s. The
[completion record](evidence/bank-validation-completion-2026-09-22.json)
pins their logs, measurement headers and limits. The arithmetic batch started
before production counter-ones adoption; it is not a combined ones+tens check.

The counter-tens candidate's native finite profile emitted a complete summary:
15,714 admitted poses, zero failures, covering 466 shaft rows at each of
carry 0/.5/1. Its [evidence record](evidence/counter-tens-native-completion-2026-09-22.json)
includes source hashes, the full log hash and the anomalous later supervisor
status 143; a zero process-exit observation is not claimed. The completed
arithmetic above, additional heights/action orders and browser adoption are
separate gates.

The [collar continuation](collar-seat-completion-2026-09-22.md) combines the
measured pin/thread clocking with bounded axial facings and verifies complete
rigid neighbours and captured moving seats. Its production acceptance is
tracked there, not inferred from the branch merge.

A refreshed [faceted rigid-rest inventory](evidence/operating-rest-inventory-2026-09-22-faceted.json)
has 389 rigid occurrences, 253 positive pairs and no refused intersections.
It includes the collar/thrust fits and the counter-ones working change, not
the new isolated clearing-cover/counter-body seat trial. The largest remaining
common is that cover/body pair, 468.059392 mm³ faceted, independently measured
as 468.259260 mm³ native. No positive contact is waived by this survey.
The subsequent [outer-seat fit](clearing-carrier-seat-2026-09-22.md) is now
adopted, with three production checks passing on each runner. Its refreshed
survey removes only that pair: 252 remain, with no added pair or refusal.
The [counter-ones production checkpoint](counter-ones-adoption-2026-09-22.md)
is committed at `eb520bf`; its original failed batch and separate passing
reruns remain distinguished in the evidence.

## Performance findings

A real crank click in the current standalone viewer was received, remained
running and reached only 96 degrees after a 45-second observation. The
displayed frame lagged behind at 60 degrees. There were no page errors and
the independent selector gesture passed. This is not a usable completed
operating check. Subsequent no-WebGL profiling also found substantial run
engine cost, so software rendering contention alone does not explain it.

The Sol agents are pursuing separately owned framework and viewer fixes.
Python profiling names repeated port-declaration enumeration; browser
profiling names repeated path binding and expression scope construction.
The pilot approved a clean framework worktree from verified main while leaving
the unrelated untracked example directory untouched, and reaffirmed that all
framework edits must be in worktrees because other agents are working.

Framework port enumeration, graph-order and path-order optimizations are
integrated, the last at `471d00a` after preserving the concurrent CI and
exact-leaf histories. The fixture-exposed exact-leaf repair is `4112d76`.
The pilot explicitly reaffirmed autonomous reconciliation of concurrent-main
updates in isolated worktrees, preserving histories and revalidating.

Viewer caches are integrated at `3ef7482`; later CI/evidence-only changes
reach `1f91191`. The pinned older export completes a no-WebGL full turn in
192.371 s and replay in 181.700 s, with identical 213-coordinate terminal
banks and snapshots. The harness exits 1 on an incorrect cumulative-recorder
comparison because restore clears those rings; that failure is preserved.
Corrected turn-local accounting passes a small fixture but has not yet
completed a new full Curta run. These are not usable two-second gestures,
fresh-current-export checks, or real-pointer completion. Further measured
evaluation work and the mechanical/pointer gates remain open.

The original source assets, untracked assembly video and untracked
`screenshots/reverser_inspection.png` are preserved.
