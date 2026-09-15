## ADDED Requirements

### Requirement: Direct mechanical controls
The maker SHALL operate the simulation by handling each physical control:
eight independent input selectors, crank lift and rotation, carriage lift and
rotation, reversing lever, clearing ring and deployable loop, and each decimal
marker. The normal operating surface SHALL NOT contain an aggregate operand
slider, an arithmetic-operation command, editable register contents, or an
automatic lift-shift-seat or lift-clear-seat sequence.

Each gesture SHALL request movement of the touched mechanism. A crank click
SHALL request one clockwise revolution, and dragging SHALL permit partial
travel. The user SHALL choose the action order. No control SHALL prepare or
repair another mechanism's position in order to make a request succeed.

#### Scenario: Set an input digit
- **WHEN** an input changes from zero to nine
- **THEN** its selector moves from the top detent to the bottom detent and its
  matching transmission gear follows the measured selector travel, without
  changing any other selector or the retained register contents

#### Scenario: Shift a decimal place
- **WHEN** the carriage is lifted, advanced one position and reseated
- **THEN** the input's contribution to the result is multiplied by ten and the
  physical carriage aligns with the next digit position

#### Scenario: Independent crank movements
- **WHEN** the maker lifts the crank and subsequently turns it
- **THEN** the lift and rotation occur as independent physical actions, and
  the resulting contribution follows the actual engagement state

#### Scenario: A nonsensical request meets the mechanism
- **WHEN** the maker attempts to shift a seated carriage, seat it between
  working detents, turn while it is unseated, or reverse against the ratchet
- **THEN** the run admits only movement allowed by the declared mechanical
  restraints and reports any stop without repositioning another control,
  silently dropping the request, or changing retained state beyond admitted travel

#### Scenario: A mid-cycle attempt does not become an operation macro
- **WHEN** the maker attempts to change a selector, crank lift, carriage or
  reversing lever while its physical locking mechanism is engaged
- **THEN** the declared lock limits movement and no controller completes the
  crank cycle or schedules the attempted movement for later

#### Scenario: Reversing the turns counter
- **WHEN** the maker moves the reversing lever and then turns the crank
- **THEN** the counter's direction follows the lever and crank engagement,
  while the result contribution follows the crank engagement independently

#### Scenario: Decimal markers are independent annotations
- **WHEN** one decimal marker is moved along its own track
- **THEN** only that marker moves, within its mechanical limits, without
  changing a selector, register value or another marker

### Requirement: The mechanism retains its state
The simulation SHALL retain register and partial-motion state in the running
mechanism. Changing an input SHALL NOT recompute past crank turns with that
new input or require a page-local register commit. Readouts SHALL report the
mechanism, not an independently maintained calculator result. Restoring a
documented run snapshot and replaying the same physical requests SHALL
reproduce the same machine state.

#### Scenario: Change the operand after a turn
- **WHEN** the maker sets three, turns once, changes the selectors to two and
  turns again from a cleared, normally engaged machine
- **THEN** the result reads five and the counter reads two, without a commit
  command, reset of crank history or explicit starting-register entry

#### Scenario: Release and resume a partial crank movement
- **WHEN** the maker turns part way, releases, and resumes turning
- **THEN** the machine continues from its admitted partial position without
  rewinding, discarding a carry, or counting the same tooth passage twice

### Requirement: Author calibration sequence
The simulation SHALL reproduce the arithmetic and associated mechanism motion
of the calibration checks on page 53 of the build manual.

#### Scenario: Zero and successive carries
- **WHEN** cleared registers receive successive crank turns with inputs 0, 1,
  9 and 90
- **THEN** the result register reads 0, 1, 10 and 100 respectively, and the
  turns register reads 1, 2, 3 and 4

#### Scenario: Cascade through both registers
- **WHEN** all eleven result dials and six turns dials start at nine and the
  maker adds one
- **THEN** every result and turns dial returns to zero through the carry sequence

#### Scenario: Add and subtract one
- **WHEN** the maker adds one to cleared registers and then subtracts one
- **THEN** both registers return to zero

### Requirement: Carry engagement and reset
The simulation SHALL move each carry lever and gear consistently with the
manual's depressed, engaged and reset positions.

#### Scenario: Carry into the next digit
- **WHEN** a dial passes nine during addition
- **THEN** its lever enables the adjacent carry gear, the tens bell advances
  the next shaft once, and the mechanism returns the lever to its upper position

### Requirement: Clearing and repeatable demonstrations
The simulation SHALL provide a small named demonstration set that includes
normal addition, carry, overflow, subtraction, carriage shifting and clearing.
Demonstrations SHALL remain separate from ordinary operation, using documented
snapshot setup and physical action replay rather than arithmetic shortcuts.
Ordinary clearing SHALL be performed by the ring with the carriage manually
lifted. Its actual sweep SHALL determine which register dials are cleared;
both allowed sweep directions, partial clearing and the two valid ring rest
positions SHALL be represented. Clearing SHALL NOT automatically lift or seat
the carriage, finish a sweep, or reset an untouched register.

#### Scenario: Clear a register
- **WHEN** the maker completes the clearing-ring movement
- **THEN** the affected dials reach zero and the ring reaches its rest position

#### Scenario: Clear only one register
- **WHEN** the maker lifts the carriage and sweeps the ring through only the
  result register's clearing interval
- **THEN** its dials clear in the swept order and the counter retains its
  previous contents; a separate sweep through the counter acts conversely

#### Scenario: Release the ring between rest positions
- **WHEN** the maker releases the ring part way through a clearing sweep and
  attempts to seat the carriage
- **THEN** the partial clearing is retained and the actual ring/carriage
  restraint limits seating, without automatically finishing the sweep

#### Scenario: Handle the clearing loop
- **WHEN** the maker deploys or stows the printed clearing loop
- **THEN** it moves around its actual rivet mounting and respects the printed
  retention, without inventing the original metal Curta's release button

#### Scenario: Replay a demonstration
- **WHEN** the same documented snapshot and physical-action sequence are replayed
- **THEN** it reaches the same retained state, and geometric sampling checks the
  moving interfaces throughout the demonstration
