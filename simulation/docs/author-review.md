# Author review: simulation fits and unresolved findings

Review checkpoint: 2026-09-20. This is a review agenda, **not a list of proven
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

## Assembly, source-representation and motion corrections — not new prints

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

## Current candidate and unresolved work

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
