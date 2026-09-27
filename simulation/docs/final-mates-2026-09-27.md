# Final operating-attachment adoption

This completes the operating-attachment refactor after detent commit `cdac345`.
Production commit `4d4456230a6fc854493eac8bbeb2b459a9a83721` records the final
source. All final validation gates pass and the result is integrated locally.
No further framework change or operator-interface change is introduced.

## Scope

The final operating tree has 185 frame mates (33 rigid). Every joint-bearing
mechanical child is attached by a mate. The only deliberately unmated joint
children are nineteen material patches: seventeen spider fingertips and two
retaining-spring hooks. Those joints describe deformation within one physical
part, not how separate parts mount. A root-level coverage test pins this exact
exception set, so a later assembly specialization cannot silently bypass
adoption. Unchanged fixed source hardware may still use its original placement
operations; the generated source scaffold is not rewritten.

New adapters cover the anti-reversal pawl and its whole return spring; the
reverser ball, knob and spring; the carriage positioning ring, spring and radial
ball; the clearing pin and spring; the loop's intrinsic swivel; and the complete
tens-bell retaining spring. Existing joint declarations, ranges, independent
freedoms, retained laws, deformation coordinates, seats and fitted shapes stay.
Original unmated classes remain available as independent witnesses.

For example, `FramedCarriagePositioning.ring_seat` states the installed thrust
ring's rest frame. `thrust_ring.datum.on(ring_seat, thrust_ring.slide)` attaches
that ring through its existing slide coordinate. The explicit frame says where
the ring sits; the original joint still says how it moves. No string names a
joint or substitutes for a declaration reference.

## Final-tree audit correction

The earlier carry increment tested `RetainedTurnsCarries`, but the operating
root selects a later `ShoulderRetainedTurnsCarries` specialization. Its five
shoulder-fitted sliders and their bearing/spring stations still used the old
placements. The new whole-root coverage test exposes this; it and the five
counter adoption subcases fail before correction, while the independent fitted
pose witness passes (three tests, 5.952 seconds, six failures).

`shoulder_carry_frames.py` now attaches those final five stations, preserving
their .35 mm shoulder relief and all original source placements. Production
selects these adapters, while the original fit-trial stations remain independent.
The carry capture bench now uses this final fitted bank. Earlier capture/pixel
evidence is evidence for its then-selected bank, not retroactively the final
shoulder bank. Two newly started long regressions were intentionally interrupted
before this correction and restarted; interrupted logs are not passing runs.

## Red-first and adversarial evidence

The drive-detail red has two structural failures (zero mates instead of two
and three), with its source pose/shape/replay witness already passing. After
implementation both tests pass in 10.827 seconds. Eighteen driven poses span
three existing shaft-seat parameter values, full knob travel and retained pawl
returns, including exact snapshot replay and bank ordering.

The remaining-attachment fixture initially omitted the two external assembly
turns carried by the actual production specializations. That fixture error was
corrected before the valid red: four structural failures, with the independent
source witness passing (two tests, 1.117 seconds). Five poses exercise ring
lift, independent radial ball movement, pin compression, loop deployment and
bell-spring spread. Every actual changed body is asserted present, all basis
points agree to eight decimal places, shape values and retained banks agree,
and snapshot replay is exact. The existing crank witness retains its stricter
nine-decimal comparison and the historical 216-coordinate hash.

All 36 focused adoption/coverage/running-marker tests pass in 46.786 seconds.
They pass again on the committed source in 43.268 seconds. The only intervening
source edits remove two trailing blank lines; no executable statement changes.
After unmodified witnesses pass, twelve independent +.2 mm frame perturbations
each fail the corresponding witness: pawl, pawl spring, reverser ball/spring/
knob, positioning ring/spring/ball, clearing pin/spring, loop, and bell spring.
Each actual leaf moves .2 mm within floating-point representation, and complete
selected bases restore exactly. An initial mutation harness without `dt` was
refused before any mutation and corrected; it is not counted as evidence.
Three further mutations of final shoulder station one's slider, station three's
bearing and station five's wire also fail, with movements
.1999999999999993, .1999999999999993 and .20000000000000284 mm; restoration is exact.

## Geometry and export

The unchanged pawl contact and six installed reverser assertions pass on the
new production adapters: seven faceted tests in 31.27 seconds (volume epsilon
zero) and seven exact tests in 62.29 seconds. An earlier exact invocation
printed seven passes in 63.38 seconds but terminated with exit 143; the complete
retry above exits zero. No weakened assertion is used.

The final shoulder-bank capture suite passes three faceted tests in 20.05
seconds (volume epsilon zero), and three exact tests in 175.19 seconds.
These assert fixed closed spring folds, .01 mm free/.2 mm blocked hook play,
and clearance from the guide seats, across all fifteen carry stations.
The actual-root installed-motion suite passes seven faceted tests in 144.66
seconds and seven exact tests in 101.28 seconds, both exiting zero.

The installed loop diagnostic passes all seven deployment samples (0, 30, 60,
90, 90.4, -.4, 0 degrees) against all 389 rigid occurrences. Native intersections
with the tool's declared STL fallback report no positive common, refused
intersection or negative signed sum; the moving vertices match the independently
calculated transport. This is a sampled interface check, not a continuous or
whole-machine clearance claim. Raw report: `_build/final-loop-mates-contacts.json`.

Native drive snapshots at rotation=-3.4 degrees and height=-4.9425 mm were
inspected at 1200 by 900. The first automatically framed view cropped the shaft
tip and is not relied on; the complete camera-distance-600 views
`_build/drive-mates-complete.png` and `drive-legacy-complete.png` include the
entire shaft, knob, pawl and return spring. Decoded RGB bytes match exactly.
The complete remaining-attachment view at rise=6, radial=.3, press=2,
deploy=90, subtract=1 also matches its independent legacy view exactly:
`_build/remaining-mates-set.png` and `remaining-legacy-set.png`. The bell,
carrier and deployed loop remain aligned. These independent-input poses are
visual attachment comparisons, not arbitrary-setting clearance claims.
The remaining-attachment rest view `_build/remaining-mates-rest.png` is also
inspected, showing the stowed loop on the complete upper stack. Final fitted
carry views at stroke=2.562 mm and camera distance 600 show all fifteen complete
stations: `_build/shoulder-mates-complete.png` and `shoulder-legacy-complete.png`.
Their decoded RGB bytes match exactly; the auto-framed close views are retained
but the complete framed pair is the relied-on comparison.

Fresh `machinome build operating_curta` exits zero. Compared with frozen outer
checkpoint `7ee005f`, all 417 model/marking occurrences have identical STL bytes.
The complete program is equal after exactly 29 asserted `stated_by` replacements:
seventeen detent relations and twelve relations in the renamed pawl, reverser,
loop, bell-spring, positioning and carrier adapters. No other program difference
is permitted. Graph identity, 216 coordinates, 301 sources, limits, profiles,
controls (26), instructions, drivers, bindings, animation and version 13 remain
equal. This is not a claim of byte-identical JSON: provenance and operation
spelling change. Export SHA-256 is
`36e6675972fe7c9e3f5618e4ebde9996d531dbe4543e6816186c808a1c6a0718`.
The full exported root also compares equal after excluding only placement
`operations` and `mtime`, and replacing model filenames with their SHA-256
content identities. Thus flexible-shape data, hierarchy, names and appearance
remain unchanged too; placement is checked by the independent basis witnesses.
The build rerun on committed `4d44562` exits zero with the same export hash.

The primary checkpoint's eight contact tests passed in 3878.007 seconds before
these final changes. That result remains scoped to `7ee005f`.

The fresh final full-root batch passes all **37 tests in 1992.475 seconds**,
exit zero. It includes six arithmetic cases; crank/reverser travel limits;
every ratchet tooth, repeated reverse requests, production replay and the
unrestrained negative control; all carriage/clearing interlocks; loop stop,
retry, relief and replay; all five marker checks; all four prepared crank
modes; four retained-phase/wrong-order contact tests; and reversed-counter
passage checked against both geometry representations. Command:

```sh
python -m unittest -v simulation.test_running.RunningCurtaTest \
  simulation.test_running_limits simulation.test_running_ratchet \
  simulation.test_running_interlocks simulation.test_operating_loop \
  simulation.test_running_markers simulation.test_running_reverser_wrong_order \
  simulation.test_running_reverser_contact_path
```

The raw log is `_build/final-mates-running-complete.log`. No request, timestep,
comparison tolerance or geometry assertion was weakened. The earlier interrupted
run is retained separately and is not counted as passing evidence.

## Completion boundaries

All jobs use the workspace venv with the integrated framework `fabfc3d`, one
BLAS/OMP thread, and separate build caches. CAD jobs have 4 GiB address-space
caps and the full-root operating batch an 8 GiB cap. No source CAD, printable
geometry, physical clearance, tolerance, viewer schema or control was changed.
This refactor does not close whole-machine geometry acceptance: the existing
`simulate-the-curta` umbrella remains 17/23 and is not archived.
`openspec validate simulate-the-curta --strict` passes. Its planning artifacts
are complete, but the six unchecked whole-machine tasks remain unchecked.

## Integration and retained evidence

Production `4d44562` and validation record `59a2697` were fast-forwarded into
the project's recorded `main`. The main checkout then passed all five
coverage/crank/retained-bank smoke tests in 11.431 seconds and a fresh
`machinome build operating_curta`, both with exit zero and no framework override.
The complete main/worktree exports compare equal after removing only `mtime`;
all 417 model/marking occurrences have identical asset bytes. The main export's
SHA-256 is `05eb138e2f4b64f029571438005f93c2a43a9a7ca0f791e3b8f3957108c77474`.

The isolated project worktree was removed cleanly after integration, without
force. All 8,203 evidence/cache/source files were copied and byte-verified in
the primary project's ignored `_build_mates_final_20260927/` directory. Paths
above beginning `_build/` now live inside that retained directory; the original
red records are retained there too. The source and record commits and their
branch remain recoverable. The main build/smoke logs are `main-build.log` and
`main-smoke.log` at that directory's top level. Existing untracked user files
and unrelated worktrees remain untouched. Nothing was pushed or published.

Framework main remains `fabfc3da547f133caf4d991f94582eebcd90f37d` and Studio
main `655a3ccc6f9a88a0dda8f579fa0180f77eb826e5`, both clean. The ratified
framework cycles retain their separately proposed/applied, adversarially
reviewed, synced and archived records. No additional framework cycle was
needed for these final project attachments.
