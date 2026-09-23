## Why

The published Curta has an assembled STEP model and a build manual, but neither
lets a maker operate the mechanism or verifies that its selectors, transmission
shafts, carry levers and registers can perform the author's calibration sequence.
The existing `simulation/assessment.md` supplies the starting evidence.

## What Changes

The pilot's scope is: "use simulate-project to simulate Calculators/Curta-Type-I-3x.
Note that there is previous research at simulation/, use it. make the code simple
and expressive with the motion api."

- Add a project-owned `simulation/` package using the standard STEP geometry,
  its placements and the manual's assembly instructions.
- Express crank, selector, transmission, carry, carriage and clearing motion
  with named joints and drive relations, direct controls on each physical
  input and a small repeatable demonstration set separate from normal use.
- Verify source identity, rigid parts, assembly interfaces and the author's
  arithmetic calibration sequence; record source defects and fidelity limits.
- Add the project manifest, build instructions, measurements and visual evidence.
- Under the pilot's September 23 decision, design a clearly labeled
  simulation-only clearing-loop mounting in place of the unresolved elastic
  clip mounting. Preserve upstream assets and map each replaced occurrence;
  verify the replacement's own travel and retention rather than attributing
  its behavior to the original printed design.

## Capabilities

### New Capabilities

- `curta-assembly`: Complete, traceable assembly of the standard three-times-scale
  Curta, with the source's geometry and physical interfaces accounted for.
- `curta-operation`: Selector setting, crank operation, decimal carry, addition
  and subtraction, carriage position and clearing, exercised through repeatable
  calibration demonstrations.

### Modified Capabilities

None; this project has no existing behavioral specifications.

## Impact

Adds Python simulation code and tests, a `pyproject.toml`, build exclusions and
project-owned OpenSpec records. Upstream CAD, STLs and the manual remain the
source material. Uses the workspace's machinome motion API and exact STEP
adapter. Keeps the project's existing license and attribution.

This is prescribed kinematics with explicit arithmetic state, not a force,
friction or spring-force solver. Upstream optional modifications are not selected.
The explicitly authorized simulation-only clearing-loop mounting is a new
project-owned exception, not an original-source or fabrication claim.
Delivery requires honest geometric evidence: an unresolved source defect or
unproven drive interface is recorded as unfinished work, never a passing test.

On 2026-09-15 the pilot approved replacing the original operation-oriented
controls with direct mechanical interaction and retained Time.running state.
The user chooses the order; no control prepares or repairs an operation by
moving another control. The approved command inventory and acceptance work
are recorded in `simulation/docs/direct-operation-2026-09-15.md`.
Implementation depends on proposed, not yet ratified, framework
`direct-part-motion` and viewer `slide-and-turn-parts` changes. This does not
archive or waive the project's outstanding geometric verification.
