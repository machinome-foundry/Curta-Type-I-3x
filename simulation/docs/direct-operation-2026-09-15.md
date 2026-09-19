# Approved direct-operation redesign — 2026-09-15

The pilot approved implementation of the physical interaction inventory below.
The user decides what to do and in what order. The simulation admits the motion
that its mechanical model permits; it never substitutes a sensible operation
for the attempted movement. This replaces decisions 5 and 8–10 of the original
pose-driven design, not its geometry provenance or validation obligations.

## Physical inputs

| Touched part | Independent movement/request |
| --- | --- |
| Each of eight setting selectors | Move that selector along its ten detents, top 0 to bottom 9. |
| Crank | Lift/lower it to its two engagement positions; separately click for one clockwise revolution or drag for partial rotation. |
| Carriage | Lift, rotate through its six working positions, and lower, as separately requested movements. |
| Reversing lever | Move up/down to choose the counter's relationship to crank engagement. |
| Clearing ring | Sweep in either permitted direction, partially or fully, acting only on the dials its teeth reach. |
| Clearing loop | Deploy/stow about the printed rivet mounting, using this design's retention. |
| Each lower and upper decimal marker | Move that individual marker on its own track, without arithmetic effects. |

There is no single number slider, register editor, add/subtract/multiply/divide
button, automatic carriage positioning, reset-both-registers command, or
page-local commit. Named inputs/instructions exposed by the normal viewer's
panel are alternate requests for these same physical actions, not a second
calculator. Demonstration and new-session setup remain visibly separate.

## Mechanical response and state

Use Time.running and the run's admitted state. The selectors, engagement,
crank phase and carriage position at each tooth passage determine its effect;
changing a setting does not replay previous revolutions with that new value.
Carry, borrow, both register moduli, counter reversal and partial clearing
remain after the user releases the pointer. Determinism comes from a stated
snapshot plus replayed actions, not from editable starting-register sliders.

Preserve the measured subtraction stroke (9 mm), carriage lift (6 mm), selector
pitch (6 mm), carriage pitch (20 degrees) and six working detents. Declare
travel bounds, detents and the measured/ documented locking relationships in
the mechanism, so an ordinary Python request has the same result as a pointer
gesture. Include seated-carriage shift attempts, unseated-crank attempts,
between-detent seating, clearing-ring intermediate positions, ratchet reversal
and locked mid-cycle adjustments. Where the real mechanism permits backlash
or partial movement, do not replace that travel with an idealized UI rejection.

The user is free to attempt a mechanically blocked action or a mechanically
valid action that yields an unwanted calculation. The former stops according
to the modeled restraint; the latter actually happens. Do not undo a valid
movement because its arithmetic was inconvenient.

This remains prescribed kinematics with declared constraints. It does not yet
claim a force/contact solver, spring-force prediction, fracture under excessive
force or manufacturing certification. Unsupported physical effects and missing
engagement proof must be named, not presented as complete physical simulation.

## Evidence and dependencies

Operating references: the manufacturer's
[instruction booklet](https://sliderulemuseum.com/Manuals/Your_CURTA_Calculator_Instructions.pdf),
the [instruction transcription](https://trmm.net/curta/), and this project's
`Manual/Curta Build Manual.pdf`. The printed loop clips onto glued rivets
(build manual page 38); do not add the original machine's release button.
Existing project measurements remain authoritative for the scaled geometry.

The approved target is not implemented yet. The framework currently declares
only Button and Turn controls and refuses controls on a two-joint body. The
viewer also requires a rotational placement for a button. The prerequisites
are proposed separately, awaiting ratification:

- Framework `direct-part-motion`, in `machinome/WTs/direct-part-motion`:
  Slide plus explicit selection of an existing posing joint.
- Viewer `slide-and-turn-parts`: sliding gestures and separately reachable
  lift/turn handles on one part, always submitting requests to the same run.

Do not import viewer code into the framework or modify those packages from
this project. Do not describe proposed APIs as currently available. The old
calculator page still represents the implemented control behavior.

## Acceptance work

The subsequent [resumption prerequisite checks](direct-operation-prerequisites-2026-09-15.md)
record the installed direct-motion and markings capabilities, the still-open
viewer pairing, and a reduced retained-angle clearing declaration refusal.
They do not mark this approved redesign as implemented.

Prove the new behavior red before implementing it. Replay the page-53
calibration sequence, carries/borrows through both full banks, input changes
between turns, subtraction and reversing-lever combinations at all carriage
positions, partial crank/release/resume, selective clearing in both directions,
and mechanically blocked actions in user-chosen orders. Every selector and
marker must remain independently addressable.

Verify actual pointer input on the real model through the standard hosted
viewer and standalone export, using public control locations and run readback.
Inspect rest, moving and stopped snapshots. Run heavyweight geometry checks
sequentially with the resource limits in the existing pause report. Preserve
and report the previously recorded whole-machine thread/contact failures
separately; this controls work does not waive them or finish the older change.
