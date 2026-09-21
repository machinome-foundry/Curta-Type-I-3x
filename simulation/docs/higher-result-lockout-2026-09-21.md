# Higher result locking — first measured missing stop

This is the next tasks 6.2/6.3 investigation, not an adopted new restraint.
The fixed-height ones profile must not be copied onto the higher sliding
stacks. All upstream geometry remains unchanged.

`python -m simulation.tools.higher_lockout_probe --channel 2` runs the actual
OperatingCurta, sets digit 2 to 3, turns to 140°, withdraws that selector to
zero, and requests 170°. The complete installed tens upper stack retains
shaft angle 169.59999999999994° and travel −4.2 mm.

| Admitted crank | Native overlap | Published-mesh overlap |
| --- | --- | --- |
| 140° | 0 mm³ | 0 mm³ |
| 170° | 0.30868623127003425 mm³ | 0.21392486170149 mm³ |

Both requests currently complete. Both native commons are valid and both
Manifold results report NoError. This proves a missing restraint in this
action order, not a defect in the author's printed part or a need to trim it.

The focused source-backed two-channel test
`simulation.test_higher_result_locking` reproduces the same retained phase
and actual stack travel. Its expected blocked request fails red with
`completed != blocked` (36.058 s). The test consumes the current ones-only
ResultLocking bench; it does not invent a new contact limit.

Next measurements use `--locate` to bracket closing contact with the complete
solids and their published meshes. At the measured retained phase and −4.2 mm
stack travel, that probe now brackets the closing boundary at:

- Native: 145.33065795898438° free / 145.33068656921387° contact.
- Published mesh: 145.32258987426758° free / 145.32261848449707° contact.

These local brackets do not certify the complete phase/axial envelope.
The separate `--carry` preparation enters
9 then 1 through ordinary requests to latch the real first carry and test its
other axial position; no joint bank is manually seeded. This actual-root case
now completes both requests, and reports:

| Crank | Shaft | Upper travel | Native overlap | Published-mesh overlap |
| --- | --- | --- | --- | --- |
| 500° | 169.60000000000002° | −8.88e−16 mm (lower seat) | 0 mm³ | 0 mm³ |
| 530° | 241.60000000000002° | −8.88e−16 mm | 0.9496263373477174 mm³ | 0.7603711547340599 mm³ |

The carry adds a real 72-degree passage while this request moves. Thus the
second case is not a fixed-shaft bisection and cannot inherit the raised-seat
145-degree stop. Both shaft rotation and axial seating must enter any proposed
higher-channel restraint. The tiny residual in the admitted axial coordinate
is recorded, not converted into an overlap tolerance.

The new `HigherLockoutBench` exposes measurement-only shaft, crank and carry
coordinates on the unchanged source `ResultTens` and complete bell. Its
geometry parity tests compare both actual-root contact poses; its new
`higher_locking_envelope` tool surveys complete revolutions at a chosen shaft
phase and carry position. These are diagnostic instruments, not operating
controls or an adopted restraint. Both native and published-mesh parity tests
now pass (2 tests, 1.215 s). A preliminary comparison rotated an already
float32-rounded mesh from 140° to 170°, differing from the root's mesh published
at 170° by 6.95e−7 mm³. Publishing at the same contact pose resolves that
measurement-method discrepancy; the final comparison is stricter (nine decimal
places), not a relaxed clearance threshold. All positive contacts remain
positive; the clear reference is still required to be exactly zero.

The geometry helper imports now load their whole-machine entry points lazily:
using `world_solids`, `rigid_leaves` or `mesh_solid` no longer compiles an
unrequested operating machine. Measurement and placement algorithms are
unchanged. Wider phase/axial coverage remains open.

A first full-revolution survey (10-degree samples with 18 bisection rounds
where contact changes sign) finds these complete-bell opening/closing brackets:

| Carry | Shaft | Kernel | Opening bracket | Closing bracket |
| --- | --- | --- | --- | --- |
| 0 | 169.6° | native | 30.716820–30.716858° | 145.330658–145.330696° |
| 0 | 169.6° | mesh | 30.792465–30.792503° | 145.322609–145.322647° |
| 1 | 169.6° | native | 32.716827–32.716866° | 145.052605–145.052643° |
| 1 | 169.6° | mesh | 32.792473–32.792511° | 145.052605–145.052643° |
| 1 | 241.6° | native | 32.755356–32.755394° | 145.052605–145.052643° |
| 1 | 241.6° | mesh | 32.827377–32.827415° | 145.052605–145.052643° |

For an opening the right endpoint is free; for a closing the left endpoint
is free. The survey rotates meshes published at the 140-degree reference;
actual-root pose parity is separately checked with meshes published at each
actual contact pose. This finite survey can miss narrow unsampled islands and
does not certify interpolation, other shaft phases or intermediate carry
heights. In particular, the lowered closing boundary is earlier than the
raised boundary, disproving a carry-independent reuse of the measured stop.

## Indexed-position finding and isolated T07 trial

The unchanged tens stack then failed native clearance at the ordinary indexed
shaft position 200°, crank 180°. Across carry positions 0, .25, .5, .75 and 1,
the positive native volumes are respectively 0.0000170565657,
0.0000767545455, 0.0000852828307, 0.0000852828308 and 0.0000511696995 mm³.
All published-mesh commons there are zero. The other four indexed flats
(−16°, 56°, 128°, 272°) clear at those five heights in both kernels.
Reproduce with `python -m simulation.tools.higher_locking_envelope --indexed`.

This is a native-solid fit finding, not evidence that physical prints jam.
As with ones F18, adopting a contact law over the currently intersecting
normal indexed pose would encode an incorrect normal-operation stop.
`higher_lockout_trial.py` isolates **T07**, a proposed additional .01 mm outer
skin on this tens lockout only (.15 → .16 mm). Its contracts require unchanged
keyway/core and axial extent, no added material, bounded removal, connected
complete upper print, clearance at every indexed flat and sampled axial
position, and retained locking four degrees to either side. The trial is not
selected by the operating model; all other lockouts and upstream CAD remain
unchanged. The unchanged .15 mm trial fails the intended native clearance at
0.000017056565662916912 mm³ and the positive-removal check; both flank locking
and complete-print integrity pass (2/4, 27.57 s). The .16 mm candidate then
passes all four native checks (14.63 s), but its faceted run passes only 3/4
(20.18 s): the lower-angle locking flank is absent from the coarse mesh.

An independent comparison reproduces that mesh blind spot **before T07**:
all five lower-angle offsets (−4°) at carry positions 0, .75 and 1 have
positive native contact but zero faceted contact. For example, shaft −20°
at carry 0 gives 0.0032965019 mm³ native before the fit, 0.0030037110 mm³
after it, and zero coarse-mesh common in either case. This is not a reason
to weaken the negative control or increase its offset.

`TrialContactBell` refines only the diagnostic bell to .01 mm linear and
.1 rad angular deflection. The native solid is unchanged (zero material
removed or added in both difference directions). The unchanged locking
checks now pass: **5/5 faceted, 30.35 s; 5/5 native, 19.23 s**, including
the added native-fidelity contract. No contact-volume epsilon is used.
The source-like production bell and all operating geometry remain untouched.

The first native/mesh coarse phase survey of this complete trial pair covers
shaft −16°..344° every 12°, at carry positions 0, .5 and 1. It is being used
to locate the axial/phase boundaries, not as an interpolated-law certificate.
The original `.15` measurements above remain evidence for the original
production stack, not profile knots for the changed trial.

That survey completes in **619.713 s**, producing 186 kernel/shaft/height
records. Its [retained boundary evidence](evidence/higher-t07-coarse-envelope-2026-09-21.json)
includes the raw-log SHA-256 and maximum positive sampled volumes. A lowered,
indexed shaft is not free for a complete frozen revolution: the carry-tooth
contact at shaft −16° enters near 148.5353° and releases near 154.8604°.
Consequently the ones law's fully free indexed-angle branch cannot be copied
onto the lowered tens stack. No generated coarse curve has been adopted.

The inspected browser captures `_build_checks/higher-lockout-raised.png`
(original raised stack near closing) and `higher-t07-indexed.png` (trial,
shaft 200°, crank 180°, half carry) show the complete stack alongside the
bell's actual locking lands, with the refined bell's smoother circular mesh.
The .01 mm fit is established by the native contracts, not discernible pixels.

`HigherResultActionOrder` adds a separate retained diagnostic with the actual
T07 source stack and a carry-height instrument. That input moves the real
upper print through its existing 4.2 mm stroke and feeds the unchanged source
tooth-passage law. It is not a substitute for the operating lever bank and
does not set a register or directly seed the shaft. Both raised and lowered
withdrawal cases require a stop and a matching long-request stop; their
contact restraint is deliberately still absent while measurement continues.
The two-test action-order run fails all three expected assertions with
`completed != blocked` (29.772 s): original source bench, raised T07 stack
and lowered T07 stack. Both trial fixtures reach the measured 169.6-degree
shaft phase and their correct axial seats before failing the missing stop.

Expanding the fit test from five crank orientations to a full ten-degree
revolution first failed at carry .75, shaft −16°, crank 150°: 1.6770822181 mm³
native and 1.6496895882 mm³ published-mesh contact. That fixture incorrectly
held an **engaged carry gear stationary through its driving tooth**. Applying
the existing source tooth passage gives shaft 7.2° at that same crank and
height, and both complete-part commons become zero. No geometry is removed
to fix this fixture, and neither part is excluded.

The full 925-pose contract now follows the unchanged carry passage and latch
threshold while checking all five starting flats and five sampled heights.
A separate negative control deliberately freezes the engaged gear and must
detect the contact before releasing it to its proper driven angle. The
expanded six-contract suite passes **6/6 faceted (10.25 s) and 6/6 native
(99.71 s)**, with no volume epsilon. This is a sampled fit/trajectory result,
not yet a higher-channel restraint or its actual-root adoption.

Ingredient-height inspection identifies the expected axial transitions. The
printed pentagon spans source Z −26.1..−24.6 mm, rising by 4.2(1−carry) mm;
the upper results locking disc spans −23.1..−21.6 mm and the lower disc
−25.5..−23.1 mm. Their axial overlap intervals change separately, explaining
why interpolating whole-contact endpoints is not adequate. The complete
upper print also contains the carry pinion at source Z −33.6..−31.8 mm;
its tooth contact must remain part of the admitted-motion checks.

The native/mesh intermediate-height survey at shaft 169.6° also shows that
opening switches from the raised boundary at carry .25 to the later boundary
at .5; closing switches to the earlier lowered boundary between .5 and .75.
Linear interpolation between two endpoint envelopes would therefore need its
own geometry proof. No such interpolation is adopted.

An arbitrary one-turn cap, an assumed
20-degree copy of the ones envelope, and a silent swept clearance cut are not
acceptable substitutes for those measurements.
