# Clocked Curta

`simulation.clocked:ClockedCurta` is the third model, registered as
`clocked_curta` beside `fast_curta` and `operating_curta`. It uses the
framework's clocked-machine support at `1a959d3`, merged to framework main
during this implementation; it does not work with the published framework
release. Neither sibling implementation is changed.

This implements the pilot's request directly in this project. The earlier
project spike at `bcf2017` supplied the neutral operation corpus and recorded
running-model oracle. Its prototype executor is not used: `State`, `commits`,
request clipping, event location, atomicity, snapshots and restore all belong
to the framework's public `Sim`.

## Operate

From this project directory:

```sh
export PYTHONPATH="../../../solid-node:$PWD"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
../../../.venv/bin/solid build clocked_curta
../../../.venv/bin/python -m unittest -v simulation.test_clocked.ClockedOperationsTest
../../../.venv/bin/python -m simulation.tools.clocked_benchmark --running
```

For browser operation, select the matching viewer checkout too (API 18,
commit `757ad84`, now on viewer main), without changing the shared installation:

```sh
export PYTHONPATH="../../../solid-node:../../../solid-node-viewer:$PWD"
../../../.venv/bin/solid viewer
../../../.venv/bin/python -m simulation.tools.clocked_browser_probe
# Optional interactive launch; not started by this implementation:
../../../.venv/bin/solid develop clocked_curta
```

The browser probe mounts the real build in headless Chromium through the
paired bundle, serves local assets through request interception, exercises
the public machine handle, writes `snapshot-clocked-browser.png`, and exits.
No persistent service or viewer/framework edit is needed.
In the browser panel, set a selector, set the `crank_rotation` nudge amount
to `360`, and press `+` repeatedly. The crank's editable position is an
absolute request; repeatedly entering the same position does not add again.

```python
from solid_node.simulation import Sim
from simulation.clocked import ClockedCurta, register_reading

sim = Sim(ClockedCurta())  # no dt
sim.move('digit_1', to=9)
sim.move('crank_rotation', by=360)
assert register_reading(sim) == 9
sim.move('crank_rotation', by=720)
assert register_reading(sim) == 27
saved = sim.snapshot()
sim.move('carriage_elevation', to=6)
sim.move('clearing_rotation', to=230)  # result-bank check
assert register_reading(sim) == 0
sim.move('clearing_rotation', to=360)  # counter-bank check
assert register_reading(sim, True) == 0
sim.restore(saved)
```

The inputs have the operating sibling's names and units: eight `digit_N`
selectors, `crank_rotation`, `crank_elevation`, `carriage_rotation`,
`carriage_elevation`, `clearing_rotation`, and ten `marker_N_rotation` inputs.
`run`, `rate` and instruction triggering do not apply to clocked requests.
The published instruction is descriptive metadata.

Session setup accepts `result_0.value` through `result_10.value` and
`turns_0.value` through `turns_5.value`, in units-first order, through
`Sim(..., state=...)`. These retained digits are not user controls.
`register_reading` reads committed digits; inspect the physical dial joints
for a mid-stroke reading.
Keep the controls at rest when supplying initial digits. Reach other starting
poses through requests and preserve them with a snapshot: a hand-written bank
must also supply consistent clearing history.

## Model and evidence

The fitted geometry and measured crank-phase, complement, carry, spring,
detent and shaft laws are reused. Seventeen digit states change together at
each forward crank revolution. Per-digit clearing events use the measured
rack pitch and the digit standing there, in both sweep directions. One
additional state, `clearing_check`, remembers the last clearing check reached;
the continuous rack travel from that check poses a partially cleared dial.
Capture sets a digit to zero and its missing-tooth gap keeps it there.
The ratchet is an own-read bound over the 116 measured tooth stops through
357° in each revolution, with the zero stop covering the remaining gap. It
selects and returns the same representable absolute tooth angle, avoiding an
unstable angle/pitch round trip. It adds no state or per-tooth commit events.

`Operation` is a geometry-free control frame: its constrained coordinates
feed the existing physical joints. It adds no part and retains no coordinate.
`PoseValues` groups intermediate ports, also outside the retained bank. This
keeps the arithmetic and input constraints explicit without copying the
mechanical geometry or integrating its hundreds of coordinates every tick.

The crank ratchet permits only its measured tooth backlash, and the zero stop
prevents crossing back over a completed stroke and committing it again.
Crank lift, carriage lift and carriage rotation have the measured stroke
limits. The crank and clearing lever cannot both leave their checks; the
carriage cannot seat with the clearing lever between checks. Decimal marker
neighbor bounds are reused from the operating model. The spike's two
deliberately open interlocks remain open: setting selectors off crank rest,
and cranking with the carriage unseated. Disengaged dials remain stationary.

The spike's assumed 180-degree clearing check is corrected here. The existing
measured `clearing_stop_motion.PIN_DROP` profile repeats its rest at **0 and
230 degrees**, not at 180. The high result racks extend beyond 180 degrees:
using 180 as a check can leave a high dial between teeth and then falsely
permit seating. The nominal 0/230 checks also bracket the complete result and
counter banks. Mid-rack inspection and reversal before capture use the
closed-form rack travel; operation and seating remain locked until a check.

There is one explicit **model-validity restriction** beyond the spike's
interlock audit: carriage lifting also starts at a clearing check. Otherwise
moving the ring while seated and then lifting into a rack mid-passage would
invent travel from an earlier check. This restriction keeps the integer-digit
closed form's starting condition valid; it is not evidence that the real
machine mechanically forbids that manipulation. A separate test pins the
restriction and the high dial that remains uncleared at 180 degrees.

`clocked_cases.py` and `clocked_oracle.json` preserve the spike's corpus and
recording (framework `81c5364`, dt 0.1), with provenance in their headers and
the fixture. Thirteen applicable scenarios compare committed readings at
stroke ends and actual dial poses at every recorded read, including partial
crank motion. The allowed pose discrepancy is the running model's documented
half-degree zero-capture band, plus fixture rounding. Five audit scenarios
exercise knowingly missing running interlocks or fractional clearing; they
are not asserted equivalent. Their relevant clocked behavior is covered by
direct expectations, including continuous partial clearing and blocked travel.

## Timing

Measured through `simulation.tools.clocked_benchmark --running` on the same
framework commit and machine, with one BLAS/OpenMP thread:

| Measurement | Seconds |
| --- | ---: |
| Clocked import | 21.2637 |
| Clocked construction | 2.3851 |
| Complete clocked stroke, median of 20 | 0.07875 |
| Clocked stroke split into 20 requests/poses | 1.56363 |
| Running construction | 5.3808 |
| Running stroke, 20 ticks at dt 0.1 | 14.4092 |

The measured whole-request speedup is **183.0×**. One request poses once,
whereas the running stroke poses on 20 ticks. At the **same 20-pose count**,
the measured speedup is **9.2×**. These are operation latencies, not browser
frame rates. Import and construction are excluded from both stroke figures.
Twenty clocked additions of nine finish at result 180 / counter 20. The final
timing run used framework main, with the geometry regression no longer running.
Its raw report is `_build_clocked_checks/final-benchmark.json`.

The finite Chromium probe on the actual marked assembly measures **36.95 ms**
median per complete stroke (20 samples), and **647.7 ms** for one stroke split
into 20 requests/poses. These include the public machine handle's pose work,
but not a separately painted display frame per request: they are not FPS
measurements. The raw report is `_build_clocked_checks/final-browser.json`.
Both reports measure the final direct tooth-position bound, not the earlier
division-based or retained-tooth prototypes.

## Limits

A viewer at API 16 and document versions 1–7 cannot execute this version-8
document. The matching viewer checkout above reports API 18 and versions 1–8
and **does execute the actual model**. Both mains were verified at exactly
the tested worktree commits after the pilot merged the branches; no product
content changed in the switch from worktrees to main.
The finite browser probe agrees with all 30 applicable committed readouts
across the same 13 oracle scenarios. It also verifies partial and repeated
strokes, a blocked mid-stroke lift, separate clearing of both banks,
snapshot/restore and the repeated-reverse ratchet boundary. Its rendered
page was visually inspected, including the surface markings that OpenSCAD
snapshots do not draw.

Operation is through the browser's input panel or its `machine()` handle,
not part dragging. The instruction remains disabled metadata under the
current clocked contract. The generic panel is large with 23 physical inputs;
this increment does not redesign the viewer's control layout.

The existing source geometry has open whole-machine integrity findings; this
model is not a new claim of fabrication readiness.

## Validation

All **38 operation and law tests pass**, including eleven clocked tests and
the arithmetic, cycle, material-connectivity, dial-cam, running-law,
running-clearing and running-limit regressions. The clocked oracle test
covers 13 scenarios, comparing every recorded dial pose and all applicable
committed readouts.

The operation tests began red with the missing sibling. The zero-stop test
then caught a real implementation defect: the tooth-pitch ratchet alone
admitted about three degrees of reverse travel at a completed revolution,
allowing that stroke to be replayed. The explicit revolution stop fixes it.
An additional red boundary check showed that recomputing a tooth index from
the clipped angle could forget a tooth through floating-point rounding:
33.853448275862064 / (357 / 116) is just below 11. Selecting from the actual
representable tooth-stop angles fixes that without an angle epsilon. A
retained per-tooth-event prototype also fixed it, but cost about 0.52 seconds
per native stroke and 88 ms per browser stroke; the own-read bound avoids
those extra events. The regression exercises all nine
rounding-sensitive tooth indices and the end of the sector over two turns.
A mutation replacing digit extraction with extraction from `value + 1`
fails the independent operation/partial-pose contract; the mutation is scoped
and automatically restored by the test.

The finite build publishes `_build/clocked_curta/viewer.json`: document
version 8, 23 drivers and 18 states, with the native clocked payload and no
running program. Every rigid asset reference resolves. Both earlier siblings
and this model have 390 rigid occurrences, 38 flexible leaves, 28 surface
markings and 148 distinct rigid pieces. The ignored snapshots
`snapshot-clocked-iso.png` and `snapshot-clocked-axis.png` were rendered with
OpenSCAD and visually inspected. They establish assembly appearance, not
accumulated operation or tooth contact.

The complete geometry regression runs all 40 companion test modules
sequentially, first faceted and then exact, with an 8 GiB virtual-memory cap.
Per-module logs are retained locally in ignored `_build_clocked_checks/`.
After the ratchet-bound correction, the operation suite, clocked root on
both kernels, finite build and browser probe were rerun; the other 39
geometry modules and their tested source were unchanged.

| Kernel | Modules | Passed | Failed | Total |
| --- | ---: | ---: | ---: | ---: |
| Faceted | 40 | 148 | 6 | 154 |
| Exact | 40 | 151 | 3 | 154 |

The exact failures are the cover overlap in both whole-machine roots and the
existing counter-reversal engagement diagnostic (no expected contact at 12°).
The faceted-only failures are the bearing overlap of 0.00000324021 mm³,
the marker overlap of 0.023397085 mm³, and the STL connectivity reading below.
These are not new unexplained regressions: the earlier
[resumption record](resumption-validation-2026-09-11.md) records the cover
and bearing findings, and the [marker record](direct-operation-markers-2026-09-16.md)
records the marker discrepancy and open counter-reversal diagnostic.

The clocked root's exact checks are **2/3**: material connectivity and the
independent crank-mesh rotation pass. Whole-machine interference reports the
same `digits_cover` / `upper_housing` overlap as the fast sibling:
224.32750533797636 mm³. The faceted root additionally treats the enclosed STL
shells of `p_10219_410002_1` as three bodies; the native connectivity check
clears that report. Neither issue was hidden with an intersection epsilon.

Coverage limits: the running-oracle comparison checks the recorded operation
corpus, not arbitrary manipulations; static geometry tests cannot establish
state retention or event atomicity. Request tests cover those separately.
Neither the snapshots nor the clocked arithmetic prove physical force,
elastic dynamics, or the intentionally unimplemented interlocks above.
