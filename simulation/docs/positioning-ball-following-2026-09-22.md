# Positioning-ball motion: the orbit candidate is rejected

The first all-rigid addition replay found a previously untested moving contact:
the source ball #419094 remains fixed while its bell pocket rotates away.
The unchanged ball is diameter 7.5 mm, despite the source's `6mm ball` name;
it is not one of the seventeen register-detent balls. Its source centre is
(9.627860318, 0, 30) mm and its native volume is 220.893233456 mm³.

The inspected source sections show a radial pocket in the bell at that height.
At a quarter turn the stationary ball intersects the complete bell by
38.827773610 mm³ native and 36.625749825 mm³ world64. Rotating measuring copies
of the unchanged ball with that pocket clears the bell, raised/unraised drum
and seated collar at the six sampled phases 0, 18, 90, 180, 270 and 360 degrees.
The native negative-control common at 18 degrees is invalid and explicitly
refused, not converted to zero. The valid quarter-turn positive is sufficient
to establish the missing motion. Manual pages 47–48 were inspected, but their
unfinished/mislabelled text is not asserted as an explicit motion instruction.

`tools/positioning_ball_contact.py` retains the read-only instrument. Its first
run stopped on the invalid negative-control common; the second records it and
continues without calling the result a clearance gate. Reports/images are
`_build_checks/positioning-ball-pockets[-refusals]-884b01e.*`; the complete JSON
SHA-256 is `b27274f92def966dbbd84a5116345456aa3dde213c864878d23ebfe2b07155f6`.

## Scoped candidate and regression

The provisional candidate gave the source ball a site-declared revolute joint
about its assembly's Z axis and directly followed the actual bell turn. Source
shape, centre radius, axial height and all rest placements were unchanged.
It did not rise with the stepped drum's 9 mm subtraction stroke or add a user
control. The whole-machine counterexample below rejects this candidate; it is
retained only in `positioning_ball_trial.py:OrbitingBallTrial`, not the manifest
or production assembly. Neither a motion law nor a manufacturing fit is adopted.

The actual-root test first fails on the measured 38.827773610 mm³ native
quarter-turn overlap. After the motion correction it passes in 43.857 s,
checking native and world64 clearance at four quarter-turn endpoints,
unchanged sphere size, the full-turn arithmetic result/counter, subtraction
lift, a further quarter turn, exact snapshot replay and identical restored
mesh vertices. The test's initial invalid `.5 / .2` cadence and incorrect
assumption that a partially moving register must already display its final
zero were test-harness errors; their failed logs remain preserved separately.

The meaningful red log is
`operating-positioning-ball-red-valid-cadence-884b01e.log` (SHA-256
`6c33588db7c4c16f38dbe62fffb0f9c2648fde45d821d5c16006a3edf2d28cce`);
the corrected green log is
`operating-positioning-ball-green-correct-partial-884b01e.log` (SHA-256
`75bd908434ef44c749abc33e29bc6dd1a3b891a3ba8562eb7c98bb72a5633b24`).

The provisional candidate bank has 214 coordinates. Five older fixture witnesses
were checked with the new ball coordinate exactly zero at rest and all original
213 entries against their unchanged historical SHA-256; none was re-recorded.
All five pass in 27.017 s. Log
`positioning-ball-preserved-witnesses-884b01e.log` has SHA-256
`3515454809628d3211431c86132b3f4f42227444521a4e2b5071a53c6bffcc07`.
These runs use framework main `a500a99`, including its independently validated
standing-bind cache, and project `884b01e` plus this explicitly recorded change.

## Whole-machine counterexample, not adopted

The candidate's 44-sample addition replay completes in 147.244 s, with the
same arithmetic outcomes and a rest inventory identical to the baseline.
It removes the bell/ball contact but adds **144.708 mm³** ball/main-frame
overlap. The stationary frame has its own radial pocket; orbiting the ball
away from that pocket is incorrect. The failed full-machine evidence is
`_build_checks/operating-addition-contacts-following-884b01e.jsonl`, SHA-256
`2efc4dced27ff4984dedc969f2f1495a5755f866ea5c85ef70e2c1b9751734f8`.
The reverse-nose/lower-drum pair remains positive and a crank/handle pair also
appears in this candidate run; none is waived or attributed to the ball
without a separate reproduction.

The provisional production wiring was removed before commit. Production
returns to its unchanged 213-coordinate bank and its existing witness tests.
The retained trial test now explicitly asserts the large frame collision,
beside the scoped bell-clearance/replay checks, and verifies production has not
adopted that joint. Radial translation within the stationary frame's pocket
is the next hypothesis to measure; it is not yet a validated motion law.

The retained negative-control suite passes two tests in 46.329 s: it reproduces
the frame collision and confirms the production root has no orbit joint. Log
`positioning-ball-rejected-orbit-contracts-884b01e.log` SHA-256:
`a1b514127bbb009223885d5631999c21a7fc6c8b40f7b1610576ad4c9c9b3ee0`.

## Radial measurement, not yet a follower law

The instrument's `--radial-sweep` uses only outward-translated copies and now
includes the stationary frame in both the measurements and inspected source
section. At 90 degrees, a 2.15 mm displacement still intersects the bell;
2.2 and 2.25 mm clear every selected neighbour. At 2.5 mm the seated collar
is penetrated by .087034407 mm³ world64. The finite sweep is six bell phases,
two drum heights and nine ball offsets (108 combinations); all numerical
refusals remain recorded, not waived. Report
`_build_checks/positioning-ball-radial-source-884b01e.json` SHA-256:
`b9400ef21e30b8ece08eee4e442dbf7a76f06675600e7d8a90497af3a5f69913`.
It supports radial travel within the frame's fixed pocket, not arbitrary
orbiting. Continuous phase following, radial capture, collar-lift interaction
and wrong-order restraints still need measurement before adoption.

Native surface extraction identifies the stationary guide as an R3.81 mm
cylinder on the X axis through (15, 0, 30), providing .06 mm radial allowance
around the original R3.75 ball. The rotating bell's outside cylinder is
R8.041 mm. Its cone has a 37.5-degree half angle and apex
(2.089951381107820, 0, 30), opening along +X at rest. These source dimensions
explain why the ball should remain on the frame's radial guide, not orbit with
the bell. The analytic outer-land centre is 8.041 + 3.75 = 11.791 mm before
any explicitly declared seating gap. The original centre is 9.627860318 mm;
its difference is 2.163139682 mm. The measured 2.2 mm displacement clears both
native and world64 solids at the quarter turn; it is not a fitted ball radius.

Raw native face identities, bounds and axes are retained in
`_build_checks/positioning-ball-pocket-surfaces-built-884b01e.json` (SHA-256
`d2faf2e7a1ff752689c6a838b507ebba5da4947661b0d7d9ad6f521b1a6a21f2`).
The first extraction omitted assembly and failed; the `-built-` run correctly
uses an assembled operating root. No source CAD or production motion changes
were made for these measurements.

## Measured radial limits: trial only

Two independent instruments now measure the available interval along the
stationary X-axis guide. They use a declared .05 mm normal seating gap:
the distance gauge is R3.80, while the tested original ball remains R3.75.
Twenty bisections locate a clear-side positional bracket; this is not a
positive-volume tolerance and every final overlap check must equal zero.

`tools/positioning_ball_envelope.py` measures 361 bell phases, 0–360 degrees
inclusive at one-degree spacing, using native point-to-solid distance.
Every final unchanged ball clears the bell and frame in native solids and
the bell, frame and seated collar in world64 meshes. The required centre
radius is 8.332135134696959 mm at rest and 11.841003148078919 mm on the
outer cylindrical land. The complete run takes 90.022 s and leaves the
production 213-coordinate bank unchanged. Its JSON-lines report is
`_build_checks/positioning-ball-radial-envelope-a2d0783.jsonl`, SHA-256
`d5cd67bd4163746466412458010656dc36dc07af4c2a16499e72b12cfc0ad5c9`.

`tools/positioning_ball_collar_envelope.py` measures 25 collar lifts from
0 to 6 mm at .25 mm spacing. The collar has no native source solid; its
point-to-triangle distances and final collar/frame clearance are world64
evidence only. Its permitted outer centre radius decreases from
11.949090957641602 mm at rest to 8.402658462524414 mm at full lift.
All 25 final ball placements clear both selected neighbours. The run takes
18.708 s and preserves the production bank. Report
`_build_checks/positioning-ball-collar-envelope-a2d0783.jsonl`, SHA-256
`efe5b7b096b1504c21bc1d06043a6093480a31a60afe718556c71ee41d61f3fc`.

The measured rest ball has slack between these surfaces. A trial therefore
tests unilateral following: the advancing bell pushes it out, the advancing
collar pushes it in, and neither retreating surface pulls the free ball.
The two intervals nearly close with the carriage raised, giving an empirical
candidate for a crank/carriage wrong-order restraint. This is kinematic
contact, not a claim about forces, friction, preload or rolling.

`positioning_ball_profiles.py` retains the measured asymmetric bell profile
and collar profile; `RadialBallTrial` is not selected by the manifest.
Dense between-knot clearance, actual retained-motion tests, incompatible
motion and relief, all-rigid replay, browser parity and inspected poses
remain adoption gates. Initial trial wiring errors (an out-of-scope read,
then reads of plain calculation ports) are preserved as failed harness
logs; they are not framework limitations or successful motion evidence.

The independent between-knot instrument now passes 1,022 placements in
176.750 s: bell ramps at .1-degree spacing, the cylindrical land at one
degree, and collar lifts at .05 mm. Every selected native/world64 common
is exactly zero and the operating bank remains unchanged. Report
`_build_checks/positioning-ball-between-knots-a2d0783.jsonl` SHA-256:
`a687ef6d59329584fc371ecad50380f2e1bf8c8a588b395df81b48663b90aa20`.
These are copied placements, not a passed motion law or all-neighbour proof.

The correctly scoped self-read trial fails both motion tests in 85.506 s.
It pushes the ball out to 2.213142830078919 mm displacement but pulls it
back to -1.2957251833030412 mm on bell retreat. With the carriage raised,
the next crank request blocks at zero rather than traversing the measured
remaining clearance. The log
`_build_checks/radial-positioning-ball-root-constraints-a2d0783.log` has SHA-256
`f224537f9d0d6c9ca8cb19cf6c3f3a687211697956aee34bf0f1ee819b2312b5`.
This demonstrates that the authored switching law does not implement the
intended unilateral follower. Framework and viewer review distinguishes the
existing endpoint-difference law semantics from the needed retained contact
behavior; no existing contract is silently reinterpreted.

## Retained following implemented; ring contact remains an adoption blocker

Framework main `f4c48f6` now supplies the separately specified `Follow` law.
The unadopted radial trial uses the actual bell and collar joints as the two
ordered envelope inputs and the ball's retained slide coordinate. Both desired
root motion tests pass in 167.896 s: the retreating bell leaves the free ball
at its previous outward displacement, and a raised carriage admits the
remaining clearance before blocking the crank. Relief then permits motion.
The corresponding log SHA-256 is
`35e9b3d75f731ca19c26239923f0c4622fb3f0571771c7014ec0e546c60895d4`.
This corrects the trial's motion semantics, not its complete geometry.

A complete rigid-pair addition inventory (44 samples, 419.718 s) removes
the bell/ball pair but adds a thrust-ring/ball pair. No other pair changes.
Its maximum world64 volume is 1.5840910147693048 mm³. The independent native
quarter-turn witness is 1.8489085924262987 mm³. The desired ring-clearance
regression remains red in both kernels (40.215 s). Production `OperatingCurta`
still has the original static ball and its 213-coordinate bank.

The unchanged seated ring has inner/outer radii 12.3/16.35 mm, bottom/top
planes at world Z33.05/34.55, and thickness 1.5 mm. Each annular plane has
area 364.52684957765837 mm². At the outward witness the native common extends
approximately X12.108..14.023, Y±2.165 and Z33.05..33.722. The inspected
section shows the collision at the bottom inner lip, distinct from the
outer collar ledge and top spring seat. A local underside passage may be
possible, but its exact protected-seat and complete-travel proofs are not
yet supplied. No ring fit, smaller ball, altered seat height or hidden
neighbour is adopted by this finding.

Artifacts under `_build_checks/` (SHA-256):

- `follow-ball-trial-addition-contacts-f4c48f6.jsonl`:
  `2861e3a1d3691eb6db80b9aeb23f887b02d39c4744fa8cd7569df3be53416200`.
- Native ring measurement report:
  `05e69db1a3568c00ea677e17b371fa5877a34b3ff8cf5b4e7829184d0f6c136c`.
- Inspected `follow-ball-thrust-ring-section-4cd6ec4.png`:
  `97f1aa80f6bad1ff6f6980c0df71884cb7f5e820955147224b58260cc9485647`.
- Desired ring-clearance red log:
  `f1428ff41dcef1630b2241083a043fc03dcca1dd856cc2284e754f7034dd5a89`.
