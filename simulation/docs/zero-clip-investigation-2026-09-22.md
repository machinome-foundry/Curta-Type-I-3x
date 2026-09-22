# Zero-cam retaining clip: unresolved installed fit

This is a read-only finding, not a replacement shape, contact exemption or
physical modification recommendation. The source clip and all motions remain
unchanged. Manual page 16 shows the spring clip securing the zero-positioning
disc and requires the disc to rotate easily; it does not specify an installed
preload shape or a force law.

In the actual operating root, the complete clip overlaps the cam by
36.589675 mm³ native / 36.266678 mm³ world64 and the bearing plate by
8.417676 / 7.284743 mm³. The cam common consists of four positive pieces,
not a single mistaken planar face. The source clip spans world
Z-143.4..-141.0. Its projected arms also enter the cam and bearing material.

Unchanged-clip Z shifts of +.45, +.509, +.55 and +1 mm never clear both
neighbours. At +.45, cam common remains 29.789421 / 29.606223 mm³ and bearing
common increases to 26.961029 / 25.697260 mm³. A simple axial placement fix
is therefore rejected. The three-plane section was inspected, including the
complete bearing plate, and the 213-coordinate retained bank stayed unchanged.

Read-only topology inspection distinguishes the bearing's full annular groove
from the cam's two finite slots. That raises a possible missing clip-following
motion, but is not proof of its installed fit or a license to add a retained
degree of freedom. The existing clip does not clear the cam even if both are
rotated together. A following motion alone therefore cannot close this finding.

Do not shrink the clip, widen away its retaining surfaces, call positive
common preload, or invent a circular-wire substitute for the printed source
profile. Any future prescribed installed shape must preserve and prove capture
against both complete neighbours, with its deformation assumptions explicit.

Reproduce the scoped survey with:

```sh
python -m simulation.tools.zero_clip_contact --output _build_checks/zero-clip-survey-new.png --axial-shift 0 --axial-shift .45 --axial-shift .509 --axial-shift .55 --axial-shift 1
```

The [evidence index](evidence/zero-clip-diagnostic-2026-09-22.json) pins the
completed survey and inspected images. No OpenSpec task is closed by this
diagnostic; the remaining whole-machine contacts are still unwaived.
