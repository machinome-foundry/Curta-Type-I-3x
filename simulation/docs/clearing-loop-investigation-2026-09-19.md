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

## Second-seat trial, 2026-09-20

`tools/clearing_loop_clip.py` independently reads the original native arcs and
source placements. The source clip centres are 28.450638765 mm apart; the
mounted rivets are 27.600000000 mm apart. Consequently, rigidly centring the
first clip cannot also centre the second. This does **not** prove the working
printed design defective: the manual explicitly requires clipping and permits
fitting, and this measurement does not account for elastic assembly strain.

At the radial deployed diagnostic pose (swivel −90°), the actual second rivet
is at (31.095555539, 25.948341482) in the loop's own frame, .9066224 mm from
the original second cavity centre. The unmodified endpoint contract fails
natively with 26.551689793 mm³ of second-rivet overlap
(`clearing-loop-seat-red.log`).

Trial **T05**, `clearing_loop_seat.py`, opens only a cylinder R3.8 through the
source's 5.46 mm thickness at that measured position. It preserves the first
clip, the complete finger loop, and all material outside that bounded cutter.
It adds no material and remains one valid native solid. The comparison image
`clearing-loop-seat-comparison.png` was inspected: source second clip is grey
on the left, trial is green on the right. This cropped inspection is not the
installed geometry or an operating control.

Trial **T06** raises the whole loop .05 mm off its cover seat, without moving
either rivet. Before this locational allowance, all three endpoint tests pass
natively but the faceted cover contact is positive by 4.702446138e−6 mm³.
No Boolean epsilon is used. With the named gap, all three endpoint/fidelity
tests pass on both kernels (20.72 s faceted, 2.83 s native), recorded in
`clearing-loop-seat-gap-{faceted,exact}.log`.

The original first clip separately passes native and faceted captive-bearing
checks at 0°, −45° and −75°: ±.02 mm radial motion is free, ±.2 mm is blocked,
and its unchanged head blocks .7 mm upward motion. This establishes an
attached snap-on bearing, **not** a permanently attached hinge. The first
clip's measured throat is only 6.2 mm across versus the rivet's 7.5 mm bearing
diameter; rigid straight-out removal is not its assembly mechanism.

T05/T06 remain diagnostic candidates, not adopted operating fits. The
intervening second-clip passage, retained grip and neighbour sweep must be
resolved before a deploy/stow input is wired into `OperatingCurta`.

The additional head/bearing retention contract passes: 4/4 total under each
kernel (`clearing-loop-seat-capture-{faceted,exact}.log`, 2.26/3.27 s).
Both rivet heads permit .2 mm upward play and block .7 mm; the first bearing
retains its ±.02 mm free / ±.2 mm blocked radial checks after the .05 mm rise.
This is axial/radial capture, not proof of a second-clip snap detent.

`tools/clearing_loop_contacts.py --seated` probes −95..15° in one-degree
steps at the fitted height against both rivets, cover, collar/washer/nut,
housing and the source crank. Native solids are used where available and
unchanged source STLs otherwise. The 111-pose sweep has two contact intervals
inside −90..0°: −89..−78° and −70..−63°, exclusively against the second rivet.
The largest sampled contact is 3.034345403 mm³ at −84°. At −92° and beyond,
the collar/washer also obstruct travel. The complete readings are in
`_build_running/clearing-loop-seated-path.jsonl`.

Importantly, the independent local probe `tools/clearing_loop_passage.py`
locates those contacts on the **lower, body-side mouth wall**, not the thin
free upper lip. At −84° the local contact bounds are X29.082..31.063,
Y21.129..22.189 mm; the second interval reaches the lower mouth corner at
(23.542395, 17.104551). Thus simply bending the obvious free lip would not
resolve this particular rigid-path conflict. Do not erase the wall along
the swept peg path and then claim the original snap retention was preserved.
Clipping remains open pending a justified compliant/assembly path; the
operating model and its existing Studio navigation are unchanged by T05/T06.

## Additional local assembly-video review, 2026-09-21

Four new contact sheets were inspected: 30:00–36:15 and 36:30–41:30 at
15-second sampling, 38:00–39:00 at two-second sampling, and 44:30–end at
eight-second sampling. The [review record](evidence/clearing-loop-video-review-2026-09-21.json)
pins the local video's hash and duration, exact sampling filters, and all
four generated image hashes. The 38-minute views show the loop already
attached when the black top-cover assembly is installed; the later sampled
operation views still do not resolve clip release or elastic passage.
These are inspected frames, not a claim that the entire film lacks a useful
moment. They justify no permanent hinge, additional material removal or
deploy/stow path. The user's video and generated sheets remain unstaged,
and the clearing-loop task remains open.

## Primary-source follow-up, 2026-09-23

The local manual's page 38 is inspected again: it specifies two glued rivets
and testing clip/unclip fit before gluing, with possible part modification.
It does not supply a rigid swivel path or a deformation law. The maintainer's
[2016 assembly account](https://wudev.digitaltorque.com/articles/curta-9/)
discusses assembling these parts and operating the clearing mechanism, but
does not establish this print's clip-release trajectory.

A [first-person historical owner account](https://www.vcalc.net/cu-news.htm)
distinguishes the later plastic clearing lever's snap-on fixed post from the
older metal lever's spring-loaded release. This concerns original machines,
not a validated deformation model for the present 3x printed parts; it does
not justify adding the metal release button here.

The project's original README explicitly points to mcmaven's
[Curta Calculator Mods](https://www.thingiverse.com/thing:3126676) for other
adaptations. That primary listing returns no readable design body in this
session. Mirrored descriptions are a research lead only, not authority to
replace the current mounting or import an unverified alternative. The local
tracked `Mods/` files contain no clearing-loop replacement. No new fitting,
permanent hinge, clip deformation or deployment control is adopted from this
search. A measured source-backed clip/assembly path, or an explicitly chosen
alternative mounting with its own provenance and proof, remains necessary.
