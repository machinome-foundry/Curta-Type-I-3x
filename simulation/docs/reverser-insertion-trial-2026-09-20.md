# Trial: can insertion depth calibrate the reversing shaft?

The pilot proposed that the forced insertion shown during assembly might
calibrate the reversing shaft's depth, and requested an attempt to fix the
engagement by that route. This trial changes placement only. No shaft, frame,
detent, operating model or inspection control has been modified.

## Assembly evidence

The original build manual, page 29, explicitly tells the builder to leave the
shaft low while aligning the counter gears, then push it upward and secure it
with the M4 nut, finally engaging one of its two detents. Page 28 separately
describes holding the spring-loaded ball while inserting the shaft into the
knob. Thus resistance while assembling the lever is not by itself evidence of
an adjustable final mounting depth.

Local video frames were inspected at 17:00, 18:00, 19:00, 19:15, 19:30 and
20:00 from the pilot's MP4. They show preparation of the lever and subsequent
installation at the frame, including access to its fastening end. They do not
resolve sub-millimetre shoulder seating, quantify insertion force, or establish
that the maker used a deliberate depth offset. No video was uploaded or
external analysis service used.

## Independent printable-file check

`simulation/tools/reverser_insertion_trial.py` tests the source shaft against
the upper frame, lower plate and top nut in the existing complete diagnostic.
It independently tests the unchanged, watertight shaft, main-body and bearing-
plate STLs in their documented source placements. No STL repair or dimensional
correction is used. File hashes and every reading are preserved in
`_build_running/reverser-insertion-trial.jsonl`.

The narrow upper neck is diameter **5.875 mm**, in a **6.114 mm** frame hole.
The shaft body below it is diameter **7.386 mm**, leaving a positive shoulder.
Its upward-facing shoulder and the frame underside already meet at Z **−22.2
mm**. The neck has nominal radial clearance; the larger shoulder cannot be
advanced into that hole as an unchanged rigid body.

| Additional insertion | Predicted gap to nine-tooth row | Upper-frame overlap: native / source STL |
| --- | --- | --- |
| −1 mm | 1.3075 mm | 0 / 0 mm³ |
| −0.1 mm | 0.4075 mm | 0 / 0 mm³ |
| 0 | 0.3075 mm | 0 / 0 mm³ |
| +0.05 mm | 0.2575 mm | 0.674343 / 0.674103 mm³ |
| +0.3075 mm | Edge contact only | 4.147209 / 4.145870 mm³ |
| +0.5 mm | 0.1925 mm axial overlap | 6.743429 / 6.741270 mm³ |
| +1 mm | 0.6925 mm axial overlap | 13.486857 / 13.482577 mm³ |
| +1.8075 mm | Full 1.5 mm band aligned | 24.377495 / 24.369811 mm³ |

Gap predictions assume the ball stays at its lower pocket centre and the
gear takes the most favourable 0.185 mm fork play. They describe axial band
alignment, not certified flank engagement. All native commons were valid and
all raw-print Manifold operations returned `NoError`. The lower bearing stays
clear at these positions. The fixed source nut begins to interfere with the
neck at the full-band trial (0.099406 mm³); a genuinely repositioned threaded
fastening would need separate assembly validation.

## Outcome

**Insertion adjustment alone does not resolve this reconstruction.** The
manual's upward insertion seats a shoulder already seated in the model;
the original printable files corroborate that stop. Pulling the shaft down
is geometrically possible but worsens the lower-row mismatch. Tightening the
nut cannot authorize interpenetrating the shoulder and frame.

This rules out the simple unchanged-rigid-parts depth correction tested here,
not every real-world explanation. Print compliance, material indentation,
unrecorded fitting or different build revisions remain unmeasured. Modelling
a modified shoulder or recessed mounting seat would be a geometry change,
not insertion calibration, and no such change is adopted by this trial.
Both lever endpoints, ball/spring capture, all six counter inputs and their
full movement would still require verification before an operating fix.

Run with the workspace environment, from the project root:

```sh
python -m simulation.tools.reverser_insertion_trial
```

The probe is successful when its measurements complete, not when the attempted
fit passes. Existing red reversing-assembly acceptance tests remain unchanged.
