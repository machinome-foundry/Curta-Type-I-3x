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
