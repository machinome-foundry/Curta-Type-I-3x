## ADDED Requirements

### Requirement: The selected input traverses its complete range at stationary home

The fitted ones input SHALL traverse all ten numbered detents and every
intermediate position in both directions at the initial and post-cascade
stationary home fixtures. Its knob and keyed input group SHALL retain the
full 54 mm stroke, 6 mm detent pitch and original shaft axes. Moving parts
SHALL remain clear of the installed housing and other obstacles throughout
the travel, except for their supported, non-penetrating working contacts.

#### Scenario: Select a digit before the first turn

- **WHEN** the ones selector traverses zero through nine and returns in the
  seated, addition-only fixture with the result wheels at `099` and crank at home
- **THEN** every numbered detent and the full intervening travel remain available
- **AND** the result wheels, output shaft rotations, other inputs, drum and
  preloaded carry stages retain their fixture positions

#### Scenario: Select zero while the second carry reset is pending

- **WHEN** the ones selector changes from one to zero, and traverses its
  remaining range in both directions, after the cascade has reached `100`
  and the crank is stopped at one revolution
- **THEN** the first carry remains released and the second remains latched
- **AND** no wheel, output shaft or carry moves as a consequence of selecting
  the next input

### Requirement: The selected detent remains assembled throughout travel

The selected input SHALL use the manual's nominal 5 mm ball and an installed
spring whose dimensions and seating are traceable to the source and manual.
The ball SHALL remain guided and supported by the shaft's detent surface;
the spring SHALL follow its installed displacement while remaining retained
at both ends. The ten seated detents and the transitions between them SHALL
have supported geometry without ball, spring or guide penetration.

#### Scenario: Inspect a numbered detent

- **WHEN** the selected input occupies any of its ten numbered positions
- **THEN** the ball is retained in its guide and supported at that detent
- **AND** the spring remains seated against the ball and its back support
  without passing through either part

#### Scenario: Inspect a between-detent position

- **WHEN** the selector passes a detent crest or settles into the next detent
- **THEN** ball displacement and spring deformation follow the actual working
  surfaces throughout the transition without penetrating adjacent material
- **AND** an endpoint-only pose or an undeformed spring does not substitute
  for the intervening assembled geometry

### Requirement: Selector fitting preserves numbering and mechanical capture

The selected shaft and number roll SHALL retain their ten seated angular
positions, 36 degrees apart, and their original supported alignment. The
selector screw SHALL remain captured by the helical groove, and the ones
input group's lower gear SHALL remain captured between the knob fingers
throughout the selected travel. Relative motion beyond the measured working
play SHALL be obstructed by the appropriate working faces in both directions.

#### Scenario: Advance and return the selected input

- **WHEN** the knob moves through the range in either direction
- **THEN** the shaft and number roll reach the corresponding numbered detents
  and the keyed group follows the knob's axial travel without changing its
  fixture rotation
- **AND** the screw/groove and gear/fork interfaces remain coupled, including
  between numbered settings

#### Scenario: Detect an input disconnected by fitting

- **WHEN** the keyed group or selector shaft is independently displaced beyond
  the measured play of its capture interface
- **THEN** the appropriate opposing working face obstructs that displacement
- **AND** removing the capture face or losing the follower invalidates the
  claimed fit even if the parts no longer intersect

### Requirement: Only documented fixed joints can retain source overlap

Only the selected screw/knob threaded joint and bottom/top shaft join SHALL
be eligible for the local fixed-seat inventory. Each accepted entry SHALL
identify an unchanged, supported source joint with constant relative pose
and a measured overlap region and volume. New, missing or changed entries
SHALL invalidate that inventory. Moving interfaces SHALL NOT be accepted as
fixed seats or exempted because their penetration is small.

#### Scenario: Verify a fixed source joint

- **WHEN** either candidate joint is inspected throughout the selected input's travel
- **THEN** its two parts retain their supported relative pose and documented
  overlap region without obstructing a moving neighbour
- **AND** a change in that region, joint placement or support prevents acceptance

#### Scenario: A moving interference is reported

- **WHEN** a ball, spring, helical follower, gear/fork or housing interface
  has positive penetration or an invalid contact result
- **THEN** the affected interface remains failing
- **AND** it is not added to the fixed-seat inventory to make the fit pass

### Requirement: A selected-input correction preserves the surrounding machine

Apart from the documented ball replacement and installed spring representation,
rigid material removal SHALL be confined to documented local regions of the
selected knob's ball guide, screw's non-threaded follower tip and housing
slot/window edges. The correction SHALL preserve shaft detent/groove working
surfaces, screw threads, spring back support, knob fork, keyed gear, bearings,
housing supports and fastening features. The other seven selectors, output
and carry mechanisms, and the completed carry/frame fit SHALL retain their
existing geometry and placement. Upstream files and attribution SHALL remain
unchanged; every original physical body SHALL remain accounted for.
Each fitted rigid part SHALL remain a valid connected solid, with no added
material outside the explicitly documented hardware/spring replacements.

#### Scenario: Inspect a local relief

- **WHEN** the fitted input and housing are compared with the original source
- **THEN** source-derived rigid reliefs occur only in the documented permitted regions
- **AND** retained supports and working interfaces keep their source geometry,
  alignment and mechanical function

#### Scenario: A proposed cut would damage a support

- **WHEN** a required relief reaches a protected thread, support, groove,
  detent or capture face, or a non-selected station
- **THEN** the proposed fit is reported as unresolved
- **AND** no broader cut, relocation or omission is silently substituted

### Requirement: Local selector acceptance remains distinct from running acceptance

The project SHALL distinguish verified selected-input geometry from unresolved
whole-machine and history-dependent running behaviour. Acceptance SHALL cover
the entire selected travel and every installed neighbouring interface, not
only a set of displayed poses. The existing calculator controls and repeatable
demonstrations SHALL retain their supported behaviour without being presented
as a causal running simulation.

#### Scenario: Complete the selected-input correction

- **WHEN** the local selector fit is reported as complete
- **THEN** its full-travel, support, capture, fixed-seat and preservation
  evidence are identified, together with any remaining project findings
- **AND** the full angular home window, complete setup, outgoing-carry boundary
  and causal running behaviour remain separate acceptance obligations

#### Scenario: A sample grid misses the remaining proof

- **WHEN** sampled poses clear but the path between them or a possible
  neighbouring obstacle has not been bounded
- **THEN** complete selected-input clearance is not reported as verified
- **AND** hiding an obstacle or reducing the selected range does not complete it
