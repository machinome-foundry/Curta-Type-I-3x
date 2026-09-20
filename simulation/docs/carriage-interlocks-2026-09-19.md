# Operating carriage and clearing restraints

Continuation of `simulate-the-curta`, tasks 1.3 and 6.2–6.3. These are bounded
simulation-owned fits under the delegated builder-fitting scope. Source STEP
and STL files are unchanged. Neither fit changes the reversing-shaft detents.
This record is incremental, not whole-machine acceptance.

## Clearing pin: measured and passing

The original 34.2 mm source pin and author STL agree in length. With the
existing measured cam follower at rest, its bottom is at world Z18.510828,
below the frame's Z21 land. All six shift positions show 16.21547832234 mm³
native overlap. The first clear lift is bracketed by
2.48915863037..2.48916435242 mm. At maximum depression and full carriage lift
the unfitted tip still overlaps the frame by 8.46928220898 mm³.

`tools/clearing_seat.py` preserves the unfitted pin and body in its source
bench. The 60-case native record is `_build_running/clearing-seat-native.jsonl`.
`FittedClearingPin` faces only the lower 2.54 mm of the pin, preserving the
head, shoulder, sleeve and cam-following placement. The rest tip is now
Z21.050828. The source and older pose/clocked pin remain unchanged.

The three geometry contracts first failed. All four final contracts pass
faceted (19.94 s) and native (5.93 s): both ring rests at all six shifts,
complete lifted clearing sweep, free/blocked axial contact at active cam
positions, and exact removal confined to the lower tip. Logs are
`clearing-seat-fit-{red,faceted,exact}.log` under `_build_running/`.

The operating carriage's lift joint reads the actual pin slide. Its minimum
lift is the pin depression minus 3.09 mm, floored at zero. This retains a
named .05 mm frame gap. It admits partial motion, but never prepares another
input. Three running tests failed before the bound and pass after it
(33.386 s): an unfinished sweep prevents seating, seated clearing stops in
its real play, and partial lift opens only its own clearance. Repeated
requests cannot walk through the stop; explicit release/resume and exact
snapshot replay pass. Logs: `clearing-interlock-running-{red,green}.log`.

The expanded bidirectional test subsequently exposed a pre-existing follower
phase error: starting from rest 0 and requesting sweep -90 completed with the
pin still at 3.089172 mm, incorrectly bypassing the new stop. The small public
API reproduction in `tools/clearing_rest.py` gives the same result without
any CAD (`--raw-remainder` preserves it without a production mutation). The
existing `% 360` expression left that negative sweep on the
piecewise profile's clamped endpoint in the compiled run. Replacing it with
the project's explicit positive `modulo` expression preserves numeric poses
and makes all six rest/direction cases stop at the actual cam/frame contact.
The full-model failure is retained in `clearing-rest-directions-red.log`.
New small tests cover repeated sweeps through negative and positive periods
and both rests in five periods. Both small tests and all nine full-model
request tests now pass (11/11, 169.157 s;
`carriage-clearing-running-green.log`). This includes both restraints requiring
their own release, all six index slots in both directions, repeated attempts,
both clearing rests and retained-state replay.

## Carriage body: verified bounded fit

The source body/frame has 214.202001923093 mm³ rest overlap in seventeen
bearing-boss contacts, world Z24.9..25.8. Radial clipping places all this
material outside R31.75 and inside R34.2. The candidate removes a .95 mm
deep annulus R31.7..34.25 and faces the general underside .05 mm so that the
6 mm lift clears the indexing-key tops by .05 mm. All axes and the central
guide remain fixed. Two remaining exact-touch contacts occur at the existing
indexing-pocket ceilings: lowering .04 mm produces 1.713636661797 and
.636172512352 mm³ at world Z30.86..30.9. Their native ceiling is local Z14.1.
The candidate deepens only that existing ceiling .05 mm within R21.9..34.25.

The original three body contracts fail seating and lifted clearance (1/3).
An initial roof cutter made by differencing translated solids failed its
independent protected-material check despite a valid one-body result. Direct
point classification also found 680 lost key-root samples, so this was not
dismissed as a Boolean reporting issue. `tools/carriage_roof.py` retains the
reproduction. The replacement cutter extrudes the actual planar source
ceiling, including its original boundary, and clips it to the measured
annulus. All five native contracts now pass (89.26 s), including the unchanged
protected-material assertion and added independent key-root classification.
No geometry test is waived. The first faceted run still failed two contracts
(4.951245 mm³ seating overlap), while the native checks passed. Refining only
`MainBody`'s mesh to .01 mm linear / .1 rad angular deflection resolves that
disagreement: all five faceted contracts pass in 29.66 s. No frame material,
placement or assertion epsilon changes. Logs are
`carriage-frame-fit-exact.log`, `carriage-frame-fit-faceted.log` (red mesh), and
`carriage-frame-refined-faceted.log`. Running results are recorded below.

## Indexing restraint: red-first implementation

The unfitted running model wrongly shifts a seated carriage through the
indexing keys and seats a carriage between slots. All three new running
contracts fail (`carriage-index-running-red.log`, 21.394 s).

Native bisection establishes seated angular play
.18798828125..1884765625 degrees in both directions at all six working
positions, unchanged at 3 mm lift. At 5.8 mm lift the existing chamfer
increases it to .833984375..83447265625 degrees. This is not an on/off lock.
`tools/carriage_index.py --envelope` measures the minimum free lift against
angular displacement; it rises from 5.2006 mm just beyond the vertical flank
to 5.9501 mm at one degree. The measured envelope is stored as a public
expression in `carriage_index_motion.py`, with .18 degrees free-side play
and .05 mm axial contact clearance, reaching the existing 6 mm lift.

The same lift joint now reads both the pin slide and its carriage turn. It
uses the greater of their minimum lifts; there is no auto-lift, snap-to-slot
or completed sweep. The new independent geometry checks cover both shift
directions and all six slots, including between-knot contact tests. Running,
geometry, retained-motion, browser and visual results are recorded below.
No broader roadmap task is marked complete by this increment.

## Real pointer regression

`tools/operating_browser_probe.py --interlocks` adds actual selected-part
mouse drags, using only public control locations and admitted run readback.
The previous export (document SHA-256
`fd5ff8f64d1d67f3fd4ba463151260140929ecbbabfb47b2089da02aa0c92c60`)
fails the new assertions: the seated carriage admits 5.666666666667 degrees,
and seated clearing admits 4.666666666667 degrees, depressing the pin to
4.779114 mm while the carriage stays at zero. There are no page errors.
This baseline is `operating-interlocks-browser-red.log`. Public run resets
are only independent fixture setup, never substituted for a mechanical
clearing action.

The fresh version-7 export retains 23 inputs and 24 controls; all 154 unique
referenced model artifacts exist. The rebuilt document SHA-256 is
`dce471221a26866c154cae5cb0d91984075494f19ee0ce85a21ddfd3d5dd90ba`.
The same real gestures now stop shifting at .17999999999998786 degrees and
clearing at 1.437226368040361 degrees, with pin depression
3.0900000000000003 mm and carriage lift zero in both cases. All probe
assertions pass and there are no page errors
(`operating-interlocks-browser-green.log`). The inspected screenshot shows
both blocked outcomes and the unchanged assembly. The probe waits for the
admitted contact boundary instead of sampling a request still in flight.
This is hosted-browser evidence for these two restraints, not the full
standalone/all-controls acceptance matrix.

## Installed-world and adjacent-interface regression

The complete operating-model motion suite now passes 7/7 faceted (107.25 s)
and 7/7 exact (81.16 s). Its new test makes real retained requests, then checks
the installed body's seated angular stop, between-slot axial stop and the
clearing pin's frame contact with independent free/blocked perturbations.
The six existing crank, carriage, clearing, spring-seat and all-marker checks
remain green. Logs: `operating-interlocks-world-{faceted,exact}.log`.

The clearing-seat suite is extended through -360..360 degrees at three shifts:
4/4 exact (24.91 s), 4/4 faceted (20.88 s). The unchanged eight carriage stop-pin
checks also pass the exact runner (2.58 s); the source STL pin contacts remain
faceted even in that run. The body facing leaves 3.895589482 mm of this
unchanged pin exposed, still consistent with the manual's “about 4 mm”. Its
faceted rerun also passes 8/8 (2.50 s).
Logs: `clearing-seat-final-{exact,faceted}.log` and
`carriage-stop-after-body-{exact,faceted}.log`.

The independently advanced shared dependencies are now framework content
`6954e7cff5aa7a541efd68ece8d784e6831fc79b` and viewer content
`038f74d719a53ef17c807b6bd007406fa3512c11`, both clean when checked.
The viewer reports API 22 / unreleased 0.2.0 and bundle SHA-256
`7b8d3efc3d534acb4c6e2b3583000bd6cd8b3345d5f4981fa0a643f2808e75e4`.
Neither repository was changed here. The rebuilt-model browser check above
uses this pair. The final combined rerun also passes 13/13 (488.091 s): the
eleven restraint/profile tests, shifted arithmetic (retained 9 plus shifted
3 gives 309, counter 101), and successive additions with selective clearing,
reverse clearing and snapshot replay. Log: `interlocks-arithmetic-final.log`.
Both dependency heads are unchanged at this final check. This increment
continued into 2026-09-20; strict project OpenSpec validation passes.

The isolated fitted-body snapshot (`carriage-body-fitted.png`) was inspected:
the source key sectors, guide, bores and shallow annular facing are retained.
The pin/frame inspection (`clearing-pin-frame-stop.png`) shows the follower
and spring in the stopped pose; its low viewpoint occludes the lower tip,
so the clearance claim rests on the geometric contracts, not that image.
The steeper follow-up (`clearing-pin-frame-stop-above.png`) was also inspected
and exposes the lower tip over the frame land. It preserves the source head,
stem and seated spring; .05 mm separation is established by the tests.
