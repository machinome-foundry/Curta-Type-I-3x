# Geometric reverser profile covers — investigation, not adoption

The [wrong-order finding](reverser-wrong-order-2026-09-23.md) remains red in
the production root. Finite angle surveys and failed interpolation do not
prove a restraint between samples. This investigation instead asks whether
explicit outward covers of the source extruded profiles can select the
absolute axial stopping planes already demonstrated by
`LocalReverserContactTrial`. It does not change source prints, fitted parts,
operating laws, controls, or task checkboxes.

## Instrument and source checks

`simulation.tools.reverser_profile_cover` inspects native planar faces,
offsets their outer wires by a named **.005 mm cover allowance**, tessellates
the candidate, and merges adjacent triangles only when the result remains
convex. Orientation is exact for the supplied finite binary coordinates;
there is no concavity epsilon. Holes are deliberately covered, not filled in
the actual part. The offset distance is not a maximum Hausdorff-error claim:
an intersection join can extend farther at a corner.

The reconstructed polygon is extruded across the source height plus the
named axial allowance. The source's native difference from that cover must
be valid with exactly zero volume. Positive, negative and nonfinite results
are refused. Tessellation settings alone are never a containment certificate.
No symmetry between the five pinion sectors is assumed.

The source outer wires consist of lines and circular arcs: the fitted pinion
has 20 edges (10 of each), the one-tooth drum segment 19, and the nine-tooth
segment 56. At linear deflection .0001 and angular deflection .025, both
round-join and intersection-join candidates contain all four native profiles:

| Profile | Round-join vertices | Intersection-join vertices | Convex pieces |
| --- | ---: | ---: | ---: |
| Ones fitted pinion, .36 relief | 1700 | 905 | 591 |
| Higher fitted pinion, .42 relief | 1695 | 900 | 591 |
| One-tooth drum segment | 1470 | 446 | 261 |
| Nine-tooth drum segment | 3692 | 1274 | 1072 |

All eight native remainders are valid and zero. Both four-row commands
terminated with exit 0. A separately tried coarser round-join candidate
(.001/.1) contains both pinions but **fails** the one-tooth drum check with
0.21325672929384742 mm³ outside; its two-row prefix is incomplete evidence.
It is not adopted, coarsened again until green, or accepted with a volume
threshold.

Evidence files under `_build_checks/`, generated from project `4035917` plus
the instrument introduced with this record:

- `reverser-native-profile-cover-4035917.jsonl`: SHA-256
  `6bbbf48a2e07f5127640e7da3334ba3c4d59b9d103cd52296b27646c089fe544`.
- `reverser-native-profile-cover-intersection-4035917.jsonl`: SHA-256
  `f81c846514f0432cacf9cfcf0158c344dc0dabe6091173d073d5d82cd7182c5e`.
- Rejected `reverser-native-profile-cover-coarse-4035917.jsonl`: SHA-256
  `2f90c45264f1fe208d988d43c1c4f42f94ea4a3f57e275880891f4cf3fbade55`.

The framework bench is `machinome/WTs/curta-reverser-profile-validation`,
opened by `scripts/dev-env` at `b2bfa1fd33be3b615d6c15e9171de2913c3d6cb1`.
That head adds review notes only to verified `26cbd63`. The older completed
input-preservation worktree was removed by concurrent cleanup; this new
validation bench is clean and contains no framework implementation edits.

From the project root, reproduce into a **new** output path:

```sh
PYTHONPATH=/home/asa/devel/machinome-studio/machinome/WTs/curta-reverser-profile-validation:. /home/asa/devel/machinome-studio/.venv/bin/python -m simulation.tools.reverser_profile_cover --join intersection --output _build_checks/reverser-profile-cover-new-run.jsonl
```

The initial instrument and subsequent numeric overlap/mesh helpers have
test-first missing-implementation failures. The separate missing-profile
regression fails because an empty profile is initially called clear; the
corrected helper refuses it. Eight focused tests cover convex merging,
preservation of a concave notch, invalid input, edge separation rather than
only bounding boxes, touching covers, missing data, and shared-index mesh
topology and exact mesh-face projections. Together with the existing phase,
reader, compiler and resume guards, **32 tests pass in 0.004 s** (exit 0).
These small tests do not certify the operating machine.

## Eight isolated placement witnesses

The intersection-join covers are rigidly placed without copying angular
sectors. The pinion uses the ones axis (−26.032898192, 31.024799946) and the
requested shaft angle. The drum segment uses its source 2.604082802° clocking
and (−.016356142, .223394941) offset, both rotated by the negative crank
angle. Both source profiles occupy their own 1.5 mm Z interval for this
isolated test; these volumes are **not** whole-print retained-root volumes.

The numeric cover helper uses AABB rejection and polygon separating axes,
including touching covers in its contact verdict. Fresh native source commons
are valid at all eight queries:

| Crank / shaft (degrees) | One-tooth native mm³ / cover | Nine-tooth native mm³ / cover |
| --- | --- | --- |
| 90 / 134 | 0 / clear | 3.530261416877801 / contact |
| 90 / 231.6 | 0 / clear | 0 / clear |
| 167.5 / 283.63498306274414 | .00017851371924113596 / contact | .00017851371924113596 / contact |
| 0 / 134 | 0 / clear | 0 / clear |

Thus the candidate distinguishes the two known crank-90 shaft histories and
does not call the native-positive half-degree witness clear. Measured numeric
helper CPU is .0049–.0361 s per query, including placement, on this run. This
Python branching helper is an offline instrument, not a published law or a
browser-performance measurement.

## Mesh coverage is still incomplete

Native coverage is not enough. The **standalone source nodes'** generated
meshes were tested against the same extruded covers with Manifold64:

| Source node | Vertices / faces | Outside result |
| --- | --- | --- |
| Ones fitted pinion | 206 / 412 | empty, 0 mm³ |
| Higher fitted pinion | 196 / 392 | empty, 0 mm³ |
| One-tooth drum segment | 94 / 184 | nonempty, 5.579560203210584 mm³ |
| Nine-tooth drum segment | 304 / 604 | nonempty, 5.620713790041652 mm³ |

All four Boolean results report `Error.NoError`. The two positive drum
remainders are failures, not a small-volume allowance or a reason to change
the source mesh. They have not yet been localized to a contact-relevant zone.
Standalone source-node meshes are not a substitute for the complete fused
installed-print meshes, whose coverage remains a separate obligation.

An initial attempt to pass CadQuery's per-face tessellation of the cover
directly to Manifold refused `NotManifold`: adjacent faces have separate
indices. That was a diagnostic construction error, not an input-mesh defect.
`cover_mesh_arrays` instead extrudes the existing planar triangulation with
shared top/bottom/side indices. No vertex-tolerance welding or repair of any
source mesh is involved. The shared-edge regression passes before the four
coverage results above are obtained.

The instrument now offers `--include-mesh`: it validates each standalone
source-node mesh and retains every nondegenerate XY-projected face triangle
as an additional convex piece. Only exactly identical projected footprints
are deduplicated. No hull, angle copy, tolerance-based coalescing or source
mesh mutation is involved. This explicitly represents the mesh footprint
beside the native cover; it does not claim the native cover alone contained
the mesh. It is a full XY projection, not yet a decomposition of complete
installed prints into their actual axial slabs.

The four-row union run terminates with exit 0 and adds 103/98/45/150 mesh
pieces to the native polygons in table order. Its evidence is
`_build_checks/reverser-native-and-mesh-profile-cover-4035917.jsonl`, SHA-256
`68ff82c84ff1faf157409b8a2e30708e71c63fd70d7c980f461a7b736c54577a`.
The eight source-placed witnesses then terminate with exit 0, preserving
every native volume and contact/clear verdict in the table above. The
combined helper costs .0054–.0438 process-CPU seconds per query in that run.
The source-pinned report is
`_build_checks/reverser-native-and-mesh-profile-witnesses-4035917.jsonl`, SHA-256
`6b2f0848a51abb9aff1cdc90ec4b2d13f8f904e2b25f9e4ea817647608b13b66`.

Reproduce the union with the earlier generation command plus `--include-mesh`
and a new output filename. Then run the source witness tool into another new
file (the following uses the already measured input):

```sh
PYTHONPATH=/home/asa/devel/machinome-studio/machinome/WTs/curta-reverser-profile-validation:. /home/asa/devel/machinome-studio/.venv/bin/python -m simulation.tools.probe_reverser_profile_cover --input _build_checks/reverser-native-and-mesh-profile-cover-4035917.jsonl --output _build_checks/reverser-profile-witnesses-new-run.jsonl
```

The fixture rejects invalid/nonfinite/negative native commons and any positive
native material which the supplied cover calls clear. A conservative cover
may still call a native-clear pose contact: available play is a separate
acceptance obligation, not implied by a containment result.

## Empirical framework requirement, not a new contact solver

Sol's bounded read-only benchmark confirms existing public math can express
pointwise SAT, but not practically as an eager scalar graph of these covers.
The ones pinion and nine-tooth source profile require **633,552** polygon
pairs before any runtime rejection; the one-tooth comparison requires
154,251. Exact histogram arithmetic for straightforward two-sided SAT on the
nine-tooth pair gives 4,253,976 axes, 48,175,962 vertex-axis dot products and
87,210,420 binary min/max calls, about 231.7 million scalar arithmetic and
reduction occurrences. These are **not unique graph-node counts**.

A capped materialization of actual triangle pairs gives 3,343 / 12,637 /
25,029 / 49,833 unique graph nodes for 16 / 64 / 128 / 256 pairs. At 256
pairs, the first Python point evaluation costs .116 process-CPU seconds;
ten warm evaluations cost .142 s total. The cap is 256 pairs, approximately
50,000 nodes and 20 seconds. No complete graph, out-of-memory experiment or
full-profile runtime extrapolation is reported as a measured result.

The viewer's existing 125,000-node reclamation trigger is not a hard
admission cap; nevertheless this full representation would greatly exceed it.
Angular inputs are held during an immediate axial gesture, so this is a
bind-time cost, **not** a cost multiplied by the 64 axial search probes.

Separate framework/viewer proposal work is commissioned for a finite,
immutable, data-driven profile-overlap predicate with runtime rejection and
SAT evaluation. It would return a numeric contact flag **inside the existing
limit expression**, selecting absolute axial stop planes just as the local
trial already does. It is not a new constraint kind, a replacement span
level, a change to initial-contact attribution, generic physics, or a
continuous rotating-motion certificate. A typed operation and its wire
representation remain under proposal review, not an adopted public interface.

Before adoption the project still owes full installed native/mesh coverage,
all relevant axial slabs and six stations, independent placement fixtures,
available-play and both-direction retained requests, first-band stopping,
relief/retry/replay, browser parity, and crank/lift-changing acceptance. This
work does not waive the clearing-loop or whole-assembly findings.

## Complete installed-print radial exclusion

`simulation.tools.reverser_installed_radial_cover` now checks all six complete
installed input prints from one untouched `OperatingCurta` root. Each native
print has a valid, exactly zero difference outside a cylinder of radius
6.3 mm about its own declared shaft axis. Every vertex of its actual published
mesh is inside that cylinder, hence so is every triangle and its enclosed
solid. A radius-6.0 cylinder is the negative control: native material remains
outside, and mesh vertices escape it, for every station.

| Station | Maximum published-mesh radius mm | Native outside R6.0 mm³ |
| --- | ---: | ---: |
| 1 | 6.2262112660703455 | 4.789428883938631 |
| 2 | 6.16427893429756 | 1.0230559092372757 |
| 3 | 6.164279843699757 | 1.0230559092372653 |
| 4 | 6.164278062867083 | 1.023055909237322 |
| 5 | 6.16427927396561 | 1.023055909237312 |
| 6 | 6.164279097765485 | 1.023055909237302 |

The actual shaft-axis radii, minus 6.3 mm and a central drum radius of 34.1 mm,
leave strictly positive radial gaps of 0.09999999955998096 mm or more. This
excludes the central drum cylinder under arbitrary own-axis input rotations,
drum rotations and axial translations. It is a geometric separation, not a
volume tolerance, and does not cover a changed shaft axis or fitted geometry.

Subtracting that central cylinder from copies of the full native drums leaves
9 upper solids and 46 lower solids. Their remaining faces are planes and
cylinders; the frame's conical, spline and toroidal features lie in the excluded
core. The upper outer material runs from Z −54.2 to −43.7: one continuous
tooth and eight additional teeth at −49.7..−48.2. Those eight source volumes
differ; no symmetry is inferred. Lower outer material reaches Z −66.3.

The lower drum cannot yet be discarded: the complete ones input starts at
approximately Z −51.95 at reverser height 3.9075. At height −6.9425 and drum
lift 9, its range reaches approximately Z −71.8 in the drum's frame. Lower
drum rows therefore belong in the axial-coverage investigation. The earlier
lift-zero samples do not establish clearance there.

The reproducible eight-row command terminated with exit 0 on project
`c526ab0` plus this instrument, against the same pinned validation bench:

```sh
PYTHONPATH=/home/asa/devel/machinome-studio/machinome/WTs/curta-reverser-profile-validation:. /home/asa/devel/machinome-studio/.venv/bin/python -m simulation.tools.reverser_installed_radial_cover --output _build_checks/reverser-installed-radial-new-run.jsonl
```

Recorded evidence: `_build_checks/reverser-installed-radial-c526ab0.jsonl`,
SHA-256 `079ea1bd2cdc26c3fb5475e78f316abf59afe86da26a056fbf7cd64480351b1f`.
This establishes the radial exclusion only. Native outer-profile covers,
actual fused-mesh axial slabs, retained admission and browser parity remain
separate obligations; no production constraint is adopted by this result.

## Installed native and fused-mesh covers

The next instrument, `simulation.tools.reverser_installed_profile_cover`,
finishes the geometric coverage investigation for the current complete prints.
It first verifies all six input envelopes at R6.3 and both entire drum envelopes
at R36.62, using valid zero native differences and every published mesh vertex.
R36.4 was explicitly rejected: native remainders are .19275438499672798 mm³
and 32.22295710717067 mm³, and the mesh radii reach 36.50265777061964 and
36.60000173200467 mm. The final envelope follows those measurements, not a
volume tolerance.

The input's R3.86 central material is separated from the entire drum envelope.
The drum's R34.1 core is separated from the R6.3 input envelopes. Lower-drum
material below Z −72 is also excluded: the minimum actual native/mesh input
height, transformed across the explicit reverser −6.9425..3.9075 and drum-lift
0..9 ranges, is −71.80000076293945 in the drum frame. The tool checks these
driver ranges; changed ranges or geometry require regeneration and proof.

An attempted cover of each radially clipped input tooth was **rejected**.
Its native remainder is .000027789705103557994 mm³, at radius
3.86..3.8616078163929. A separately separated R3.87 cylinder contains that
native residue with exactly zero remainder, but the candidate triangulation
has nine reversed triangles among 260 and 22 inconsistent directed edges.
Its extruded mesh refuses `NotManifold`. Neither a source mesh nor this
candidate is repaired. A new red regression catches folded triangle
neighbours before convex merging; all four earlier source decompositions
remain unchanged under that check. The exact-zero remainder helper also has
red-first checks for tiny positive/negative, nonfinite and invalid results;
an optional exclusion is checked geometrically, never used as a threshold.

Instead, the complete, previously checked source pinion covers are placed at
the actual installed tooth bands. All remainder tests are then performed on
the **complete installed prints**, not on the source ingredients alone.
Drum covers come directly from the radially clipped installed native solids.
The resulting 27 profiles are:

- Three ones bands at Z −45.35..−43.85, −40.85..−39.35 and −36.35..−34.85;
  five higher input bands at −40.85..−39.35. Each uses 591 convex pieces.
- Nine upper-drum components, 19–21 pieces each: one −54.2..−43.7 continuous
  tooth and eight −49.7..−48.2 teeth.
- Ten lower-drum components, 20–23 pieces each: one −72..−66.3 continuous
  tooth and nine −67.8..−66.3 teeth.

Every complete-print native remainder is valid and exactly zero after the
stated exclusions and covers. The complete input meshes and upper drum have
empty, zero mesh remainders. The lower mesh has a valid positive remainder of
.0007006970741025602 mm³, whose **entire vertex set** lies within radius
34.11579905290836. That cylinder is strictly separated from every R6.3 input
envelope (minimum axis radius 40.49999999955998); its volume is not waived.
The inscribed polygon used for the first core subtraction need not contain
every radially irrelevant facet: the residual cylinder proves the remainder
irrelevant independently. All mesh results have `Error.NoError`.

Removing the covers leaves positive contact-region control volumes for all
eight prints (ones 118.3807743697585 mm³, higher inputs about 35.94165 mm³,
upper drum 90.88653561914697 mm³, lower drum 88.68881347057243 mm³). Thus an
empty result is not merely a probe that excluded the entire print.

The final reproducible 44-row run exits 0; the artifact includes each profile's
actual reference shaft angle and reverser height:

```sh
PYTHONPATH=/home/asa/devel/machinome-studio/machinome/WTs/curta-reverser-profile-validation:. /home/asa/devel/machinome-studio/.venv/bin/python -m simulation.tools.reverser_installed_profile_cover --source-profiles _build_checks/reverser-native-and-mesh-profile-cover-4035917.jsonl --output _build_checks/reverser-installed-profile-new-run.jsonl
```

Evidence: `_build_checks/reverser-installed-profile-reference-a428dea.jsonl`,
SHA-256 `d41e1b46ee7f4c92b61d2ddae586f01242574213942d7dd93f0e9c4aefad01a3`.
The earlier successful file without explicit reference fields has SHA-256
`a41fbbc97b72ade7ed17535d4322852f645ee12a1de5b947d58940ce4771392f`.
Both use the pinned source-profile input `68ff82c8…` and the unchanged
validation framework bench. The failed nine-row candidate prefixes remain
diagnostics, not complete evidence.

All 27 published polygon sets also construct successfully under the new
framework worktree's exact-binary `ConvexProfile` validator. That is a
development capability check, not reliance on an already integrated API.
The inspected two-panel plot
`_build_checks/reverser-installed-profile-histories.png` shows the expected
overlap at crank 90 / shaft 134 and clear gap at shaft 231.6 in the relevant
XY profiles. It is not a retained-root or continuous-motion certificate.

This advances **geometry coverage**, including the actual fused meshes and
the lower drum. It does not yet prove the portable Bound implementation,
available play, stop/relief/retry/replay, cross-runtime parity or full changing
crank/lift admission. No production law or umbrella task checkbox changes.
The final focused run passes 29 tests (profile cover, phase boundaries, pose
cache/refusal, phase compiler and refinement-resume modules) in .003 seconds;
the ten profile-cover tests include both new red-first regressions. These
small tests complement, not replace, the terminated 44-row geometry run.

## Portable installed trial — two remaining failures

The independent eight installed-pose witnesses now run reproducibly through
`simulation.tools.probe_reverser_installed_profiles` against the developing
framework predicate. They match the earlier native results: home and both
crank-90/shaft-231.6 poses are clear; crank-90/shaft-134 at heights 1.0475 and
0 contacts; the half-degree witness remains native-positive and covered.
The height-1.0775 control and lowered-lever/raised-drum endpoint are clear.
The eight-row command exits 0; evidence
`_build_checks/reverser-installed-profile-witnesses-a0b4539.jsonl` has SHA-256
`9469337aa95250cf6fd620119cda8b85cbc21ad70638852191873b3261d94560`.

The installed trial groups equal-height drum components without angular
symmetry and uses all six independent input phases. Its lower-drum omission
has a further axial proof: the lowest covered input tooth is −56.205 over
all reverser travel, while the highest covered lower-drum tooth is −57.295
over all crank lift. Radially excluded input cores were already checked
against the complete drum. Thus complete-print lower material was measured
before this optimization, not discarded from the original whole-print bounds.

`InstalledReverserProfileTrialTest` fails red before its factory exists.
After implementation against the isolated framework candidate, its four
inherited retained tests terminate in 244.918 seconds: the original
penetrating request and long-request/retry/replay/relief tests pass; the
precontact endpoint and alternate-history preparation fail. The production
root remains unchanged. The endpoint at 1.0675000000000001 is just below the
candidate's conservatively expanded limit 1.067500000000004. This is a
representation/coverage-choice failure, not permission to add a volume or
contact epsilon. Axial cover padding must be independently justified if
revised.

The alternate-history trial stops the crank at 81.93237719286117 with ones
shaft 179.9672140343115 and lever −4.9425. All six native input/drum commons
are zero there and at +.01 and +.1 crank degrees along the measured 6.4-degree
shaft advance per crank degree. But farther along that same motion there
is a **real previously untested contact**:

| Crank / shaft | Native ones/top-drum mm³ | Published mesh mm³ |
| --- | ---: | ---: |
| 82.43237719286117 / 183.16721403431148 | .0019561049905521917 | .00079150041326653 |
| 82.93237719286117 / 186.3672140343115 | .004558793175615966 | .0028154123562718443 |

The new `ReverserContactPathTest` reproduces the first contact in the actual
unconstrained retained production root, not just an independently transformed
bench. The request completes and the expected shaft is reached, but both
zero-common assertions fail: native .0019561049905521813 and mesh
.0007915004132666966 mm³. That run terminates with two failed subtests in
23.713 seconds against the unchanged validation framework bench. The earlier
clear 90-degree endpoint never proved the intervening path clear. The
alternate-history completion assertion is preserved, not weakened; a bounded
fit candidate must also retain the fork's axial capture and source fidelity.

Independent Sol timing isolates another framework limitation: five running
ticks for a .5-second crank request use 49.75 CPU seconds without CAD meshes,
with 7,800 predicate calls consuming 33.36 seconds and 15,600 repeated profile
placements consuming 17.44 seconds. The held-angle axial request costs .91
seconds, with only 24 calls. Paired package completion is held for an
evidence-backed scoped-reuse review; global caches, relaxed validation,
changed sampling and truncated profiles are not accepted remedies.

## Inner-flank candidate and independent axial allowance

The retained collision's source-pinion survey used 81 native poses from
80 through 88 degrees at .1-degree spacing. Maximum native commons at
83 degrees were .000330821745259808 mm³ for .40 mm uniform relief,
.0001427492171062817 for .405 and .000032512695330331293 for .41.
.415 and .42 had zero native common at these samples. This is a bounded
diagnostic, not a full-motion certificate.

The isolated .415 uniform candidate cleared the actual retained regression
in both representations (1 test, 40.234 seconds), but failed the existing
fork capture contract at lowered lever/crank 75. No production fit changed.
The fork's contact was localized to the middle tooth, at radii
6.165746366181353–6.226209785896065, while the crank-83 drum interference
was at radii 4.508289922567249–4.619494848745804. Both directions of .3 mm
axial perturbation lost their former .001151693969354527 mm³ native contact
under the uniform fit.

`reverser_ones_fit_trial.py` therefore tests an inner-flank-only candidate:
the existing .36 mm fitted outline remains outside R6, and .415 mm relief
is applied inside R6. It changes neither tooth phase, keyed bore, height,
fork nor upstream design. Native fidelity checks find one valid solid,
zero added volume, 2.9432728962945607 mm³ removed, and zero removal outside
R6 or inside the protected R3.5 keyed region. The existing 15 faceted seat,
capture, whole-bank sampled sweep and engagement contracts pass (27.40 s).
The new retained-root collision test also passes on both native and world64
geometry (41.649 s). Exact whole-bank and installed-Bound acceptance remain
separate gates at this checkpoint.

The inspected image
`_build_checks/reverser-inner-flank-profile-comparison.png` compares the two
outward XY covers: it shows their coincident protected tips and the recessed
inner contact flank. These are labelled .005 mm outward covers, not source
outlines or a rendered full machine.

The axial cover thickness is now an independently declared geometric length.
Old records retain their isotropic .005 mm default; a new record may declare
`axial_allowance_mm=.001` without changing its .005 mm XY offset. A new unit
test fails red with the old isotropic extrusion, then all 11 cover tests pass
after both native and shared-index mesh extrusion read the declared length.
Zero, negative and nonfinite axial allowances refuse. A reduced length is
not accepted merely because it makes a Bound test pass: full native and
published-mesh containment is rerun before that record is consumed.

That rerun completed all 44 records on the isolated inner-flank root:
`_build_checks/reverser-inner-flank-installed-cover-a0b4539.jsonl`, SHA-256
`1cc0cf7f434318d66a813c5cb62046433ae283b0985a5117d2c671edc91da0ff`.
Its new source pinion has 637 convex pieces and zero native uncovered volume.
All eight complete installed prints have valid zero native uncovered volume.
All six input meshes and the upper drum are empty after subtraction; the
lower drum retains the same .0007006970741025602 mm³ residual inside the
independently separated radial region, never dismissed by volume size.
The .001 mm axial allowance thus has its own complete-print coverage check.
The original pinned evidence and trial remain available unchanged in meaning;
new evidence/model arguments select this candidate explicitly.

The exact 15-test seat suite subsequently passes in 420.62 seconds. The
installed inner-flank trial terminates **3/4 passing** in 151.567 seconds:
wrong-order penetration, long request/retry/replay/relief and precontact play
pass. Alternate-history crank preparation remains blocked. Independent XY
checks identify the cover contact from about 82.6 through 83.4 degrees;
native minimum distance at 83 degrees is only .00043888341213706866 mm,
smaller than the two .005 mm outward covers. The native minimum distances
at 82.8 and 83.2 are .0037773569213893025 and .001954919621565924 mm.
The .415 inner fit is therefore a geometry/capture checkpoint, **not an
adopted operating restraint**. No completion assertion is relaxed.

The repeatable coverage entry point is
`python -m simulation.tools.reverser_inner_flank_cover --source-profiles
_build_checks/reverser-native-and-mesh-profile-cover-4035917.jsonl
--source-output <new-source.json> --installed-output <new-installed.jsonl>`.
It covers the explicitly named current trial, keeps prior evidence, and
requires the entire output stream to terminate successfully before use.

## .43 inner-flank candidate: geometric and retained gates

A finer 25-pose distance check over 82.4–83.6 degrees at .05-degree spacing
finds only .00035090425543188677 mm native gap at 83.05 degrees for the .415
inner fit. The named .01 mm minimum flank gap (the two .005 mm outward
covers) fails at 16 poses; no volume threshold is substituted. Increasing
only the inner relief to .43 mm passes all 25 distances and the unchanged
protected-tip/key/one-body checks (2 tests, 23.815 seconds). R6, the outer
.36 fit, source height, tooth phase and every upstream file remain unchanged.

The .43 candidate passes the 15 existing faceted contracts in 28.65 seconds
and the 15 exact contracts in 590.39 seconds. The actual retained collision
regression passes in 43.778 seconds. Whole installed coverage is independently
regenerated by the committed entry point, with all 44 rows and the same eight
successful full-print verdicts:

- source cover `_build_checks/reverser-inner-flank043-source-79f3de8.json`,
  SHA-256 `37fcd0bd751f33da99797bc8d393ee71b1547b9300c3b0a41de5f0908f294122`;
- installed cover `_build_checks/reverser-inner-flank043-installed-79f3de8.jsonl`,
  SHA-256 `4253236b35204ba03b94b4b9c948d10222a9a5f2b81ac09c4e2f8789f71de896`.

`InnerFlankInstalledTrialTest` now passes **4/4** in 171.750 seconds: wrong-order
blocking, the alternate retained-history withdrawal, the long request with
retry/restore/relief, and admission of the independently asserted precontact
play. This uses the new complete .43/.001 evidence, not the earlier .415
record. It still does not assert completion of every operating mode or of
the larger operating-Curta change.

`compile_reverser_profiles` emits readable Python model data so runtime
operation does not depend on ignored diagnostic output. It refuses absent,
duplicate or failed whole-print verdicts, dropped components, nonfinite or
negative remainders, unjustified radial residuals and a lower drum that is
not axially separated. It retains all six independent shaft references and
groups only identical axial drum bands. Four compiler tests fail red before
the module exists, then pass. The independent compiled-law fixtures also
fail red before implementation and pass afterward; 19 compiler, cover and
numeric-law tests pass together in .761 seconds. A separate compiled-root
trial exercises the same retained contracts without loading a diagnostic
file. Production wiring is held for paired package integration and the
remaining operating-mode checks.

Residual runtime performance is recorded separately from contact correctness.
The accepted cache reduces the measured installed tick from 13.72 to 8.33 CPU
seconds, but this is not real-time Python operation. A subsequent bounded
profile attributes most remaining work to repeated kink-chart evaluation.
Exact-time, shared-node-result and graph-root topology cache experiments did
not establish a material gain: the graph evaluator already caches each
value's traversal, and newly compiled roots were distinct. These rejected
experiments change no repository source, sampling, contact rule or program.

## Complete-stroke gate: tighter covers required

The self-contained compiled trial passes all five retained-motion/path tests
in 184.024 seconds. Framework `main` now contains the separately reviewed
profile primitive/cache at `8d0fd156787f5136174fb752be78451ce172bce8`;
the final package suite passes 3655 tests and the merged-state focused gate
passes 34 tests plus 14 subtests. This does not make the project trial adopted.

Four full 360-degree, two-second requests expose a distinct cover precision
failure. Normal lever/lowered crank and reversed lever/raised crank complete;
reversed/lowered and normal/raised stop at 102.70793504742323 degrees. At the
stop the first two retained shafts are 312.9307843035087 and
164.9307843035087 degrees. The higher input, not the protected-tip ones, causes
this stop. `CompiledReverserStrokeTest` reproduces it red in 42.082 seconds,
without relaxing completion or preparing any extra control.

Independent complete tens-print placement at crank 103, shaft 166.8, lever
−4.9425 and crank lift zero gives exactly zero native and world64 common
against both complete drum halves. The native upper-drum distances at
cranks 102.7, 102.8, 103, 103.2 and 103.5 are respectively
.012169409965601482, .008777357065223066, .005438883588495964,
.006954919830790235 and .018967583845857984 mm. Shaft values follow the
already-retained local law `114 + 6.4*(crank-94.75)`. The lower drum stays
6.90525155825229 mm away. At 103 degrees the compiled lower limit is
−3.440500000000006, incorrectly excluding the clear −4.9425 pose; a small
independent law regression is red too.

The first response is therefore to investigate tighter outward XY covers,
not to remove more actual gear material. The coverage entry point accepts
an explicit `--xy-allowance` and regenerates both input source covers and
every installed drum cover. The complete native and published-mesh
containment checks remain mandatory and unchanged; a narrower mathematical
offset alone is not proof that any material is contained. Existing .005
records remain evidence of their own checkpoint and are never overwritten.

The uniform .001 XY attempt is refused, not adopted: the ones print leaves
.007025915854924476 mm³ of actual mesh outside, reaching radius
4.168057178290999. Keeping the .005 ones cover but trying .001 on the higher
inputs is also refused: the installed tens print leaves .0025967477635878604
mm³, reaching radius 4.168484523844867. Both partial JSONL files remain failed
evidence and cannot pass the compiler's complete-record gate. A standalone
higher-pinion .004 cover has an empty, exactly zero mesh difference.

The asymmetric candidate then passes **all 44 installed-proof rows**, with
.005 XY on ones, .004 on higher inputs, .001 on drums and .001 axially:

- `_build_checks/reverser-inner043-asymmetricxy-source-79f3de8.json`, SHA-256
  `d3ee959ea9a1a3745dade26905522d870e641d07fad2fe43decffb3bb3159ea9`;
- `_build_checks/reverser-inner043-asymmetricxy-installed-79f3de8.jsonl`, SHA-256
  `22335517e243651826084aa60aacd38911b647b79a14d8001cb690e226186327`.

All eight native remainders are valid and exactly zero. All six input mesh
remainders and the upper-drum remainder are empty and zero. The lower drum's
nonempty .0028186569405925697 mm³ remainder is independently separated:
its radius 34.1574731052492 plus the input envelope 6.3 is strictly below
the measured minimum axis distance 40.49999999955998. No volume is waived.
Reproduce with the coverage command above plus `--xy-allowance .001
--ones-xy-allowance .005 --higher-xy-allowance .004` and new output paths.
No physical geometry, mesh precision, tooth phase or operating law changed
between the uniform and asymmetric cover attempts.

The generated model data now pins that complete record. The 103-degree
false-stop regression turns green; all 20 compiler/cover/law tests pass
in 2.013 seconds. The five compiled retained-motion/path tests pass in
182.695 seconds. The full-stroke test passes all four prepared modes in
488.301 seconds, reaching 360 degrees without extra preparation. These
are retained-motion gates, not a continuous swept-solid certificate.

A complete mesh export of the unadopted trial is built at
`_build_checks/reverser-compiled-asymmetric-v13`, manifest SHA-256
`3388020498a62ea4d75b4adfa7acd1b995e098d47bc101dfd9b8e6c0cc6c3587`,
version 13, eight profiles, program identity
`200219dcb6356bb3d27324e22f8dce01fdc5779fdb0ba2b06a9c56c28be3c8e8`.
It is 7,488,148 bytes. The producer warns that the still-installed viewer
main at that moment supports only versions 1–12; the artifact is retained
for the separately verified version-13 viewer. No browser acceptance or
production adoption is inferred from successful serialization.

## Hosted replay and visible lever, before endpoint correction

The independent viewer profile cycle is now on its local main at
`b976a172a7964b269183eaee289c8cf26668cd58`, API 26, supporting documents
1–13. With framework main `8d0fd156787f5136174fb752be78451ce172bce8`,
`tools/reverser_operating_browser.py` exercises the complete exported trial
at the viewer's default `dt=1/240`. It compares all 214 coordinates by
IEEE-754 bits after each of nine explicit Python/browser requests.
All nine banks and statuses agree exactly, including blocked retry,
snapshot replay and reverse relief. No browser error is reported.

The actual visible reversing-lever control also reaches a terminal
wrong-order stop. A 100-pixel downward drag issues two admitted −1 mm
requests followed by a blocked −.8480000000000061 mm request, landing at
1.0594999999999941 mm. Pointer release is observed and the command queue
is empty. Every other driver and every `.turn` coordinate retains its
prepared bits. The inspected screenshot shows the complete hosted machine;
this is interaction/placement evidence, not a view of its internal contact.

The overall gate deliberately **fails**: the ninth request, withdrawing
directly from −4.942499999999999 to the legal upper endpoint 3.9075 mm,
incorrectly reports `blocked` and banks 3.9075000000000006. Both runtimes
exhibit the same one-ulp overrun. A separate framework-only one-driver
Prismatic fixture reproduces it with a literal range, without Curta or
profile contact. Separate framework/viewer correction cycles are required;
splitting the request or tolerating the wrong status is not acceptance.
The diagnostic's ideal decimal shaft angle uses a 1e−9 absolute comparison
(231.60000000000002 versus 231.6), but runtime-to-runtime comparisons of all
state bits, material-contact tests and endpoint-status expectations are exact.

Evidence retained, not overwritten:

- `_build_checks/reverser-asymmetric-browser-da9808a-04.json`, SHA-256
  `d0003c7930578f920e9106b86215cc4cc2a417aabb1bdb29736b0436dda2dd04`;
- adjacent `.png`, SHA-256
  `8e6e5a899c947f47c1f7558f978ceb409475c82e131175267075d35f5c82bc64`;
- tested bundle SHA-256
  `fedcfb260574337b00837652fd3c5d335442c7ff00eae2e0fcb1ac1e27877847`.

That historical report retains `validation: pending` alongside its explicit
assertion failure; it is not a pass. The tool now labels future exceptions
`failed`. Earlier reports 01–03 also remain failed diagnostic evidence.
Production geometry/wiring and completion checkboxes remain unchanged.

The final .43 mm inner-flank pinion is also inspected in independent
OpenSCAD isometric and axial orthographic snapshots, produced through the
public snapshot command on `simulation.reverser_ones_fit_trial:TrialOnesPinion`.
The five source-derived tips, keyed bore and extruded plate remain visibly
present. These views complement, rather than replace, the preserved-material,
capture and two-kernel clearance contracts above. Both commands exit zero,
using the clean scalar-evaluation worktree at framework `1a34b3c`:

- `_build_checks/reverser-inner043-pinion-iso-7f56368.png`, SHA-256
  `7880cef5242b526c7c5bdeea686015761b3c78fbac9a87f7dfa2fbce8ac4ea4a`;
- `_build_checks/reverser-inner043-pinion-axial-7f56368.png`, SHA-256
  `92fd763284abdae5a4a522628c7a61c1559c235beadd8c383ff9c2fe03dcdd74`.

The separate scalar-evaluation framework cycle is integrated locally at
`1a34b3cd0eb85f20c7769f6f3f5c28ebfef01cd1` (plan `a507412`). Its full
suite passes 3,660 tests, with four skips and 2,153 subtests; the final focused
gate passes 45 and the merged-state smoke gate 28. On the older pinned
installed-profile tick, six alternating runs preserve all 439,729 ordered
numeric results and the full 214-coordinate bank. Median process CPU improves
8.843014→8.481218 seconds; one pair is slower. This modest measured gain
does not change contact evaluation, timestep, exported documents or the viewer,
and does not establish real-time operation. The framework owns the complete
archive at `2026-09-23-streamline-graph-numeric-evaluation/evidence.md`.

The six unchanged `test_running.RunningCurtaTest` arithmetic contracts now
pass against `CompiledReverserTrial` in **1193.279 seconds**, with an observed
zero exit. The test process substitutes only the module's model factory with
`unittest.mock.patch.object`; expected readings, initial state, timestep .1
and public command sequences are unchanged. Coverage is independent selectors,
successive additions/selective clearing, manual carry calibration, partial
crank release/snapshot replay, carriage reassociation and subtraction/borrow
through both registers followed by addition undo. This is a trial acceptance
batch, not production-root or whole-machine geometry acceptance.

The process imported framework main at `8d0fd15` before the separate scalar
cycle advanced that checkout to `1a34b3c`. It retained those imported modules;
the run is not relabelled as a post-integration test of the scalar change or
of the still-unfinished endpoint correction. These observations are the
terminal test summary, not a separately captured raw log file.

## Endpoint candidate: first complete hosted pass

At project `ffafa3f`, fresh unchanged **production** tests still fail red:
wrong-order reversal has native/world64 commons .02353507611251452 /
.023458419217706056 mm³ and reports `completed` instead of `blocked`;
the reversed-counter passage retains .0019561049905521813 /
.0007915004132666966 mm³. Two tests produce five failing assertions in
47.027 s, exit 1. Log `_build_checks/reverser-production-red-ffafa3f-a9f10b8.log`,
SHA-256 `d91716a5e0be8930cccad45d13cd978eaceedc1e94d3ea722879dc9d6d9dd073`.
They run against the isolated combined framework head `a9f10b8`, now also
integrated on clean local main. Both earlier CI commits `a87abc5` and
`e05d9c5` remain its ancestors. No push or other worktree cleanup follows.

The separate endpoint candidates now pass the hosted trial gate, including
all nine requests, exact equality of every Python/browser bank coordinate,
strict stopped/replay and prepared/relieved Python snapshots, and an actual
100-pixel downward drag of the visible lever. The pointer admits −1, −1 and
then −.8480000000000061 mm, reports completed/completed/blocked, stops at
1.0594999999999941 mm, observes release and leaves no queued command. Other
drivers and all `.turn` values retain their prepared bits. Reverse-first
now lands at exact −4.9425; the ninth withdrawal completes at exact 3.9075.
There are no page errors, the report says `passed`, and process exit 0 is
observed. The screenshot is inspected: complete front/side assembly and
hosted control panel, not an internal-contact certificate.

This is explicitly an **intermediate candidate**, not final package acceptance:
framework planning head `4fcb770`, with `run.py` SHA-256
`be7b82702520d6fdfaf4b61b56d5ea133abfc0abd6ab9a5f99c6cdacc6f45801`
and `trajectory.py`
`32004c0f9a76a10d43481473ffbe44a1378eb6444cc29f57ebc975904fcf00ce`;
viewer planning head `b6fafbf`, bundle
`f0862fd5ab438764b06fdc47426a44cc7828fd130dbf2e70d6577fa654b83d67`.
Later snapshot/periodic-law edge-case corrections require fresh final evidence.
The frozen asymmetric export above is unchanged.

- `_build_checks/reverser-asymmetric-browser-ffafa3f-05.json`, SHA-256
  `a01dd2374990b641b24fafb239269f1c410ef4397b621190b8d88d61e1d47afa`;
- adjacent `.png`, SHA-256
  `71aed3d5e7182aa9d824ec5f74483a82d2765f4d47e3b30bf342db730a18d97b`.

The five compiled-trial geometry/motion tests also pass against that frozen
Python candidate in 192.218 s, exit 0. Log
`_build_checks/reverser-compiled-endpoint-ffafa3f-05.log`, SHA-256
`c0d6fa80e35bd667105bef958e255eae950e34b4595ce274582469c8dd9eaf0c`.
Production remains unchanged pending final paired endpoint integration and
adoption; no whole-machine task checkbox changes.
