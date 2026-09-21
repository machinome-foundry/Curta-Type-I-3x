# Collar seating: height-only correction rejected

This is an unresolved task-1.3 contact investigation, not an adopted fit or a
claim that the author's printed calculator fails. No source geometry,
operating placement, spring law or control has changed.

## Complete-neighbour survey

At project `07dc3f3f953d77de481550362627dc6bf947cd2a`, the initial
`OperatingCurta` has 213 coordinates and 389 rigid occurrences. The probe
translates only a measuring copy of the collar, checks it against every other
rigid occurrence, and confirms that the run bank remains unchanged. This
count belongs to the current model, not the earlier 390-occurrence inventory.
The collar is the author's standard STL, so all these contacts use Manifold
on published meshes, including contacts with otherwise native parts.

The initial inline survey and the retained `tools/collar_seating.py` reproduce
the same nine pose rows exactly. All measurements completed; no worker was
terminated. Selected volumes in mm³ are:

| Collar rise, mm | Spider mount | Thrust ring | Collar nut | Each carrier pin, approximately |
|---|---:|---:|---:|---:|
| 0 | 504.871504 | 225.523065 | 8.288378 | 11.430455 |
| .25 | 316.487173 | 259.906715 | 0 | 10.205438 |
| .5 | 128.102841 | 293.701503 | 0 | 8.980422 |
| .65 | 15.072241 | 313.695722 | 0 | 8.245412 |
| .7 | 0 | 320.313352 | .595261 | 8.000409 |
| 1 | 0 | 359.524492 | 76.373163 | 6.530389 |
| 2 | 0 | 369.540515 | 270.944995 | 2.191197 |

The full values, including .75 and 1.5 mm, belong to the accompanying
[evidence](evidence/collar-seating-2026-09-21.json). These are discrete
measurements, not a proof over every intermediate height. Every tested height
leaves material contact, and the first sampled height clearing the spider
makes thrust-ring interference worse. A height-only correction is not adopted.
Earlier whole-spider translations were independently rejected in
[the spider measurements](measurements.md#register-balls-and-the-tapered-spider-spring).

No positive volume is removed by an epsilon. The shared measurement helper
recognizes an exactly empty or zero-thickness common as zero. Nonfinite or
negative spatial volumes stop this probe as an error. This is not a replacement
whole-machine inventory: only collar neighbours are intersected, flexible
wires are not included, and no operating trajectory is certified.

## Section and manual evidence

The inspected `_build_checks/collar-seating.png` is a Y=0 section of the
unchanged operating model, with full-stack and spider-seat views. It shows
the spider mounting ring extending above the collar's outer underside and
the thrust ring entering its internal tapered bore. These are different
interfaces; clearing one does not establish the other. The section includes
the cover, carrier, washer and nut, but is not a substitute for the complete
3D neighbour checks, especially the off-section carrier pins.

Manual page 44 shows the collar, washer and threaded nut assembled around
the clearing cover. It allows thread fitting but provides no numeric collar
height correction. Page 39 calls for approximately 4 mm exposed carrier pins
for the spider. Page 48 shows the thrust ring below the spring and sleeve;
its unfinished caption supplies no dimension that resolves the internal
seat. Pages 44 and 48 were rendered and visually inspected. Nothing here
justifies translating the whole carriage or suppressing either contact.

The separate local Y=0 source sections, inspected in
`_build_checks/collar-source-sections.png`, visually agree at the internal
taper and spider shoulder. There is no observed missing seat in just the
printable representation. This is not a global shape-equality test: the STEP
tessellation is non-watertight and remains unsuitable for contact acceptance.
The STL is watertight. Both local Z ranges end at 58.5 mm, while the coarser
STEP facets give different Y bounds and mesh volume. The source files remain
unchanged; replacing the valid print with the invalid mesh is not a remedy.

## Reproduction

From the project repository, using the existing workspace environment:

```sh
ulimit -v 8388608
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export PYTHONPATH="/home/asa/devel/machinome-studio/machinome:$PWD"
export SOLID_BUILD_DIR=_build_checks
/home/asa/devel/machinome-studio/.venv/bin/python -m simulation.tools.collar_seating \
  --section _build_checks/collar-seating.png
/home/asa/devel/machinome-studio/.venv/bin/python -m simulation.tools.collar_seating \
  --source-sections _build_checks/collar-source-sections.png
```

The optional `--rise` may be repeated for explicit diagnostic heights. The
source-section mode does not construct an operating pose. Both commands exited
zero, and all 213 run coordinates stayed unchanged through the assembly survey.
Framework content was `e6a42c80e6dcc686c180b8a6d94037301c4213a5`; no browser
or framework implementation was involved in this project diagnostic.

Before any fitting change, establish the retained seats and a bounded removal
envelope. A candidate must preserve threaded retention, the spider's mounting
and finger roots, spring capture/travel, cover freedom and carrier-pin
engagement. It must fail the current geometry first and pass scoped
source-fidelity and moving-neighbour checks after the fit. Task 1.3 and the
complete operating-machine acceptance remain open.
