# Curta frames and mates migration

This records incremental adoption, not a claim that every Curta joint or source
placement has been converted. The generated source tree, printable geometry,
fitted clearances and arithmetic laws are unchanged. Whole-machine geometry
acceptance remains open under the existing project record.

The [central-assembly increment](core-mates-2026-09-27.md) attaches the
stepped drum, tens bell, operating carriage and complete clearing-ring
assembly through their existing joints. Their native central-shaft frames
preserve rest placements, independent lifts and all existing laws. This uses
the existing API without another framework change; independent pose/replay
witnesses, installed motion on both kernels and the full-root export pass.

The [zero-mechanism increment](zero-mates-2026-09-27.md) attaches its cam,
drive pin and follower through their existing joints. It required the
pilot-ratified explicit-direction precision rule, integrated as framework
`fabfc3d` with Studio companion `655a3cc`. Strict independent pose/state/replay
checks and six geometric contracts on both kernels pass without changing
any tolerance, shape, control or coordinate path.

The [eight-selector increment](selector-mates-2026-09-27.md) additionally
attaches both shafts and the sliding knob of every input channel through their
original joints. It exposed and verified the internal mate rotation correction
integrated as framework `82a9774`; no new interface or caller tolerance was
needed. Its 56-leaf independent pose/replay witness, scoped geometric checks,
native views and full-root build preserve the existing operator surface.

## Attachment and contracts

`AttachedCrank.spindle` and `RunningMainDrive.crank_seat` name the existing
central Z motion datum. `RunningMainDrive.turn` now mates those frames with a
revolute freedom. The crank's independent 0..9 mm lift remains a child joint;
the two coaxial freedoms commute. The mate generates the same physical
`main_drive.crank.turn` coordinate that the old site declaration generated.
It replaces the former plain `turn` port and explicit port-to-crank relation.

The pawl-dependent `Bound` lives on the mate's freedom and reads the
anti-reversal pawl in the declaring drive assembly. The five ancestor crank
constraints, the crank's Turn/Button coordinate selections, arithmetic source
relations and the reversing-lever Bound now name `main_drive.turn`. They do
not create another retained coordinate, change input units or change the
operator's controls. The negative ratchet fixture independently restates the
same mated drive without its pawl bound; it does not bypass mate inheritance
checks by replacing an inherited moving child.

## Framework requirement and ownership

On framework `49a8fc5`, a moving mate rejected Bound reads in its freedom,
could not be constrained through its own coordinate, and could not be selected
explicitly by a control. The pilot ratified the additive extension before
OpenSpec proposal. The separately owned `mates-in-mechanical-contracts` cycle
uses one Sol proposer, another Sol implementer, and root adversarial review
before spec sync/archive. No compound freedom or viewer schema is introduced.

The framework cycle has planning commit `956d063` and implementation commit
`163afcc868155eba94dac16ab10345662d3ce5bc`, integrated locally into framework
main after root review. Its three specs are synced and the record is archived
at `openspec/changes/archive/2026-09-27-mates-in-mechanical-contracts` in that
repository. ADR-153 records the decision. The separately owned Studio API
companion `c0f2bfd6dacc9008e7766ecbac24d148294b82aa` is integrated into Studio
main. Both completed worktrees were removed cleanly; commits and branches
remain. Nothing was pushed or published. The workspace environment now uses
the integrated framework without a worktree override.

## Evidence

Starting project: `fb5505d`. Starting framework: `49a8fc5`.

- Original `simulation.test_running.RunningCurtaTest`: 6 passed in
  1009.671 seconds, before migration.
- New adoption tests first failed because `RunningMainDrive` had no mate and
  the crank controls selected `main_drive.crank.turn` instead of the mate.
- The independent joint-declared witness passed before implementation. It
  compares the complete drive subtree's transformed basis points, every bank
  entry, pawl stops, repeated requests and snapshot replay in both lift modes.
- Initial migrated focused run: 6 tests passed (adoption/twin and stroke
  limits). Full-root retained-bank and positive/negative pawl checks: 3 passed.
  The 216-coordinate bank retains the previously pinned historical hash;
  it was not regenerated to accommodate the refactor.
- Framework review reproduced and corrected foreign same-name read acceptance
  and inferred-node aliases evading self/duplicate read checks. A separate
  control-declaration cache mutation was also corrected before completion.

- Fresh `machinome build operating_curta` passes. Its document retains version
  13, all 216 coordinate ids, all 26 control names and 301 program sources.
  All 389 mesh occurrences resolve to existing assets. The graph identity
  changes with the new declarations; this is not a byte-identical export claim.
  Crank lift/turn operation order changes, but their coaxial transforms agree
  in the independent subtree witness in both modes.
- `machinome test simulation/crank_coupling_seat.py --faceted`: seven passed
  in 114.87 seconds, with volume epsilon zero. The default exact runner:
  seven passed in 97.42 seconds. These cover the actual crank/drum/pin
  interface, coaxial bore datum, unchanged bounded relief, capture, retained
  bank and actual turn/lift geometry. They are not whole-machine acceptance.
- Isometric and axial native snapshots were inspected at
  `_build/operating_curta/mates-iso.png` and `mates-axial.png`; no detached or
  displaced crank assembly is visible.
- The hosted browser probe passes on the fresh export with no page errors:
  a pointer lift reaches 1 mm without turning the crank, and dragging the
  first selector moves only that selector and its shaft. The screenshot is
  `_build/operating_curta/mates-browser.png`. This is a scoped pointer check,
  not a repetition of the earlier all-26-control acceptance campaign.
- A deliberate 0.2 mm spindle-frame mutation exposed that the initial pose
  helper walked empty `children` lists in a non-meshed Sim. It now walks
  public child declarations too, asserts the real crank leaf is present,
  and fails on that mutation with a measured 0.2 mm crank displacement.
  The deliberate source mutation was restored; the corrected four-test
  adoption suite passes in 6.824 seconds.
- After framework integration, the same four tests passed in 6.937 seconds
  with no `PYTHONPATH` override.

The migrated batch passed all 30 tests in 1347.230 seconds:

```sh
python -m unittest -v simulation.test_running.RunningCurtaTest \
  simulation.test_mate_refactor simulation.test_running_limits \
  simulation.test_running_ratchet simulation.test_running_interlocks \
  simulation.test_operating_loop
```

This includes all six existing arithmetic cases, actual production ratchet
and negative-control behavior, carriage/clearing interlocks and loop replay.
Tests used the workspace venv, the framework cycle through `PYTHONPATH`,
an 8 GiB address-space cap and one BLAS/OMP thread. The corrected four-test
pose suite was rerun separately after the batch had imported its earlier
test definition. Framework final validation passed 933 tests and 954 subtests;
all 37 baseline specs passed strict validation. The strict manual build has
the same five unresolved-reference warnings as the unchanged framework base,
recorded in the archived evidence rather than waived as a successful build.

## Next finding: repeated dial coordinate names

`ResultDials` has eleven sibling dials and `TurnsDials` six, each with a local
`turn` joint. `register_reading` consumes those seventeen retained paths,
as do the existing arithmetic laws and replay witnesses. A separate two-dial
authoring probe confirms that uniquely named `ones_turn` and `tens_turn`
mates currently generate `ones.ones_turn` and `tens.tens_turn`, not
`ones.turn` and `tens.turn`: the assembly's mate name also names its child's
generated joint.

The choice was presented to the pilot before another OpenSpec change:
optionally let `.on(..., joint_name="turn")` preserve a local physical name
while the assembly mate has a distinct name, retaining today's default;
or keep separate dial joints and use rigid mates only for frame placement,
with no new API. The pilot rejected the naming-string approach. On
27 September the pilot ratified the declaration-reference alternative:
`ones_mount = ones.axle.on(ones_seat, ones.turn)`, with both frames defined
and the dial's `turn` an existing declared joint. That next framework cycle
is separate from the completed crank adoption.

## Dial adoption: all seventeen register dials

The `mate-existing-child-joint` framework cycle branched from `163afcc`.
Its reviewed planning commit is `d79c3bf`; implementation commit
`928ac64c0968838ccedd84dc86336fac125c691b` is integrated into framework main
after root adversarial review, five-spec synchronization and archival at
`openspec/changes/archive/2026-09-27-mate-existing-child-joint`. ADR-154
records the reference-mode decision. Studio contract companion
`a42d45c4b4cee3aa9f8ee2a490c56007af973dec` is integrated into Studio main.
Both cycle worktrees were removed cleanly; commits and branches remain.
Nothing was pushed or published.

`simulation/dial_frames.py` adds attachment datums to the fitted dial types.
All seventeen original site `turn` declarations remain unchanged in
`registers.py`; distinct mount handles reference those declarations. Fifteen
pin-and-dial groups keep their native source coordinates inside their children,
so their matching parent and child connector frames yield identity rest
placement. The two bare type-2 dials instead take the full source rotation and
translation from their seats, replacing the corresponding parent `render()`
placements. Their seat triads were computed from the original normalized
axis-angle rotations, including roll. The register's centering and clocking,
fitted geometry, initial values and arithmetic/readout laws are unchanged.

The independent witnesses in `test_register_mates.py` restate the old site
joints and source placements using the original fitted types. Before adoption,
their numerical/pose comparison passed and structural adoption failed for
both banks (zero mates instead of eleven and six). After adoption, the
then-current framework main (`163afcc`) rejected the first
`.on(seat, child.turn)` at class creation.
Against the framework worktree, all six dial/crank adoption tests passed in
7.118 seconds, including original coordinate ordering, all seventeen actual
dial leaf poses at five requested angles, replay and the historical
216-coordinate bank hash. A deliberate 0.2 mm first-seat shift failed the pose
witness with a 0.199990788 mm X-component discrepancy after register clocking;
the mutation was restored and the two dial tests passed again at the start of
the operating batch.

Root framework review found an ordinary-expression performance regression
(300 terms: 0.015848 seconds on main, 4.983257 seconds in the first patch) and
foreign mate handles being silently resolved against same-named local children
inside derived formulas. The apply agent corrected both and added regression
tests; root adversarial review is clear. The final selected framework
motion/document suite passed 959 tests and 986 subtests. The full test-directory
run was not green: 4045 passed, 4 skipped and 11 failed. All eleven failures
reproduced on unchanged main and concern missing vet fixtures, outside this
cycle.

`simulation.test_clocked.ClockedOperationsTest` passes all eleven tests in
35.475 seconds against the same framework worktree, covering carry, separate
clearing, partial poses and replay. An initial whole-module unittest invocation
also selected three geometry-harness tests without providing a meshed node;
two correctly errored on receiving a class instead of an instance. The corrected
operation-only invocation above is the evidence, not a geometry acceptance.

The expanded running batch passed all 32 tests in 1349.559 seconds:

```sh
python -m unittest -v simulation.test_register_mates \
  simulation.test_running.RunningCurtaTest simulation.test_mate_refactor \
  simulation.test_running_limits simulation.test_running_ratchet \
  simulation.test_running_interlocks simulation.test_operating_loop
```

This includes all six arithmetic cases, the independent dial and crank
witnesses, ratchet behavior, carriage/clearing interlocks and loop replay.
It used the framework worktree, an 8 GiB address-space cap and one BLAS/OMP
thread. It imported the framework before the performance/foreign-formula
corrections. A fresh six-test dial/crank preservation run after those
corrections passed in 7.372 seconds; the eleven clocked-operation tests above
also ran after the corrections. The tested project source blobs are:

- `simulation/registers.py`: `1d4d1d4a0ad659dddf0ac6804597dcb36d30e1c4`
- `simulation/dial_frames.py`: `b97ebe7dc290d9fef636d074582ba1a5a3de68b9`
- `simulation/test_register_mates.py`: `f4be8c08af9b4779c8bfe466cc4820a71b490f50`

After framework integration, the six dial/crank adoption tests passed again
in 6.915 seconds without a `PYTHONPATH` override. Framework post-archive
regression passed 959 tests and 986 subtests in 34.97 seconds; all 37 baseline
specs passed strict validation. Those selected checks do not erase the
separately recorded full-suite and manual baseline limitations.

### Separate build-identity correction ratified

The first faceted register geometry command was interrupted because it kept
regenerating the same type-2 dial STL, not because a geometry assertion failed.
The existing `dial_fits.FittedDialType2` leaves and new
`dial_frames.FittedDialType2` adapter are different Python classes with the
same qualified class name and STEP source. On unchanged framework base
`928ac64` too, both received the exact artifact path
`_build/simulation/_source/curta-FittedDialType2-1d3ddea04ccb.stl`, despite
different source timestamps (1790100303329848018 and 1790509484210848006
nanoseconds) and unequal source digests. The builder alternates those
freshness records indefinitely. Non-meshed state/pose checks do not expose it.

This is outside the completed joint-reference cycle. After an explanation
using the two same-named dial classes, the pilot ratified a separate internal
cache-identity correction: distinguish external-file wrappers by stable
project-relative defining-source identity plus qualified class name, while
preserving generated joint-specialization identity. It adds no author API or
naming string, and changes no controls or document schema. Affected cached
artifacts rebuild once. The same separate Sol propose/apply and root review
gates applied. At that point mesh validation and final dial-adoption acceptance
remained open despite the green non-meshed operating and pose checks, and the
dial migration was left uncommitted until the correction was completed.

Against the separate cache-identity worktree (planning commit `93ef041`,
reviewed uncommitted implementation), the formerly looping register command
now terminates: three faceted tests pass in 19.00 seconds and three default
exact tests pass in 0.36 seconds. A fresh-process rebuild of both type-2 dial
wrappers performs zero native exports, with their distinct STL and BREP paths
simultaneously current. Both exact solids have volume 3317.8854523044974 mm³
and BREP SHA-256
`dfbad7f74cb64aeba321bc34f88bb674235fa025589f5cd9577590c880d7279d`, matching
the pre-change cached BREP. Their new STL bytes match each other but differ
from the pre-change STL bytes; no old STL byte-identity claim is made. The
old and new STL canonical oriented-triangle contents are exactly equal,
with digest `8768562b3d85c1d2b6d25409a43bac903d33b9232adec24d1e3842a6f4fee657`.
Thus the cached mesh's piece identity is preserved too.

The cache cycle is complete: planning commit `93ef04122e0437374d2399f010620083f53c4281`
and implementation `6ca6061f576a512fb31d6412815c38bd6c1e6485`, locally integrated
into framework main after the separate Sol proposal/apply and root adversarial
review. Two baseline specs are synced; the change is archived at
`openspec/changes/archive/2026-09-27-external-wrapper-cache-identity`; ADR-155
records the internal identity decision. The clean worktree was removed,
retaining its branch and commits. Nothing was pushed or published. No Studio
API update was needed for this internal fix.

Final selected framework validation passed 591 tests and 574 subtests;
post-archive checks passed 154 tests and 88 subtests, and all 37 baseline specs
passed strict validation. The full run before test-fixture corrections had
4060 passes, four skips and fourteen failures: eleven reproduced on unchanged
base; three assumed the old cross-module artifact identity/names. Those three
were corrected without weakening solid-byte/piece equality or the exclusion of
marking geometry, and the complete marking module passes. The full suite was
not rerun after those test-only changes and is not described as fully green.

### Dial increment acceptance on integrated main

Against framework main `6ca6061`, with no `PYTHONPATH` override, a fresh
`machinome build operating_curta` succeeds. Its exported document remains
version 13 with exactly the previous 216 coordinate ids, 26 control names and
301 program sources. All 417 mesh references resolve to files: 389 solid mesh
occurrences and 28 marking occurrences. This verifies rebuilt asset references,
not another all-control browser interaction campaign.

The final independent dial/crank preservation run passes all six tests in
6.958 seconds, including every dial's pose at five angles, replay and the
historical retained-bank hash. Native snapshots were generated and inspected
for the result bank at rest and result `12345678901`, and for the counter bank
at a 36-degree request, at `_build/dial-mates-rest.png`,
`_build/dial-mates-set.png`, and `_build/counter-mates-set.png`. The radial
banks remain assembled with no detached or displaced dials. The native
renderer intentionally omits surface markings; these images are placement
evidence, not a visual test of the printed digit labels.

The seventeen-dial increment is accepted with its original joints, controls,
geometry and readouts preserved. Other assemblies have not all been migrated.
The separate selector experiment is not part of this accepted increment;
its production source was restored while a new numerical finding awaits pilot
ratification. Whole-machine geometry acceptance and the umbrella project
OpenSpec change remain open; this refactor does not close them.
