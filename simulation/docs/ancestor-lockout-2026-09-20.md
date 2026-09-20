# Ancestor constraint: complete-bell wrong-order diagnostic

This is framework acceptance in the real operating tree, **not completion of
Curta's lockouts**. Production `OperatingCurta` and its manifest remain
unchanged. The opt-in `AncestorLockoutCurta` inherits every physical assembly,
coordinate, existing restraint and control; it adds one ancestor declaration.
No upstream CAD or simulation print fit is changed.

## Red evidence in the full operating tree

Starting from rest: set `digit_1=3`, move `crank_rotation` to 90 then 120,
withdraw `digit_1=0`, then request 150. The actual crank coordinate is negative
(`main_drive.crank.turn=-120`), and
`transmission.result.ones.turn=189.60000000000002` is retained. Other selectors
remain zero; the tens shaft is -16, unlike the earlier two-channel diagnostic
which set both inputs to 3. No reduced-fixture shaft value is substituted.

Before the declaration, the complete model reports `completed` at 150 and
its actual ones upper locking assembly intersects the complete bell by
**1.0804018099400123 mm³**. `test_ancestor_lockout.py` was run with its model
aliasing unmodified `OperatingCurta`: **1 failed, 129.27 s**, specifically
`'completed' != 'blocked'`.

## Source geometry decides the boundary

`tools/ancestor_lockout_contact.py` obtains world solids/meshes from the full
retained operating tree, then rotates the entire bell against the held
locking assembly. It does not replace the bell by one isolated disc.

Targets:

- `carry_mechanism.tens_bell.tens_bell_1`
- `transmission.result.ones.p_10221_1`

Twenty bisections start from [120, 150] degrees; any positive volume means
contact, without an overlap epsilon. The small phase offsets check the local
neighbourhood used to recognize this particular retained state.

| Shaft angle | Kernel | Last free crank | First positive contact |
|---|---|---|---|
| 189.599° | OCCT | 125.33048629760742° | 125.33051490783691° |
| 189.600° | OCCT | 125.33065795898438° | 125.33068656921387° |
| 189.601° | OCCT | 125.33082962036133° | 125.33085823059082° |
| 189.599° | published mesh / Manifold | 125.32241821289062° | 125.32244682312012° |
| 189.600° | published mesh / Manifold | 125.32258987426758° | 125.32261848449707° |
| 189.601° | published mesh / Manifold | 125.32276153564453° | 125.32279014587402° |

Both kernels report no positive volume at 120, 122, 124, 125, 125.3 and
**125.32°** at all three sampled phases. Both report positive volume at
125.34, 126, 130, 140 and 150. At nominal phase and 150, the published mesh
has 0.8306023345003557 mm³ overlap. These are different representations, not
equal-volume claims. The complete-bell boundary supersedes the isolated-disc
125.335121..125.335169 bracket for this diagnostic.

The law rounds down to **125.32°**, on the measured free side of both kernels.
It recognizes shaft phase 189.599..189.601 and a committed crank in 120..150.
Outside that prepared window its one-turn permissive fallback is merely a
diagnostic envelope, **not a contact law or a safe-operation certificate**.
Sampling this narrow neighbourhood does not prove every phase between samples,
all indexed bands, later revolutions, carry positions, subtraction or other
channels. Only the stated retained history is the acceptance scenario.

## Validation environment and reproduction

Framework cycle: `ancestor-joint-constraints`, base `0ce71cd`, planning
`644f5b2`, with its implementation worktree on `PYTHONPATH`. Curta starting
content: `0db199f`. Commands run from that framework bench with the actual
project root (not its shop symlink):

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
PYTHONPATH="$PWD:/mnt/data/machinome-projects/Calculators/Curta-Type-I-3x" \
/home/asa/devel/machinome-studio/.venv/bin/python \
-m simulation.tools.ancestor_lockout_contact
```

The retained test is `simulation/test_ancestor_lockout.py`; its acceptance
checks the actual crank stop, held shaft, both geometry kernels, replay and
small reverse relief within the original anti-reversal backlash.
Browser acceptance uses `tools/ancestor_lockout_browser.py` against a separate
export. It never resets or changes the pilot's Studio session.

Two probe setup failures are not mechanical evidence: `meshes=False` leaves
exactness unavailable to the world-solid walker until the tree is prepared;
and re-tessellating the transformed locking BREP produced an invalid Manifold
input. The final measurement uses `meshes=True` and the actual published
meshes, whose native Manifold status is checked. No mesh repair, welding
tolerance, discarded positive overlap or source change was used.

## Retained acceptance

After installing the ancestor declaration, the same real-tree test passes:
**1 passed, 175.85 s**; the final rerun with explicit Manifold status checks
also passes (**1 passed, 174.24 s**). The request stops at crank 125.32°, the shaft stays
189.6°, and the stopped complete bell/lockout pair has zero native and no
positive faceted overlap. Restoring the prepared snapshot and repeating the
request gives an identical snapshot. A .05° reverse relief completes within
the original pawl's backlash; one idle tick does not resume discarded travel;
a new forward request blocks at 125.32 again. The old anti-reversal bound
still participates: the ancestor has not replaced it.

A separate export to `_build_ancestor_lockout/` succeeds. It requires this
framework cycle on `PYTHONPATH` until the pilot separately authorizes integration;
it is not selected by the project manifest.

## Browser and visual acceptance

The installed viewer completed its independent running-time cycle during this
validation. The tested bundle is API **23**, version 0.2.0, with clean viewer
content `4355da1a7f64dacd7d86eb27dbdfdf7ced94598f`. No viewer source was changed
by the ancestor-constraint cycle. The document stays **version 7** and uses
the existing span/expression format.

`tools/ancestor_lockout_browser.py` compares against the existing operating
build: **all 608 descendant paths, 25 controls, and the complete coordinate
declaration/default bank are unchanged**. Public hosted requests reproduce the
125.32° stop, .05° relief, held shaft and exact snapshot replay. A real
rightward 240-pixel crank-handle drag produces five completed 1° requests and
a blocked request admitting only .3199999999999932°: the final crank is
125.32°, with shaft 189.60000000000002°. No page errors were reported.

The stopped image `_build_ancestor_lockout/stopped-lockout.png` was inspected:
the actual complete bell and ones locking assembly are correctly isolated,
and the panel shows 125.3200° and a blocked request. Pixels establish the
parts, orientation and committed state; the two kernels, not pixel resolution,
establish the very small free-side clearance. The pilot's Studio session was
not opened, reset or otherwise changed.

Reproduce the hosted check after exporting the diagnostic:

```sh
python -m simulation.tools.ancestor_lockout_browser \
  --build /mnt/data/machinome-projects/Calculators/Curta-Type-I-3x/_build_ancestor_lockout \
  --baseline /mnt/data/machinome-projects/Calculators/Curta-Type-I-3x/_build/operating_curta/viewer.json
```

Use the workspace venv and cycle/project `PYTHONPATH` above. Do not inherit a
CAD process's virtual-memory cap into Chromium. Full readbacks and navigation
are saved as the ignored `_build_ancestor_lockout/acceptance.json`.

Content SHA-256:

- viewer bundle: `427e5090bc8119fa0e4cf80e0ca2366a72567cb5c945adddfc60631d5dc6944d`
- diagnostic manifest: `ff5d9e6b9b41c84433753311ee1a9993208973d486f2413875253eb310686c0d`
- baseline operating document: `a15c92eb9dc0b8e6e2c8bfa820a101a9a1ef379d06f86b1802d2d0765c411586`

The first pointer attempt requested insufficient travel (124.5°, not the
stop). The longer frame-paced gesture above fixes that test setup, without
changing the model or viewer. A first screenshot timed out after individually
hiding every leaf; hiding unwanted assembly branches instead completed the
capture. Those setup failures are retained here, not counted as acceptance.

The exact tested framework implementation source is pinned independently of
the later documentation/archive commit: SHA-256
`3e48841917e38e79cbf44e51ff5659e9a09c4b5cfb0ae52c009315cb4f27261c`, computed
from `sha256sum` lines for, in order, `machinome/motion/constraints.py`,
`machinome/motion/couplings.py`, `machinome/node/assembly.py`,
`machinome/node/base.py`, `machinome/node/declarative.py`,
`machinome/node/phase.py`, and `machinome/simulation/program.py`, with those
relative filenames, piped through `sha256sum` again.

Focused unmodified operating-model regressions pass: **3 passed, 871.17 s**.
The exact tests are
`test_running_reverser.py::RunningReverserTest::test_counter_direction_changes_without_recomputing_result_or_history`,
`test_running_partial_inputs.py`, and
`test_running_reverser.py::RunningReverserTest::test_detent_is_not_an_invented_hard_stop`.
They preserve the four-turn arithmetic/reversal sequence, retained partial-input
history and replay, and original reverser travel limits. They do not broaden
the diagnostic's accepted contact window or close the remaining roadmap tasks.
