# Curta3x production consumer evidence

Status: final stable-source paired API acceptance and draft export passed.
No fabrication or whole-machine geometry acceptance is claimed.

Project base: `fb4708e98463b3cb4c0130cc3e92514c2a31155b`.
Project branch: `production-layer-3x`.
Project worktree: `WTs/production-layer-3x` in the independent
`Curta-Type-I-3x` repository. The primary worktree's pre-existing untracked
files were not copied, edited or removed.

Initial paired framework planning commit: `5ecd4eae1f0f867626def307bc9ecbe08cd8f3d2`,
based on completed source branch commit
`e570068287c56e84f6ccb4ed73f0bae7bed5a07c`. Final tested framework and
project content identities will be recorded after acceptance.
The planning commit was subsequently amended to
`bf29dff5a836dc3b6ecb01db47836f6488917da8`, on the same source base.

## Independent source evidence

Marcus Wu's project README points to the
[3x author BOM](https://docs.google.com/spreadsheets/d/16EJePozXW-uC6UFISzyT2eMk7c8wh6v-EP5L1U8fzfM/edit).
Inspected 2026-10-04. Printed sheet header: Curta Type I - 3x FDM,
workspace Main, created 12/2/2016.

| Author printed item | Quantity | Current selected occurrence | Provenance |
| --- | ---: | --- | --- |
| Crank handle pin screw | 1 | main_drive/crank/crank_handle_1/crank_handle_pin_screw | Source-backed STEP part |
| Crank handle | 1 | main_drive/crank/crank_handle_1/crank_handle | Existing SeatedCrankGrip fit replacement |
| Main crank | 1 | main_drive/crank/crank_handle_1/main_crank | Existing SeatedMainCrank fit replacement |
| Crank handle pin | 1 | main_drive/crank/crank_handle_pin | Source-backed STEP part |

Sheet rows 8, 10, 66 and 76 respectively support those quantities and
their infill/layer instructions. Filing and threading the printed pin
screw comes from row 8. No polymer or measured finished mass is established.

The [non-printed hardware sheet](https://docs.google.com/spreadsheets/d/16EJePozXW-uC6UFISzyT2eMk7c8wh6v-EP5L1U8fzfM/edit#gid=1182246287)
has header Curta 3x FDM tools IN_PROGRESS, created 12/4/2016. Its item 2
lists seven M4 nuts and contains a hyperlink to
[Bolt Depot product 4784](https://www.boltdepot.com/Product-Details.aspx?product=4784).
Its supplier-indexed primary-source description gives DIN 934 and 4 mm x
0.7 mm thread. Direct supplier retrieval was restricted. Grade is omitted
because the indexed title and internal supplier description differ; no
manufacturer or offer is inferred. Four `frame/fasteners/m4_nut_1..4`
and three `frame/upper_frame/m4_nut_1..3` provide the actual seven
model occurrences. The sheet's broad assembly wording does not establish
more than that reconciliation.

The local `Manual/Curta Build Manual.pdf`, printed page 30, specifies ten
result and five turns carry levers, with about 57 mm of 0.6 mm music wire
per spring. The hardware sheet item 11 agrees on fifteen made springs.
Each current mounted spring has one flexible `wire` leaf; that is fifteen
handled-wire candidates, not fifteen additional wrappers. Their made-wire
process remains unsupported and unassigned, with instructions scoped to
the actual ten/five subproduction boundaries.

## Retained limitations

One author printed tens bell spring is represented by `RetainingSpring`
as five rigid/flexible patches. Their unassigned candidate records are
not an assertion that five springs should be printed. Author hardware
items 10 and 12 ambiguously list decimal-marker 3 mm balls with quantities
10 and 15; those rows are not blindly summed. The local manual's printed
page 48 leaves its carriage-spring explanation unfinished.

`MechanisticCurta` retains the existing simulation-only captive clearing-loop
mounting and open complete-geometry acceptance. This work does not change
any simulation source, modified fitting geometry or author STEP/STL asset.
Mesh identity, glyphs, STEP ingredient counts and terminal-patch counts
are not independent author BOM quantities. Two controlled production
bindings are regression evidence over one 3x instance, not another workshop.

## Local source identities

SHA-256 at the project base:

| Source | SHA-256 |
| --- | --- |
| Manual/Curta Build Manual.pdf | af2a7e512063ec485ae992bbf490f5f1e14aac5dc35277183603ff725fb2ab7c |
| CAD/Curta Assembly.step | 943ec7545d9cbcbe69266f0e8b1b65e912f80fa46cad0c974dea164bdcbbbee3 |
| simulation/crank_coupling_parts.py | df29ec5beaf09cc35195e0f49647dfeceb5a30c6144468039596c2995de91519 |
| simulation/crank_grip_parts.py | 813733d60f2fc99a77479a19bda3babb18ac4514cff57bd102e29c0f9f3b0770 |
| simulation/retaining_spring.py | 0aef1c6b8d82e255889a70678d6dc3a3e841ee34e3bbb165d7f83ed8c0108c85 |

## Verification record

2026-10-04 initial red: the installed framework has no
`machinome.components`, so collecting `production/test_production.py`
failed with ModuleNotFoundError. No test was skipped and no fallback
private interface was used. This is missing-capability evidence, not
a geometry failure. Framework application is in progress.

The first launch mistakenly supplied a nonexistent framework `src/`
directory. Import-path inspection showed it used the primary editable
framework, not the paired bench. The correct flat-layout PYTHONPATH is
the production worktree root. All paired acceptance must use that root;
the following earlier baseline is not paired-framework proof.

Narrow existing simulation baseline against the installed primary framework:
`simulation/test_remaining_mates.py` and
`simulation/test_transmission_mates.py` passed six tests and six subtests
in 28.49 seconds. These exercise existing attachment selection, poses,
state and replay. They are not new production acceptance and do not
discharge the open whole-machine geometry acceptance.

The first correctly paired production run passed three tests and failed
three in 114.44 seconds. It exposed an authoring error in this consumer:
the three upper-frame nuts had been referenced under the bell assembly.
The public API correctly returned absent targets and only four assigned
nuts. Project source class boundaries and existing occurrence evidence
place the other three at `frame/upper_frame/m4_nut_1..3`. The profiles
were corrected; the independent acceptance remains seven nuts, not four.

Corrected paired run: **12 passed, 6 subtests passed in 94.80 seconds**.
Exact command from the dedicated project worktree:

```sh
env PYTHONPATH=/home/asa/devel/machinome/machinome/WTs/v0.8-production:/mnt/data/machinome-projects/Calculators/Curta-Type-I-3x/WTs/production-layer-3x SOLID_BUILD_DIR=_build_production /home/asa/devel/machinome/.venv/bin/python -m pytest -q production/test_production.py simulation/test_remaining_mates.py simulation/test_transmission_mates.py
```

Verified import locations:

```text
machinome.__file__ = /home/asa/devel/machinome/machinome/WTs/v0.8-production/machinome/__init__.py
machinome.production.profile.__file__ = /home/asa/devel/machinome/machinome/WTs/v0.8-production/machinome/production/profile.py
```

Six independent production tests cover actual flexible-wire occurrences,
fitted model types, lazy structural consumption, local instruction files,
four printed units and seven standardized sourced nuts, unknown material
and mass, two controlled profiles over one live nondefault simulation,
access-order invariance, source/parameter/state preservation, and a hashed
draft export. Six existing tests plus six subtests cover narrow attachment
and replay regressions. This is not complete geometry acceptance. No private
framework traversal, altered geometry or weakened seven-nut oracle was used.

### Final frozen-source acceptance

The same exact command above, including the stronger assertion for all five
unassigned retaining-spring patches, passed **12 tests and 6 subtests in
100.25 seconds** on 2026-10-04. Both module locations above were rechecked.
Framework HEAD was `41d24cef37817f2a8c0c79ea9014eb93b77a0261` before
and after the run; its implementation was still uncommitted. Python source
was explicitly frozen by the apply agent; manual/evidence-only edits could
continue without being asserted as executable acceptance.

Framework package fingerprint before and after:
`43628972f1a4458c5938f673c341fc9c0caadfe42397b8f1b8e61e6badab9738`.
Computed from the framework worktree with:

```sh
rg --files machinome -g '*.py' | sort | xargs sha256sum | sha256sum
```

Tested project index tree before and after:
`bcb6da65a05a446bf46d5473af6875cfb45b9f99` (`git write-tree`).
Tested production files fingerprint before and after:
`514a6ddb3ddf0bfd4e1d4c4fd94552e205b294c2d3dc216fc26227afdcdf5757`.
Computed with:

```sh
rg --files production -g '*.py' -g '*.md' | sort | xargs sha256sum | sha256sum
```

This final record is an evidence-only addition after that tested tree.
`git diff --name-only HEAD -- simulation CAD Manual pyproject.toml` was
empty. Primary project HEAD and all four pre-existing untracked entries
remained unchanged. Parent reviewed the complete project diff and authorized
the focused project commit after this stable green run; no merge or push.
