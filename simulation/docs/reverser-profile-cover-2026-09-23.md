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
