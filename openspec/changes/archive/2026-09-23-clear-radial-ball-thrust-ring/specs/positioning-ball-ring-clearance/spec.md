## Purpose

Allow the positioning ball's supported radial passage beneath the thrust ring
without losing the collar and spring seats that support the carriage stack.

## ADDED Requirements

### Requirement: Radial positioning movement clears the seated thrust ring

The simulation SHALL keep the unchanged positioning ball clear of the complete
seated thrust ring throughout its supported radial travel and carriage lift.
The ring and both supporting neighbours SHALL remain present.

#### Scenario: Move the ball outward and raise the carriage

- **WHEN** the ball occupies any supported radial position and the carriage
  moves through its full supported lift
- **THEN** the ball does not penetrate the ring
- **AND** neither shorter travel, a smaller ball nor hidden material replaces
  the required passage

### Requirement: Ring fitting preserves the supported carriage stack

The fitted ring SHALL remain one valid connected solid, with removal confined
to independently documented underside passage bounds. The complete upper
spring seat, outer collar-support material, installed ring placement, other
parts and motion laws SHALL remain unchanged.

#### Scenario: Inspect and perturb the seated stack

- **WHEN** the maker inspects the ring and its neighbouring supports throughout
  carriage lift and shift
- **THEN** the original spring and collar seating contacts retain their
  measured free play and capture
- **AND** no added spacer, relocated seat or removed support conceals contact

#### Scenario: Detect an invalid passage

- **WHEN** the passage is omitted, misplaced or removes protected material
- **THEN** the clearance or preservation checks fail
- **AND** positive overlap is not accepted through a volume tolerance

### Requirement: Local ring completion does not imply ball-motion adoption

The completion record SHALL identify source preservation, full-path ring
clearance, retained supports, negative controls and inspected geometry while
keeping unresolved other contacts and final operating acceptance explicit.

#### Scenario: Complete the ring correction

- **WHEN** the bounded ring correction is adopted
- **THEN** the record identifies its passing local evidence
- **AND** the ball's complete moving-interface and viewer acceptance remain
  separate gates unless independently verified
