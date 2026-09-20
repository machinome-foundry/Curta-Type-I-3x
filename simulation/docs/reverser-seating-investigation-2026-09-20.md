# Reverser seating, not a replacement shaft

No operating stroke, shaft translation, new detent, altered spacer or source
print correction is adopted here. The earlier three assembly acceptance tests
remain red. This investigates an alternative to the withdrawn detent redesign.

Detent centres need not be working endpoints: a spring ball can bear on a
pocket flank against an independent stop. The native cone axes confirm centres
at local Z78.6 and Z90.6, both on +X, apex X.81 and half-angle 63 degrees.
`tools/reverser_measurements.py` now reports those analytic centres instead of
approximating them from conservative face bounding boxes. Their separation is
12 mm. The inspected `reversing-shaft-native-front.png` shows both unchanged
pockets. `reverser-detent-extents.jsonl` preserves the native surface data.

## Ball-following diagnostic

`tools/reverser_detent.py` independently intersects an R2.5 faceted sphere with
the author's unchanged shaft STL. At knob displacement +3.9075 mm (the already
measured upper spacer seat with .05 mm gap), radial ball contact lies between
4.252474785 and 4.252481461 mm from the shaft axis. At the lower detent centre,
-6.8425 mm, it lies between 3.615931511 and 3.615938187 mm. The unchanged source
ball placement has radial distance 5.531068964 mm, so simply translating that
ball axially cannot represent its spring-loaded seating. Between pockets, at
the source knob height, that same ball penetrates the print by 1.359006219 mm³.
This is a faceted contact probe, not a validated spring law or retention test.

The probe's native-sphere common is **not a reliable reference**. Below a
cone centre it can report zero where the print and the analytic cone require
contact. For example the lower frame-seat candidate at -7.6427 mm gives mesh
contact radius 4.023290634..4.023297310 mm, but a native search falsely gives
3.208091736..3.208098412 mm. At the source height a sphere centred at radius
2 mm gives native zero but print overlap 54.330470331 mm³. Some other native
commons are invalid and were refused. Changing the sphere's pole direction
does not resolve this. No volume tolerance or assertion exclusion is used.

Logs under `_build_running/` preserve both failed searches
(`reverser-ball-seating-{z,oblique}-seam-refused.jsonl`) and the final comparison
(`reverser-ball-seating.jsonl`). The final probe uses the source print to locate
contact; `--native` audits native commons .01 mm either side without presenting
them as accepted clearance. This is evidence about this source/kernel Boolean,
not proof of a physical defect or a framework defect.

## Complete input stack

`tools/reverser_stack_stops.py` moves knob and all six input stacks together
through nine candidate heights from -7.6427 to +3.9075 mm, including both the
lower detent centre and the proposed shorter-stroke lower region. It keeps both
drum halves, both frame stops and all six shafts/carry stacks. Native common
tests find no additional lower axial stop at those sampled parked-crank poses.
Thus the hypothesis that a hidden gear-stack stop retains the lower ball on
its flank is not established. These samples are not a continuous movement or
full crank-cycle certificate.

The sixth input print overlaps the source yoke by 1.585791285 mm³ at every
sampled height; this relative contact needs its own measured fit. Ball and
spring are explicitly excluded from this stack diagnostic because their radial
following is unresolved and is measured separately above. This exclusion is
not made in any whole-machine acceptance contract. Output:
`_build_running/reverser-stack-stops.jsonl`.

Continuation: establish a source-backed pair of retained endpoints and the
complete knob/yoke/spring fit before adding the operating reversing input.
Neither a 9 mm stroke nor a 12 mm stroke is certified by these findings.
