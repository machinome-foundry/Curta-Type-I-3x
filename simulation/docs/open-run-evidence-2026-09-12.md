# Open-run preparation: recovered profiles and installed clearance findings

Status: evidence pass, 2026-09-12. The historical profile inputs are recovered
and reproduce the committed profiles. Fresh isolated carry tests and a scoped
static `099` check pass. The subsequent installed transition diagnostic finds
native spring/frame and slider/frame intersections at both selected carry
stations. The mechanical evidence gate is therefore not satisfied. This is
not a causal running simulation or approval to begin production implementation.

Project: `60979adbc795785fc51a28a386f85d1a49bfedf7` in this project's
`WTs/open-run-simulation`. Framework: `6e41f2da132a8604f9b68895967247fb8876fc4d`
in the workspace's `solid-node/WTs/open-run-simulation`. No viewer was exercised.
Both primary checkouts and all production source were left unchanged.

## Profile recovery and reproduction

All three raw logs were found in this project's primary `_build_evidence/`.
Their complete-file SHA-256 hashes match the framework spike's recorded
`workflow/open-run-simulation/evidence/provenance.json`. All six source files
in that provenance also match this project worktree. The primary remains at
the recorded project commit.

The verified full logs were recovered into this worktree's ignored
`_build_evidence/`. Compact, durable inputs are under
[evidence/open-run-profiles/](evidence/open-run-profiles/): the original JSON
measurement lines, in order and without numeric rewriting, with build chatter
removed. The [verification record](evidence/open-run-profiles/verification.json)
retains both the original-log hashes and the different compact-file hashes.
The compact records retain the project's source attribution and licence.

| Input | Recovered measurement records | Used by the committed profiles |
| --- | ---: | --- |
| Installed half-pin approach | 50 | All, combined with the full-pin envelope |
| Full-pin approach | 50 | All, at matching digit positions |
| Reset cam, both banks | 81 | 21 rising result-bank samples |

`simulation/tools/compile_carry_motion.py` was evaluated without applying its
printed patch. Both the recovered full logs and the compact inputs reproduce
`simulation/carry_profiles.py` **byte for byte**, including its 32 pin knots
and 8 reset knots. No profile regeneration or model edit was needed.

Fresh numeric checks reproduce the historical bounds:

- Maximum pin-envelope compaction error at input samples: **0.000905336 mm**.
- Minimum pin-profile minus measured-drop margin at those samples:
  **0.049365486 mm**.
- Maximum rising-reset compaction error at input samples: **0.000955659 mm**.

These are compression and sampled-offset measurements, not a physical
clearance-error budget. The original `carry_trigger.py` and
`carry_reset_profile.py` probes use Manifold on tessellated fitted parts.
Neither a matching hash nor sub-0.001 mm compression proves continuous exact
contact between samples, and the 0.05 mm profile gauge is not a tolerance
permitting overlap. No new pin/reset CAD probe was run in this recovery pass.

## Fresh carry and initialization checks

Heavy jobs ran sequentially, with an 8 GiB address-space limit, a 300-second
timeout per job, and `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1` and
`MKL_NUM_THREADS=1`. The workspace `.venv/bin/python` and `.venv/bin/solid`
were used with explicit `PYTHONPATH` entries for this project worktree and
the framework worktree above. Import origins were checked before testing.
The faceted test used this worktree's `_build`; the exact test and static
diagnostics used `_build_open_run_evidence`. No primary CAD cache was borrowed.
Environment: Python 3.12.3, Linux x86_64, CadQuery 2.7.0, cadquery-ocp
7.8.1.1.post1, Manifold 3.5.2, trimesh 4.4.9 and molejo 0.2.0. Framework
package metadata still says 0.6.0; the exact imported worktree commit above,
not that metadata alone, identifies the tested motion contract.

| Check | Outcome | Scope |
| --- | --- | --- |
| `solid test --faceted simulation/carry.py` | 12/12 pass; 24.01 s test time, 28.31 s process wall time; 671420 KiB peak RSS | Existing result/counter lever stroke, spring clearance, retention and material checks at tessellation precision |
| `solid test --exact simulation/carry.py` | 12/12 pass; 51.02 s test time, 54.88 s process wall time; 820564 KiB peak RSS | Same existing isolated contracts on exact geometry |
| Static `099`, input 1, crank 0, addition, carriage seated at zero | 12 candidate-pair native Boolean checks; no positive overlap or invalid result; 32.95 s diagnostic wall time | Two result sliders against the selected pins, bearings, bell rigid parts and first three transmission stacks |
| Selected input-group travel at crank phases 0 and 357 degrees | 55 positions at each phase, 0–54 mm in 1 mm increments; no overlap or invalid result; 25.54 s | Fixed home tooth phase, independently translated fitted input group against all five rigid drum bodies; 55 native Booleans at phase 0, disjoint native bounding boxes at phase 357 |

The [exact test output](evidence/open-run-profiles/carry-exact-tests.txt) and
[static setup record](evidence/open-run-profiles/initial-099.json) retain the
results and the latter's complete 27-part selection. Exact bounding boxes
excluded disjoint pairs before the 12 Boolean comparisons. The diagnostic
compared each of the two sliders with every selected non-slider part; it did
not assert that every pair among the 27 bodies is clear.

The `099` pose has **both carry levers preloaded by 1.1630815 mm**, an engagement
fraction of 0.276924167. That is below the candidate 2.562 mm trip threshold.
Initializing the wheel digits with both sliders fully raised is therefore
not the measured setup. The static diagnostic used the existing prescribed
model to pose this initial fixture only; it does not demonstrate persistent
latch state or remove the old arithmetic dependency.

The isolated carry tests sample the entire 4.2 mm stroke at 41 positions for
spring/slider clearance, and selected poses for spring/bearing and retention
checks. They do not sweep the actual two installed result stages past every
guide, cover, neighbour and flexible part while the crank and dial are frozen
at the proposed snap event. No continuous-path certificate, complete setup
validation or new visual inspection is claimed here.

The [selector rest-phase diagnostic](evidence/open-run-profiles/selector-rest-phases.json)
checks the pinion/drum interface without using calculator output or the
prescribed turning law during its travel sweep. It is evidence at two crank
phases and discrete axial samples, not a proof of the intervening angular or
axial intervals, selector guide/knob/shaft clearance, or input ownership.
An initial diagnostic selection incorrectly named the non-rigid drum group
as one solid; its selection assertion failed before any clearance check. The
corrected run explicitly includes both printed halves and all three joining
pins, and refuses a missing selected solid.

The [negative control](evidence/open-run-profiles/selector-negative-control.json)
holds the one-row input pinion at that same home tooth phase while rotating
the drum to crank 120 degrees, inside engagement. The exact Boolean is valid
and reports **2.945019787 mm³** of overlap. Thus the diagnostic detects a
tooth-phase conflict; its clear rest samples are not merely a comparison of
parts that can never meet. No source geometry was mutated for this control.

## Installed trip/reset transitions: native counterexamples

The evidence-only [transition diagnostic](../tools/open_run_transitions.py)
poses the existing prescribed Curta at each candidate event, freezes the
background, and independently moves the selected slider, its coupled sleeve
and its fitted flexible spring. Its public driver changes the slider state;
frame/volume checks first match the standalone station to the installed
station, and a separate guard verifies actual 4.2 mm slider travel. This is
a contact probe, not an implementation of the new running law. Its event
locations use the recovered profiles and candidate detent thresholds; they
are not independently established spring-force equilibria.

The complete physical inventory has **428 bodies: 422 native and six
source-mesh bodies**. Each moving part is checked against all 425 other
bodies, plus the other movers. Native bounding boxes exclude disjoint pairs;
no neighbouring body is excused because it belongs to an omitted subsystem
or would be hidden in a viewer. This is not an all-pairs check of the static
background. The inventory and its SHA-256 are retained in the
[first faceted record](evidence/open-run-transitions/trip1-faceted-9.json);
every native run records the same inventory hash and its full candidate list.

Each run checks **nine discrete poses including both endpoints**. Trip travel
is 2.562–4.2 mm drop; reset travel is 2.35–0 mm. The table reports the largest
observed positive native overlap with `Curta.frame.upper_frame.main_body`:

| Event | Crank angle, degrees | Slider/frame, mm³ | Spring/frame, mm³ |
| --- | ---: | ---: | ---: |
| [First trip](evidence/open-run-transitions/trip1-native-9.json) | 117.060439767 | 0.099225000 at 4.2 mm drop | 0.473787294 at 2.562 mm drop |
| [Second trip](evidence/open-run-transitions/trip2-native-9.json) | 149.935439767 | 0.099225002 at 4.2 mm drop | 0.473787290 at 2.562 mm drop |
| [First reset](evidence/open-run-transitions/reset1-native-9.json) | 355.016337334 | 4.626577659 at zero drop | 0.473748701 at zero drop |
| [Second reset](evidence/open-run-transitions/reset2-native-9.json) | 375.016337334 | 4.626577660 at zero drop | 0.473748698 at zero drop |

All four completed native runs deliberately exit **1**, reporting a failed
clearance check, with no invalid Boolean results. Together they perform 1151
native and 108 source-mesh-interface Booleans; the latter remain faceted even
under `--kernel exact`. Diagnostic wall times are 41.07, 42.04, 44.94 and
43.17 seconds respectively. Jobs ran sequentially with the same environment
and 8 GiB limit as above, but a 600-second timeout per diagnostic. The first
coarse faceted run performs 261 comparisons in 32.32 seconds. Its additional
4.44e-16 mm³ slider/bearing contact is retained in that record; the native
check does not reproduce it. No positive result was suppressed with a volume
epsilon. No other candidate pair is positive at these sampled poses.

These are sufficient counterexamples to the proposed clearance claim. A
denser sweep cannot turn those measured intersections into clearance. Nor
would nine clear samples have certified a continuous transition or all
possible backgrounds, partial pin preloads, setup states or commands.

The earlier green isolated `carry.py` tests do not include the upper frame.
The installed `test_carry_bank.py` cascade tests compare sliders with dial
pins, not the frame or spring/frame interface. These new findings therefore
expose a coverage gap, not a newly introduced production regression. The
previous project resumption report already left frame/carry-guide passages
open; this pass supplies named native counterexamples in the selected slice.

During diagnostic construction, a direct-port prototype was rejected because
reassembling it reused the cached pose. A first Manifold attempt also refused
a directly re-tessellated world BREP. The retained tool uses driver-owned pose
updates and the nodes' public meshes; neither failed attempt supplied a
completed clearance result. Lightweight guards pass for all four profile
crossings, boundary-preserving box filtering and refusal of a missing crossing.

The [localization record](evidence/open-run-transitions/frame-contact-localization.json)
adds 20 native slider/frame and spring/frame comparisons: both stations at
zero drop, the initial `099` preload, trip onset, full drop and reset onset.
All results are valid. The springs intersect the frame at all five selected
poses, including **0.473384639 / 0.473384637 mm³ at the initial `099` preload**.
The two sliders clear the frame at that preload, trip onset and reset onset,
but not at the raised/lowered endpoints above. Thus the starting `099`
snapshot is not fully clearance-valid with the current fitted springs;
the earlier selected slider-pair pass must not be presented as full setup
acceptance.

[Native section views](../../_build_evidence/open-run-frame-sections.png)
were generated and inspected. They show the spring penetrating the frame
near its lower leg/fold region, a 0.075 mm-wide lowered-slider intersection,
and a wider shoulder intersection in the raised pose. Red outlines are
measured Boolean intersections, not proposed material removals. The image
is an ignored generated artifact, hashed in the
[manifest](evidence/open-run-transitions/manifest.json); the evidence-only
[section tool](../tools/open_run_contact_sections.py) regenerates it with
`python -m simulation.tools.open_run_contact_sections` in the same environment.
Its exit zero means reporting and image generation completed, not that
clearance passed.

Reproduce a transition from this project worktree, using `trip1`, `trip2`,
`reset1` or `reset2` as the event:

```bash
ulimit -v 8388608
PYTHONPATH="$PWD:/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation" \
SOLID_BUILD_DIR=_build_open_run_evidence OPENBLAS_NUM_THREADS=1 \
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 timeout 600 \
/home/asa/devel/libresolid-studio/.venv/bin/python \
  -m simulation.tools.open_run_transitions --event trip1 --samples 9 --kernel exact
```

The numeric records, diagnostic source hashes and execution metadata belong
to [evidence/open-run-transitions/](evidence/open-run-transitions/). No source
STEP/STL, production model, profile, compiler or viewer code was changed.

## Reproducing the compact-input check

From this project worktree, use the workspace Python. This calls the existing
compiler with the durable record directory and compares its printed patch's
file content; it does not apply a patch or alter the model:

```python
import contextlib, importlib.util, io, json
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'compiler', 'simulation/tools/compile_carry_motion.py')
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)
data = Path('simulation/docs/evidence/open-run-profiles')
compiler.records = lambda name: [
    json.loads(line) for line in (data / name).read_text().splitlines()]
output = io.StringIO()
with contextlib.redirect_stdout(output):
    compiler.emit()
generated = '\n'.join(line[1:] for line in output.getvalue().splitlines()
                      if line.startswith('+')) + '\n'
assert generated == Path('simulation/carry_profiles.py').read_text()
```

## Remaining evidence and next action

1. **Resolve the installed frame-contact finding first.** The subsequent
   source check and proposed remedy are recorded in the 2026-09-13 follow-up
   below. Review and ratify the bounded, project-owned frame-fit proposal
   before changing geometry. Preserve the native failures as named regression
   checks; do not omit the frame or change the runtime law to hide contacts.
   A different spring mounting, guide or slider correction would require a
   revised decision. After an authorized correction, recheck the complete transition and
   relevant preloads, then finish the subassembly boundary inventory. The
   current discrete counterexamples close no continuous-clearance obligation.
2. **Home window and full input travel.** Establish the interval from fitted
   geometry, including the selected pinion, selector guide/knob/shaft path
   and neighbouring bodies. `zero.py`'s follower table has a zero-departure
   segment at crank phases 357–360 degrees, but a cam table alone does not
   prove selector admission. The new 110-position pinion/drum diagnostic
   supports the candidate rest phases, but does not close the intervals or
   other interfaces. Existing selector tests measure integer digit placements;
   they do not prove between-detent clearance or an interlock.
3. **Complete setup and outgoing boundary.** Finish the `099` snapshot's
   coordinate/frame and local-memory inventory, retain the measured preload,
   and locate the hundreds wheel's outgoing pin/contact boundary. This
   pass's selected-pair check does not certify the remaining interfaces.

These are evidence obligations under the already ratified scope, not another
request to choose the scope. If a measurement contradicts that scope or
requires a different fidelity, return the concrete finding to the pilot.
After this gate closes, prepare the three coherent repository-owned OpenSpec
proposals, preserving Curta's unfinished `simulate-the-curta` record. No new
cycle was opened during the 2026-09-12 measurement pass, no existing task
checked off, and no production code changed.

## 2026-09-13 follow-up: source check and correction proposal

Manual pages 30–31 were read and visually inspected, confirming the installed
spring/support topology, fork/flange placement and free-snap/reset requirement.
The figures do not supply final pocket dimensions or prove spring forces.
The evidence-only [source comparison tool](../tools/open_run_frame_sources.py)
tests the first station at four drops using both original and fitted moving
parts against the native frame and the supplied frame STL. All 16 native and
16 Manifold results are valid; the
[record](evidence/open-run-transitions/frame-source-comparison.json) includes
source/tool hashes, the unchanged project/framework revisions and execution
metadata. It ran sequentially under the same 8 GiB/thread guard with a
300-second timeout. Its successful exit means reporting completed, not that
the contacts passed.

The original static STEP spring already overlaps the native frame by
0.510484 mm³. Original and fitted sliders reproduce the same endpoint
contacts. The supplied `main body.stl` is watertight and consistently wound,
but also reproduces those contacts in its supplied coordinates: about
4.640764 mm³ raised and 0.099226 mm³ lowered; fitted spring contacts are about
0.466 mm³. Thus neither restoring the original spring nor swapping the frame
to the print mesh cures this local obstruction. No automatic alignment,
hole repair, source mutation or claim of complete STEP/STL equivalence was
made; default duplicate-vertex processing on STL load is recorded explicitly.

The Curta-owned
[clear-result-carry-frame-contacts proposal](../../openspec/changes/clear-result-carry-frame-contacts/proposal.md)
now has proposal, design, delta spec and tasks, all passing strict OpenSpec
validation. It recommends bounded stationary frame reliefs at the two
selected stations, preserving the current spring, guides, moving parts and
motion profiles. A proposed 0.05 mm running gap must fit within independently
measured passage limits and avoid protected seats/fasteners; a conflict or an
unbounded path returns to the pilot rather than changing the repair silently.
The raw sources and production model are unchanged. The original change is
still active at 7/17 tasks and passes strict validation unchanged.

The pilot ratified this frame-only prerequisite on 2026-09-13 ("ratify,
go on"), including the stop conditions; the running cycles remain unratified.
The planning commit is `7d39306`. The new independent frame bench produces
six native red tests with three placement/travel/validity guards passing.
Subsequent native support mapping found that both slider endpoint gaps reach
the protected guide/frame seating land at each station. Work paused under the
ratified stop condition; see the [gate report](carry-frame-gate-2026-09-13.md).
The pilot approved the bounded seat-edge exception, committed as `9c58255`.
The two-station frame fit is now verified: all 17 new contracts pass both
runners, as do full-stroke frame enclosures, four installed transition sweeps,
dimensional/protected-feature measurements and twelve negative controls.
The complete regression is 159/161 faceted and 160/161 native, with only the
named pre-existing failures; native sections and OpenSCAD assembled views were
inspected. See the [completion record](carry-frame-validation-2026-09-13.md).
This local correction is only one prerequisite for the later running
proposals. The pilot requires an explicit go-ahead once
the evidence is ready, before actual solid-node feature implementation.
