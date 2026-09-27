# Zero mechanism frame adoption

The cam, drive pin and follower now attach through three mates referencing
their existing joints. This increment follows selector commit `a465d13`.
The pilot explicitly ratified the precision-contract change on 27 September
2026. The standalone framework cycle `explicit-frame-direction-precision`
was based on `82a9774` and is integrated locally as `fabfc3d`.

`test_zero_mates.py` freezes the original cam, pin and follower joints and
parent placements, independently of attachment frames. Before any adoption,
the pose/state/replay comparison passes and the structural test fails with
zero mates instead of three (2 tests, 0.675 seconds). The candidate preserves
all original joints, laws, ranges and source geometry and replaces only the
cam/pin parent placements with full source-derived frame triads. The follower
uses matching native pivot frames. It is saved at the ignored
`_build/zero-mates-candidate.patch`; production `zero.py` was restored exactly
to its committed version pending the decision, then reapplied after ratification
for red/green caller validation.

## What failed

The candidate's structural test passes, but its unchanged physical-basis
comparison fails during motion at `.mechanism.zero_positioning_disc_pin`:
`-14.56100394597477` versus `-14.561003960427621`, a difference of
`1.4452851360147179e-8` mm. The other eight selector/dial/crank tests pass
(10 tests total, one failure, 8.844 seconds). This is numerical preservation
evidence, not an observed mechanical fit failure. The existing six geometric
zero-cam tests all pass on the faceted kernel at volume epsilon zero in
20.62 seconds, including full cam clearance, pin slots and spring endpoints.

The original pin rotation is -179.92640235 degrees around the normalized
source axis `(.707106635, .000642261, .707106635)`. Its transformed local X
is `(-3.2740476996195866e-13, 3.6046641539722035e-10, 1)` and local Z is
`(.9999983500045653, .0018165869499783267, -3.2740476996195866e-13)`.
Frame resolution deliberately erases the small components. Unlike the prior
axis-recovery bug, this follows the current mates specification's requirement
"A realized node reads its resolved frames": direction components within
`1e-9` of zero or +/-1 must read as those integers, and mates must use those
same resolved vectors.

A read-only/in-memory diagnostic patched only `node.frames._snapped` to return
its input during fresh construction. The identical pose/state/replay test
then passed in 0.696 seconds. No framework source was modified, no test
tolerance was loosened, and the diagnostic is not a production solution.

## Ratified choice

The pilot authorized empirical ratification for fixes with no interface
change. Changing this documented resolved-frame rounding behavior is instead
a public numerical-contract change, even if `Frame(...)` keeps the same
arguments. The pilot ratified the choice before OpenSpec: retain full normalized
directions when an author explicitly supplies the complete frame triad,
rather than rounding their components before mate composition; preserve the
existing final rotation-axis/angle snap and principal-axis default behavior.
No precision flag, magic name string, caller workaround or changed fit is
proposed. The confirmed diagnostic establishes causality, not a settled
implementation design. Separate Sol agents proposed and applied the change;
root adversarial review preceded synchronization and archival. No tolerance
was relaxed.

## Verification against the framework worktree

The ratified cycle's planning commit is
`2be1be7a48958327528643af824a42f3160ea163`, based on
`82a9774dfeaaf60b04f1e46b452198bab8611c4f`. Its runtime source blob is
`b8df16f0d2d84d2df3ea1a8ad1406da3bfdb2938` for `node/frames.py`.
These checks used the cycle through `PYTHONPATH`, the workspace environment,
an 8 GiB address-space cap and one BLAS/OMP thread.

- Fresh unchanged-main red: zero's two tests in 0.730 seconds, structural
  adoption passes and the same strict moving pin comparison fails.
- Corrected framework: all ten zero/selector/register/crank adoption tests
  pass in 9.448 seconds, including the historical 216-coordinate bank hash.
- A deliberate in-memory +0.2 mm pin-seat shift fails the independent pose
  witness at the actual pin by 0.1999999999999993 mm (0.606 seconds).
  The context manager restores it; no source mutation is retained.
- All eleven clocked-operation tests pass in 34.527 seconds, including
  carry, clearing, retained state and replay. These are not a new full
  running-arithmetic batch.
- The six existing geometric zero-cam contracts pass on the corrected
  framework: faceted 3.59 seconds with volume epsilon zero, exact 48.35
  seconds. On unchanged main, the candidate also passed exact in 49.91
  seconds; the defect was strict pose preservation, not a detected fit loss.
- Native underside views at rest and half-turn/subtraction were inspected:
  `_build/zero-mates-rest-underside.png` and
  `_build/zero-mates-subtract-underside.png`. The cam, sliding pin and
  follower remain attached; the roller follows the cam. Initial top-side
  views were occluded by the bearing plate and are not acceptance evidence.

The cam and pin mates replace only their parent rotation/translation;
the follower's matching native pivot frames preserve its internal source
placements. Original `turn` joints, independent pin `lift`, ports, laws,
source geometry, fitted clearances and public controls remain unchanged.

## Completed framework cycle

Framework planning `2be1be7a48958327528643af824a42f3160ea163` and implementation
`fabfc3da547f133caf4d991f94582eebcd90f37d` are integrated into framework main.
The mates and user-documentation baselines are synchronized and the change
is archived at
`openspec/changes/archive/2026-09-27-explicit-frame-direction-precision`.
The separate Studio contract companion
`655a3ccc6f9a88a0dda8f579fa0180f77eb826e5` is integrated into Studio main.
No new arguments, naming strings, viewer fields or document versions were
introduced. Only explicitly supplying both x and z opts into unsnapped
normalized frame directions; omitted directions and final mate/joint snap
retain their previous rules. This is a ratified public numerical change,
not a claim of no interface change.

The final framework selection passed 505 tests and 1017 subtests; its
tutorial passed three tests, and all 37 baseline specs passed strict
validation. Studio passed 36 tests. Ordinary warnings-as-errors HTML builds
passed; nitpicky builds reproduced exactly the same five unresolved-reference
warnings on unchanged main and the worktree. The architecture synthesis was
updated; no architectural ADR was warranted and historical ADR-147 remains
unchanged. No push or publication was performed.

After fast-forward integration, the same ten caller tests passed again in
8.939 seconds with no `PYTHONPATH` override. `machinome build operating_curta`
also passed on integrated main. Its document keeps version 13, the exact
same 216 coordinate IDs, 26 control names and 301 program sources as the
pre-selector export. All 417 model references point to existing files.
The completed framework and Studio worktrees were removed cleanly; their
branches and commits remain. This closes the zero increment, not the
remaining frame/mate adoption or whole-machine geometry acceptance.
