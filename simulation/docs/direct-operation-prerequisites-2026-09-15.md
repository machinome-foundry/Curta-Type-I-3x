# Direct-operation resumption: prerequisite checks

The pilot requested implementation on `direct-operation`, followed by markings.
The project started clean at `c83bf00`. This record describes capability checks,
not an implemented migration or a completed mechanical acceptance task.

## Installed content

- Framework: `8d29cf5e4b289da79e65bd09e3d0c13f5721f305`, including the
  original direct-part-motion change and the markings producer (ADR-120).
- The selected-joint hardening commit `d1108a4` is **not** an ancestor of
  that framework head. The API skill describes that correction separately.
- Viewer committed head: `4cfa251adaae20b4ff7e998dcd8f8a9afaa807fd`, with
  pre-existing uncommitted API-13 implementation. `machinome viewer` reports
  API 13, document versions 1–5 and package metadata version 0.1.0.
- Installed bundle SHA-256:
  `42e214cb1d3cc0483548f53d4a8c27324d4ebca816f1b29ae9b66789800733b7`.

These facts do not establish the tested framework/viewer content pair required
by task 6.1. The viewer's `slide-and-turn-parts` acceptance checklist remains
open. No framework or viewer files were changed during these checks.

## Independent crank freedoms work in Python

The geometry-free public-API diagnostic is
[`tools/direct_operation_probe.py`](../tools/direct_operation_probe.py).
From the project root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD" \
  ../../../.venv/bin/python -m simulation.tools.direct_operation_probe
```

It declares a crank with rotational and prismatic joints, explicit `Turn`,
`Slide` and `Button` selections, and `Time.running()`. Lifting to 9 mm and
requesting one clockwise revolution produces 9 mm and -360 degrees, with
both commands reporting `completed`. This tests command construction and
independence, not publication or pointer interaction with the real Curta.

## Retained-angle clearing needs a supported representation

The approved clearing behavior requires a dial to stop accepting rack travel
at its missing-tooth zero gap while the clearing ring can continue. A second
sweep over an already-zero dial must leave it at zero; a partial sweep must
resume from the retained angle. Resetting the run or supplying a saved register
value from the page would violate the approved operation contract.

The reduced diagnostic attempts a law whose sources are rack travel and the
wheel's retained rotation and whose output is wheel rotation. Class declaration
fails before a run is constructed:

```text
TypeError: wheel.rotation is named as both a source and a driven end of one relation:
a coordinate is a source or a driven end of one relation, not both.
```

This proves that this direct state-dependent engagement representation is
unsupported; it does **not** establish that every possible representation is
impossible or prescribe a particular framework API. A supported representation
must be established before implementing this part of the migration. A joint
range alone would stop the pushing ring input at the dial's zero, whereas the
required missing tooth disengages the dial and lets the ring continue.

The fixture's gate is deliberately schematic. It establishes the declaration
refusal only, not the actual tooth profile, clearing angle or a contact verdict.
Existing `cycle.cleared_position` uses an explicit starting position and one
normalized sweep; those pose-model inputs cannot supply retained clearing state
for arbitrary repeated operations.

## Markings readiness

The new public manual is `machinome/docs/markings.rst`. It documents
`Marking`, `Svg`, `Flat` and `Wrapped`, including source-relative SVG paths,
nominal zero-volume surfaces and separate decal artifacts. It explicitly says
that neither the browser viewer nor the OpenSCAD path draws these markings yet.
Declarations and portable exported artifacts can be implemented independently
of consumer display, but visible markings cannot yet be claimed.

The project's original SVG artwork exists under `Drawings/`; no replacement
font or image generation is needed. `Drawings/cricut-images/README.md` records
the intended artwork dimensions. Initial exact surface checks find the input
number roll's R9.3 cylinder spanning z=0–15 mm and the result roll's R9.45
surface matching the 59.376 mm artwork circumference. Artwork clocking,
placement on each fitted variant, housing labels and visual registration remain
implementation and verification work.

## Disposition

No operating code, geometry, SVG, test expectation or OpenSpec task checkbox
changed. Direct operation and markings remain unimplemented. The additional
clearing question and the unfinished viewer pair are recorded without changing
the approved physical inventory or waiving the earlier geometry failures.
