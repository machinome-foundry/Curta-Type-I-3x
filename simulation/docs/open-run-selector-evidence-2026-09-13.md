# Selected input at stationary home — readiness finding

The existing selected input does **not** pass installed travel clearance.
At both the initial `099` home and post-cascade `100` home, eight native
intersections occur at all ten seated settings. Adding the nine half-detents
finds a ninth pair and larger ball/shaft overlap. This is a Curta geometry
and installed-detent finding, not a reason to change the proposed running
contract. No operating part, placement, law or framework/viewer code changed.

The completed carry/frame correction remains separate and unchanged. Its
191-file regression fingerprint still matches every recorded source. These
new probes cover interfaces the earlier frame/carry checks did not certify;
the prior regression is not re-labelled as a whole-input clearance pass.

## A frozen machine, not a rewritten calculator input

[The probe](../tools/open_run_selector.py) assembles the complete existing
Curta once per fixture, then transforms independent native copies of eight
selected input bodies. It never changes the root operand while moving them.
All 428 installed physical bodies remain in the neighbour inventory: 422
have native geometry and six retain their explicitly named source meshes.
Only disjoint bounding boxes exclude a pair. Every candidate in these runs
has native geometry; no faceted fallback is exercised.

Three selector shaft/number-roll bodies rotate about the actual source axis
`(58.5, 0, Z)` by 36 degrees per setting. The knob, screw, ball, spring and
keyed ones input group translate -6 mm in Z per setting. The eight independent
placements match the existing public `SelectorBank` and `TransmissionBench`
at each of the ten seated settings. Maximum native vertex discrepancy is
`1.503e-14 mm`; maximum volume discrepancy is `2.729e-12 mm³`. Those are
placement comparisons, not collision tolerances or proof of physical coupling.

The frozen roots retain these values throughout the sweep:

| Fixture | Result | Ones/tens/hundreds shaft angles, degrees | First/second carry fractions |
| --- | ---: | --- | --- |
| Initial home, crank 0 turns | 99 | 652, 632, -36 | 0.2769241667, 0.2769241667 |
| Post-cascade home, crank 1 turn | 100 | 4, -16, 36 | 0, 1 |

All eight root drivers, all three dial angles, selected root setting and
original native placements are also checked unchanged. The diagnostic copies
traverse 0–9 while the old root remains at operand one. Thus the second carry
is genuinely held in the probe's post-cascade fixture; this is **not** a
production runtime persistence test or an admissible new root control.

Negative placement witnesses detect reversed knob travel (12 mm discrepancy),
omitted keyed-input travel (6 mm), and rotation about the machine origin
instead of the selector axis (36.155 mm). Four new lightweight probe tests
cover the signed transforms, mover allowlist and numeric-driver/port distinction.

## Native counterexamples

The [complete retained record](evidence/open-run-selector-2026-09-13.json)
contains exact occurrence paths, intersection locations, candidate neighbours,
the complete inventory, frozen states, probe hashes and raw-record hashes.
No positive volume is waived, including the small between-detent screw contact.
All recorded intersections are valid native results; invalid-result and
negative-volume diagnostic counts are zero.

| Pair, selected selector unless stated | Maximum overlap in the 19-pose initial sweep, mm³ | Positive poses / 19 |
| --- | ---: | ---: |
| Screw / knob | 13.141988148 | 19 |
| Ball / knob | 1.195387659 | 19 |
| Knob / lower housing | 9.253229594 | 19 |
| Spring / ball | 3.499180785 | 19 |
| Spring / knob back seat | 2.661638395 | 19 |
| Bottom shaft / screw | 0.000526496 | 9, half-detents only |
| Bottom shaft / ball | 2.866621266 | 19 |
| Bottom / top shaft joint | 0.533679777 | 19 |
| Number roll / lower housing | 4.169640238 | 19 |

The post-cascade sweep reproduces the same nine pairs. At seated settings only,
the maximum ball/shaft overlap is 0.387855792 mm³; it grows to 2.866621266 mm³
at setting 0.5 under the existing rigid-ball placement. A parked-ball model
therefore cannot be accepted as the installed detent travel merely because
the ten numbered positions were sampled.

These are not nine independent travel obstructions. The screw/knob and shaft
join are co-moving assembly fits; spring contacts require installed compression
and seating evidence. The housing and detent interfaces have relative motion.
Classification is an obligation for a proposed correction, not an overlap waiver.

## Source/manual and physical-connection evidence

Manual pages 32–33 were rendered and inspected. Page 32 specifies a 5 mm ball,
holding the ball and spring compressed while inserting the selector shaft,
and M4 tap/die operations for the knob and selector screw. Page 33 places the
ones input group's lower gear between the knob fingers.

The native source ball has one valid spherical solid, diameter 5.4 mm in all
three axes and volume 82.447957601 mm³. An independent nominal 5 mm sphere at
the same center has volume 65.449846950 mm³. Native differences show that the
source contains that sphere entirely, with 16.998110651 mm³ outside it.
This confirms a source/manual size discrepancy, not just a loose bounding box.
The nominal sphere is a measurement witness only: no ball was replaced, and
choosing 5 mm has not been proved to resolve the installed contacts.

[The contact-localization probe](../tools/open_run_selector_sections.py) also
perturbs the independently frozen setting-zero parts:

- Keyed input group versus knob: zero overlap at the declared pose; a -0.01 mm
  independent axial shift enters a fork face by 0.107988198 mm³. Positive
  shifts through +0.25 mm are clear; +0.5 mm enters the opposite face by
  0.658727976 mm³. This supports the manual's captured-gear interpretation,
  but does not certify force transmission or the complete moving contact path.
- Bottom shaft versus selector screw: zero overlap at the declared pose and
  at ±0.1 degree perturbations; both ±1 degree witnesses produce positive
  native overlap. The groove constrains relative rotation, but the later
  half-detent finding prevents accepting the existing linear relationship as
  an everywhere-clear helical follower law.
- The source bottom/top shaft joint overlaps axially by 0.025 mm. It is not
  a travel-dependent interference or authority to move either shaft.

## Inspected pixels

The [six native sections](../../_build_evidence/open-run-selector-sections.png)
were opened and inspected, with equal axis scales and measured overlap in red.
They localize the knob at one housing-slot edge, the number roll at the housing
window, ball/shaft penetration, both spring seats and the axial shaft join.
These are source-pose diagnostic sections, not repaired geometry, a complete
assembly rendering or a spring-force solution. PNG SHA-256:
`a50e8cce256d7c0bf655d3565dc269973ae0159832f1219f9a953560ff33e3a2`.

The inspected manual extracts are generated artifacts:
[page 32](../../_build_evidence/open-run-selector-manual-32.png) and
[page 33](../../_build_evidence/open-run-selector-manual-33.png).
Their hashes are respectively
`f8d9b49ddb56a90f77121824543b4caa178b67dcd62437ee335eedb5b2510aa1`
and `aa6632e44e01ea333370ff8d51e34e4577fc37ecd18a7aa9f480fe9f14486557`.
The tracked manual PDF hash is
`af2a7e512063ec485ae992bbf490f5f1e14aac5dc35277183603ff725fb2ab7c`.
Generated images and CAD artifacts remain ignored; the evidence JSON is retained.

## Reproduction and verification

Source content is Curta `739c91a5144fba8bac3a904ddb7b2fb5338fc363`, plus the
named new diagnostic files whose hashes accompany each run. The baseline 191
source hashes are referenced from the retained frame regression record, checked
against every probe input and rechecked on disk after the sweeps. No historical
full CAD matrix is claimed as newly rerun in this diagnostic-only pass.

Use the workspace Python 3.12.3 environment with CadQuery 2.7.0,
cadquery-ocp 7.8.1.1.post1, molejo 0.2.0, NumPy 2.2.6, manifold3d 3.5.2 and
trimesh 4.4.9. Framework content/import is the matching worktree at
`6e41f2da132a8604f9b68895967247fb8876fc4d`, not just metadata version 0.6.0.

From the Curta worktree, run each CAD command sequentially:

```sh
ulimit -v 8388608
export PYTHONPATH="$PWD:/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation"
export SOLID_BUILD_DIR=_build_open_run_evidence
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
timeout --kill-after=10 300 /home/asa/devel/libresolid-studio/.venv/bin/python -m simulation.tools.open_run_selector --fixture initial --samples 10
timeout --kill-after=10 300 /home/asa/devel/libresolid-studio/.venv/bin/python -m simulation.tools.open_run_selector --fixture postcarry --samples 10
timeout --kill-after=10 300 /home/asa/devel/libresolid-studio/.venv/bin/python -m simulation.tools.open_run_selector --fixture initial --samples 19
timeout --kill-after=10 300 /home/asa/devel/libresolid-studio/.venv/bin/python -m simulation.tools.open_run_selector --fixture postcarry --samples 19
timeout --kill-after=10 300 /home/asa/devel/libresolid-studio/.venv/bin/python -m simulation.tools.open_run_selector_sections
```

| Probe | Native pair evaluations | Process wall seconds | Maximum RSS, KiB | Exit |
| --- | ---: | ---: | ---: | ---: |
| Initial, 10 seated settings | 280 | 80.68 | 570740 | 1 |
| Post-cascade, 10 seated settings | 280 | 92.62 | 610128 | 1 |
| Initial, 19 settings | 530 | 120.29 | 691004 | 1 |
| Post-cascade, 19 settings | 530 | 118.59 | 778572 | 1 |
| Native contact localization | Separate named measurements | 35.34 | 652084 | 0 |

Exit 1 deliberately reports the native counterexamples. No completed run timed
out. JSON `wall_seconds` measures the probe body, while this table includes
interpreter/import startup. The first helper launch failed before clearance
because it incorrectly read numeric root drivers with `.value`; a focused
test reproduced that error before fixing the probe alone. The initial three
transform tests also ran red before the helper existed. Both red outputs are
retained in the evidence JSON. The final lightweight command passes 16 Python
tests (four probe, six arithmetic, six cycle), and all five existing calculator
JavaScript tests pass. These do not turn the geometric failures green.

## Recommended next step — not ratified

Open a separate **Curta-owned, selected-selector fit and detent** proposal.
Resolve the installed ball size/seat and spring compression against the manual;
measure the actual helical follower path; classify the co-moving screw/shaft
fits; and bound any necessary housing-slot/window relief to this one station.
Any adapters must remain source-derived, preserve upstream files and protect
the housing's supports, threads and the other seven selectors. Do not assume
a new running gap or cut a swept pocket before measuring those protections.
An explicit fixed-seat inventory is a design choice to review, not permission
to exempt moving contacts or globally ignore the nine pairs.

The approved carry/frame correction did not authorize these changes. The
selector correction therefore needs its own reviewed scope before production
geometry changes. Keep the existing framework law/interface direction and
the selected 0–9 acceptance requirement; do not shrink the input to zero/one,
hide the housing, or substitute a cosmetic normalized selector.

After that prerequisite is settled, resume continuous travel/home-window,
complete initial setup, remaining neighbour and outgoing-carry boundary
evidence. These discrete counterexamples do not certify any unsampled path
or determine a safe angular home-window width. The original `simulate-the-curta`
remains active at 7/17; the frame correction stays archived but not integrated.
The three coordinated running proposals and the pilot's explicit solid-node
feature-start gate are still ahead.
