# Installed housing-thread fit

This is a bounded simulation-owned fitting of the author's two printed covers,
not a new thread design or a change to their upstream STL/STEP files. Their
previously verified window-aligned position, seventeen axle seats, clearing
plate and dial placements remain unchanged. Task 1.3 still owes the complete
source-overlap inventory, beyond this interface.

## Red and measured region

`HousingThreadTest` initially fails both installed-clearance and axial-play
contracts. The unchanged thread contact is 224.327505338 mm³. Moving the male
cover +.3 mm still leaves 65.364034289 mm³; moving it -.3 mm worsens contact to
529.579027460 mm³. This is not fixed by changing the already verified common
carriage datum. `tools/housing_thread.py` preserves the measurement procedure;
the initial output is `_build_running/housing-thread-measurements.jsonl`.

The fit laps only the female housing against its actual mating print. The
relative placement is taken from `standard.layers.CarriageCovers`, independent
of the common carriage recentering. A continuous fitting envelope expands that
male surface by +/-.02 mm in X/Y and +/-.05 mm axially. Removal is clipped to
the female's local R71.9..75 mm, Z35.9..42.4 mm thread/seat region. Neither part
is scaled, their thread pitch is unchanged, and no material is added. The
existing axle-pocket fit plus this thread fit removes about 367.31923 mm³ from
the 122340.222561 mm³ source housing. After the export correction below, the
fitted mesh has 49820 triangles and no non-two-sided edges.

Sampled axial envelopes and a radially scaled cutter were rejected: they left
edge slivers and failed the unchanged zero-overlap and .02 mm free-play checks.
The accepted trial uses a continuous Minkowski envelope, with the same bounded
removal zone. No overlap epsilon or whole-machine exclusion is introduced.

## Verification status

Installed clearance, +/-.02 mm axial free play and blocking at +/-.3 mm now
pass. The measured rest common is zero; +.3 and -.3 mm give 5.303561390 and
289.815583225 mm³ respectively. The full nominal cutter allowance is not
claimed as certified free travel: -.05 mm still gives .000547471 mm³ at the
encoded boundary. Tests use the smaller verified .02 mm free interval.

Material preservation is checked separately from clearance. Boolean differences
can retain zero-thickness coincident shells with a tiny signed floating volume
(one added-material audit returned 2.026236988e-13 mm³). Those are not waived by
a volume threshold: vertices and face interiors must coincide with the before
surface within .00001 mm, and any difference outside the fitting zone must
coincide with BOTH before and after surfaces. This is source/STL length
precision, not an interference tolerance. The existing cover fidelity test
also audits protected surfaces in both directions, now naming this additional
fit explicitly. A fresh/built comparison guards the generated artifact.

The neighbouring cover suite then caught an export defect that a fresh-shape
connectivity check missed: the first fitted binary STL had 362 non-two-sided
edges. A fresh in-memory STL round-trip reproduced it, ruling out a stale
artifact. Simplification alone, even at .001 mm, did not cure the remaining
artificial face seams. Resetting only the generated Boolean's face-provenance
metadata before .000008 mm simplification allows coplanar faces from separate
cutters to collapse together. No source mesh is repaired or welded, and no
contact assertion acquires a tolerance. `tools/thread_encoding.py` retains
the comparison procedure; `housing-thread-encoding-final.jsonl` shows the
accepted reset/.000008 mm case is watertight after actual STL encoding. The
scoped test now checks fresh, round-tripped and
actually built connectivity, as well as vertex/face-centre artifact fidelity.

The strengthened module passes 3/3 under the faceted runner (33.42 s) and 3/3
under the exact runner (16.91 s). The seven neighbouring cover tests pass again
under both runners (59.61 s faceted, 44.92 s exact), including complete dial,
carry and clearing motion, all axle neighbours and protected source surfaces.
Both covers are source-STL parts, so their contacts remain faceted under either
runner. Logs are `housing-thread-final-{faceted,exact}.log` and
`covers-after-thread-{faceted,exact}.log`.

The whole operating model gets past this interface on both runners, and its
solid-integrity check passes. Its ordinary interference check remains red:
the faceted runner next reports lower housing/base plate at
.000028108318 mm³; the native runner gets past that pair and reports the
upper sleeve/bottom housing at 909.434743190 mm³. Each root run is 1/2
(10.03 s faceted, 11.84 s native). These are new findings to investigate,
not exclusions or completion of the rest inventory. Logs:
`operating-root-after-thread-{faceted,exact}.log`.

The close inside view `housing-thread-fitted-inside.png` was inspected: the
inner ledge, thread and axle-seat cuts are visible, with the external knurl
retained. It is a cropped detail, not a whole-machine acceptance image. The
inspection class changes only colour for visibility. No roadmap task is
marked complete by this scoped increment.

The uncropped `housing-thread-fitted-full.png` was also inspected, showing the
complete housing outline, inner seating ledge, thread and retained external
knurl. These views support the scoped geometry checks, not final whole-machine
or manufacturing certification.

The rebuilt operating export retains schema 7, 23 drivers and 24 controls;
all 154 unique model references resolve in the build output. Its document
SHA-256 is `3cc0620e443eb3d24ce8d758e0d3a00697dd112b2fa3a8856a792fd02a851c08`.
Strict OpenSpec validation passes. This is export integrity, not completion
of the remaining full-machine collision and control matrix.
