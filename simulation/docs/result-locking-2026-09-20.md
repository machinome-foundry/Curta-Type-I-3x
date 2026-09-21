# Ones-shaft closing restraint: continuation in progress

Later checkpoint: the framework and viewer periodic-stop fixes are integrated,
and the [measured ones restraint is now on the operating crank](operating-ones-lockout-2026-09-20.md).
That record carries current acceptance and remaining scope. The investigation
and previously blocked states below are preserved as historical evidence.

Framework `ancestor-joint-constraints` is integrated into main at `8d2bd71`.
This continuation addresses project tasks 6.2/6.3; the framework diagnostic
alone did not adopt a general operating restraint. No upstream CAD changes.

## Starting failures

`test_result_locking.py` uses the existing source-backed `ResultActionOrder`
bench, with the complete printed bell and complete ones upper assembly.
Selector 3 is withdrawn to zero at crank 115, 118, 120, 121 and 123 degrees.
Every subsequent request to 150 incorrectly completes: **five failing
subtests, 24.70 s** on the unconstrained model. The retained shaft phase,
not the selector's new zero setting, determines the closing contact.

Additional acceptance checks require ordinary three-turn requests to remain
unrestricted and a deliberately wrong-order long request to meet its first
contact rather than pass through a forbidden interval. No finite arbitrary
one-turn envelope from the earlier local diagnostic will be adopted.

## Measurement underway

`tools/locking_envelope.py` samples the two actual periodic angles using the
complete bell and ones upper stack, in both native solids and the published
meshes. Native validity and Manifold status are required; every positive
intersection is counted. The initial ten-degree crank grid is a survey, not
proof against narrower unsampled contacts.

The faceted sweep produces apparent late-cycle release gaps near an indexed
shaft angle (for example 6 degrees). Native solids remain in positive contact
there. Those polygonal-circle effects are not physical release windows.
At the 45.6-degree shaft phase the reduced bench's native closing bracket is
125.335121..125.335159 degrees. The previously measured full-tree phase
189.6 has a slightly earlier bracket; fivefold equivalence is therefore a
claim to check, not an assumption about the exported fitted source.

The bell is axially stationary during crank lift; its spring changes shape.
The ones locking assembly does not perform the higher channels' carry slide.
This makes this pair a two-angle contact question, without implying the same
law applies to higher channels or the turns counter.

## Indexed-flat finding and bounded fit

The five-flat check then found a contact in **normal operation**, not only in
the wrong-order sequence. Input 3, crank 90 then 180, gives shaft 220 degrees.
The actual operating model and the independent complete-pair bench agree on
**0.0000596979837931 mm³** of valid native solid overlap; the faceted common is
zero. The native sliver is about .0090 × .0164 × 1.05 mm, centred at
(35.20698, 3.66845, -22.125). It is not a contact-volume tolerance or a
numerical zero. Adding a restraint before addressing this would jam a normal
integer input.

The existing simulation-owned .15 mm outer-profile fit is extended to
**.16 mm on the result ones lockout only** (`FittedOnesLockout`). Every other
lockout retains its previous fit. No part placement, shaft/dial clocking,
keyway, axial height, motion law or upstream file changes. This is a further
builder-style outer-flank fit, not a recommendation about printed strength.

Before that correction the explicit native indexed-clearance contract fails
with the volume above, while the two-sided locking contract passes: **1/2
passing, 1.71 s**. Afterward, **4/4 faceted (20.60 s) and 4/4 native (30.92 s)**
pass. They cover all five indexed flats over a ten-degree full bell revolution,
contact four degrees to either side, connected/native-valid complete groups,
no added material, bounded removed volume, unchanged material inside R4
(including the keyway) and unchanged axial extent. The faceted result alone
was blind to the original sliver.

One probe setup failure used the perturbation helper about the source common
origin rather than the shaft at X40.5. Its misleading missed-lock result is
not mechanical evidence; the corrected test poses the actual shaft joint
four degrees either way.

The actual operating-tree recheck completes the same input-3 request at
crank 180°, shaft 220°, with **zero native and zero faceted common volume**.
Temporarily restoring the earlier `FittedCarryLockout` in `Part10221_1`
reproduces the exact clearance failure at 0.00005969798 mm³ (and correctly
fails the positive-removal check): 2/4 pass, 26.82 s. The .16 mm class is
restored. This is a source-code mutation, not a test tolerance change.
The final restored native run passes **4/4 in 30.87 s**.

At crank 180°, native bisection gives the following free-side angular bands
after the correction (degrees; each free/contact bracket is under .000020°):

| Indexed shaft | Lower free limit | Upper free limit |
|---|---:|---:|
| 4 | 1.304993 | 4.311031 |
| 76 | 73.303944 | 76.311031 |
| 148 | 145.303944 | 148.307903 |
| 220 | 217.310715 | 220.063820 |
| 292 | 289.518196 | 292.308113 |

These are separate source measurements, not five copies of one ideal flat.
They describe the closed land at this crank pose, not an independently
certified full-motion clearance envelope or a prediction of dial settling.

OpenSCAD isometric and shaft-axis snapshots at shaft 220° / crank 180° were
rendered and inspected. They show the complete bell and the separate keyed
ones upper stack at the expected side of the locking land, with no detached
fragments. The images cannot resolve a .01 mm fit; the native contracts prove
that clearance. Reproduce with `simulation/ones_lockout.py:OnesLockoutBench`,
`--drive shaft_angle=220 --drive crank_angle=180 --autocenter --viewall
--projection ortho --imgsize 1200x900`, camera `0,0,0,55,0,25,250` (isometric)
or `0,0,0,0,0,0,250` (axis). Evidence is under `_build_running/ones-lockout-*`.

The manifest and restraint laws are unchanged at this checkpoint. Refreshed
contact envelopes and broader restraints remain in progress. No roadmap task
is marked complete by these scoped checks.

## Experimental restraint, not yet adopted

`result_locking.py` adds the candidate only to the existing two-channel
diagnostic. It reads the actual retained ones shaft and the actual co-rotating
drum, and constrains the existing bell joint. The source tree is not replaced
by a synthetic mechanism. In the full assembly the corresponding restraint
would act on the existing crank, reading the actual bell and ones shaft.

Its contact region uses separate measured opening/closing profiles for
all five flats. Reading the real co-rotating part allows a free branch without
an arbitrary `own - 360` limit. The signed-gap diagnostic puts the crank's
periodic cut in the common open window at 90°, not across the closed locking
land; the current candidate states the next closing surface directly. A .1°
free-side stopping stand-off and .002° inset into the measured indexed bands
are explicit angular guards, not discarded positive intersection volumes.

The compiler consumes native and faceted survey records and chooses the
free-side opening/closing brackets of both kernels. The separate
`tools/check_locking_profile.py` must prove the interpolated boundaries against
the complete printed pair, including between-knot samples; a generated table
alone is not acceptance. Retained running tests must also prove ordinary
multi-turn motion, first-contact stopping on a long request, all five flats,
reverse relief and exact replay before any production adoption.

The first coarse table failed 28/2072 faceted boundary samples and 12/2072
native samples. The closing failures locate a sharp profile corner near
shaft phases 13° + 72n; the mesh also has a narrow opening contact island
that a ten-degree coarse survey misses. Quarter-degree shaft samples around
the corner and quarter-degree crank samples through the opening resolve
these findings without any contact-volume tolerance. The refined table
compresses both curves to at most .01° deviation at measured knots; this
does not waive between-knot geometry checks.

After refinement, **1888/1888 boundary samples pass under each kernel**,
including the half-degree shaft grid, retained table knots and their
midpoints. The complete bell and ones upper assembly are used throughout.
Logs: `_build_running/locking-profile-refined-check-{faceted,exact}.jsonl`.
This is scoped sampled geometry evidence, not a continuous collision proof
or whole-machine motion acceptance.

Reproduction: run `tools/locking_envelope.py --all-flats` under each kernel;
add phases 13, 13.25, 13.5 and 13.75 plus each multiple of 72°. For the mesh
also remeasure phase 6 + 72n with `--opening-grid`. Feed both full surveys,
the native `--index-bands` output and both refinement files to
`tools/compile_locking_profile.py --compact`; apply its emitted patch, then
run `tools/check_locking_profile.py --kernel faceted` and `--kernel exact`.

The refined numerical checks pass (2 tests, 30.528 s): all eleven source
tooth counts at all five starting flats remain outside the forbidden region
through a half-degree crank sweep, and the next-surface bound agrees with
the signed contact region on a three-revolution grid. Four actual legal
three-turn requests also pass (one test, 45.634 s): blank, input 3, input 9,
and zero-input subtraction retain the expected ones-shaft totals.

The first signed-gap formulation stops the prepared short request at
125.220816°, holding the shaft at 189.6° (about 8.17 s for that stop). Both
that formulation and the next-surface formulation fail the immediate long
request with a framework `StopInvariantError`. The
[small source-backed reproduction](periodic-lockout-stop-2026-09-20.md)
removes the measured table and preserves the failure. This is the current
production-adoption blocker. The earlier five-flat replay suite was
interrupted after 194 s to isolate the cost; it is not recorded as passing.
