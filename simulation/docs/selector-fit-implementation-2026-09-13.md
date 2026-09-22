# Selected-input fit: implementation evidence

Ratified planning commit: `aec7ca4877c58820c6c02a32c44d8c6c206c9e9b`.
Ratified alignment revision: `da432fbdc7fe0e7f89e308237f281e9c3d368754`,
2026-09-13 ("ratify, go o"). Its separate planning commit preserves the
original plan and leaves the red evidence/probes with implementation work.
Change: `fit-selected-input-selector`, Curta `open-run-simulation` worktree.
This record is implementation evidence, not a completed fit or running feature.
No operating geometry has been changed at the red baseline below.

**Current disposition:** paused at the pilot's request to steer project
direction. See the [checkpoint handoff](open-run-handoff-2026-09-13.md).
Sections 1–4 retain the earlier measurement chronology; §§5–7 record the
ratified revision's later evidence and final 2/22-task state. This checkpoint
commits diagnostic work without completing or archiving the change.

## 1. Independent native red baseline

`SelectorFitBench` binds the source selected selector and keyed input group to
an independent fractional setting, with the original housing fixed. Its two
keyed shaft rotations are 652° (initial) and 4° (post-cascade), independent of
the root operand law. Twenty named contracts ran; **3 passed, 17 failed**.

Passing guards: valid connected native source parts; full 54 mm knob/keyed
travel with fixed housing; independent placement agreement with both complete
frozen source fixtures at all ten digits and settings 0.5, 4.5 and 8.5.
This last contract also compared the full 428-body inventory and every retained
state field against the committed pre-fit evidence on each fixture. It did not
discard any installed body or reconstruct the root operand during travel.

Each row below failed separately in **both** fixtures. These are exact-kernel
positive intersection volumes, not an allowance table.

| Interface | Setting | Native intersection (mm³) |
| --- | ---: | ---: |
| Ball / knob guide | 0 | 1.1953876585803762 |
| Ball / shaft, seated | 0 | 0.3878557919231307 |
| Ball / shaft, between detents | 0.5 | 2.866621265898005 |
| Spring / ball | 0 | 3.4991802113553003 |
| Spring / knob back seat | 0 | 2.661638394442298 |
| Screw follower / shaft | 0.5 | 0.0005264794076108581 |
| Knob / housing slot | 5 | 9.253229593654433 |
| Number roll / housing | 0 | 4.169640237750814 |

The seventeenth failure is the ball diameter: 5.4 mm measured, 5.0 mm required.
The two conditional fixed-joint candidates were not waived by these tests;
their separate classification was then open (subsequently completed in §5).

Command, from the Curta worktree (stderr and stdout captured together):

```bash
ulimit -v 8388608
PYTHONPATH="$PWD:/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation" \
SOLID_BUILD_DIR=_build_open_run_evidence \
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
/usr/bin/time -f 'RESOURCE wall=%e rss_kib=%M exit=%x' \
timeout --kill-after=10 600 /home/asa/devel/libresolid-studio/.venv/bin/solid \
test --exact simulation/selector_fit.py:SelectorFitBench
```

Retained log: `_build_evidence/selector-fit-red.log`, SHA-256
`86bd403bb5bed56b2de6f9a7c7d82aa9749525437e81c405633148aa6260bd8d`.
Runner time 47.50 s; process wall time 53.94 s; peak RSS 611792 KiB; exit 1
(expected red). An earlier uncaptured run produced the same 20/3/17 result,
44.17 s wall and 608108 KiB peak RSS.

### Frozen fixtures and provenance

The complete inventory and exact driver/shaft/dial/carry values remain in
[`evidence/open-run-selector-2026-09-13.json`](evidence/open-run-selector-2026-09-13.json),
`physical_inventory` and `runs[0:2].frozen_state`, file SHA-256
`eea2287ed271fb6d9a8870e20d70bad10927ccfe554c42c19be4e3aff7676dba`.
Both inventories hash to
`af09629ffdd781d4b798e8a0edc400c149d3fbc43139dfab99ccbb3044eac6cb`:
428 physical bodies, 422 native and six explicitly named source-mesh bodies.
Initial result is 99 with carry fractions
`[0.27692416666666614, 0.27692416666666614]`; post-cascade result is 100 with
`[0, 1]`. The independent bench leaves all their recorded fields unchanged.

All 191 prior simulation source hashes in
[`evidence/carry-frame-regression-2026-09-13.json`](evidence/carry-frame-regression-2026-09-13.json)
were rechecked successfully with `sha256sum --check --quiet`. That record's
SHA-256 is `b6a28d9c768f5af7f1414c02a6b9ce14434302d15b380574c829f3386ea4e0fb`.
The three later selector-diagnostic source hashes are unchanged:

| Source | SHA-256 |
| --- | --- |
| `simulation/tools/open_run_selector.py` | `8fa1bce531c22c2ecbd7de7469e59308856072689fec662127e478be49d45c64` |
| `simulation/tools/open_run_selector_sections.py` | `6cbe70cf7d6fcd8fc0363cb6e18b9ef8617a7fdca526f916e3aa907152156013` |
| `simulation/test_open_run_selector.py` | `e4d44e328a63511767024b274c5fee030428238176cdafdffa169ff41970eed0` |
| New independent `simulation/selector_fit.py` | `b21013dbf1dda11f25712fe219a7b4323d57c44d0a2d7801d5720fa0f30495bc` |
| New red `simulation/test_selector_fit.py` | `1e8e57210eecdb2caca77874aa57f6133a40d43e479bceb5d77cbababb8c1d58` |

Framework import: the paired `solid-node/WTs/open-run-simulation` checkout at
`6e41f2da132a8604f9b68895967247fb8876fc4d`, with only pre-existing workflow
document changes, no framework source modifications. Original STEP SHA-256:
`943ec7545d9cbcbe69266f0e8b1b65e912f80fa46cad0c974dea164bdcbbbee3`.
Manual SHA-256: `af2a7e512063ec485ae992bbf490f5f1e14aac5dc35277183603ff725fb2ab7c`.

## 2. Native source measurements before fitting

Retained machine-readable evidence:
[`evidence/selector-fit-measurements-2026-09-13.json`](evidence/selector-fit-measurements-2026-09-13.json).
It contains native source surface identities, 115 radial support measurements,
the indexing witnesses below, all current diagnostic/test source checksums,
raw log/image hashes and resource use. It references the full frozen inventory
and the unchanged 191-source frame baseline rather than copying them.

| Interface | Source measurement in setting-zero world coordinates |
| --- | --- |
| Ball/spring guide | Radius 2.6185 mm, axis along X at Y=0, Z=−55.785999642 mm; native knob cylindrical faces 27 and 28 |
| Spring back seat | Plane X=72.6000000002046 mm, disk radius 2.6185 mm; native knob face 29 |
| Spring | Wire diameter 0.51 mm, centerline radius 2.295 mm, outside diameter 5.10 mm, 6½ turns, plain circular cut ends |
| Source spring axial position | End center X=63.0 and 74.1 mm, 11.1 mm axial centerline span; rear extent 74.355 mm, 1.755 mm beyond the back-seat plane |
| Spring hand/pitch witness | +6.5 turns in increasing X using angle `atan2(Z−guide_Z, Y)`; sampled pitch 1.707713794 mm, maximum linear-phase residual 0.009704294 rad |
| Detent cone at digit zero | 55° semi-angle, source axis `(0.9970527522, 0.0767190281, 0)`, center height −54.695 mm; corresponding cones repeat 6 mm / 36° |
| Screw follower | Non-threaded 1.2 mm radius cylindrical tip from X=54.3 to 55.5 mm, rounded end to X=56.1 mm; thread-sized body/lead is behind X=54.3 mm |
| Screw/knob source joint | One native intersection region, 13.141988148136306 mm³, X=49.5…54.236126830457046 mm; does not reach the follower tip beginning at 54.3 mm |
| Bottom/top shaft source joint | Two native intersection regions totaling 0.5336797772072533 mm³, Z=−43.2…−43.175 mm |
| Housing selector slot | Source walls Y=−3.154158051 and +4.645841949 mm; knob handle walls are Y=±3.3 mm |
| Housing number window | Source radius 9.9 mm at `(58.294099644, 0.745841949, Z)`; number roll radius 9.3 mm at `(58.5, 0, Z)` |

The spring's winding/hand comes from sampling its actual native seam, not a
volume guess. The phase residual means that a constant-pitch analytic helix
has **not** been proved equivalent to the complete source end/coil geometry.
No installed spring was authored. At this measurement stage the two fixed-joint
regions were candidates only: canonical-pose/region invariance and inventory
mutations were unfinished. Their subsequent classification is recorded in §5.

The measurement scripts were run sequentially under the same 8 GiB / one
numerical thread / 600 s guards as §1, using the workspace Python and paired
framework PYTHONPATH. Substitute `python -m <module>` for the `solid test`
command in §1:

| Module | Wall time | Peak RSS | Exit |
| --- | ---: | ---: | ---: |
| `simulation.tools.selector_fit_measurements` (final surface record) | 28.66 s | 609600 KiB | 0 |
| `simulation.tools.selector_fit_contacts` | 462.73 s | 610296 KiB | 0 |
| `simulation.tools.selector_fit_indexing` | 47.56 s | 586468 KiB | 0 |

The first surface-only exploratory run took 24.34 s / 610448 KiB; the final
record above also retains the analytic cone axes, apexes and angles.
These are localized measurements, not complete stroke or support certificates.

## 3. Design conflict: numbered coordinates are not the source guide's seats

**Historical pause during task 1.2, before a production cut.** The nominal 5 mm ball
can be radially placed without penetrating either the shaft or the source
knob, but at the required numbered setting it rests on a cone flank, not at
a local minimum of required spring compression along the existing selector
path. Holding that pose numerically is not the ratified detent settlement.

A native minimum-distance bracket for a 2.5 mm radius sphere, on the actual
source guide, gives:

| Source setting | Required ball-center X (mm, upper end of <10⁻⁸ mm bracket) | Native ball/shaft and ball/knob overlap |
| --- | ---: | --- |
| 0.975 | 63.549707474187024 | Both zero |
| **1.000** | **63.675127589330074** | Both zero |
| 1.025 | 63.80383151695132 | Both zero |

Moving the knob only 0.15 mm toward the preceding digit permits the ball to
move inward by at least **0.125420108 mm**, reducing required compression for
the fixed-back-seat radial spring arrangement. The 0.025-setting sampled
trace has its trough at **0.825**, around 1.05 mm of knob travel before the
numbered one. That is an approximate trough, not a certified exact minimum
or a force/friction prediction. The same downward witness repeats for all
ten source-numbered positions; the below-zero witness is explicitly an
extrapolation, while all nine other witnesses lie inside the approved stroke.
The in-range setting-one witness alone is sufficient to reject the seating
assumption. None of the 115 samples certifies unsampled full travel.

Independent acceptance contract
`SelectedInputFitTest.test_numbered_one_is_retained_by_ball_detent` reproduces
the failure using the actual bench occurrence placements and fresh native
distance queries, not the saved trace. The final native run has **21 tests:
3 passed, 18 failed** (the previous 17 plus this indexing contract), 51.25 s
runner time / 56.29 s process wall / 615104 KiB peak RSS, exit 1 expected.
Log: `_build_evidence/selector-fit-index-red.log`, SHA-256
`bed962abe01e8d897da4f07c0ed7b2fc3f3a121e5473eaad6604e527ea01f05b`.
The updated test source SHA-256 is
`2c871504505c826203ecb745a34be6777f42731b52c153c5da584d91d1a384f5`;
§1 retains the earlier 20-test source fingerprint as historical red evidence.

### Read-only alternative and the decision boundary

The guide center is **1.090999642 mm below** the source cone's center height.
The unmodified guide offers only **0.1185 mm** radial center play to a 5 mm
ball. An independent cone-centered sphere is obtained from the native apex
plus `axis × (2.5 / sin(55°))`, giving center
`(62.834124973067105, 0.3334927414534689, −54.695)` mm at digit zero.
It has zero native intersection with the unmodified shaft, but intersects
the unmodified knob by **9.389392719858634 mm³**. It is an uninstalled witness,
not a replacement part or a selected final guide dimension.

This points to correcting the **selected ball/spring guide alignment while
preserving the shaft, fork, keyed group and numbered coordinates**. That is
the recommended next design step, not permission already inferred from the
ball-diameter decision. A matching straight guide and spring back seat would
explicitly reopen the protected back-seat/alignment decision. Its remaining
walls, support and guide play must be proved before adopting dimensions; for
example, merely shifting the present-radius bore upward to the cone height
would leave only about 0.3515 mm to the source top plane locally. This is not
a qualified manufacturing land or an accepted correction.

Keeping the old back seat with an offset/bent spring and a relieved guide is
not proved impossible by these measurements. It would need a separately
justified ball-guidance, spring-seat and working-play path; a wider void plus
an arbitrarily prescribed ball trajectory is not such proof. No such
alignment/fidelity substitution has been silently adopted. Re-phasing only
the *between*-detent interpolation likewise does not recenter the existing
guide and cone at the protected numbered endpoints. The measured conflict
must be resolved explicitly rather than relabeling a held flank pose as a seat
or changing the numbered stroke without approval.

Actual native image inspected:
`_build_evidence/selector-fit-indexing.png`, SHA-256
`3291781687e0df85ec8ddfa877bf63d4175d215976e22ae7918e72790fab6ea9`.
It shows the sampled contact curve, source-guide flank contact, and the
uninstalled cone-centered ball's guide interference. No OpenSCAD publication
or operating geometry was changed for this native-section diagnostic.

## 4. Preservation checks and remaining work

- The 16 existing lightweight Python tests pass (`simulation.test_open_run_selector`,
  `simulation.test_arithmetic`, `simulation.test_cycle`; 0.033 s).
- All five `node --test simulation/viewer/calculator.test.mjs` tests pass.
- The existing full-root viewer document remains byte-for-byte unchanged:
  SHA-256 `6e8b0eb44a3ba79475767e56597a77a2b3b4641789b7aa4cd27f2d78820ddee2`,
  schema 4, 9969 bindings, eight drivers, seven instructions. Inspection-only
  CAD publication did not replace it.
- No production simulation source, raw import, upstream STEP/manual, non-selected
  occurrence, completed carry/frame fit, framework or viewer feature code was
  changed. The full 39-module regression is not rerun for this paused pre-cut
  diagnostic pass; its 191-source content baseline remains verified unchanged.
- At the original pause task 1.1 was complete; the remaining 21 tasks were open. No production fit,
  continuous-travel certificate or completed fixed-seat inventory is claimed.
  No completed implementation commit or archive was created at that pause.
  The later ratification and pilot-requested diagnostic checkpoint are recorded
  below. The original `simulate-the-curta` remains independently active.

The subsequent ratified revision and resumed measurements are recorded below.
The later home-window/setup/outgoing-boundary evidence and explicit
**ask before solid-node feature development** gate remain unchanged.

## 5. Ratified alignment: pre-reconstruction gates

Revision `da432fb` is planning-only, strictly validated (three records passed,
none failed), and follows rather than amends `aec7ca4`. Operating wiring and
geometry remain unchanged. Read-only measurements resumed under the revised
source-parallel guide/local restoration permission.

Retained native measurements:
[`selector-fit-alignment-gates-2026-09-13.json`](evidence/selector-fit-alignment-gates-2026-09-13.json).
The new probe identifies the ten **radial** pocket cones separately from two
axial shaft-tip chamfers. All ten source cone-centered 5 mm balls agree with
the unchanged numbered 6 mm / 36° coordinates: maximum alignment error
2.06×10⁻¹⁴ mm, native ball/shaft intersection zero at every seat. This verifies
the candidate endpoint alignment, not the intervening path or working-play
retention.

### Local support feasibility before a reconstructed part

The native old outboard guide and shaft-clearance surfaces define the permitted
restoration region: old outboard cylindrical cavity, excluding the main shaft
void and existing material. It is not a box around the knob. Its full eligible
volume is 226.756535857 mm³; that is an allowance-region measure, **not a claim
that all of it will be filled**. The shifted candidate cylinder intersects
63.292385753 mm³ of existing source material, including 6.699740463 mm² of the
source shaft-support face at its localized new mouth. The remaining original
support face has area 548.202782773 mm². Area alone is not the preservation guard;
the complete protected surface still needs a source-difference contract.

Independent complete support witnesses were checked without constructing a
fitted knob:

| Witness | Native result |
| --- | --- |
| 0.34 mm annular guide wall, X=62.3235…72.6 mm | All missing source material lies inside the permitted old-cavity restoration region; missing outside it is exactly zero |
| Full back-seat disk plus the annular land, X=72.6…74.99 mm | Already wholly inside the unchanged source body; missing material exactly zero |
| Deliberately excessive 0.35 mm wall at X=64…72.6 mm | Fails: 0.002485155 mm³ lies outside source and permitted restoration |

Actual nearest outer-face distances are **0.3515 mm above**, **0.348007259 mm
on the positive-Y side**, and 1.014992741 mm on the negative-Y side. Relative
to the old guide, the top wall thins by 1.090999642 mm and the positive-Y wall
by 0.333492741 mm. The proposed 0.34 mm witness is a geometric continuous-shell
bound, with the thinner side explicitly accounted for; it is **not a minimum
printable wall, strength rating, or complete ball/spring support certificate**.
The localized shaft mouth, full working play and actual installed contact
footprints remain separate gates before production reconstruction.

The new native sections were actually inspected:
`_build_evidence/selector-fit-alignment.png`. They show the old cavity,
candidate relocated guide, continuous annular witness and retained back-seat
block in transverse and longitudinal sections. No viewer/OpenSCAD publication
was replaced.

### Source spring ends

The seam is the +X pole of the circular wire section, **0.255 mm from its
centerline**, not the centerline itself. After accounting for that offset,
the 1301 native samples depart from a constant-pitch helix by up to
0.002573173 mm axially. The discrepancy repeats along the winding; it is not
evidence of flattened end coils. The planar end-cap normals are parallel to
Y, whereas the seam tangent has a nonzero X component at both ends. Retain
that oblique plain-cut source-end detail when establishing the installed
representation; a circular normal sweep is not automatically identical.
The full sampled trace and endpoint tangents are retained. No spring has been
authored and no sample residual is claimed as a global approximation bound.

### Two fixed-source joints classified

Task **1.3 is complete for the current source-backed bench**. The independent
reference is a fresh unmodified `DigitSelectorAxle1`, not the operating fit
or a maximum-volume table. Exact canonical intersection differences in both
directions are zero. The registered regions are:

- screw/knob: 13.141988148136306 mm³, one region, ending at X=54.2361268305 mm
  before the non-threaded follower beginning at X=54.3 mm; manual page 32's M4
  tap/die joint;
- bottom/top shaft: 0.5336797772072533 mm³, two regions over the unchanged
  0.025 mm axial source engagement.

Their complete occurrence names, relative matrices and intersection bounds
are retained. Four 37-position runs (both directions in both frozen homes)
have maximum relative-matrix roundoff 1.42×10⁻¹⁴. Constant relative placement
between samples follows from the common knob translation and the shafts'
same-axis equal rotation: the shared transform cancels algebraically.
This argument names and fingerprints the current relation declarations; it
does not infer continuity from the sample grid.

Nine negative controls are rejected: missing joint, added moving-contact entry,
swapped regions, equal-volume displaced thread region, altered shaft-join
region, changed relative pose of either joint, physically shifted screw, and
physically shifted top shaft. The unmutated regions pass again afterward.
Every later fit must preserve these exact regions and poses. No moving ball,
spring, screw/groove, gear/fork or housing contact is exempted, and the old
whole-machine findings remain unchanged.

Commands use the resource guard and environment in §1, substituting
`python -m simulation.tools.selector_fit_alignment` or
`python -m simulation.tools.selector_fit_fixed_seats`.
Successful runs: alignment 39.92 s / 563968 KiB; fixed seats 35.94 s /
569668 KiB, both exit 0. Two probe-development errors (empty boolean operand
and axial chamfers initially included as pockets) are retained in the JSON;
neither was resolved by accepting penetration or changing source geometry.

Progress after these gates: **2/22 tasks complete** (1.1 and 1.3). Further
in-scope measurements followed as recorded below, but the later pilot pause
supersedes the instruction to continue automatically.

## 6. Last working-play and spring measurements before the pause

Complete numerical results, raw file/log hashes, commands and resource use
are retained in
[`selector-fit-handoff-2026-09-13.json`](evidence/selector-fit-handoff-2026-09-13.json).
These probes change no operating geometry. Their successful process exit
means the measurement finished, not that its mechanical queries all passed.

### Screw/groove and fork capture

The capture probe evaluated twelve selector settings with five shaft-phase
perturbations each: **60 queries, 23 valid zero-overlap, 31 valid positive-overlap,
six invalid native booleans**. Refusals occur at setting 0.625 / phase delta
−0.05°, and setting 0.75 / every sampled phase delta (−1°, −0.05°, 0°, +0.05°,
+1°). Their reported signed volumes are retained only as invalid-result
diagnostics, not reliable overlap measures or accepted contact.

The first probe stopped on the first invalid boolean (100.66 s wall,
464736 KiB, exit 1). The revised diagnostic preserves explicit
`kernel_refusal` rows and continues gathering evidence; it does not replace
them with zeros. The completed run took 215.05 s / 631984 KiB, exit 0.
At setting 0.5 the unchanged source phase has positive overlap
0.0005264794123 mm³; a −1° perturbation has zero overlap. This localizes a
phase/profile issue without establishing a valid replacement follower path.

Twenty-two gear/fork perturbations cover both frozen fixture rotations.
Source geometry has approximately 0.439 mm axial room toward the upper fork
face: knob face Z=−62.98599974966 mm, gear top Z=−63.42499975 mm. A −0.025 mm
shift produces about 0.26997 mm³ overlap; +0.2 mm is clear and +0.5 mm produces
about 0.658728 mm³ in both fixtures. These are localized opposing-contact
witnesses, not continuous capture or a permitted gear-placement adjustment.

### Ball support under sampled guide play

The candidate guide was measured at 31 settings, producing **75 native
distance brackets**: centred samples throughout the first pitch and nearby
endpoints, plus four cardinal lateral offsets at eleven settings. The
nominal radial play is 0.1185 mm. The centred setting-zero/one ball-center X
brackets end at 62.83412497565 mm; at setting 0.5 the centred value is
64.68652792424 mm, and the largest sampled cardinal value is 64.69109584391 mm.

Near numbered one, centred setting 0.975 requires X=62.9483390983 mm and
setting 1.025 requires X=62.9539959267 mm. Cardinal samples at the nominal
seats also require more outward displacement than the cone-centred position.
That supports investigating retention, but **does not prove it**: the full
play disk is not covered, source linear shaft phase is not a fitted follower
law, and spring-end contact/compression remains unmodelled. Below-zero samples
are explicitly diagnostic extrapolation, not admitted travel. No entire-stroke
or coupled retention-basin certificate is inferred from this grid.
Run: 422.51 s / 631312 KiB, exit 0.

### Analytic spring comparison

An uninstalled Molejo `Circle(0.255)` / `Helix(radius=2.295, turns=6.5,
height=11.1)` was aligned to the source hand and end centres. The end-centre
disagreement is at most 1.44×10⁻⁹ mm. The source caps are parallel to Y,
while the analytic cap normals have X components of approximately ±0.117604,
an end-plane tilt of **about 6.75°**. Source volume is 19.24933413953 mm³;
the analytic comparison is 19.28107740785 mm³.

The analytic BRep's declared 10⁻⁶ mm approximation tolerance is not permission
to ignore this source end-form difference. Matching dimensions and centres
does not establish equivalence. No installed spring, supported end treatment,
compression law or force/strength result is delivered. Run: 39.64 s /
447716 KiB, exit 0. This remains an unresolved representation/seating gate,
not a demonstrated need to change spring hardware or framework code.

## 7. Checkpoint verification and disposition

The last native run of the §1 command now has **23 tests: 4 passed, 19 failed**.
The four passing guards are connected source parts, full stroke/fixed housing,
independent agreement with both complete frozen fixtures, and exact fixed-joint
regions/relative poses. The new continuous-wall contract fails with
**23.60698934166411 mm³** missing from the unchanged source knob; the previous
18 red failures remain. The red suite intentionally exposes the unfitted
source. No failure is suppressed or converted into a passing fit.

Runner time: 75.80 s; wall: 82.95 s; peak RSS: 614692 KiB; exit 1.
Log: `_build_evidence/selector-fit-alignment-red.log`, SHA-256
`300c6debb014c9b0dc1dfb902d1cd3305021a0db64c755a59ad4b0badb3e0815`.
Test source SHA-256:
`3360781f5f4166b67249d37440dd3bd4a9eb2e83522aebea4255d9921c940def`.
The checkpoint JSON retains all test results and assertion traces, removing
only generation chatter. Earlier source hashes in §§1 and 3 remain historical.

For the pilot-requested closeout, all 16 lightweight Python tests passed
again (0.035 s) and all five calculator JavaScript tests passed
(79.840409 ms). The 191-source carry/frame baseline and fixed-seat source
fingerprints were rechecked successfully. The full-root viewer document
retains the §4 hash. No heavy CAD tests, geometry probes, full regression,
builds or snapshots were rerun for documentation closeout.
Strict OpenSpec validation passes all three records; all nine diagnostic/test
Python files compile. These are checkpoint hygiene checks, not mechanical
acceptance.

The checkpoint commits the existing diagnostic code and retained evidence,
not operating fits. Tasks remain **2/22 complete**; tasks 1.2, 1.4 and 1.5
have partial evidence only, and tasks 2–4 remain unfinished. Neither this
handoff nor the lightweight checks complete the final fitted-part acceptance
tasks. The original simulation remains 7/17, independently open.
No delta specs are synchronized, no incomplete change is archived, and no
integration, push, publication or worktree cleanup is performed.

Await the pilot's project direction. Ratified decisions and source-protection
constraints remain available for any later resumption or explicit revision;
this checkpoint chooses neither. Actual solid-node feature development still
requires the pilot's separate go-ahead.
