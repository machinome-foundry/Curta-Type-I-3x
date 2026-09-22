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
