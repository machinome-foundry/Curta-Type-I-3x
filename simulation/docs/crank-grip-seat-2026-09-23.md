# Crank grip: lower-face seating gap

The paired reverse-nose replays both expose the same crank/grip contact at
addition times 1.6 and 3.7 seconds (crank 252 and 594 degrees). It is not
introduced by the reverse-nose fit. Native commons are valid and empty;
world64 commons are respectively 3.552713678800501e-14 and
5.684341886080802e-14 mm³. Their bounds have positive thickness between
Z94.34999999999998 and 94.35. This is not an exactly planar common, and no
small-volume exemption is used.

`SeatedCrankGrip` removes only the lowest .05 mm of the source grip, whose
bottom face is local Z0. Its original placement, central bore, screw seat,
upper geometry and motion remain unchanged. This is a simulation-owned fit;
upstream assets are unchanged and it is not manufacturing advice.

The original addition test fails red on the first positive common. The first
fit passes moving clearance but fails the bounding-datum check: using the
source BRep bounding box as a cutter datum carries its 1e-7 mm padding into
the face location. The corrected cutter uses the measured plane Z0. That
failed run is retained rather than reclassified as passing.

Four production tests now pass in 103.919 seconds on pinned framework
`a500a99`, before this fit's project commit. They cover all 44 actual addition
samples in native and world64 geometry, the expected (5, 2) arithmetic outcome,
one connected valid solid, no added material, removal confined to the lower
face, preserved external dimensions elsewhere, .02 mm downward free play and
.1 mm downward capture. The fourth test compares the complete native source
and fitted screw commons geometrically: neither contains material outside the
other. It does **not** declare this existing screw overlap clear.

The complete rigid-pair addition replay finishes 44 samples in 168.254 seconds.
Against the preceding reverse-nose replay, it removes only the crank/grip pair
at two samples and adds no pair. Every other pair's volume is bit-identical
except the existing screw/grip common, which changes at rest and all samples.
Its rest world64 value changes from 28.35132899553573 to 28.35132901451297 mm³.
Native source/fitted common volumes are 28.396506783799737 and
28.396506783799754 mm³; both geometric differences have exactly zero volume.
Thus the scalar results are not bit-identical even though the protected native
common is geometrically unchanged. No volume tolerance or inventory exemption
is introduced, and this remaining overlap is not accepted as clearance.

The inspected section shows the .05 mm face gap separately from the unchanged
central shaft and retaining-screw opening. It is scoped interface evidence,
not a whole-machine view. The bank, motion laws and controls are unchanged.
The existing seven crank-coupling contracts rerun against the final face
datum and pass in both CLI kernels (52.01 s faceted, 54.27 s native), including
both legal crank modes, the original 213-coordinate bank and transverse-pin
capture. Both processes exit zero.

## Reproduction and evidence

```sh
python -m simulation.test_crank_grip_seat
python -m simulation.tools.crank_grip_seat --image _build_checks/crank-grip-seat-section-new.png
python -m simulation.tools.operating_demonstration_contacts --demonstrations addition
```

Evidence is retained under `_build_checks/`:

| Artifact | SHA-256 |
|---|---|
| `crank-grip-seat-red-99c3f2a.log` | `7f9f3b9b5929dde46eb17b7c08e46c52839f4656b80506997017d284acc68803` |
| `crank-grip-seat-green-99c3f2a.log` — failed padded-datum assumption | `f5a6d9d953c644613db443e2d82e9bbe1dc0851f36c2bacd24bc2b2fde6385b0` |
| `crank-grip-seat-protected-green-99c3f2a.log` — four passing tests | `ba78ee3c21b221f63db08ede4274fe1984ef175f25ca4a45e8a0eb16787845fb` |
| `crank-grip-seat-datum-addition-99c3f2a.jsonl` | `0974390b3ee5adeaff1537f4b4d5c8b2c51087028cc93f31ada17a9b16716766` |
| `crank-grip-seat-section-99c3f2a.json` | `dc3e4827714a2ccab4254b3e4fdf6dec5b64b840799678332703c31b351f4533` |
| `crank-grip-seat-section-99c3f2a.png` — inspected | `53837387f94e28fec7c43324ba8c92acea77fd65247bedb990704a856028949c` |
| `crank-coupling-final-grip-faceted-99c3f2a.log` | `6b5e778ec5b1d5e43002bdd2d761f748bb6126abc843a26ba242ded3dea96524` |
| `crank-coupling-final-grip-exact-99c3f2a.log` | `787db542af15ee9c9f40a413a273bf83d3fe0a6d5460ad0bc8956a5fb7f3c8a1` |

The earlier [reverse-nose record](reverse-nose-seat-2026-09-23.md) pins the
paired baseline. Other positive contacts, flexible leaves, the radial ball
law and complete viewer operation remain separate obligations. No OpenSpec
task checkbox is completed by this fit.
