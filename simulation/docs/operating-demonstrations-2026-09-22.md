# Separate retained-operation demonstrations

## Current loop-enabled production checkpoint — 2026-09-23

The adopted 216-coordinate `OperatingCurta` now passes both unchanged tests:
2/2 in 1,919.092 seconds, observed exit zero. All six named demonstrations run
twice from their fresh-machine snapshots, with every requested action and
retained reading checked and complete snapshots/outcome lists equal after
replay. The runtime is project `e39d05a` (unchanged through documentation and
test-tool head `4486849`), framework `e4ff031`; the process uses CPU 12 and
the test's unchanged `dt=.1`, not the browser timestep.

Log `_build_checks/operating-loop-production-demonstrations-01.log` SHA-256:
`c591a668b37355385886341a0805d6f043c6532899e6df4a2d6c53faab8eccb5`.
This supersedes the older 214-coordinate root for arithmetic/replay acceptance.
It does not certify moving contacts throughout every demonstration; that
whole-machine obligation remains open. Loop deployment has its own travel,
retention, stop/replay and actual-pointer gates in the
[mounting record](clearing-loop-replacement-2026-09-23.md).

## Demonstration interface and historical evidence

`simulation.operating_demonstrations` supplies six named physical-request
sequences: addition, carry, overflow, subtraction, shift and clearing.
They are not added to the ordinary part-control surface and do not replace
any independent control. The legacy posed `Demo` is unchanged and must not
be mistaken for this operating acceptance.

Each sequence starts by restoring a caller-owned fresh-machine snapshot,
then issues only ordinary selector, crank, carriage and ring requests.
There are no register setters or arithmetic result assignments. Overflow
prepares both nines banks by physically subtracting one from zero; shifting
explicitly lifts, turns and seats the carriage; clearing explicitly lifts,
sweeps the result and counter halves, sweeps back and reseats. Every action
has a positive duration, must retire completed and checks its stated retained
readings. Ordinary operation does not call the demonstration helper.

Example Python fixture (the `.1` step is the explicit project acceptance
setting; this does not alter the browser's default timestep):

```python
from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.operating_demonstrations import replay

sim = Sim(OperatingCurta(), dt=.1)
initial = sim.snapshot()
outcomes = replay(sim, 'carry', initial)
```

After the missing-module red baseline, the definition and actual replay tests
pass on framework `4bff28e`: two tests in 740.222 s, observed exit zero.
The replay test runs all six sequences twice, checks every command/readout
and compares the complete snapshots and outcome lists exactly. This was the
production root before higher-counter adoption (the mechanism is unchanged
between `5872ce1` and `ad841f2`), with the new demonstration files. The retained log
`_build_checks/operating-demonstrations-first-2026-09-22.log` has SHA-256
`859f188f5f8df927d721d936ed35dc4f088aca91a5c1d0fafc735adcf5d116c4`.

The fresh adopted production root (`7107b1c`, unchanged runtime through
`e5636f8`) subsequently passes the same two tests in 840.603 s, observed exit
zero. All six demonstrations replay twice with exact snapshots/outcomes.
The log `_build_checks/operating-demonstrations-production-7107b1c.log` has
SHA-256 `d17e96d71a9444cddcd221cf8e76ad45d8e300269bae128c86dfb9a81462c6b8`.
Framework `a659cc7` has unchanged runtime from `4bff28e`.

Callers may install `sim.every` sampling before replay. Fresh native/world64
moving-interface checks throughout these demonstrations, browser demonstration
delivery and final layer/whole-machine acceptance
remain separate obligations. No OpenSpec checkbox closes from this replay
result alone.

## Production reverser checkpoint — 2026-09-23

The actual retained production runtime `8668330` (documentation-only main
`c44e5bc`) passes both unchanged tests again on framework `1b136de`:
2 tests, 1,935.036 seconds, observed exit 0. All six named sequences replay
twice; every request must complete, each stated reading is checked, and the
complete terminal snapshots and outcome lists match exactly after restore.
The process used CPU 15 while an independently pinned hosted-pointer gate and
later isolated mounting work ran elsewhere; this duration is not a paired
performance measurement. Log
`_build_checks/reverser-production-final-demonstrations-01.log` SHA-256:
`676ab5478b83a2b858ae2f2e18c51ea7633422bc4aa12fb9aebf01957e8412e3`.

The pilot authorized a simulation-only loop mounting while this run was in
progress. That unadopted fixture does not alter this 214-coordinate production
root. These results must not be relabeled as a future loop-enabled root's
regression or as whole-machine moving-clearance acceptance.
