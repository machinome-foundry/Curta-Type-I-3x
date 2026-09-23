# Author review: simulation fits and unresolved findings

**2026-09-22 follow-up:** the placement-only thrust-ring/spring seating
candidate is now in the operating root (`1fc3e00`); source solids are unchanged.
Its scoped geometry, motion and browser evidence is in
[the resumption record](resumption-2026-09-22.md). The September 21 status
below predates that adoption. Higher-result/counter candidates and the
clearing-loop clip remain unresolved; no whole-machine acceptance is claimed.

**Later September 22 reconciliation:** the collar shoulder and pin/thread
clocking are now adopted together with bounded .05 mm collar-bottom and
washer-end facings. The default operating assembly passes all four scoped
collar contracts on both runners; see F19 below. Historical trial descriptions
later in this register retain their original checkpoint status.

**Counter-ones follow-up:** F20 below installs only the fixed-height T08
counter-ones fit and measured crank restraint. Production stop/replay/contact
and independent fixture checks pass; fresh final pointer/performance
acceptance and every higher counter remain separate obligations.

Review checkpoint: 2026-09-21. This is a review agenda, **not a list of proven
defects in the author's working printed calculator**, nor instructions to
modify a physical machine. The simulation reconstructs the supplied assembly
and assumes rigid contact except where flexible motion is explicitly modeled.
Actual print compliance, finishing, glue depth and assembly calibration can
differ. All upstream STEP/STL files remain unchanged.

“Implemented” below means present in the simulation, with scoped evidence;
it does not mean whole-machine or manufacturing acceptance. Older trial values
in the measurement log are historical; the values below identify current code.
No overlap is waived by this index.

## Implemented material-removing fits to review

| ID | Part/interface and current simulation change | Evidence and implementation |
|---|---|---|
| F01 | Input gear outer profile relieved .35 mm; counter ones stack .36 mm. The operating candidate's five higher counters use .42 mm (trial T04); keyed bores and heights retained. | [Measurements F4 and complete drum](measurements.md#f4-drum-to-input-tooth-fit), [full-bank reversal](reverser-fork-and-follower-2026-09-20.md), [fit.py](../fit.py), [reverser_inputs.py](../reverser_inputs.py). |
| F02 | Input sleeves and spacers reduced to outside R3.85; keyed bores retained. | [fit.py](../fit.py), measurements F4; same input/drum tests. |
| F03 | Bevel head seated 1.2 mm lower with the newly protruding stem end removed, preserving the original bearing-plane datum. Historical .8 mm isolated trial is not the installed value. | [Frame clearance](measurements.md#bevel-fit-must-also-clear-the-frame), [fit.py](../fit.py), `test_bevel_bank.py`, `test_transmission.py`. |
| F04 | Carry pinion outer profile relieved .42 mm; locking outline .15 mm with its clipping profile clocked back 4°, not its keyway. | [Carry fits](measurements.md#carry-fits-and-current-engagement-boundary), [fit.py](../fit.py), `test_carry_mesh.py`, `test_carry_bank.py`. |
| F05 | Carry slider fork sleeve cut R4.02, bounded flange cut R6.22, reset shoe disc/sole relief with .05 mm seat gap; guide and detents retained. | [carry_fits.py](../carry_fits.py), [carry measurements](measurements.md#carry-trigger-fork-and-reset-shoe--open-contact-checks), `test_carry_fits.py`. |
| F06 | Carry slider dial-pin contact tip faced to installed Z31.15 for result sliders, Z16.45 for counter sliders. | [carry_heads.py](../carry_heads.py), measurements following F05; `test_carry_heads.py`. |
| F07 | Bearing plate receives a .70 mm diameter, 6.1 mm deep pawl spring-tail bore; pawl collar top trimmed .20 mm. | [Pawl and mounts](measurements.md#anti-reversal-pawl-and-its-spring-mounts), [fit.py](../fit.py), `test_frame.py`, `test_pawl.py`. |
| F08 | Carry-spring closed-fold seats relieved for .60 mm wire with .05 mm radial allowance; long legs/hooks unchanged. | [Spring seats](measurements.md#carry-springs-and-their-detent-seats), [carry_seat.py](../carry_seat.py), `test_carry.py`. |
| F09 | Clearing cover annular floor deepened .675 mm to local Z8.325, R49.05..52.5; walls and mounting pattern unchanged. | [Clearing strips and fitting](measurements.md#clearing-strips-omitted-from-the-step), [clearing.py](../clearing.py), `test_clearing.py`, `test_clearing_contact.py`. |
| F10 | Dial clearing-cam outer flanks relieved .10 mm only in the clearing bands; dial faces and bevel teeth retained. | [dial_fits.py](../dial_fits.py), measurements clearing section; `test_dial_fits.py`. |
| F11 | Formed clearing strips/spacer receive a retaining-screw back relief R2.15; no clearing tooth removed. | [Retaining screw](measurements.md#clearing-retaining-screw-relief), [clearing.py](../clearing.py), `test_clearing_fasteners.py`. |
| F12 | Operating clearing pin lower tip shortened 2.54 mm; head, shoulder and follower position retained. | [Carriage/clearing fits](carriage-interlocks-2026-09-19.md), [clearing_seat_fit.py](../clearing_seat_fit.py), `test_clearing_interlock.py`. |
| F13 | Counter/carriage body underside: .95 mm annulus R31.7..34.25, general underside .05 mm facing, existing indexing-pocket ceilings deepened .05 mm within R21.9..34.25. | [Bounded body fit](carriage-interlocks-2026-09-19.md), [carriage_frame_fit.py](../carriage_frame_fit.py), `test_carriage_frame.py`. |
| F14 | Digits cover inner top land faced .10 mm through R61.55; seventeen axle retaining flats extended .15 mm; upper housing receives seventeen R2.995 axle-end pockets. Windows and axle bearing lengths retained. | [Cover neighbours](measurements.md#cover-neighbours--measured-local-fits-after-resumption), [cover_fits.py](../cover_fits.py), `test_covers.py`. |
| F15 | Female housing thread/seat locally lapped against the actual male print, with ±.02 mm X/Y and ±.05 mm axial fitting envelope, clipped to R71.9..75 and local Z35.9..42.4. Thread pitch unchanged. | [Thread fit and rejected cutters](housing-thread-fit-2026-09-20.md), [cover_fits.py](../cover_fits.py), `test_housing_thread.py`. |
| F16 | Reversing actuator's sixth sleeve seat opened at the actual input axis to R3.9 through 4.5 mm; only its existing 1.685 mm tooth slot opened to R6.28. Original axial faces and other five seats retained. Originated as T02. | [Fork measurement and bounded removal](reverser-fork-and-follower-2026-09-20.md#local-fork-relief), [reverser_fits.py](../reverser_fits.py), `test_reverser_seat_trial.py`. |
| F17 | Reversing-shaft body raised 1.9 mm; mounting shoulder shortened to local Z115.05, neck end119.6, stud end125.6 mm; finished M4 major envelope R2.0. Installed fastening-end height retained. Both pockets and all geometry below local Z110 unchanged. Originated as T01/T03. | [Initial dimensions](reverser-seat-trial-2026-09-20.md), [continued M4 fit](reverser-fork-and-follower-2026-09-20.md#finished-m4-end-not-the-unthreaded-blank), [reverser_seat_trial.py](../reverser_seat_trial.py). Not a release drawing or thread-load certification. |

## Additional ones-lockout fit — F18

Implemented scoped fit: **F18**, result ones locking outline only,
.15 → .16 mm outer-profile relief. A normal input 3 leaves a valid native
overlap of 0.00005969798 mm³ at shaft 220° with the earlier fit; the published
mesh misses it. All five indexed flats clear after the additional .01 mm,
with the keyed core, height and two-sided locking retained. See the
[restraint and fit record](result-locking-2026-09-20.md). The actual operating
tree clears the input-3 pose in both kernels; restoring the earlier source
class reproduces the failure. Four fit contracts pass under both runners,
including protected material and retained locking. This is not a finding
that the author's physical build jams or a manufacturing recommendation.
The separately isolated [periodic-stop software defect](periodic-lockout-stop-2026-09-20.md)
is now corrected in both executors. The fixed-height ones profile is
[wired into the operating crank](operating-ones-lockout-2026-09-20.md), with
full-root lockout, neighbouring arithmetic/history and browser acceptance
passing. This introduces no further geometry fit
and does not adopt the profile on other channels.

## Collar seats — F19

The [completed collar fit](collar-seat-completion-2026-09-22.md) removes the
previously measured .72 mm annular shoulder skin, .05 mm at the collar bottom,
and .05 mm from each washer end. It does not translate the collar or washer,
change their radial datums or remove thread/pin-roof material. The collar is
clocked to world -90° to meet the actual carrier pins, and the unchanged nut
is phased to 40° at its retained Z12.3 seat. All source assets are unchanged.

The default-root checks prove complete rigid rest neighbours, moving
clearance and capture at all six carriage positions and both clearing-ring
rest positions, plus the independent fixture and unchanged initial bank.
They pass 4/4 on each runner. The collar remains faceted geometry in both.
An independent 1,161-pair survey has no residual collar/nut/washer contact;
the whole-machine inventory remains separate. This is a simulation fitting
record, not a physical manufacturing recommendation.

## Counter-ones locking outline — F20

The [production continuation](counter-ones-adoption-2026-09-22.md) adopts only
the counter-ones portion of T08: existing .15 mm outer-profile relief becomes
.16 mm, with finer complete-print tessellation. The keyed core, axial extent,
source placement and two-sided locking remain. The production part equals
the independently measured trial; an explicit pre-adoption fixture preserves
the bounded-removal proof after adoption. Both short/long actual crank stops
are clear on native and mesh geometry, with positive .2° overtravel,
snapshot replay, reverse relief and retained idle state.

This fit changes no upstream asset and is not a physical-build failure claim
or manufacturing recommendation. The separate framework stale-exact-artifact
bug exposed by its fixture is fixed in `4112d76`; the final two-test fixture
rerun passes. The higher-counter trial below retains its historical status;
those five stations are not adopted by F20.

## Clearing-cover / counter-body seat — F21

The [outer-seat continuation](clearing-carrier-seat-2026-09-22.md) removes
only the counter body's local Z0..0.85 land outside R46.75 to clear the actual
R46.8 cover shoulder, with a .05 mm radial/axial gap. The source body datum,
inner bearings, bores, indexing geometry, extents and remaining flange are
preserved; the cover and clearing teeth are unchanged. Production checks pass
3/3 per runner, including sampled sweep/shift clearance, retained axial stop,
bounded removal/connectivity and an unchanged initial bank. The refreshed
rest inventory loses only this pair and adds none. This is a simulation fit,
not a manufacturing instruction or whole-machine clearance certificate.

## Lower housing key and bearing seats — F23

The [lower-frame continuation](lower-frame-seat-2026-09-22.md) retains the
concentric source datums while relieving the upper key flank's measured
.39 mm crossing plus .05 mm clearance. Its bounded local cutter is capped
at R64.4805 and Z128.2..132.1; the deeper key and outer wall remain. A separate
.05 mm facing of the Z12 bearing shoulder inside R64.111 establishes a real
seat gap where local-STL rounding otherwise overlaps native-flush faces.
Production checks pass 6/6 per kernel; the five original enclosure regressions
also pass per kernel. Both seats retain .1 mm blocking capture. Full world64
rest inventory adds no pair; other contacts are not waived. No upstream asset
changes and this is not a manufacturing recommendation.

## Pinned crank coupling — F24

The [crank seat correction](crank-coupling-seat-2026-09-22.md) translates the
complete handle assembly (-.091031728, .337283020, 0) onto the unchanged
shaft and pin axis. Only the R4.56 internal pocket roof is extended to local
Z29.15, .05 mm beyond the installed shaft tip. The transverse bore, pin,
crank clocking and height are retained. Seven contracts pass per kernel,
including actual two-mode turning, bounded removal/connectivity, unchanged
initial bank and ±.75 mm pin capture. The rest inventory loses only the
crank/axle pair and adds none. This is not a manufacturing recommendation.

## Remaining result locking outlines — F22

The [production bank continuation](result-bank-adoption-2026-09-22.md) adopts
the T07 .15 → .16 mm outer-profile relief at stations 3..11. Each source-specific
complete upper print, keyed core, axial extent and installed pivot is retained;
the fitted prints equal their independent trial. All ten higher stations pass
indexed-clearance and two-sided-contact checks; the finite dense matrix has
471,120 admitted native/faceted checks. Actual hundreds/eighth withdrawal
stops, short/long requests, overtravel contact, exact replay and reverse relief
pass. Fresh browser stopped/relieved banks match Python exactly in all four
cases. Expanded-root arithmetic now passes all six tests; full pointer
acceptance remains open. Historical faceted matrices used world32; the
[precision record](mesh-probe-precision-2026-09-22.md) identifies the new
world64 rechecks and their finite sampling boundary.
No upstream asset changes and this is not a manufacturing recommendation.

## Higher result lockout — historical T07 adoption checkpoints

The [higher-result investigation](higher-result-lockout-2026-09-21.md) records
**T07**, a .15 → .16 mm outer-profile trial on the result tens lockout. Its
source-backed normal indexed pose has a tiny native-solid overlap missed by
the mesh. The trial keeps the keyed core, height and placement. Coarse mesh
also misses an existing negative locking contact both before and after T07.
Refining only the diagnostic bell's tessellation restores that contact without
changing its native solid. The expanded six contracts pass on both kernels,
including 925 sampled poses following the actual carry tooth passage and a
deliberately frozen engaged-gear negative control. Upstream CAD is unchanged.
The isolated moving-restraint candidate now stops raised/lowered withdrawal
and axial entry, with exact replay, reverse relief and complete-print
stop/overtravel checks. Python and an isolated browser agree; ordinary source
tooth trajectories remain admitted. Native-only release measurement first
missed both a mesh contact and an isolated native Boolean blind spot; the
combined profile now passes dense verification, carry-tooth support refinement
and full-tree Python/browser acceptance with exact retained-bank agreement.
The trial's three neighbouring arithmetic cases now pass (8666.232 s).
The default operating root has been wired to the same tens fit, refined bell
and moving bound; the historical trial entry point inherits them without
repeating the constraint. Production stop/replay/free-support (3/3), the
original ones/pawl regression, both six-test fit suites and fresh browser
acceptance now pass. All four 213-coordinate production Python/browser
stopped/idle banks agree exactly. Production arithmetic remains in progress,
so final adoption acceptance remains open. See
the [continuation record](operating-continuation-2026-09-21.md).
This is not a manufacturing recommendation.

The then-new independently placed result-bank probe also finds indexed contact on
all ten higher result stations with the existing .15 mm simulation fit:
normalized flat 3, both carry seats. The complete-print indexed test is red
with 30 kernel/station/seat failures. No bank-wide .16 mm fit or shared
restraint was adopted at that checkpoint; F22 above records the later production
continuation. The [checkpoint evidence](evidence/handoff-checkpoint-2026-09-21.json)
retains all 100 measured poses. These small rigid-simulation overlaps do not
establish that the author's physical builds fail.

## Higher-counter locking outlines — F25

The [production counter-bank continuation](counter-bank-adoption-2026-09-22.md)
adopts the independently measured T08 .15 → .16 mm outer-profile relief at
stations 2..6, retaining each complete source upper, key, height and pivot.
Five default-root short/long withdrawal tests pass native/world64 clearance,
positive overtravel contact, replay, relief and idle/retry checks; their reports
are byte-identical to the independent trial. Six production parts/fixture/law
tests pass. Further final acceptance gates are recorded separately; there is
no upstream asset change, whole-machine clearance claim or manufacturing advice.

## Reverse-nose plate lower drum seat — F26

The [bounded seat fit](reverse-nose-seat-2026-09-23.md) relieves only .05 mm
from the lower face inside the drum's R9 swept land plus .05 mm radial gap.
The original upper axial stop, outline, screw mounting and all placements
remain unchanged. Native and world64 clearance/capture and material-preservation
checks pass, with exact unchanged bank and all other rigid meshes at rest
and after a half-turn. Paired 44-sample addition replays remove only this
moving contact, adding no pair or changing any other spatial overlap.
Five production checks pass. This is a simulation fit, not manufacturing
advice or a whole-machine clearance claim; upstream assets stay unchanged.

## Crank-grip lower face — F27

The [grip-seat fit](crank-grip-seat-2026-09-23.md) removes only .05 mm from
the source bottom face, leaving its bore, screw seat, placement and motion
unchanged. Four production tests prove moving clearance, bounded removal and
retained axial capture. The paired addition survey removes two tiny positive
crank/grip contacts and adds no pair. The existing screw/grip common's native
material is unchanged, while its scalar native/faceted volume results are
not bit-identical; that overlap is explicitly retained as a finding. Upstream
assets remain untouched. This is not manufacturing advice or whole-machine
acceptance.

## Complete carry-bank frame passages — F28

The [bank-wide frame fit](carry-bank-frame-investigation-2026-09-23.md)
extends the verified first pair to all ten result and five counter stations.
Only independently bounded shoulder and spring-leg passages change, with a
.05 mm running gap and at least 99.78% of the mapped guide registration lands
retained. The frame remains one valid connected solid; protected bores,
fasteners, moving parts, placements and laws stay unchanged. All fifteen
slider/spring paths have native conservative enclosure proofs and native/
world64 sampled clearance. Production material/stroke and root-identity checks,
spring/fork capture and six exact demonstration replays pass. The separate
unchanged guide/slider contacts remain unresolved. This is a simulation fit,
not manufacturing advice or whole-machine clearance certification.

## Positioning-ball thrust-ring passage — F29

The [bounded ring passage](thrust-ring-passage-2026-09-23.md) removes
2.428916 mm³ only from the lower inner lip for the unchanged R3.75 ball's
supported radial path. The complete upper spring seat, outer collar support,
installed heights and all other parts remain unchanged. Native continuous
enclosure, 2,501 native/world64 poses, negative controls and production
seat/capture/lift/shift/replay checks pass. The paired radial addition replay
removes exactly the ball/ring contact and changes no other pair. Only the ring
is adopted: production ball motion and whole-machine acceptance remain open.
Upstream assets are unchanged; this is not manufacturing or strength advice.

## Reversing ones inner-flank fit — F30

The [operating adoption record](reverser-operating-adoption-2026-09-23.md)
records the three ones pinions' .43 mm flank relief inside R6 only. Outside
that radius the existing .36 mm fitted profile is retained, preserving the
fork-capture tips; the keyed core, axial extent and phase are unchanged.
The five higher input pinions retain their existing .42 mm fit. This is a
source-derived simulation fit, not an upstream CAD edit or manufacturing
tolerance recommendation.

Uniform relief was rejected because it lost fork capture. The protected
inner-only adjustment passes one-valid-solid, no-added-material and bounded
removal checks, and the 25-pose closest-passage survey retains at least .01 mm
native separation. Installed native/published-mesh outward cover proofs and
the earlier capture evidence are retained in the
[contact-cover investigation](reverser-profile-cover-2026-09-23.md).
Five default-root contact/path tests now pass with the compiled lever bound;
fresh arithmetic, export and production browser checks remain distinct gates.
This does not certify the whole machine or continuous swept clearance.

## Counter lockout trial — historical T08 checkpoint

The [counter investigation](counter-lockout-investigation-2026-09-21.md)
records indexed-position native contact on all six counter stations with the
existing .15 mm fit. The isolated **T08** candidate increases only their
outer-profile relief to .16 mm and refines the complete upper-print meshes;
source pivots, keyed cores and axial extents are retained. Sixty indexed
poses clear and 300 two-sided locking poses retain contact in both kernels.
Protected-material and connected-print checks pass. Ordinary motion now passes
12,645 complete-print poses across all six candidate stations in both kernels.
The fixed-height ones profile now passes 11,858 admitted poses per kernel;
its isolated full-machine short/long stops pass native/faceted contact,
replay and relief checks. An independent browser run reaches the same stop
angles with replay/relief/idle/retry and no page errors. A fresh Python
idle/report test passes; all four 213-coordinate stopped/idle banks match
the browser exactly. Ordinary trial arithmetic is still running.
Higher-counter profiles and operating restraints remain unproved; the three
sampled tens heights already show changing contact windows.
No production counter geometry or upstream CAD changes from this candidate;
it is neither a physical-build failure claim nor a manufacturing recommendation.

## Assembly, source-representation and motion corrections — not new prints

The separate [collar shoulder trial](collar-seating-investigation-2026-09-21.md#isolated-shoulder-facing-trial)
is not adopted. A .72 mm annular facing leaves .05 mm below the unchanged
spider, preserving the actual source stem profile, bore, threads and flange.
Four scoped tests pass on both runners (collar contacts remain faceted),
including clearance/capture, bounded removal, STL validity and the source
negative control. The actual-root measuring copy clears the spider but still
contacts the thrust ring, nut and two pins. No complete collar fit, operating
adoption or manufacturing recommendation follows from this trial.

The separate [thrust-ring/spring seating candidate](thrust-seat-investigation-2026-09-21.md)
uses the existing collar ledge and sleeve underside, with .05 mm seating gaps.
It raises the ring 7.5275 mm and prescribes coil height from the two seats,
retaining wire size, radius and turn count. No rigid print is cut. Five tests
pass on both runners, and the actual-root rest measuring copy clears all
777 ring/wire neighbour pairs without changing the run bank. This remains
unadopted; it is not a force/preload calculation or whole-machine acceptance.

| ID | Correction or explicit assumption | Record |
|---|---|---|
| A01 | Register carriage recentered by (.537721035, −.038177283, 0) mm and clocked .549916905°; result tens shaft X corrected −.079764273 mm. | [F3](measurements.md#f3-register-bank-alignment-and-bevel-seating), [fit.py](../fit.py). |
| A02 | Input clocking +4°, bevel/dial clocking −3°, dial-zero indexing and carry half-pin orientation reconciled with installed contact. Half-pin type-2 mounts have an additional 9° source difference. | [Installed phase](measurements.md#installed-bank-engagement-and-phase-centering), [pin_mounts.py](../pin_mounts.py), measurements clearing/carry sections. |
| A03 | Author's printable carriage-stop pin used instead of contradictory STEP Boolean representation; installed .51 mm deeper, retaining about 3.846 mm protrusion. | [Operating completion](operating-curta-completion-2026-09-19.md), [carriage_stop.py](../carriage_stop.py). |
| A04 | Lower enclosure group recentered (.406900356, −.745841949, 0) mm; base and bolts seated .05 mm lower. All lower markers/fittings move with their group. | [Enclosure seats](enclosure-seats-2026-09-20.md). |
| A05 | Reverser spacers moved to measured frame seats: upper +3.9075 mm, lower −7.6427 mm. Now used by the operating candidate. Working knob positions −4.9425/+3.9075 mm; lower housing overtravel stop −6.9425 mm. Pinions sit .0925 mm above knob displacement, centring the source fork play. | [Reverser continuation](reverser-fork-and-follower-2026-09-20.md), [reverser_assembly.py](../reverser_assembly.py). The lower detent is not modeled as a rigid stop. |
| R01 | Invalid zero-positioning spring replaced by a manual-based analytic wire model: 1.1 mm wire, five turns. | [F1](measurements.md#f1-invalid-zero-positioning-spring). |
| R02 | Unreliable STEP cover/housing/collar solids use original printable STL representations; three missing clearing strips are imported from the author's prints and formed per the manual. This is distinct from F09/F11/F14/F15. | [F2](measurements.md#f2-unreliable-digits-cover--upper-housing-boolean), [clearing strips](measurements.md#clearing-strips-omitted-from-the-step). |
| R03 | Pawl, carry, clearing-stop and drum-positioning springs have prescribed flexible motion; native mounts/hooks retained where stated. Spider retains native ring/tips, with seventeen analytic tapered fingers using a bounded inner approximation of the upper cone. Named seat/preload allowances are not force/strain validation. | [Spring measurements](measurements.md#stepped-drum-positioning-leaf-spring-source-and-ownership), [spider](measurements.md#register-balls-and-the-tapered-spider-spring), [retaining_spring.py](../retaining_spring.py), [spider.py](../spider.py). |
| R04 | Finer frame, sleeve, track and spring tessellation; bounded generated-mesh encoding corrections for cover fits. Native source geometry is unchanged by tessellation. Tiny positive intersections remain failures, not silently rounded away. | [Cover/thread evidence](housing-thread-fit-2026-09-20.md), [enclosure](enclosure-seats-2026-09-20.md), [rest inventory](operating-rest-inventory-2026-09-20.md). |
| R05 | Reversing ball follows the original pockets, rim and shaft land radially; analytic spring retains source .51 mm wire, R2.295 coil centre, 6½ turns and 11.1 mm free centreline height. A .05 mm named seating gap preserves contacts. Ball remains the source's R2.7, not silently replaced by nominal 5 mm hardware. | [Follower dimensions and independent original-print checks](reverser-fork-and-follower-2026-09-20.md#radial-ball-and-spring-following), [reverser_following.py](../reverser_following.py). Geometric restoring direction only, not force/friction or automatic snap. |
| M01 | Negative clearing-sweep modulo corrected; retained carriage/clearing restraints use measured contact envelopes and require separate release. These are simulation logic corrections, not physical modifications. | [Restraints and red-first evidence](carriage-interlocks-2026-09-19.md). |
| M02 | Result engagement now derives from actual lower-drum axial bands and pinion heights instead of a half-lift mode switch or fractional tooth count. No print geometry changes. | [Partial-result engagement](result-partial-engagement-2026-09-20.md). Both contact kernels, retained partial-selector/replay, calibration and full-bank subtraction/overflow checks pass. Wrong-order locking-disc restraint remains open. |
| M03 | The operating crank now reads the actual bell and retained ones shaft for its measured closing restraint, intersecting the original pawl limit. Both executors attribute a long request's push at first contact. | [Full-root adoption and remaining acceptance](operating-ones-lockout-2026-09-20.md), [paired software correction](periodic-lockout-browser-2026-09-20.md). No new print modification; higher sliding channels remain separate. |
| M04 | Carry preparation under a higher-stack observer exposed two engine errors: wrong relative landing direction and false chatter from rounding in following contact. Corrected in framework and viewer without a clearance/tolerance or carry-law change. | [Integrated correction and full-bank parity](mixed-contact-engine-2026-09-21.md). This is not a defect attributed to the author's printed mechanism and requires no physical modification. |
| M05 | The provisional T07 contact table falsely blocked ten geometrically clear near-edge positions. All 110 support-edge measurements now refine that table without changing a printed part; a physical selector-withdrawal request changes from falsely blocked to completed in Python and the browser. | [Support refinement and acceptance gates](higher-support-refinement-2026-09-21.md). This is a trial simulation-restraint correction, not a new manufacturing recommendation. |

## Current candidate and unresolved work

The [positioning-ball orbit candidate](positioning-ball-following-2026-09-22.md)
is rejected: it clears the bell but penetrates the stationary frame. Its scoped
passes are not whole-machine acceptance; radial following remains to investigate.

The [fork/follower continuation](reverser-fork-and-follower-2026-09-20.md)
preserves trial IDs T01–T04 and their rejected variants. The tested candidate
is now wired into `OperatingCurta` (F01/F16/F17, A05/R05 above). This is scoped
simulation adoption, not whole-machine or fabrication acceptance.

- Counter reversal now passes the six-input working-position bank on both
  kernels, spring/follower and housing-overtravel checks, and the first
  four-turn retained-arithmetic scenario. Partial lever engagement is derived
  from the actual source tooth bands, including one-tooth engagement on higher
  channels when unseated. Installed-world motion passes both kernels, and
  ordinary hosted down/up gestures pass, as do all 24 carriage-position ×
  crank-mode × lever-position cases. The standalone/full pointer matrix and
  mid-cycle restraints remain tracked in the continuation.
  These results include F01 tooth relief; they do not certify untouched gears.
- The [operating rest inventory](operating-rest-inventory-2026-09-20.md) records
  390 rigid occurrences with 268 positive faceted pairs / 166 native-or-STL
  pairs at its dated checkpoint. These counts are not independent defects.
  Largest contacts include spider mount/collar, clearing cover/counter body,
  and thrust ring/collar; bottom housing/main body, threaded fasteners and
  internal ball/spring seats also remain. The committed pair lists preserve
  exact targets and quantities. No later full inventory is claimed here.
  The subsequent [collar-only height survey](collar-seating-investigation-2026-09-21.md)
  rejects all nine tested rises as complete fixes: clearing the spider worsens
  the thrust-ring fit and leaves other contacts. No new fit is adopted.
- [Clearing-loop clip/release](clearing-loop-investigation-2026-09-19.md)
  remains unresolved. A forced permanent hinge or straight upward release is
  not justified by the manual's clipping action.
- Crank/selector wrong-order restraints, full motion/interference matrices,
  and complete hosted/standalone pointer checks remain on the
  [roadmap](../../openspec/changes/simulate-the-curta/tasks.md).
  A mid-turn selector withdrawal now has a measured closing-disc/lockout
  contact and a [nested-constraint reproduction](nested-lockout-constraint-2026-09-20.md);
  its [ancestor-constraint acceptance](ancestor-lockout-2026-09-20.md) uses a
  separate full-tree diagnostic, not a production whole-machine restraint or
  evidence for modifying the author's locking disc. The complete bell and
  published mesh both clear at a local 125.32° stopping point; other phases,
  channels and action orders remain unvalidated. Hosted requests and a real
  pointer drag stop there with the existing 608 descendant paths and 25 controls;
  focused existing-model arithmetic, partial-input replay and reverser-limit
  regressions pass. The linked record preserves the exact tested content.

## Questions to resolve with the author

The [clearing-loop continuation](clearing-loop-investigation-2026-09-19.md#second-seat-trial-2026-09-20)
also records **unadopted** trials T05 (bounded second-cavity opening at its
actual mounted rivet) and T06 (.05 mm loop/cover seat allowance). Their deployed
endpoint passes both kernels, but clipping travel and grip are not yet proven.
The measured .850639 mm difference between clip and rivet centre spacings may
involve intended elastic clipping or assembly fitting; it is not listed as a
proven defect or recommended physical modification.

1. Which source revision and exact printed shaft/knob/spacer variants were
   used in a build demonstrating counter reversal in both directions?
2. What are the installed shaft shoulder/fastening heights, spacer lengths,
   lever endpoints and usable detent positions? Is either position intentionally
   retained on a detent flank rather than at its centre?
3. Which fitting operations were actually needed (especially tooth flanks,
   fork slots, spring seats, threaded covers and glued/pressed insertion depths)?
4. Is the “5 mm” reversing ball actually 5 mm diameter? The supplied STEP ball
   measures 5.4 mm. We have not silently chosen a replacement.
5. Which of the remaining rigid overlaps represent intended elastic/preloaded
   contact, assembly pose inaccuracies, or geometry-version differences?

The downloaded assembly video/manual are useful assembly evidence, but they
do not supply all these dimensions or certify the simulation's modifications.
The [insertion-only trial](reverser-insertion-trial-2026-09-20.md) rejected
simply pushing the unchanged shaft farther through its original shoulder.
The earlier 9 mm/.37 mm isolated-pinion trial is **not an adopted full-bank
fix**. These rejected hypotheses are retained to prevent circular debugging.

## Explicit simulation-only clearing-loop replacement

On September 23 the pilot authorized a new mounting instead of inferring the
source elastic clip motion. The [replacement record](clearing-loop-replacement-2026-09-23.md)
maps the same three source occurrences to a captive loop, headed stop pivot
and flush plug. The first clip neighbourhood gains a closed bearing and
bounded stop recess; the finger loop and source assets stay unchanged. The
lower stems are offset to the existing cover-hole datums, and a .01 mm
mounting seat clears the published shoulder/cover interface. The independent
control is explicitly labeled simulation-only.

This is a newly designed simulation exception, not another recovered source
fit or a recommended printable modification. Native, faceted and full-world
Mesh64 checks, retention, physical stop negatives and retained operation are
recorded separately. The default root now adopts this mounting; the paired
hosted and standalone handles have independent-motion evidence in that record.
The original clip question above stays open, as do unrelated whole-machine
geometry findings.
