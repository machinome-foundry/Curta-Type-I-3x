# Pinned crank / drum coupling

Status: adopted simulation-owned seat correction, not a claim about the
author's working prints or a recommendation for physical modification.
Upstream assets, the shaft, pin, crank height and clocking are unchanged.

The source crank bore R4.56 is centred at world (.081490712, -.263733179),
while the actual R4.4425 axle and retaining pin use (-.009541016, .073549841).
Their complete native solids overlap by 44.04961 mm³; the full-precision
placed meshes overlap by 43.51703 mm³. The native CLI independently fails
clearance at 44.04963 mm³. Both initial two-test runs pass the pin and fail
crank/axle clearance (5.47 s native, 6.38 s faceted).

Manual page 50 shows the transverse retaining pin. Aligning the complete
handle assembly by (-.091031728, .337283020, 0) leaves that pin untouched,
and removes the long lateral intersection without cutting the bore wider.
The remaining native 13.94378 mm³ is the shaft tip above the source internal
roof: world Z88.35..88.95. `SeatedMainCrank` extends only that existing R4.56
pocket to world Z89.00, giving .05 mm tip clearance. Its local cutter is
R4.56, Z28.45..29.15. The handle and its fastening screw move with the crank;
their mutual datums are not changed.

Six rest contracts pass in both kernels (12.79/10.40 s): complete crank/axle
clearance; actual mating bore coaxiality; pin clearance against both parts;
removal bounded to the pocket with no addition, one connected solid and
unchanged external bounds; retained transverse-pin capture; and the fixed
pre-fit 213-coordinate initial-bank witness. Both pin seats are free at
±.02 mm and blocked at ±.75 mm. An initial .3 mm capture assumption failed;
a native offset survey shows the source holes allow more play, and the
tests now record the measured retained capture rather than tightening a
source hole to satisfy that assumption. An initial coaxiality test also
included unrelated lower circles of the complete drum; the final test
measures the actual coupling band above Z68.

The seventh contract issues actual crank requests in two independently
initialized modes (lift 0 and 9), checking all three pair clearances at 90°
and 270°. All seven production checks pass with observed exit zero:
142.83 s native and 133.72 s faceted. The earlier sequence changed mode at
90° and then requested 270°; the operating restraint blocked it at
123.75965935694694°. That retained failed log is not called a legal-mode
pass or proof of that mixed-mode action order's correctness.

The paired world64 rest inventory changes 259 → 258 positive pairs, removing
only crank/axle and adding none, with no refused common. The other contacts,
including the handle's own fastening interfaces, are not waived. The final
three-panel section was inspected: the bore is concentric, the pin remains
in the transverse hole, and the expanded vertical view shows the .05 mm
roof gap. Inspection leaves all 213 coordinates unchanged.

Evidence under `_build_checks/` includes `crank-coupling-red-*`,
`crank-coupling-contracts-red-exact.log`, `crank-coupling-first-exact.log`,
`crank-coupling-fit-*`, the failed mixed-mode `crank-coupling-production-*`,
and successful `crank-coupling-legal-modes-*`. The read-only datum and native
offset reports are `crank-drum-{coupling-datums,centered-datums,fitted-inspection}-2026-09-22.json`.
One initial fitted plot failed on an empty common's bounding box; the final
instrument handles an empty common explicitly. The evidence index pins the
final sources, section, inventory and acceptance logs. No whole-machine or
OpenSpec task completion follows from this scoped fit.
