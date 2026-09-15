# Running-operation prerequisite checkpoint — 2026-09-15

The pilot visually accepted the markings and authorized Python-side interactive
implementation while the viewer's retained-angle work continues. Browser
support is not a prerequisite to implementing and testing Python mechanics;
actual pointer operation and Python/viewer replay still need later validation.
This supersedes the earlier clearing declaration refusal as the current
checkpoint. No production mechanism or control has been migrated yet.

Project starting commit: `637e5fd`, branch `direct-operation`.
Framework tested: `8e15791e5fe66aecced30fc3c1735a62c71cad90`, clean, including
ADR-121 (`32cfc56`). No framework or viewer code was changed here.

## Retained-angle clearing is available in Python

The original declaration probe now constructs. Its old one-sided schematic
gate was insufficient for bidirectional clearing: with a zero wheel, requesting
-12 then -720 degrees moved the wheel to -732 degrees. The new test first
failed on that actual motion, then passed with ADR-121's finite zero band.

`simulation/tools/direct_operation_probe.py` now accepts a fixture's initial
angle and uses the documented half-degree example band. This width is NOT a
Curta clearance measurement. The tests cover all ten initial digits, both
directions, a partial request, completion, another complete sweep over the
cleared wheel, snapshot restore and identical replay. The ring finishes its
travel while the wheel stays in the gap. These are public-API prerequisites,
not tests of the real rack or a completed clearing implementation.

## New finding: changing carry association forms a conditional cycle

The real project keeps the carry levers and transmission shafts on the fixed
frame; the number dials move with the carriage. `transmission.shifted()` and
`channel_values()` already express which dial is above each fixed channel in
the pose model. For fixed channel 1, its lever is tripped by dial `shift`,
and its output shaft engages dial `shift + 1`. Retained operation must keep
the lever's latch and each dial's history on their actual mechanical parts.

The geometry-free `simulation/tools/shifted_carry_probe.py` reduces that
association to two wheels and one fixed carry lever:

| Carriage position | Lever reads | Lever's output drives |
| --- | --- | --- |
| 0 | Lower wheel | Higher wheel |
| 1 | Higher wheel | The next wheel, outside this reduced fixture |

Each position's active graph is acyclic. Across both possible positions,
however, the higher wheel and the fixed lever appear on both sides of a
dependency. The mutually exclusive gates do not eliminate that cycle from
the compiled program.

The two fixed-position specializations construct and admit a crank request.
The identical association with a live carriage input fails during `Sim`
construction, before any operation:

```text
UnsupportedLaw: the relations
(crank, shift, clearing, carry.travel, higher.turn) drives higher.turn,
(lower.turn, higher.turn, shift, carry.travel) drives carry.travel
form a cycle the run cannot order: each waits on a coordinate another determines.
A running program is acyclic, because the rest render solved every relation
in one direction.
```

The fixture's latch thresholds, direct drive and clearing term are schematic;
it does not claim Curta timing, tooth contact or a correct arithmetic result.
Its purpose is to distinguish fixed-position construction from the live
association the migration needs. The separate finite-band fixture above
establishes that the new own-coordinate gate works on this same installation.

## Required resolution before migration

Establish a supported public representation that keeps real fixed carry-lever
state while changing its dial association as the carriage moves. This probe
proves the direct representation is refused, not that every possible
representation is impossible. If no supported composition exists, the
framework needs its own design decision and change; this project does not
select a cycle solver or new API spelling.

The following are not substitutes for the approved operation:

- Freeze carriage position as a construction parameter: both fixed graphs work,
  but this removes the live physical input.
- Reconstruct the model/run on a shift: this changes program and snapshot
  identity and does not establish retention of the existing mechanical state.
- Add per-dial virtual latch parts, a page-local register, or per-tick project
  bookkeeping: the accepted design puts memory on real run-banked coordinates.
- Drive decorative carry levers from a separate arithmetic answer: that would
  stop testing the carry mechanism as the source of the next digit's motion.

The operating references remain the project build manual and the manufacturer's
[instruction transcription](https://trmm.net/curta/): carriage movement changes
the digit alignment, while its controls and the crank remain independently
operated under their physical interlock. Geometry and interlock measurements
are still needed after the representation is settled.

## Reproduce

From this project root, using the workspace environment:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD" \
  ../../../.venv/bin/python -m unittest simulation.test_direct_operation_probe
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD" \
  ../../../.venv/bin/python -m simulation.tools.direct_operation_probe
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD" \
  ../../../.venv/bin/python -m simulation.tools.shifted_carry_probe
```

The first two succeed. The last prints both working fixed associations and the
live-selection refusal, then deliberately exits 1. It is not a passing
interactive-machine test. No CAD build is needed for these probes.

All 32 standalone project unit tests pass, including the two prerequisite
tests, and `openspec validate simulate-the-curta --strict` passes. Full CAD
regressions and new snapshots were not rerun: only diagnostics, tests and
records changed, not production geometry, motion or the published controls.

## Disposition

Pause the full Python migration for this representation decision. The existing
machine, markings and pose-based geometry tests remain unchanged. Tasks 6.1–6.6
remain open: viewer-pair and pointer validation are deferred by the pilot, not
waived, and these prerequisite tests do not complete the mechanical run tests.
The earlier whole-machine thread/contact findings remain separate and open.
