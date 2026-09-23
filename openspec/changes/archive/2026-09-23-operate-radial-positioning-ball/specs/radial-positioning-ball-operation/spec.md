## Purpose

Make the positioning ball respond to the bell and carriage collar while
retaining free position and preventing incompatible physical actions.

## ADDED Requirements

### Requirement: The positioning ball follows contact radially and retains slack

The unchanged positioning ball SHALL move along its stationary radial guide
when the bell or collar presses it, and SHALL retain its current position
when neither surface presses. Its source size and axial placement SHALL remain
unchanged, and it SHALL NOT orbit with the bell or gain an independent control.

#### Scenario: Turn the bell through its pocket and return

- **WHEN** the maker turns the crank through the bell's outward contact and
  returns to the open pocket
- **THEN** the ball moves outward without penetrating its neighbours
- **AND** the retreating bell does not pull it back through the free space

#### Scenario: Raise the carriage against the retained ball

- **WHEN** the collar approaches the ball during carriage lift
- **THEN** it presses the ball inward along the same guide
- **AND** source supports and clearances remain present through that movement

### Requirement: Incompatible crank and carriage movement stops at contact

The simulation SHALL stop an incompatible crank or carriage request at the
measured contact limit while preserving admitted travel before that limit.
It SHALL require explicit relief, without automatically lowering, lifting,
turning or finishing another physical input.

#### Scenario: Attempt to turn with the carriage raised

- **WHEN** the maker requests crank travel that closes the ball's available
  space between the bell and raised collar
- **THEN** the request stops at the contact boundary
- **AND** idle, retry and exact replay preserve that retained stopped state
- **AND** explicitly relieving the collar allows the crank to continue

#### Scenario: Attempt to lift against an outward bell contact

- **WHEN** the maker raises the carriage while the bell holds the ball outward
- **THEN** lift stops when the collar reaches the available radial limit
- **AND** the machine does not turn the crank automatically to create room

### Requirement: Radial-ball adoption preserves the rest of the operating model

The simulation SHALL preserve the existing physical controls, original rest
coordinates, other part shapes and ordinary demonstration outcomes. Python and
the current viewer export SHALL agree on the retained ball and complete state
through normal motion, contact stops, replay and relief.

#### Scenario: Operate the adopted model

- **WHEN** the maker uses the existing demonstrations or actual part gestures
  in a hosted or standalone viewer
- **THEN** the existing arithmetic and physical inputs behave consistently
  with the Python model and the ball remains clear of its neighbours
- **AND** no hidden calculator or automatic preparation substitutes for action

#### Scenario: Record local completion

- **WHEN** this positioning motion has been verified and adopted
- **THEN** its source, geometry, retained-state and current-viewer evidence are
  identified in the completion record
- **AND** unrelated whole-machine contacts and unfinished controls remain
  explicit rather than being waived by this local completion
