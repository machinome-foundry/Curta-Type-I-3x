# Curta selector mates

The eight selectors retain their existing two `turn` joints and one knob
`travel` joint each. Source-backed frame adapters leave top-shaft/number-roll
and knob internal placements untouched; matching native connector frames
place those assemblies. The lower shaft's mate instead replaces the original
parent's rotation and translation, including its source clocking. No driver,
control, ratio, range, shape or retained coordinate changes.

The independent declarations in `test_selector_mates.py` copy the old joints
and inherit only the original source placement classes. Before adoption,
their state/leaf-pose/replay comparison passed; all eight structural cases
failed (zero mates instead of three). After the first adoption patch, all
structural cases pass, as do the six dial/crank preservation tests, but the
selector pose comparison fails: selector six's lower shaft gains a tiny tilt.
The measured discrepancy is 1.0524132676437148e-8 mm on a one-mm basis point.
The historical 216-coordinate bank hash still passes. No tolerance has been
relaxed; that first candidate was not accepted or committed.

A read-only reproduction on unchanged framework main shows its mate rotation
conversion maps a pure -95.6-degree Z rotation to axis
`(-5.028708403180495e-9, -5.028708403180495e-9, -1)` instead of `(0, 0, -1)`.
The diagonal square-root extraction beyond 90 degrees amplifies roundoff in
zero components. This is numerical preservation evidence, not an observed
mechanical fit failure. Root proposed a narrow stable internal conversion to
the pilot, preserving genuinely small components and half-turn behavior,
without an API change or loosened checks. The pilot ratified that fix on
27 September and additionally authorized empirical evidence to ratify future
fixes that make no interface change. Interface changes still go to the pilot
first. The separate `stable-mate-rotation-conversion` framework cycle now
branches from clean main `6ca6061`, with one Sol proposing, another applying,
and root adversarial review before synchronization and archival.

The full running root's selector-independence test passes in 14.560 seconds:
each of the eight selectors moves only its own shaft and neither register is
driven by that operation. This state check does not resolve the pose failure.

While ratification was pending, `selectors.py` was restored to its unchanged
committed version so final dial-only acceptance used no unaccepted selector
implementation. After ratification the candidate was restored, and the two
selector tests on unchanged framework main `6ca6061` reproduced the same
failure (1.033 seconds, structural test passed). The patch is also preserved at
the ignored
`_build/selector-mates-candidate.patch`; its new `selector_frames.py` and
independent `test_selector_mates.py` remained uncommitted pending acceptance.
The temporary rollback removed only root's selector edit, not user changes.

## Reviewed numerical fix and acceptance

The framework cycle's planning commit is `42b42eacb2a6d4e05deacbd6a5d60a0179b41290`
and implementation commit is `82a9774dfeaaf60b04f1e46b452198bab8611c4f`.
Root reviewed the implementation before the mates baseline was synchronized
and the change archived at
`openspec/changes/archive/2026-09-27-stable-mate-rotation-conversion`.
It is integrated locally on framework main and the clean cycle worktree has
been removed. This is an internal numerical correction, with no API, Studio,
viewer, schema or snap-policy change, and no new architectural decision/ADR.
The final framework selection passed 424 tests and 880 subtests; all 37
baseline specs passed strict validation. Nothing was pushed or published.

The unchanged selector, dial and crank witnesses passed all eight tests in
8.980 seconds against the framework worktree, then 8.855 seconds after main
integration without a `PYTHONPATH` override. The selector comparison covers
all 56 physical leaves over all-zero, distinct digits, all-nine, fractional
and returned-to-zero settings, with retained state and snapshot replay.
A deliberate in-memory +0.2 mm mutation of selector one's lower seat made the
same test fail by 0.2 mm at the actual lower shaft; the declaration was restored
on leaving the mutation check and no source mutation was persisted.

The existing selector-bank geometric travel test passed on both kernels:
faceted 18.34 seconds and exact 0.43 seconds, before the rotation correction.
After integration, both were repeated without an override and passed in
0.46 seconds (faceted, volume epsilon zero) and 0.44 seconds (exact).
Native snapshots against the corrected framework were inspected at
`_build/selector-mates-rest.png` and `_build/selector-mates-set.png` (input
12345678). All eight shafts remain aligned, the knob sliders show their
expected staggered heights, and no detached subassembly is visible. This
renderer omits digit markings; these images do not prove label rendering or
whole-machine interference clearance.

The full `machinome build operating_curta` completed on integrated framework
main without an override. Its export retains document version 13, the exact
same 216 coordinate IDs and 26 control names, and 301 program sources. All
417 file references exist (389 solid mesh occurrences plus 28 markings).
The historical retained-bank hash also passes unchanged. This is not a claim
of byte-identical export JSON or whole-machine geometry acceptance.

The separately started operating regression finished successfully: 26 tests
in 1326.451 seconds across `RunningCurtaTest`, running limits, ratchet,
carriage/clearing interlocks and the operating-loop module. It imported
framework `6ca6061` before the rotation fix was integrated and before any
zero-mechanism edits. It therefore proves operating-state preservation for
the selector adoption, not final numerical acceptance on `82a9774` or
acceptance of the later zero-mechanism increment. The eight-test fresh pose
run and final full build above provide the post-integration evidence.
