## ADDED Requirements

### Requirement: Supported result-carry travel clears the frame

The simulation SHALL allow the first two result-carry levers, their fitted
springs and coupled sleeves to occupy their supported raised, preloaded and
lowered positions and traverse their complete 4.2 mm lever travel without
penetrating the upper frame. The frame and installed supports SHALL remain
present and stationary during this movement.

#### Scenario: Initialize the selected carry pair at ninety-nine

- **WHEN** the first three result dials start at `099`, input one is selected,
  the crank is at home, addition is selected and the carriage is seated at zero
- **THEN** both selected levers retain their measured 1.1630815 mm pin preload
- **AND** their springs, sliders and sleeves do not penetrate the frame

#### Scenario: Traverse the two detent positions

- **WHEN** either selected carry lever moves from its raised position to its
  lower position and returns through the supported intermediate positions
- **THEN** the full 4.2 mm travel remains available without frame penetration
- **AND** neither a shorter stroke nor removal of the frame substitutes for clearance

### Requirement: Carry fitting preserves the working mechanical interfaces

The corrected assembly SHALL preserve the selected levers' source-derived
support placement, seated spring folds, retaining hook contacts, slider guides,
fork/sleeve capture, dial-pin approach and reset-cam contact. Clearing a frame
passage SHALL NOT disconnect or relocate the mechanism it supports.

#### Scenario: Inspect an assembled lever throughout its travel

- **WHEN** either selected lever occupies a supported position between its two
  detents
- **THEN** its bearing still guides the slider, the spring remains seated and
  its hooks retain the slider within the measured contact play
- **AND** the fork and coupled sleeve remain engaged with their original
  relative travel and support locations

#### Scenario: Trip and reset the installed carry pair

- **WHEN** each selected stage traverses its supported trip and reset movement
  in the `099` plus one fixture, including the second reset after a revolution
- **THEN** the existing pin, sleeve and reset interfaces retain their measured
  contact behaviour and the moving parts clear the surrounding assembly
- **AND** the correction does not change the carry/reset timing to conceal a collision

### Requirement: A local frame fit preserves the rest of the assembly

The corrected frame SHALL remain one valid connected solid and preserve its
guide-support, fastening, main-shaft, bearing and other station features.
Only the documented local passage regions for the first two result-carry
stations SHALL differ from the original frame. Upstream source files and
attribution SHALL remain unchanged.

#### Scenario: Inspect the corrected frame

- **WHEN** the maker inspects the frame and its mounted assemblies after fitting
- **THEN** the two selected stations have the documented local running gaps
- **AND** support seats, fasteners, shaft alignment and non-selected stations
  retain their original geometry and placement
- **AND** no material is added or removed outside the documented passage regions

### Requirement: Clearance evidence does not conceal unresolved findings

The simulation SHALL distinguish verified local carry/frame clearance from
unresolved whole-machine or running behaviour. A residual obstruction, invalid
part, missing neighbour or damaged support SHALL prevent the affected local
clearance claim from passing, regardless of how small the interference is.

#### Scenario: An inadequate or excessive fit is detected

- **WHEN** a required local passage remains obstructed or its relief damages a
  protected support feature
- **THEN** the affected station and physical interface are reported as failing
- **AND** hiding a part or accepting its overlap does not turn that result into a pass

#### Scenario: The focused correction is completed

- **WHEN** the two selected carry/frame interfaces have been verified
- **THEN** the completion record identifies that bounded result and its evidence
- **AND** unresolved housing, other stations, complete setup, selector admission
  and causal running behaviour remain explicitly outside that result
