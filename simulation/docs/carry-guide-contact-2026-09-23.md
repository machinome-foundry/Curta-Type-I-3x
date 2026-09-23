# Carry-slider guide: localized source contacts

Read-only continuation of the [complete carry-frame work](carry-bank-frame-investigation-2026-09-23.md).
No guide, slider, spring, operating coordinate or source asset is changed.
The radial-ball adoption is separately complete at `64719ce`; this finding
does not reopen that local motion or complete the whole-machine inventory.

`simulation.tools.carry_guide_contact` inspects the first result and first
counter stations at drops 0, 2.1 and 4.2 mm in the independent full-bank bench.
Counter sections rotate the complete native parts -130 degrees about world Z
to the common station frame; volumes are measured in their actual world frame.
The earlier 450-row all-station play survey remains broader finite evidence.

## Native shoulder obstruction

The unchanged counter slider enters its guide at full drop by
0.595349994535576 mm³ native / 0.5953568840272344 mm³ world64. Its native
common is a rectangular shoulder region with these station-frame bounds:

- X 60.3750000009…61.7249999949 mm;
- Y -7.8900000006…-6.4199999997 mm;
- Z -17.0999999984…-16.7999999985 mm.

Thus the localized obstruction is approximately 1.35 × 1.47 × .30 mm,
not the whole slider guide or the frame passages already fitted. The inspected
longitudinal section at Y=-7.155 mm shows the counter's outer shoulder entering
the guide's upper ledge. The corresponding result shoulder reaches the same
ledge without this .30 mm penetration. This is localization, not permission
to shorten the stroke, move the guide, file either contact or waive the common.

The inspected transverse section at Z=-20 mm also shows nominally coincident
slot/slider faces and asymmetric lateral play. The prior unchanged guide
survey reports negative .01 mm displacement into the guide as positive contact,
whereas positive .2 mm tangential displacement can leave the open guide face
without contact. A claim of complete capture must therefore include the real
remaining assembly and retention, not invent an opposing guide wall.

## A diagnostic guard false positive, kept separate

On framework `83aad09`, three of the six native measurements are refused by
the new false-empty guard. Independent Sol examination of the first result
station at drop 2.1 mm found its proposed shared-interior witness
(60.22464937443688, -7.8900000000000015, 20.24964937443688) is actually on
the nominally coincident planar boundary: nearest face distances are only
2.6645352591e-15 and 7.1054273576e-15 mm, while those native faces carry
1e-7 mm kernel tolerances. Moving Y by -1e-7 or +1e-7 puts the point in
opposite solids, not both. Zero-tolerance classification reporting IN alone
is not sufficient evidence of strict interior here.

A separate isolated framework correction is underway to resolve witness
certainty against native face uncertainty. It must not turn positive volume
into zero, add an overlap allowance, or lose the radial ball's independently
verified strict interior controls. The native .59535 mm³ counter obstruction
is nonempty and is unaffected by this distinction. Tiny mesh commons and
nominal source tangencies are not silently reclassified as accepted clearance.

## Evidence and reproduction

The six-row shoulder and transverse surveys completed successfully, but their
exit status means measurement completion, not mechanical acceptance. The first
tool launch failed on an incorrect helper argument count before producing rows;
that log is retained and the harness call is corrected.

- `carry-guide-shoulder-a139fe0.jsonl`:
  `2dd72f912553948685d4cc03414f46533652b7323ff9db08dc1231400a3030fc`.
- Inspected `carry-guide-shoulder-a139fe0.png`:
  `cd5ddfff055dbd96796de5b7811f3ebb61100e069301ed161eb1e9192d81ee46`.
- `carry-guide-profile-a139fe0.jsonl`:
  `774b4d1c53adc0dab21b584aa9b3c94b75fbb62f1b2dbab625be4a73644d1823`.
- Inspected `carry-guide-profile-a139fe0.png`:
  `5189f4cdeccac8af83e7f395f56cb9a8fc4edaaedd8397328229607dc9ab4bc4`.

These ignored artifacts live in `_build_checks/`. Reproduce on the recorded
framework with fresh output paths:

```sh
python -m simulation.tools.carry_guide_contact --image _build_checks/guide-shoulder-new.png --section-y -7.155 --z-range -19 -10
python -m simulation.tools.carry_guide_contact --image _build_checks/guide-profile-new.png --horizontal-z -20
```

Before proposing a fit, independently bound the changed material and prove
which surfaces retain guidance, mounting and the full source stroke. Preserve
the existing spring fold/detents, reset shoe, pin head, moving laws and already
proved frame passages. No fit choice is made by this diagnostic.
