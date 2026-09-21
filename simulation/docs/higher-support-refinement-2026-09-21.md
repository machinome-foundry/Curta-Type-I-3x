# Higher-result contact-support refinement

Continuation of tasks 6.2/6.3 after the integrated engine correction. The
pilot's goal remains completion of the operating Curta, not completion of
the engine detour. This increment changes the measured trial restraint, not
upstream CAD or the production model's geometry.

## Failure pinned before changing the profile

`simulation.test_higher_support_admission` checks the complete T07 bell and
upper print in both native and published-mesh representations. At each of
the five independently measured source flats:

- Shaft `22.22 + 72*flat`, crank 146.5: both representations are clear, but
  the coarse candidate blocks.
- Shaft `49.13 + 72*flat`, crank 159.5: both representations are clear, but
  the coarse candidate blocks.
- Nearby shafts `22.27 + 72*flat` and `49.08 + 72*flat` have positive
  contact at those same crank angles and must remain blocked.

The first run gives **ten failing free-side subcases**, with all physical
clearance assertions and all ten contact-side subcases passing (two tests,
5.668 s). Log: `_build_checks/higher-t07-support-admission-red.log`.
No positive contact volume is discarded. These are false jams in the
provisional table's two-degree support brackets, not print defects.

## Measurement and acceptance sequence

1. Measure the native carry-tooth pair and complete published mesh near
   each of the ten independently bracketed support edges. Keep the separate
   boundary lists and their interval union; do not fill disconnected gaps.
2. Regenerate the diagnostic profile from those records, retaining the
   existing measured lower-lock release and explicit angular guards.
3. Pass the new free/contact regression, complete-print knot/midpoint/edge
   checks in both kernels, and ordinary source-trajectory admission.
4. Recheck retained short/long stops, replay, release, real carry, and browser
   execution before considering production adoption.

The support brackets, geometry fit and original engine acceptance are in
[the higher-result record](higher-result-lockout-2026-09-21.md) and
[the integrated software record](mixed-contact-engine-2026-09-21.md).

Measurement commands, from the project root with the workspace environment:

```sh
python -m simulation.tools.higher_support_curves \
  _build_checks/higher-t07-refined-support-brackets.log --side birth
python -m simulation.tools.higher_support_curves \
  _build_checks/higher-t07-refined-support-brackets.log --side death
python -m unittest simulation.test_higher_support_admission -v
```

The resumed birth survey completes **55 rows, eleven per source flat**.
The corrected death surveys supply another **55 rows**. Their measured
boundary lists, separate native/mesh brackets, and input-log hashes are
preserved in the [numeric evidence](evidence/higher-support-refinement-2026-09-21.json).
Source identity and disconnected contact-union checks pass **6/6 (1.120 s)**
on framework `9016f00`.
Viewer main is `a1ae12d`; neither dependency is modified by this increment.

## Refined candidate

The generated profile keeps the lower locking-disc table byte-for-value
unchanged. Its ten carry-tooth strips grow from 170 to 270 measured knots,
with the original .1-degree crank stand-off and .002-degree shaft guard.
No print geometry or collision-volume tolerance changes. Profile SHA-256:
`1cf2bed3b1be41ba66bccc2eb788fb24ddc5c21698853478e8d0f02813e10529`.

- The new free/contact regression and all **79,310** ordinary source-path
  samples pass (three tests, 141.218 s).
- Complete-print verification passes **8,063/8,063** knot, midpoint and
  support-edge samples on **each** of the faceted and native kernels.
- The expanded support suite also checks admitted near-edge poses across
  carry fractions .28/.3/.5/.51/.64/.65: **3/3 tests, 48.850 s**.
  Every admitted geometric sample is checked in both representations.
- Disabling only the implemented carry-contact strips at runtime makes
  **all ten** contact-side subcases fail (3.343 s). The mutation is restored;
  the final support suite above passes on the unchanged generated table.
- The existing retained-motion suite passes **6/6 (333.496 s)**, including
  every source flat on later revolutions, raised/lowered short and long
  requests, actual complete-print stop/overtravel, axial entry and relief.

### A physical request that the old table wrongly blocked

The new retained regression sets input 1 on the lowered diagnostic stack,
turns to `133.5 + (22.22 + 16)/(72/11.25)`, and withdraws the selector.
The source tooth law, not a manually seeded bank coordinate, leaves the
shaft at 22.22 degrees. Continuing to 146.3 is physically clear; the real
carry transfer has not yet started at 146.375.

Substituting the previously committed table reproduces **blocked instead
of completed** (10.501 s). The refined table completes and replays exactly
(13.329 s). The original browser export independently reproduces the false
stop at **144.94640960699735**, with the shaft held at 22.22. The fresh
export reaches **146.3** and preserves exact replay.

The isolated browser also passes the two existing retained-stop cases,
their unsplit long requests, relief/idle/retry and eight legal three-turn
requests, with no page errors. Raised/lowered stops still match Python at
145.22323837279146 and 144.9514572141925 degrees. Both free-support and
stopped close-up images were inspected. The document is version 5, and
all referenced rigid artifacts exist.

- New export: `_build_higher_refined_lockout/manifest.json`, SHA-256
  `548c85d3a6543ce4592a4d4500faad2348507b10d87e05eef0b5e9119a4ae690`.
- Original red export: SHA-256
  `3415ba04e5ca46ea8efeed9f8f46c16af426dff79eaf80dcacf6821fc5292938`.
- Viewer bundle: SHA-256
  `1098d52b62445f2a8ef6fece5ce38b4d9723ae1f8a6c74d21729668d4bb6d1aa`.

## Full-tree acceptance completed; production adoption remains next

The two original raised/carried stop tests pass **2/2, 1215.666 s**. Their
report is `_build_checks/higher-refined-python-acceptance.json`. The new
`test_real_carry_preparation_preserves_the_free_support_approach` also passes
separately: **1/1, 657.766 s**, log
`_build_checks/higher-t07-refined-full-free.log`.

The fresh complete export `_build_higher_refined_operating/` passes all
browser carry/withdrawal/short/long/replay/relief/free-support cases with no
page errors. Its document SHA-256 is
`15617702eb301b7b00f6e88448fabe4886d565c0d1977ae92aa22da3990b1b62`.
All **213 coordinates at each of four stopped/idle states match Python
exactly**, maximum difference zero. The free-support request reaches 506.3
degrees and replays exactly. The three full-model screenshots were inspected;
they confirm the assembly and poses, not hidden contact clearance.

The default-root regression now independently fails as intended:
`OperatingHigherLockoutTest.test_raised_tens_withdrawal_stops_the_actual_crank`
reports completed instead of blocked (**66.318 s**). T07 is therefore still
unadopted, not silently accepted in the production model. A neighbouring
three-test arithmetic batch on HigherOperatingTrial was interrupted during
its first test at the pilot's requested fresh-agent handoff (exit 130).
**None of that batch is counted as passed.**

The [handoff](handoff-2026-09-21.md) names the next adoption steps and remaining
roadmap. [Checkpoint evidence](evidence/handoff-checkpoint-2026-09-21.json)
preserves comparison results and raw-log hashes. The roadmap remains 12/23;
this increment does not mark any whole-machine task complete.
