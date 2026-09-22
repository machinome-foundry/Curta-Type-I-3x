# Pointer completion is a separate acceptance gate

`tools/operating_pointer_matrix.py` exercises actual selector and marker
parts through public hosted-viewer controls, at the unchanged default
`dt=1/240`. It uses camera changes and real nearest-hit gesture targets, not
hidden proxies or host motion calls. Public reset separates cases. The tool
is a diagnostic under development, not completed standalone or full-control
acceptance.

Its report validator requires a terminal completed/blocked outcome for the
intended input, no refused outcome, no pending commands, actual movement,
unchanged other inputs and unchanged register turns. Five unit tests pass
after the missing-tool red baseline; they reject intermediate readbacks,
cancel-only/refused outcomes, no motion, missing outcomes and unrelated changes.
The logs are `_build_checks/operating-pointer-validator-{red,green}-2026-09-22.log`.

Two real first-selector probes on the expanded counter-bank export fail the
pending-command requirement. Both load viewer bundle `8a03c3a3...` at default
dt, perform a 60-pixel downward drag in 12 pointer steps, then release:

- `counter-bank-pointer-first-d9c1833.json`: handle 0 completes one digit;
  the captured state is 1.6666666666666665 with another 48-tick one-digit
  move still active (started at tick 55).
- `counter-bank-pointer-first-settled-d9c1833.json`: even after a public
  snapshot temporarily reports no commands and a completed outcome, the
  next snapshot has another move active and digit 1 at 1.3333333333333333.

Those report/log stems live in `_build_checks/`, remain `pending`, and both
processes exited 1. This demonstrates that the first terminal outcome, or a
transient empty command bank, is not yet sufficient evidence of a completed
multi-event pointer gesture. Whether this is expected queued-gesture behavior
needing a better observation barrier or a viewer defect is being diagnosed in
the viewer repository. No timing change, command truncation or relaxation of
the terminal gate has been adopted. Existing earlier prerequisite pointer
readbacks are not retrospectively relabelled as full terminal acceptance.

## Release-aware first-selector gate

The viewer review finds that a drag may issue successive quanta, and that
`onOutcome` precedes the planner's completion callback. Its pointer-up handler
ends the gesture and prevents subsequent queuing. The harness now first
observes pointer-up bubbling through the actual `#view` mount, then requests
a fresh public snapshot and waits for an empty command bank and terminal
outcome. It retains every outcome rather than assuming one command per drag.
The missing-release validator is mutation-tested red; all six validator tests
pass after restoration. No viewer code or timestep changes for this correction.

The first-selector real-browser rerun now passes with observed exit zero:
three one-digit commands retire completed, the final digit is 3, all other
inputs and all register turns remain unchanged, and no pending command or page
error remains. The final screenshot is inspected. This is one hosted selector,
not the entire pointer matrix or an assertion of real-time performance.

Retained artifacts under `_build_checks/`:

- `counter-bank-pointer-first-release-b15695b.json`, SHA-256
  `94f326dfca3d800523c79d5fefd1606cb6a0c81c704145e99ed0010998abea6c`.
- `counter-bank-pointer-first-release-b15695b.png`, SHA-256
  `fad202c6300c30acaa2a92f7afb7b8394eee5557c78585464e286ceff57b07d5`.
- `operating-pointer-release-validator-red-2026-09-22.log` and
  `operating-pointer-release-validator-2026-09-22.log` keep the mutation and
  passing validator results separate.

The full selector/marker matrix is running in a separate report. Its result
is not inferred from this first selector.

## Async polling correction

The complete-matrix attempt `counter-bank-pointer-matrix-b15695b` fails on
its first selector despite observing release. Inspection of the installed
Playwright implementation finds the harness error: `Page.wait_for_function`
tests the async predicate's Promise for truthiness before its boolean resolves.
The active command had not retired; the diagnostic was correctly rejected by
the final report validator. This is not evidence of a viewer queue defect.

The harness now uses `page.evaluate` to await an explicit asynchronous polling
loop, which awaits each snapshot before examining pending commands. A small
browser regression returns active snapshots twice, then empty, and requires
all three calls before the helper returns. Seven report/barrier tests pass.
An initial test-placement edit put two existing methods in the wrong test
class and produced two setup errors; that log is retained as
`operating-pointer-async-barrier-first-2026-09-22.log`, distinct from the
corrected `...-green-...` result. The full matrix is running again under
`counter-bank-pointer-awaited-5872ce1`; no result is inferred from the earlier
single-selector pass or the corrected unit test.
