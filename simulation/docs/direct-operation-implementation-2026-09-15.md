# Direct-operation implementation checkpoint

The Python prerequisites are available at framework `0b0f02a` (ADR-121 and
ADR-122). The live shifted-carry fixture now constructs, matches its fixed
twins at 1, 12 and 240 ticks, and retains/replays its coordinates across shifts.
The new live-association regression fails on the preceding retained-angle
framework worktree, so this is evidence for the merged change, not just a
construction smoke test. Framework and viewer sources were not changed here.

Implementation is in `simulation/running.py:OperatingCurta`. This is a
development root, **not yet the manifest's replacement**. The existing pose
model and accepted markings remain in place. OpenSpec tasks 6.1–6.6 remain open.

## State and ownership

The development root uses `Time.running`. Its independent setting, crank,
carriage and ring inputs drive the existing source-backed parts. All seventeen
dials, seventeen transmission shafts and fifteen carry sliders keep their
history on their actual joints. The carriage's actual turn/lift select the
fixed-shaft/dial association. There are no virtual per-dial latches, accumulated
operand totals, imperative run updates or editable arithmetic registers.

`register_reading(sim, counter=False)` decodes the committed dial bank. It is
observation only, not a source of mechanical motion. A direct `.value` property
on a lazily enumerated tree is not used as a substitute for that bank.

The shared physical dial/selector banks have been separated from the older
pose calculator's grouped bindings. Named bindings permit the running carry
sliders and clearing-stop pin to be the source of their followers without
duplicating parts. The original fitted shapes and placements are unchanged.

## Contact-law migration

The pin and reset profiles remain the measured `PIN_DROP` and `RESET_LIFT`.
The run retains an over-centre latch on the real slider. A parked nine's pin
limits reset, and withdrawing the carriage releases an unlatched preload with
the existing one-millimetre-per-millimetre contact law.

Red tests caught reset pushing through a parked pin, failure to release its
preload on lifting, and a zero-target latch comparison written with unnecessary
offset cancellation. The corrected comparisons use the actual endpoint and
evaluate the moving pin stop only during the cam's resetting flank. A scalar
zero outside that flank also belongs inside the comparison: merely multiplying
its output by zero left an inactive own-coordinate surface in the walk. Inactive
levels are kept off comparison/floor boundaries; this changes no active contact
threshold and avoids needless searches of a dormant surface.

The old pawl law prescribed an instantaneous spring return. Under incremental
operation it accumulated 331.153935 degrees of false rotation in one turn.
`running_pawl.py` traverses the previously probed 0.005-degree release interval
continuously, including the shortened ratchet interval. It is prescribed
kinematics, not a spring-dynamics claim. Its return regression and all seven
exact geometry contracts pass, including samples through the new return path.

## Clearing capture band

`tools/clearing_gap.py` rotates each representative zero dial about its
validated radial axle while sweeping its actual fitted row through 0–80 degrees
at quarter-degree intervals. Both rows are clear at offsets -0.5 and +0.5
degrees. A +1-degree perturbation intersects the outer row at ring 11.75 degrees
and the inner row at 12.5 degrees. The gap is asymmetric: negative offsets
through -4 degrees remained clear in this faceted probe, whereas -8 did not.

`clearing_gap.py:ClearingGapBench` independently confirms the bilateral
half-degree band with the native kernel over the same sweep. The running law
uses that conservative capture band around the calibrated zero. It is not the
entire missing-tooth clearance or a force simulation of the spider's final
settling. It must not be justified merely by the framework example's coincident
half-degree number.

The nine-tooth rack law uses the source pitch, fitted first-contact datums and
each dial's station. Its isolated production-law tests pass every digit at all
seventeen stations in both directions, repeated sweeps and snapshot replay.
Opposite half-sweeps reach different registers. Integration into the full machine
additionally passes lifting without clearing, selective half-sweeps, completion,
reverse sweeping over cleared wheels and snapshot replay. This is not interlock
acceptance.

## Validation and remaining work

Verified so far:

- 34 existing standalone unit/prerequisite tests pass.
- Four running contact-law tests pass (pin latch/reset, parked-pin stop,
  carriage withdrawal and pawl return).
- Three rack-law tests pass, including 340 digit/station/direction cases.
- Three full-machine tests pass: independent inputs and successive additions
  followed by selective/repeated clearing; page-53 calibration through 100;
  partial crank release, resume and exact snapshot replay. Together with the
  seven contact/rack tests above, the final run passed 10/10 in 528.874 seconds.
- Two additional full-machine tests pass (279.078 seconds): subtract one
  from zero through both complete register banks, then add one back to zero;
  and retain 9/1 while lifting and shifting two places, then add 3 to obtain
  309/101. These used the pre-stroke-bound running root. The subsequent
  crank-only bound change separately passes the reduced overtravel tests.
- The existing standalone/prerequisite tests plus the two new stroke-limit
  tests pass together: 36/36 in 6.279 seconds.
- Exact original dial regressions: 3/3; exact selector regression: 1/1.
- Exact finite pawl-return contracts: 7/7; exact clearing-gap contract: 1/1.
- The development root's rest snapshot builds and has been visually inspected
  at `_build_running/direct-operation-rest.png`. This is static rest evidence,
  not a run replay or browser-control acceptance.

The checked full-machine calibration and full-bank borrow/overflow cases are
not the complete shifted mode matrix. The development root must not be promoted on that
basis alone. Python crossing searches are expensive: an early
20-tick revolution took about 42 seconds after construction, and the moving
pin-stop laws cost more. The latest quiet-tick probe measured 3.38, 2.93 and
3.39 seconds per 0.1-second tick. Expanding measured polylines into explicit
comparison pieces was slower and was reverted. Performance is not yet
interactive. `python -m simulation.tools.running_probe --ticks 3` reproduces
the timing probe; omit `--ticks` for full calibration with progress output.

The pilot requested a wart, not a Python handoff, and directed continued
Python implementation. The finding is committed as `f21c46e` in framework
worktree `solid-node/WTs/curta-running-performance-wart`, in
`workflow/warts.md` under the originating Curta follow-up. It is a local,
unratified finding, not an external issue or a framework optimization cycle;
it has not been integrated into framework main.

The running crank now enforces its measured 0–9 mm lift on the actual joint.
Two reduced running tests first admitted requests to 12 and -3 mm (red),
then stopped at 9 and 0 mm respectively after the joint bounds were added.
The upper-stop test also verifies lowering back to zero and that the drum
follows the admitted crank, not the requested overtravel. This is stroke
validation only, not proof of the mid-cycle crank-lift lock.
An integrated `OperatingCurta` request to 12 mm also stops both crank and
drum at 9 mm while both retained registers remain zero.

Run the new state tests with:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD" \
  ../../../.venv/bin/python -m unittest -v simulation.test_running \
  simulation.test_running_laws simulation.test_running_clearing
```

The tests use the public `Sim` API. An ordinary independent request is
`sim.move('digit_1', to=3)`, followed by `sim.trigger('Turn crank')` and
`sim.run(2)`. Read `register_reading(sim)` and `register_reading(sim, True)`;
do not replace a run with a pose at a new total crank angle.

The remaining scope includes full-bank carry/borrow and shifted-mode matrices,
crank/selector/carriage/ring interlocks with measured backlash, independent
counter reversal, clearing-loop deployment and all ten movable decimal markers.
The current mid-stroke drive-selection gates are development assumptions, not
verified engagement limits. Do not use them as evidence for permitted
intermediate operation. Existing whole-machine thread/contact findings remain
open and independent of this migration.

No viewer implementation was attempted. A matching runtime for document version
7, pointer validation and Python/browser replay remain separate acceptance
work. The pilot deferred that work; these Python checks do not waive it.

## Open reversing-lever investigation

`simulation.tools.reverser_measurements` reports source shaft detent centers
about 12 mm apart, a 1.685 mm fork slot and a 1.5 mm pinion, leaving 0.185 mm
axial clearance. The exported shaft STL independently has the same 12 mm
detent spacing. The already documented normal-counter pose lifts its input
groups 4.5 mm relative to the source pose. Combining that pose with a 12 mm
reverser throw has not established complementary tooth engagement.

`counter_reversal.py` isolates the higher-counter pinion against the complete
upper drum; `test_counter_reversal.py` asks for free nominal passage and
engagement under a 12-degree pinion perturbation at three tooth stations.
This is an **unresolved red diagnostic**, not an accepted mechanism or a
proposed fit. A 9 mm candidate also fails the engagement assertion. Independent
world-axis overlap sampling (`simulation.tools.reverser_engagement`) helps
distinguish contact, phase and fixture errors; it does not certify a new throw.
Neither the printed shaft nor the running counter law has been changed to
adopt that candidate. Do not infer a proven source-design flaw or a 9 mm fix
from this incomplete investigation.
