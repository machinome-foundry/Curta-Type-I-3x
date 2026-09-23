# Pointer completion is a separate acceptance gate

## September 23: current radial-ball production matrix

The current 214-coordinate production export also passes all **23 non-crank
controls** in one hosted-browser run, exit zero and no page errors. It uses
program `b81b2ce7af6556c12a68829fa3444d1dc6efc7c110d2cd88aff57fff0b9700f4`,
manifest `bab5b1248bf8f100b764bf37bfd00065770df876bb83ec191b44549a9727569b`
and viewer bundle `0d602f50532ffe3c906b0bea285352cf60c5165da9b77d818d948f75f5e113df`.
Every case observes the actual pointer gesture and release, terminal outcome,
empty pending bank, unchanged other inputs and unchanged register turns.
The inspected final PNG shows coherent assembly and visible control outcomes;
its close view clips the crank top and machine base, so it is not a whole-model
alignment image. The seated shift stops at .18 degrees and seated clearing at
1.437226368040361 degrees. Neither is relabelled a completed free movement.

Artifacts in `_build_checks/`:

- `operating-final-prefix-all-noncrank-262378b.json`, SHA-256
  `7bd03a0854f8e114eeaeb43f37f18639364348f94f57f5691f094319628d0bb9`.
- `operating-final-prefix-all-noncrank-262378b.png`, SHA-256
  `5374ebb98305966015c4d7311997211938d7b9dc2264aa9dec96d4d1379ce665`.

This supersedes the older 213-coordinate non-crank gate below. It does not
complete crank gestures, wrong-order sequences, the standalone matrix or
mechanical clearance acceptance.

## Fresh complete non-crank matrix

All **23 non-crank controls** now pass in one production-export hosted-browser
run: eight selectors, ten decimal markers, crank lift, reversal, carriage lift,
seated carriage shift and seated clearing. This uses the unchanged default
`dt=1/240`, program `3e1d5051...` with all 213 coordinates, and integrated
standing-cache bundle `0d163827...` in `_build_operating_standing_cache_884b01e`.
Every case uses a real hit/handle, observes release, waits for an empty pending
command bank and a completed/blocked outcome, and checks other drivers and all
register turns unchanged. No page errors occur; process exit zero is observed.
The final screenshot is inspected: it is a close control view cropped at top
and bottom, not a whole-machine alignment view or 23 separate pose screenshots.

Report `_build_checks/standing-cache-production-all-noncrank-pointers-884b01e.json`
SHA-256: `e0636948315868a93cd9e0d20fcb650a9e7fb82705ce27172e20e903ba218073`.
Named no-op attempts remain in the report and are not counted as coverage.
Marker neighbours, seated carriage shift and clearing encounter their declared
physical stops. Crank rotation/full-turn arithmetic, released-carriage operation,
wrong-order sequences and the full standalone-page matrix remain separate
gates. This result is not whole-machine mechanical clearance.

## Earlier diagnostic history

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

## Eight selectors and first marker

The corrected awaited matrix preserves eight passing selector cases in
`_build_checks/counter-bank-pointer-awaited-5872ce1.json`: all intended moves
retire, no command remains and all other drivers/register turns are unchanged.
The process then fails on marker 1, so the report remains pending and is not
full-matrix acceptance. A separate marker diagnostic shows the first vertical
drag submitted no quantum: release is observed, tick stays zero, and both
outcomes and pending commands are empty. This is not evidence of a stuck engine.

The harness now preserves settled no-op directions as attempts and tries the
next cardinal direction. Such attempts never count as coverage, and unrelated
motion/refusal is rejected before trying again. Eight validator/barrier tests
pass (`operating-pointer-noop-direction-green-2026-09-22.log`). A fresh marker-1
run passes with final admitted rotation 3 degrees and three completed quanta,
no pending command and no unrelated input/register change. Its screenshot is
inspected; artifacts are `counter-bank-pointer-marker-directions-190b1bd`
under `_build_checks/`. It uses the frozen combined-trial export and unchanged
default dt; remaining markers and standalone/full-control coverage are owed.

The subsequent nine-marker run now also exits zero and passes. Marker 2..10
each admits a completed or neighbour-blocked movement, with observed release,
an empty command bank and unchanged other drivers/register turns. The final
screenshot is inspected. Its report
`_build_checks/counter-bank-pointer-markers-190b1bd.json` has SHA-256
`403a2f7660ac0e93b72bb292e4c694ab031ee05a4523d251715dd5e0395e4ab7`.
This completes the ten-marker hosted reset-case matrix on that frozen trial,
not free travel through neighbours or production/standalone coverage.

The tool now additionally offers crank lift, reverser, carriage lift, seated
carriage shift and seated clearing, retaining the same independence assertions.
The selectable-input regression fails red for missing `crank_elevation`, then
all nine harness tests pass. Those five real production-export pointer cases
are running separately. Crank turning and its one-revolution button require
their own arithmetic-aware gate; they are not silently accepted under a test
that assumes unchanged register turns.

Those five fresh production-export cases now pass with observed process exit
zero. Crank lift admits 2 mm, reverser -3 mm and carriage lift 2 mm; seated
carriage rotation stops at .17999999999998786 degrees and seated clearing at
1.437226368040361 degrees. All other inputs and register-turn coordinates
remain unchanged, all commands retire, and no refusal/page error is observed.
The final screenshot is inspected (its closer camera crops the crank tip and
bottom, so it is an interaction image rather than a whole-machine overview).
Report `_build_checks/counter-bank-production-noncrank-pointers-7bdd0a3.json`
has SHA-256 `fecc8086aa0dab8503d7e260c77a8b2ec6f8b1ce120b064e4b882b19793e7e6b`.
This does not cover lifted-carriage free shift/clearing, crank turning, the
one-revolution button, or the unmodified standalone page.
