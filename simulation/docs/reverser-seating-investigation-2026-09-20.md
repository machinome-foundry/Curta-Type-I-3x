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

Unvalidated next hypothesis: the upper frame stop may retain the upper ball
on its cone flank while the lower ball reaches its true centre. That gives
about 10.75 mm knob travel, not 9 or 12 mm. A different vertical seating of
the separate actuator in the knob could then put the lower input pinions into
the nine-tooth band without changing either shaft detent. Measure the actual
knob/actuator slot before assuming that adjustment is available; the .185 mm
gear/yoke play alone is insufficient. Also measure the actual source ball
centre and radius rather than relying on its part name: the downloaded video's
automatic captions say “six millimeter” at 17:23 whereas the CAD names a 5 mm
ball. That discrepancy is evidence to check, not authority to substitute one.

## Actual ball and separate yoke seat

`tools/reverser_knob_seat.py` now measures the actual native spherical face:
its radius is **2.7 mm**, not the 2.5 mm implied by the part name. Its centre
does coincide with the source placement at
(19.505705679, 59.407726119, -53.7575). Manual page 28 specifies a bought
5 mm ball; the video's 6 mm caption is not consistent with either value.
The earlier R2.5 radial probe therefore describes the manual's nominal
hardware, not the actual CAD ball. It is not sufficient to certify the
represented assembly. The probe now defaults to the measured R2.7 and names
the radius in every output row; the nominal comparison remains explicit via
`--ball-radius 2.5`. No operating ball or spring has been changed.

The yoke is not fitted into a narrow vertical knob slot. Its bottom rests
at the knob shoulder Z-46.2575 and its top is Z-41.7575. The upper spacer
begins at Z-41.1575: the source assembly has .6 mm total axial space above
the yoke. Both kernels find it clear at positive rises through .6 mm, and
blocked by the upper spacer at .61 mm (.265071880 mm³ native,
.262499221 mm³ faceted). Negative .1 mm meets the knob shoulder
(8.633033550 mm³ native, 8.480464319 mm³ faceted). At the exactly flush
source shoulder, native common is zero and faceted common is 1.31e-11 mm³;
no positive common is waived as clearance. Output is
`_build_running/reverser-knob-seat.jsonl`.

This establishes available play, **not** a rigid .55 mm raised mounting or
a retained working endpoint. The knob, floating spacers and yoke must keep
their physical support through travel. Shaft fastening-seat checks are next;
neither a new shaft placement nor new detents are adopted by this probe.

The fastening-seat probe (`tools/reverser_shaft_seat.py`) closes the simple
shaft-repositioning alternative: its R3.693 shoulder is already seated at
the upper frame's underside Z-22.2. The frame bore is R3.057. Raising the
unchanged shaft .05 mm intersects the frame by .674342863 mm³; +.5 mm gives
6.743428631 mm³. Source rest, -.1 and -.6 mm are clear, but lowering would
move the detents in the unhelpful direction. The lower bearing and upper nut
remain clear at the sampled heights. No shaft translation is adopted.

## Printable files qualify the yoke hypothesis

The actual `STLs/27 - Assemble Reversing Lever/reversing lever knob.stl`
contains **both** knob and yoke, not a separately supplied actuator print.
Its two closed mesh components meet at the same shoulder plane. Thus the
separate CAD bodies do not establish an independently adjustable working
yoke. Treat the .6 mm space above it as an envelope measurement only; raising
the yoke within that space would detach it from its printed shoulder and is
not an authorized assembly correction. This withdraws the raised-yoke
hypothesis above rather than quietly adopting it.

The original printable upper drum also agrees with the STEP's tooth rows.
`tools/reverser_print_rows.py` cuts each 1.5 mm band and counts separate
outer-tooth sections beyond R35: 1, 1, 1, **9**, 1, 1, 1. The nine-tooth
band is print-local Z16.6..18.1, or Z-49.7..-48.2 at the source drum-frame
datum. No different nine-row location in that print explains the mismatch.
The raw top-drum STL is not watertight, so this is sectional source evidence,
not an adopted replacement or Boolean-clearance certificate. File hashes and
section data are in `_build_running/reverser-print-rows.jsonl`.

The actual knob bore does not stop inward ball travel before either pocket
centre: both native and faceted CAD checks are clear at sampled radial centres
2.5..6.5 mm. The original knob-print component gives the same result for
both R2.5 and R2.7 balls (`tools/reverser_ball_bore.py`), with positive
blind-end witnesses at radial centres 15, 17 and 19 mm. Thus an assumed bore
lip cannot turn these pockets into a shorter-travel pair of retained stops.

One still-unmeasured stop belongs to the complete machine rather than that
earlier frame bench: the housing opening around the lever. It must be checked
before concluding that a geometry correction is necessary. The former
“complete stack” finding above covers its listed neighbours, not that housing.

External cross-check: the author's [public issue list](https://github.com/marcuswu/Curta-Type-I-3x/issues)
showed two open issues, neither about reversal. [Max Fan's separate build](https://maxrfan.com/projects/curta-calculator/)
describes counter reversal during division, but also says roughly thirty parts
were modified and reports upright division jamming. It is evidence that his
modified build reverses, not a dimensional certificate for this checkout's
unchanged shaft, knob and housing. No contributor was contacted.

## Housing-window check

`tools/reverser_enclosure_stops.py` adds the actual recentered operating shell
and upper sleeve to the six-input bench. The source lower detent centre
(-6.8425 mm knob displacement) clears both on both kernels, as do -6, -5.5,
-5, -4.5, -4, 0, 3, 3.9075 and 4.5 mm. At -7.6427 mm the knob meets the
lower window edge: 15.112070350 mm³ native and 15.112047424 mm³ faceted,
at Z-71.6002..-70.95. The knob finger's bottom at source rest is Z-63.9575,
putting the flush lower-window stop at about -6.9925 mm. It is below the
lower detent centre, not the earlier stop needed to retain the ball on that
pocket's upper flank. Thus the housing does not rescue the proposed shorter
stroke. Output: `_build_running/reverser-enclosure-stops.jsonl`.

The remaining lower-detent engagement discrepancy is .3075 mm even at the
most favourable source gear/yoke play. Pocket spacing alone was not sufficient
evidence for a redesign, but the now-measured knob print, bore, shaft seats,
floating spacers, gear stack and housing also do not establish an unchanged
working reversal. This is a limitation of the validated source assembly, not
a claim that the author's filmed physical build cannot work.

The next design decision is whether to permit a bounded simulation-owned
mounting-seat correction (for example, facing the shaft's existing upper
shoulder so its unchanged pockets can sit higher). That alternative leaves
the detent geometry and spacing unchanged but still changes a functional
shaft mounting dimension. It has **not** been implemented or certified and
needs pilot authority before development. Both complete operating positions,
all six input stacks, knob/spring capture and both crank modes would still
have to pass. Other whole-machine findings remain in the separate rest
inventory; no failed contract has been removed.

The pilot subsequently requested an insertion-depth calibration trial.
The [independent native/print comparison](reverser-insertion-trial-2026-09-20.md)
confirms the same shoulder stop in the author's original printable files.
Raising the shaft +0.3075 mm merely closes the axial tooth-band gap while
intersecting the upper frame by 4.147209 mm³ native / 4.145870 mm³ from the
prints. No insertion-only fix is adopted; altering the shoulder or seat
remains a different action from positioning the unchanged shaft.
