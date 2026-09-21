# Carry-contact engine correction — integrated acceptance

The carry preparation failure was a software error, not evidence of an
incorrect printed part. The pilot approved its correction and precision
extension without changing clearance, tolerances, source carry laws or
genuine mechanical-error refusals.

## What was wrong

1. A threshold moving past the lever could cross in the opposite direction
   to the lever's own tiny travel. The engine searched the wrong side for
   the next engagement state and refused the turn.
2. Correcting that direction exposed round-off in following contact:
   +2.22e−16 appeared as relative movement where the declared law has none.
   It falsely switched a reset and then diagnosed an impossible sliding mode.

The first correction establishes the local relative crossing before the
existing nearest-float landing. The second proves constant relative position
algebraically, piece by piece through continuous profile knots. Unsupported
cases and every nonzero relative slope retain ordinary execution. Bank
arithmetic is unchanged. No epsilon, print modification or new carry law is
used to make these tests pass.

## Integrated content

Both independent repositories were clean at their recorded bases and were
fast-forwarded locally after validation. Each cycle has exactly two commits:

| Repository | Base | Planning | Completed / main |
| --- | --- | --- | --- |
| machinome | `e63700e` | `5673d1f` | `9016f00d80ebec651f9a8db505441445a06b42b1` |
| machinome-viewer | `e82b521` | `f77dab4` | `a1ae12dc3ca7c09638898c22501542b123b78acc` |

Both archive `openspec/changes/archive/2026-09-21-mixed-threshold-landing/`,
with synchronized baselines and strict validation. Framework ADR-136 and
viewer ADR-070 record the decisions. No push or release occurred.

After integration, main's focused producer check passes **25 tests / 91
subtests**, its faithful Curta reduction passes **2/2 (46.488 s)**, and
main's viewer corpus/proof check passes **41/41**. Main's rebuilt installed
bundle has the exact accepted hash below. Its missing local `esbuild`
dependency was restored with the existing lockfile before rebuilding; no
dependency versions or lockfile changed. Only the two clean cycle worktrees
were removed, with both branches retained. The live Studio session and
unrelated worktrees were left alone.

## Acceptance

- Framework: **3499 passed / 2033 subtests**, four existing skips, 729.80 s.
- Viewer widget: **1413/1413**, 62.64 s; Python/browser suite:
  **192 passed / 20 subtests**, 436.98 s. Typecheck, bundle and fresh-wheel
  installation smoke pass. Earlier host-load speed failures also reproduced
  on unchanged main; the final suite passes the original, unweakened floor.
- Faithful CAD-free source-law reproduction: **2/2**, 54.046 s.
- Full source-backed `HigherOperatingTrial`: **2/2**, 1145.059 s. Both raised
  and genuinely carried withdrawal, short/long requests, exact replay and
  reverse relief with idle retention pass. This uses real carry preparation,
  not a manually seeded lever or register.
- Complete native/mesh stop and .2° overtravel checks, eight ordinary
  three-turn tooth-count cases and four pin/pawl/reset controls:
  **6/6 tests**, 88.940 s. Both kernels are clear at the admitted stop and
  detect positive interference beyond it.
- Support-curve regressions and **79,310** ordinary trajectory samples:
  **5/5 tests**, 105.705 s.
- The real exported assembly passes in an isolated Chromium worker, including
  exact carry replay, both withdrawal cases, short/two-revolution requests,
  exact stop replay, relief and idle retention. No page errors. The full
  assembly's carry and relieved-state screenshots were inspected.

Python and browser stop at **145.22323837279146°** raised and
**504.9514572141925°** carried, both retaining the tens shaft at **169.6°**.
All **213 coordinates** agree exactly at each stopped and relieved/idle
state: four complete-bank comparisons, **maximum difference 0.0**.

The five new producer conformance cases cover both directions, an observer,
following contact and an unmoving follower. All 23 old scenarios remain
value-identical. Producer/viewer corpus copies are byte-identical.

## Evidence identities and reproduction

- Export: `92719ac99b1188cc50cdc100683946c0235c5a3116be7a2993dff1f15d75c7db`.
- Viewer bundle: `1098d52b62445f2a8ef6fece5ce38b4d9723ae1f8a6c74d21729668d4bb6d1aa`.
- Python report `_build_checks/mixed-threshold-python-acceptance.json`:
  `75c294c40f3c124a0461fbe76f56c45b91cb737a251d9aab2fd03ade7d3aa931`.
- Browser report `_build_higher_operating_trial/carry-browser-acceptance.json`:
  `f5e736d94e5cdf777817ea94a23cdf11a9ec03657f05face7f850b2255d370b4`.

Run `python -m unittest simulation.test_carry_constraint_repro -v` for the
faithful fast reduction and `python -m unittest
simulation.test_higher_operating_trial -v` for the full assembly. Setting
`CURTA_ACCEPTANCE_REPORT` to an output filename records its stopped/idle
banks. `python -m simulation.tools.higher_operating_browser --build
_build_higher_operating_trial --python-report <report>` exercises the exported
worker and checks every value against that report. Select the matching
framework/viewer checkouts in the environment; no live Studio session is used.

## Scope still open

This closes the software gate, not Operating Curta's whole roadmap. The
default model, upstream CAD and production constraints were not changed.
T07 remains a separate, unadopted fit/profile trial. Near-edge carry-tooth
refinement, the other higher/counter channels, further action orders,
clearing-loop fitting and final whole-machine acceptance remain under the
existing project record. See
[higher-result investigation](higher-result-lockout-2026-09-21.md) and
[author review](author-review.md). No task 6.2/6.3 completion is inferred from
this scoped engine correction.
