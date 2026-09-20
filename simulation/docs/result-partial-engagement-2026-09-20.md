# Actual result-row engagement between working positions

The operating result law previously treated any crank lift below 4.5 mm as
addition and any lift at or above 4.5 mm as subtraction. It also used a
fractional selector setting as a fractional number of teeth. Those rules
agree at the working endpoints but do not describe the printed drum between
them. Counter reversal already has an axial-overlap mapping; this increment
applies the same physical question independently to the lower result drum.

## Failure and correction

The native `ResultEngagement` bench first failed with the production law:
selector 3, crank lift 1.5 mm, crank angle 39°, first input stack/drum overlap
0.321982036 mm³. The complete printed drum and fitted input stack were used;
no tooth was omitted (`_build_running/result-partial-lift-red.log`, 0/1).

`result_modes.py` records the lower drum's 37 occupied axial bands from
Z−67.8 down to −121.8 mm, each 1.5 mm thick. Their counts come from the actual
source segment names and are guarded against the placed source meshes.
The two segments at Z−73.8 share their final tooth; their union is nine teeth,
not ten. Every train shares its angular terminal tooth, so simultaneously
engaging several rows uses the longest train, not their sum.

The ones stack has pinions at Z−64.92499975 and −58.92499975; higher stacks
have one at Z−64.92499975. Selector travel moves them down 6 mm per digit;
crank lift moves the actual drum upward. Positive axial overlap chooses
the encountered source trains. Face touching alone is not engagement.

At selector 3 and lift 1.5 mm, the first two channels meet eight and seven
teeth respectively, rather than both meeting three. A first selector at .25
with the crank down reaches the ten-tooth row, not a quarter-tooth. These are
unwanted partial-input consequences, not new recommended operating positions.
All ten integer settings retain the established addition/complement counts
at crank lifts 0 and 9 mm, including the ones channel's extra complement tooth.

Only the simulation motion law changes. There is **no new print fit**, no
change to the source drum, no rounding/snap to a detent, and no automatic
preparation of another control. The older prescribed-pose and clocked siblings
retain their existing working-position laws.

## Validation scope

Three numeric mode checks pass, covering both working modes, actual partial
counts and the absence of fictional fractional teeth. The geometry suite
passes 4/4 faceted (5.62 s): source band table, every sampled driving tooth,
five partial crank heights, and six partial-selector/lift combinations.
Full revolutions are sampled every 3° using both the ones and ordinary input
stack. All four native checks also pass (333.63 s), recorded in
`_build_running/result-partial-engagement-exact.log`. The partial-pose snapshot
`result-partial-engagement.png` (selector 3, lift 1.5 mm, crank 60°) was
rendered and inspected; both input stacks and their engaged bands are visible.

The retained partial-selector test passes: first selector .25 followed by a
full revolution produces result 10; returning the selector to zero and turning
again leaves result 10 and counter 2. Restoring the intermediate snapshot and
replaying produces the identical final snapshot. No register is directly set.
The combined retained run passes 3/3 (923.007 s), including the complete
page-53 calibration and subtraction from zero followed by addition through
both full register banks. Log: `result-running-regression.log`.

The actual operating build succeeds, version 7 with 25 controls and all 155
unique model/decal references present. The hosted pointer probe passes again
with no page errors: selected crank lift, independent first selector, seated
carriage/clearing stops and reversing-knob down/up gestures. These remain
scoped committed-frame gestures, not a standalone/full-stroke certificate.
`result-operating-browser.json` records document SHA-256
`a15c92eb9dc0b8e6e2c8bfa820a101a9a1ef379d06f86b1802d2d0765c411586` and
viewer bundle SHA-256
`329015221a9e2968a2c7dccc80af30f2890d6365a8f19639bcde54db182ef4fd`.

This is an engagement correction, **not completion of the wrong-order
restraint work**. The benchmark starts each fixed-setting sweep in its
matching tooth phase. It does not prove that changing a selector/lift while
already engaged is admissible, or that a misphased retained gear can enter a
new row without meeting a mechanical stop. Those action-order cases remain
separate obligations; no synthetic global “crank not home” lock is invented.

## Next action-order finding: the closing locking disc

`result_action_order.py` is a separate retained two-channel diagnostic, not
a newly constrained operating model. `tools/result_action_order.py` starts
at selector 3, turns to 120°, withdraws the selector to zero, turns to 150°,
then returns it to 3 and continues. The shaft angles genuinely remain at
189.6° and 41.6° after withdrawal; no readout or register is directly seeded.

Checking the lower drum alone finds no contact at the first resumed poses,
but eventually finds 0.264561692 mm³ at crank 450°. Including the real bell
and both shaft lockouts exposes the earlier relevant restraint: at 150°,
the ones lockout/bell intersection is 1.080401810 mm³ and the tens assembly's
is .025109092 mm³. The requests currently report completed despite these
contacts. Logs: `result-action-order.jsonl` (drum-only first pass) and
`result-action-order-with-lockouts.jsonl` (expanded diagnostic).

`tools/result_lockout_boundary.py` now isolates the identified native ones
locking disc at source Z−23.1 and fitted pentagon at Z−22.65 to measure its
closing contact versus actual retained shaft angle. This is evidence for
the next restraint, not an adopted global lock or a new geometry correction.

The reduced running probe's first attempt failed before contact measurement
because a numeric constant latch left a literal `False` in its symbolic
program. The bench now supplies the same typed latch input that the production
law receives. This changes neither production geometry nor its operating law;
it is not recorded as a mechanical failure.

After that diagnostic wiring correction, the complete geometry suite was
rerun: 4/4 faceted in 6.18 s and 4/4 native in 427.90 s. Final logs are
`_build_running/result-partial-final-faceted.log` and
`_build_running/result-partial-final-exact.log`.
