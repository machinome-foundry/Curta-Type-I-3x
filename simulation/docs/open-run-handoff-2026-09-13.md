# Curta checkpoint — paused for project direction

The pilot requested: "wrap this up and commit, leaving Curta in a documented
state, I want to steer the project direction."

This is an evidence/diagnostic checkpoint, not a delivered selector fit or a
completed simulation. Work is paused. Await the pilot's direction; do not
automatically resume the previous measurement or implementation sequence.
The checkpoint preserves the existing ratified scope without choosing a new
direction, abandoning a change, or promoting unimplemented requirements.

## Repository and state

Work remains on branch/worktree `open-run-simulation` in
`projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation`.
This commit follows alignment planning commit
`da432fbdc7fe0e7f89e308237f281e9c3d368754`; the containing commit is the
checkpoint identity. Nothing is integrated, pushed, published or removed.
The project primary checkout and all other repositories are untouched by
this closeout. Cross-repository roadmap documents were not refreshed here;
this handoff is the latest Curta disposition.

| Record | State at checkpoint |
| --- | --- |
| Original `simulate-the-curta` | Open, unarchived, 7/17 tasks; untouched by this checkpoint |
| `clear-result-carry-frame-contacts` | Completed and archived; implementation `3afcac9`, archive `739c91a`; not integrated |
| `fit-selected-input-selector` | Ratified original plan `aec7ca4`, alignment revision `da432fb`; open and paused, 2/22 tasks (1.1 and 1.3) |
| Running simulation | Curta readiness incomplete; no solid-node/viewer feature implementation |

The existing complete Curta still uses prescribed calculator/pose laws.
The selected selector, spring, ball, follower and housing have **not** been
changed by the selector-fit work. New `simulation/selector_fit.py`,
`test_selector_fit.py` and seven `tools/selector_fit_*.py` probes are
diagnostic only; they are not wired into the public root or manifest.
The previously completed two-station carry/frame correction remains installed.
Upstream geometry, all other operating parts, controls and instructions remain
unchanged. The frozen evidence accounts for all 428 physical bodies.

## What the evidence establishes

- The unchanged source guide misindexes the nominal ball: a held numbered
  position is on a detent flank. The ratified source-parallel correction
  aligns all ten nominal seats without changing their numbered datums.
- A 0.34 mm continuous-wall witness and retained back-seat block fit within
  the candidate local restoration bounds. This is local geometric
  feasibility, not an installed part, complete support proof or print rating.
- Both allowed fixed-source joints are classified by exact canonical
  intersection regions and constant relative placement, with nine rejected
  mutations. No moving contact is exempted.
- The completed carry/frame correction retains its independent acceptance
  and unchanged 191-source regression fingerprint.

## Unresolved work, not selected next actions

- **Installed spring:** source-sized analytic helix end centres agree, but
  the end planes differ by about 6.75°. Plain-helix source equivalence,
  supported installed ends and coupled compression/retention are unproved.
- **Screw/groove and gear/fork capture:** localized play measurements are
  retained. Of 60 follower queries, 23 have zero overlap, 31 have positive
  overlap and six return invalid booleans. Invalid results remain unresolved;
  the completed probe's exit 0 is not mechanical acceptance.
- **Ball guidance and retention:** 75 support brackets include cardinal
  lateral-play samples; they are not a complete play-disk or continuous
  coupled-retention proof. The source phase law remains unchanged.
- **Local reconstruction:** complete mouth/support protection, separate
  added/removed-material guards and damage mutations remain open. No fitted
  knob, operating ball/spring, follower or housing relief has been authored.
- **Acceptance:** both frozen homes, full bidirectional installed-neighbour
  travel, continuous bounds, fitted-part regression and inspected fitted
  views remain open. The broader home-window, initial-setup and outgoing-carry
  boundary obligations are also unresolved.

The ratified bounded correction and all stop conditions remain in the
[change design](../../openspec/changes/fit-selected-input-selector/design.md).
Neither these findings nor this checkpoint select a replacement machine,
revised fidelity, release 0.7/0.8, or new development order. The separate
explicit pilot go-ahead before solid-node feature implementation still applies.

## Last verification and durable evidence

The last native selector run has **23 tests: 4 pass, 19 expected red failures**
(75.80 s runner, 82.95 s wall, 614692 KiB peak RSS, exit 1).
The additional continuous-wall test fails against the unchanged knob;
the additional exact fixed-joint guard passes. The other 18 red failures
are the previous source-geometry baseline. This is not a green fit.

For closeout, the 16 lightweight Python tests and five calculator JavaScript
tests pass again. The prior 191 operating-source hashes and the fixed-joint
source fingerprints match. The existing full-root viewer document is
unchanged. Strict OpenSpec validation passes all three records, and all nine
diagnostic/test Python files compile. No heavy CAD probe, full 39-module regression, build or snapshot
was rerun to prepare this checkpoint. The previous full regression remains
159/161 faceted and 160/161 native, with the named bearing-facet and
housing/thread findings; it does not include passing selector-fit acceptance.

Read the [implementation chronology](selector-fit-implementation-2026-09-13.md)
for measurements, interpretation, commands, source provenance and limitations.
The committed evidence is split into:

- [Original selector-fit measurements](evidence/selector-fit-measurements-2026-09-13.json):
  source surfaces, original misindexing and red baseline.
- [Alignment and fixed-joint gates](evidence/selector-fit-alignment-gates-2026-09-13.json):
  all ten seats, wall/seat witnesses, spring seam and nine joint mutations.
- [Checkpoint evidence](evidence/selector-fit-handoff-2026-09-13.json):
  full capture/play and spring comparison data, six kernel refusals, final
  native test transcript with generation chatter removed, hashes and
  closeout check results.

Raw logs, native-section images and CAD caches remain in the worktree's
ignored `_build_evidence/` and `_build_open_run_evidence/` directories;
they are not part of Git delivery. Their hashes and measured numerical
contents are retained in the committed records. No ignored artifact was
deleted. The reproduction commands are for a future explicitly resumed task,
not an instruction to run more work during this pause.
