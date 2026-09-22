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
main `684c583`. The additional unmerged framework `harden-direct-part-motion`
and viewer `draw-at-the-declared-tempo` cycles are undergoing reconciliation
and verification in their own repositories.

The actual default remains `simulation.running:OperatingCurta`. Arithmetic,
complete counter-tens candidate admission and collar acceptance are running
against the recovered state. No partial run is reported as a pass, no pending
physical trial is adopted by this branch reconciliation, and no task checkbox
is changed merely because its commits are now on main.

The original source assets, untracked assembly video and untracked
`screenshots/reverser_inspection.png` are preserved.
