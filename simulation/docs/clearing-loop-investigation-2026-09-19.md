# Printed clearing-loop investigation

Task 6.4 remains open. No deployment axis, range, fit or running input has
been adopted by this investigation.

Build-manual page 38 explicitly describes clipping and unclipping the printed
ring from the two glued rivets, and allows part modification to obtain that
fit. Its exploded drawing shows two open clip seats, not the original metal
Curta's release button. The page was rendered and inspected locally at
`_build_running/clearing-loop-manual.png`.

`tools/clearing_loop_measurements.py` reads only the two unchanged author STLs
and fits circles to their section outlines. These are approximate mesh
measurements, not native-circle tolerances or a working-assembly proof:

- The ring is a watertight print, local Z0..5.46000004 mm.
- Its finger opening is approximately R19.5 at (91.5, 0).
- Its two clip arcs are approximately R3.825 at (40.5, 0) and
  (30.51, 26.64). Their centre spacing is about 28.45 mm.
- The rivet is watertight, Z0..14.5899 mm. Its lower stem is approximately
  R2.94 and its clip-bearing section R3.75 (sampled at Z9 and Z11).

The native probe `tools/clearing_loop_native.py` confirms both clip arcs are
R3.825, centred at (40.5, 0) and (30.506928, 26.637893), through the complete
5.46 mm thickness. The rivet stem is R2.9375 to Z6.6; its R3.75 bearing section
ends at Z12.6, followed by the retaining head. The native cover's two R3.107
mounting bores are centred at (0, -40.5) and (25.948341, -31.095556), Z0..5.7.
All three native solids are valid. The STEP and print agree here; do not
attribute the mounting question to mesh corruption. Native readings are in
`_build_running/clearing-loop-native.jsonl`.

`clearing_loop.py` is an unconstrained diagnostic, not an operating input.
It retains the fitted cover/carrier, both rivets, covers and source crank,
and permits independently probing swivel about the first source clip and
vertical release. `tools/clearing_loop_contacts.py` is prepared to measure
both native and source-STL neighbours without an overlap epsilon.

## Calibrated diagnostic, 2026-09-20

Two independent world-vertex contracts first failed (0/2): joints mistakenly
declared at the assembly site used part-local axes and a part-local pivot.
Moving those declarations onto the source-part subclass fixes both contracts
(2/2 under each runner). These are placement tests using meshes, not two
independent Boolean-kernel certifications. The actual mounted first rivet is
the rotation datum; a +3 mm release moves only the loop upwards in world Z.
Logs are `clearing-loop-frame-red.log` and
`clearing-loop-frame-green-{exact,faceted}.log` under `_build_running/`.

Discard `clearing-loop-contacts.jsonl`: it used the incorrect diagnostic
frame. The corrected `clearing-loop-contacts-calibrated.jsonl` covers 125
poses: -180..180 degrees at 15-degree intervals, at heights 0, .05, .5, 3 and
8 mm. It uses native intersections where available, source-STL intersections
otherwise, and refuses invalid Boolean results without a volume epsilon.
At source height the sampled interval -75..15 degrees has no positive
overlaps against the included neighbours. At -90 degrees the second rivet
overlaps by 26.55168979 mm³; at +30 degrees the collar and washer overlap by
357.03013760 and 279.94507216 mm³. These are sampled poses, not a continuous
clearance certificate or an adopted travel range. Raising the loop 3 mm
crosses the first rivet's retaining head (20.969650 mm³ at zero swivel), so
vertical release alone is not the clipping action either.

The inspected `clearing-loop-native-top.png` clearly shows the two open clip
mouths. The downloaded video at 39:05 shows the finger loop projecting beyond
the carriage while the builder tests clearing; it does not establish a
deploy/stow path or a retained hinge. The clip throat's elastic passage and
the second clip's seat still require evidence. No geometry was removed and
no operating control was added from this diagnostic.

Next evidence: determine the permitted clip/release path against
the collar and crank. Do not infer a permanent single-rivet hinge or a
horizontal folding hinge merely from the control inventory. The source pose
and the manual's clipping action must establish the actual motion first.
