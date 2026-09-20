# Lower enclosure datum and base seat

The full-machine rest check reached these contacts after the housing-thread
fit. The focused enclosure bench reproduced both failures: lower housing/base
plate at .000028108318 mm³ on the faceted runner, and upper sleeve/bottom
housing at 1046.848968492 mm³ faceted, 909.434743190 mm³ native. The native
base pair is clear. These are separate findings, not reasons to introduce a
volume tolerance.

## Measured source placement

`tools/enclosure_seats.py` retains the unchanged source assembly probe. Native
circles put the upper sleeve on (0, 0), but the entire lower shell and base on
(-.406900356, .745841949), about .85 mm off axis. The sleeve's mating bore is
R68.5 and the bottom housing's outside is R68.1: their intended concentric
radial clearance is .4 mm. Translating the unchanged bottom housing by
(.406900356, -.745841949, 0) changes native common from 909.434755896 mm³ to
zero. No radial scaling or part-bound-box centering is involved.

`RunningEnclosure.render()` now carries the lower housing group, all five lower
marker assemblies, the base plate, its two countersunk bolts and the lower
side screw through that common translation. The upper sleeve, ring and upper
fasteners keep their source positions. The source-reference and pose assemblies
retain their original datums. A world-vertex contract independently checks the
translation and the unmoved upper fittings; lower marker joints retain their
source-local axis inside the translated parent.

The coarse sleeve tessellation still overlapped the centered lower shell by
42.114888092 mm³. Native rest and radial free/captured tests already passed.
Changing only the sleeve's tessellation to .01 mm linear/.1 rad angular
deflection makes those same tests pass on the faceted runner. The native STEP
solid is unchanged.

## Base seat

The source plate's top face is exactly flush with the lower-housing shoulder
at Z-180.75. Native translations of -.01, -.001 and 0 mm are clear; +.001 mm
intersects by .627018911 mm³ and +.01 mm by 6.270189106 mm³. The faceted
near-coincident faces give the tiny positive rest common above.

The operating placement names a .05 mm downward locational clearance at this
seat, carrying the two countersunk bolts with the plate. No surface is cut or
intersection waived. Tests admit +/-.02 mm and block .1 mm toward the shoulder
(local -Z on this upside-down source plate). The plate remains radially
captured by the source socket. This is a stated simulation assembly clearance,
not evidence that the physical builder left a .05 mm air gap.

## Verification

The initial five-contract faceted run was 0/5; the first centered run exposed
the sleeve mesh error and a rejected test direction spelling. After correction,
all five pass faceted (19.46 s) and native (5.31 s). Adding an explicit base
socket radial capture check retains 5/5 on both (1.07 s faceted, 8.14 s native).
The contracts cover rest
clearance, axial and radial free/blocked seats, group fidelity and every lower
marker's body, ball and spring. No whole-machine or roadmap completion is
claimed by this scoped result.

The complete installed-world motion module passes 7/7 faceted (113.19 s),
including all ten marker movements and carriage/clearing transport. The
uncropped `enclosure-seats-full.png` and `enclosure-seats-bottom.png` were
rendered and inspected: they show the complete shell, centered sleeve, lower
marker bank and seated base with both countersunk heads. The earlier close
isometric is cropped and is not the whole-assembly view.

The same installed-world suite passes 7/7 native (78.20 s). The whole
operating model passes solid integrity and gets past both original enclosure
pairs on both runners. Its next contact is bottom housing/main body:
75.264082522 mm³ faceted and 2.977762908 mm³ native. Each whole-root run
therefore remains 1/2 (9.48 s faceted, 11.94 s native). That frame interface
is a separate finding, not waived by the successful enclosure increment.

Evidence under `_build_running/`:
`enclosure-seat-measurements.jsonl`, `enclosure-seats-red-{faceted,exact}.log`,
`enclosure-seats-contracts-red-faceted.log`,
`enclosure-seats-recenter-exact.log`, and
`enclosure-seats-final-{faceted,exact}.log`.
