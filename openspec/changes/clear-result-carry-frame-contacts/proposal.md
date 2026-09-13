## Why

The two result-carry stations selected for the open-run Curta slice intersect
the upper frame: their fitted springs already penetrate it at the `099`
starting pose, and their sliders penetrate it at both stroke endpoints.
Those measured contacts prevent the manual's freely moving carry/reset
operation and must be resolved before this slice can validate a running engine.

## What Changes

The pilot ratified this bounded correction and authorized continuation on
2026-09-13: "ratify, go on". This authorizes the frame-only implementation
below, including its protected-feature stop conditions, not the running model.

- Establish a verified frame interface for the first and second result-carry
  stations, retaining their installed supports, springs, sliders, coupled
  sleeves and every neighbouring obstacle.
- Add bounded, stationary frame reliefs at those two stations within the
  simulation layer. Preserve the spring installation, guide placement,
  measured 4.2 mm stroke and working pin, detent, fork/sleeve and reset-cam
  interfaces. Return any need to change a protected seat or moving part to
  the pilot rather than treating it as the same repair.
- Add named red-first frame-contact and fit-preservation contracts, then verify
  the initial `099` preload, full lever travel and both trip/reset transitions.
- Retain source comparisons, bounded correction dimensions, negative controls
  and inspected before/after images as project evidence. Report any residual
  obstruction instead of waiving it or hiding its part.

## Capabilities

### New Capabilities

- `result-carry-frame-clearance`: The first two result-carry stations can occupy
  their supported starting, engaged and reset positions and move between them
  without penetrating the frame or losing their mounting and driving contacts.

### Modified Capabilities

None. This repository has no promoted baseline specifications. The active
`simulate-the-curta` change owns the broader `curta-assembly` and
`curta-operation` deltas; this focused capability complements them without
rewriting, superseding or completing that unfinished change.

## Impact

Owned entirely by this Curta repository, in the existing
`WTs/open-run-simulation` worktree at project base
`60979adbc795785fc51a28a386f85d1a49bfedf7`. Likely implementation touch points
are the upper-frame adapter in `simulation/mechanism.py`, a narrowly scoped
frame-fit module, and independent geometry tests and evidence tools. The design
sets the correction boundary and the conditions requiring another pilot choice.

The empirical basis is `simulation/docs/open-run-evidence-2026-09-12.md` and
its hashed native records. Upstream STEP/STLs, manual, licence and attribution
remain unchanged. No framework/viewer dependency or public API changes are
required; the three-repository running campaign and its undecided 0.7/0.8
release target are unaffected.

Out of scope: repairing all fifteen carry stations or the whole machine,
clearing the known housing/thread finding, new carry timing or force models,
selector home-window admission, full initial-snapshot certification, outgoing
carry behaviour, and runtime implementation. Completing this local correction
reopens those remaining evidence steps; it does not satisfy them by itself.
