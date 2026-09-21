## Context

Start from `simulation/assessment.md` and upstream geometry commit
`7023381a6d1c8797d84ae146abf47f4403b7f780`. The standard AP242 STEP contains
276 product definitions and 547 leaf occurrences. Its hierarchy supplies the
placements; the manual supplies the assembly and calibration evidence. There
is no previous executable simulation. The assessment remains historical evidence.

The pilot authorized implementing the simulation on 2026-09-11. This plan
records working implementation choices under that request, not a separate claim
that the pilot ratified every motion detail. On continuation the pilot explicitly
authorized modeling the documented spring and delegated routine engineering
decisions: make evidence-backed choices and record them without repeated approval
requests. Manufacturing certification remains out of scope.

The pilot subsequently paused implementation for a framework memory fix.
The project checkpoint and proposed framework-cycle handoff are recorded in
`simulation/docs/pause-report-2026-09-11.md`. This change remains active;
neither the original scope nor its delivery requirements are reduced.
Work resumed after the pilot integrated machinome's `expression-graphs`
cycle (`446bc22` / `5e59147`, ADR-101). Fresh project export and browser
verification now pass; the mechanical delivery scope remains unchanged.

## Coordinates

Preserve the STEP's millimetres, vertical Z axis and common main-shaft axis.
Read placements from the document; do not center individual parts on their
bounding boxes. A moving group owns a joint in its own rest frame. Site joints
are appropriate for imported parts whose axis is known in the assembly frame.
The completed model can translate the entire machine to a presentation origin.

## Goals / Non-Goals

Goals: the complete standard assembly; simple named joints and drive relations;
all eight selectors, eleven result dials and six turns dials; addition,
subtraction, carries, decimal shifting and clearing; repeatable demonstrations;
source, geometry and arithmetic contracts.

Non-goals: redesigning print geometry, optional modifications, contact dynamics,
friction, spring-force prediction, or fabrication certification.

## Decisions

1. **Import STEP components and preserve provenance.** Scaffold through
   `machinome import-step`, retaining its hierarchy and transforms as an auditable
   source map. Simplify the moving mechanism into meaningful subassemblies only
   after source-drift checks exist. The STL assessment shows substantial topology
   defects, so replacing the STEP indiscriminately with STLs would lose evidence.
2. **Resolve ambiguous hardware explicitly.** `M4x10` and `6mm ball` each name
   two products. Compare their geometry and occurrences before choosing an import
   representation. No arbitrary first-name match is acceptable.
3. **Validate before animating.** Identify the invalid native solid by durable
   product identity. A correction must be explicit and measured; do not quietly
   repair the upstream document. Inventory pre-existing overlap pairs and their
   measured volumes where the author's unfinished fits overlap. Do not excuse a
   new motion collision with a volume threshold.
4. **Relations state mechanical dependencies.** Use `Revolute` and `Prismatic`
   at the moving bodies, broadcast repeated digit motions, and keep nonlinear
   intermittent laws in a small kinematics module. Keep structural placement in
   `render()` and runtime inputs in relations or `simulate()`.
5. **The running mechanism retains state.** As approved on 2026-09-15, use
   Time.running and run-banked joint state for retained registers and partial
   motion. Reproduce a state by restoring a run snapshot and replaying the
   same physical requests, not by making the user supply starting registers
   or by retaining a second arithmetic state in the page. Readouts derive
   from the mechanism. Deterministic fixture setup is not an operating control.
6. **Evidence supplies motion dimensions.** Derive selector travel, subtraction
   lift, carry travel, gear phase and carriage pitch from the source and manual;
   keep the probe and readings. A demonstration's timing is stated as a chosen
   manual operating speed and is not a measured speed rating.
7. **The navigation tree teaches the mechanism.** The pilot explicitly requested
   meaningful show/hide layers: enclosure, frame, input selectors, main drive,
   transmission, carry mechanism, and carriage/registers. Group by mechanical
   role, not STEP export order. Keep fasteners with their supported assembly,
   individual digit channels reachable, and moving carriage covers within the
   carriage's own frame. The raw source hierarchy remains a separate reference.
8. **The controls are the physical inputs.** The approved replacement gives each
   of the eight selectors its own direct control. Crank lift and turn, carriage
   lift and turn, reversing lever, clearing ring, clearing loop and every decimal
   marker are separately handled on their own parts. There is no operand slider,
   arithmetic-operation mode or editable register in normal operation. A crank
   click requests one clockwise revolution; a drag can request partial travel.
9. **The user chooses the order; constraints enforce the mechanics.** Lifting,
   shifting, seating and clearing are independent movements. The page does not
   perform one to prepare another. Declare actual travel limits and mechanical
   interlocks in the run so Python requests and browser gestures meet the same
   stops. A blocked request does not repair the pose or postpone itself until
   another control moves. Preserve the measured 6 mm carriage lift, six working
   detents and 9 mm subtraction stroke. Lower markers stay with the housing.
10. **Examples and operation remain separate.** Worked examples restore a stated
    test snapshot and replay physical actions for teaching and regression, never
    as the ordinary control path. A new empty machine is session setup, not a
    mechanical reset button. Clearing is performed with the ring, with partial
    and selective clearing retained. No page-local register commit remains.
11. **Material-inspired colors teach the layers.** The pilot requested aluminum,
    bronze and black contrast while physical verification continues. The display
    palette uses silver structure/drum, bronze transmission/carry gearing, brass
    guides/clearing teeth, steel shafts/springs/hardware, black housing/controls
    and ivory number rolls. These are illustrative display choices, not a claim
    about the printed project's construction materials or a metal Curta's bill
    of materials. Colors are declared on material leaves and fused prints, so
    recursive navigation and exports retain them without altering geometry.

## Findings

### Counter lockout indexed fit — 2026-09-21

The counter's six source-backed upper prints match the independently posed
retained root, but each has a tiny native common at its third indexed flat
with the existing .15 mm simulation fit. The parked-crank test fails 19
kernel/pose checks; meshes miss several native contacts. The isolated T08
.16 mm outer-skin candidate clears all 60 indexed poses while preserving
the keyed cores, axial extents, connected material and 300 two-sided locking
poses. It is not adopted: counter contact profiles, ordinary motion and
actual-root/browser wrong-order acceptance remain open. See the
[counter investigation](../../../simulation/docs/counter-lockout-investigation-2026-09-21.md).
This does not establish a fault in the author's printed machine or recommend
a manufacturing tolerance; upstream CAD remains untouched.

### Operating ones-lockout adoption — 2026-09-20/21

Framework `e63700e` and viewer `e82b521` resolve the periodic first-contact
software prerequisite. The fixed-height ones profile now constrains the actual
crank across the preserved assembly tree, intersecting its original pawl bound.
The project-owned [adoption record](../../../simulation/docs/operating-ones-lockout-2026-09-20.md)
separates passed full-root requests, contact kernels and pointer evidence from
the still-running broader regressions. It introduces no further print fit and
does not generalize the ones profile to axially sliding higher channels.

### Direct-operation prerequisite — 2026-09-15

The approved interaction inventory is in
`simulation/docs/direct-operation-2026-09-15.md`. The public framework presently
has no sliding control and refuses a control on a body with two joints. The
viewer also assumes a rotational placement for every control. Proposed changes
`direct-part-motion` (framework) and `slide-and-turn-parts` (viewer) address
those specific limits. Their implementation awaits separate ratification;
this project record does not declare the proposed APIs available. The prior
calculator page is still the implemented behavior, not the approved target.

The complete 547-occurrence source assembly builds and its placement contract
passes. Duplicate product names are resolved by suffixing only those names with
their existing STEP entity numbers in an ignored import copy; a restoration test
proves that every other source byte is preserved. This is necessary because the
same hardware names designate different geometry, and repeated subassembly names
otherwise conflate their definitions in the scaffold. Generated empty render
methods are removed mechanically. See `simulation/docs/measurements.md`.

The invalid solid is the zero-positioning spring (#419219). Automatic repair
remains invalid and produces two native solids. An analytic replacement based
on manual page 14 and measured mounting points was authorized by the pilot.
The initial digits-cover / upper-housing boolean also yielded invalid geometry.
The fitted covers now produce a valid positive thread intersection, but no
certified nominal overlap inventory exists yet. The spring replacement now
passes native validity, wire-size and exact/faceted mounting contracts. Crank,
drum and eight selector motions are implemented with joints and relations, and
the arithmetic unit tests pass. Seven educational layers preserve every original
source placement. The complete result/counter drum passes both kernels after
recorded outside-profile and sleeve fits. All seventeen installed bevel pairs
now pass exact/faceted engagement checks, including sampled carriage positions.
Their axial fit alone had biased play; an additional -3° dial clocking centers
both flank limits without weakening the ±12° engagement contract. The new stem
trim keeps that axial fit above the frame bearing plane.

Fifteen carry sliders, the tens bell, carriage and clearing plate now move.
The first carry channels pass full-bell sweeps and bidirectional engagement in
both kernels after tooth-profile fitting and measured phase corrections, without
relaxed assertions. Later checkpoints below extend that proof to all carries
and clearing teeth. Complete source overlap inventory, adjacent moving
interfaces and full demonstration interference remain open. Checkpoints and
detailed measurements are in simulation/docs/measurements.md.

The zero-positioning cam now rotates at its retained height while its transverse
pin slides through the axial slots for subtraction. A measured cam profile drives
the grouped roller/lever and the documented spring's moving terminal. Six contact,
travel and spring contracts pass both kernels. The pawl's repeating ratchet ramp
includes the source's shorter closing tooth interval; its contact sweep passes,
and its spring and mounting fits now pass exact. The collar trim and missing
spring-anchor bore are explicit builder-style fits confined to simulation. The
pawl's reverse-blocking contract recognizes tooth-pitch backlash and separately
checks that release clears the tooth; it does not claim an ideal one-way clutch.

The carry U-wires now spread against measured slider detents while their closed
folds stay on their supports. The fixed bearing grooves gain .05 mm radial wire
allowance without modifying the guide or slider. Twelve motion, seating and wire
contracts pass both kernels. The missing clearing components are the manual's
two tooth strips and spacer, supplied as flat standard STLs. They are formed
into the measured cover groove and retained as three separately selectable
leaves. The operating inventory is consequently 550 represented source occurrences,
including every original STEP occurrence; the immutable source-placement
inventory remains 547. Reconstructing the bell spring with five proven-connected
patches gives 554 material leaves without changing that occurrence count.
The later seventeen-finger spider reconstruction brings this to 588 material
leaves, still representing the same 550 source occurrences, not 550 independent
physical pieces: some source ingredients belong to fused prints.
The groove, retaining-screw relief and progressive clearing-to-dial contact
and timing are now verified.

### Carry contacts and timing

The carry forks, reset shoes and pin-contact tips require local fitting, bounded
by native permitted-removal contracts. The half pins also need their cutaway
side selected deliberately: the manual's approximately 36-degree flat angle
alone leaves two orientations. Both complete dial banks now pass native and
faceted carry/parked-pin checks at all six carriage positions. The measured cam
resets some levers in the next crank revolution, so carry motion retains the
previous cycle's latch until that station's cam arrives. See the reproducible
profiles and validation in `simulation/docs/measurements.md`.

### Register detents

The source spider is unloaded: each of its seventeen fingers intersects its
6 mm ball by about 11.937 mm³, and each ball intersects its dial by about
.001647 mm³ natively. The operating layer now drives the balls from the actual
dial joints through one measured periodic rise profile, then drives each
finger from its ball. The source ring and rounded tips are retained; a
variable side-profile sweep preserves each arm's tapered thickness. Native
contracts prove the full reconstruction remains one connected spring, adds no
source material when unloaded and removes only a bounded upper-cone skin.

The ring retains its source collar interference, to be named in the fixed-seat
inventory rather than advertised as clearance. A ±4 mm height survey rejects
moving the whole source spring as a cure: lowering enters the carrier and
raising increases collar/cover overlap. A named .05 mm carrier seating gap is
separate from each finger's .05 mm ball gap. Bending is prescribed, not a
spring-force or strain calculation. The first station passes native and
faceted full-pitch clearance and free/blocked seating checks. The complete
bank now also passes both kernels through all digit/shift combinations,
carry and subtraction cascades, and progressive clearing; every ball is
independently checked as captured by its own dial and spring tip.

That complete-bank exact result used the sampled profile. The later compact
native-circle law preserves the measured envelope and passes first-station
native and complete-bank faceted checks; its complete-bank exact regression
remained pending at pause. On resumption all four complete-bank native checks
also pass on the compact law (457.17 s), closing that verification gap.

The clearing stop is now a source pin driven vertically by the cover's measured
cam. Its documented eight-turn .6 mm wire spring compresses between the native
sleeve seat and pin shoulder, with .05 mm seating gaps. Native distance
measurement replaces an invalid near-contact Boolean measurement; independent
full-sweep contact and spring tests pass both kernels. No pin or sleeve geometry
is changed. The whole-machine audit still needs cover/window and frame-guide
interfaces resolved before the source overlap inventory can be accepted.

The operating carriage's bottom stop pin has a measured insertion-depth fit:
.51 mm deeper than the source assembly, leaving 3.845589482 mm exposed against
the manual's approximately 4 mm instruction. Both source frame representations
clear it across the working travel and still block at the outer barriers.
The STEP pin gives inconsistent native boolean and containment results even
outside the simulation, so this one operating part uses the author's unchanged,
watertight printable STL. Its contacts are explicitly faceted on either runner;
the native ambiguity is retained as a reproducible finding, not waived with an
intersection epsilon. See the 2026-09-19 operating completion record. No source
file is edited, and this does not establish the seated-carriage shift lock.

The cover-datum trial is retained, with three measured neighbour fits added on
resumption: a .10 mm inner top-land facing beneath the clearing ring, seventeen
R2.995 shallow housing pockets around the fixed axle ends, and .15 mm retaining-
flat extensions on those axles. Neither source axle placement/length nor the
working clearing ring's placement is changed. Seven faceted contracts now pass,
including a bounded axial ring seat, all axle neighbours and protected source
surfaces; removing each fit separately fails its intended physical contract.
All seven also pass on the exact runner, with STL interfaces remaining faceted.
The source prints themselves remain untouched. Their mutual thread overlap and
other frame-guide findings still prevent whole-machine acceptance. Measurements
record the rejected axle translations and the explicit mesh-fidelity limits.

### Reverser trial continuation — 2026-09-20

The pilot authorized testing the shaft mounting-seat correction and asked for
all fits to be documented for author review. The detent-bearing body rises
1.9 mm while the shortened fastening end retains its installed height. Its
two original pockets remain unchanged. The continued trial also fits only
the sixth fork seat/slot, represents the manual's M4 die-cut end, and applies
differentiated counter tooth relief: .36 mm on the ones stack, .42 mm on the
five higher inputs. A source-sized radial ball and analytic spring now follow
the original cones/rim; the upper flank biases the spring-loaded ball toward
the measured upper stop. These are prescribed geometry and restoring-direction
checks, not force/friction certification. The operating candidate now binds
the actual knob to all six gear heights, maintaining .0925 mm mid-play offset.
Counter tooth passage derives from positive overlap with the seven adjacent
source drum bands, including one-tooth engagement on higher channels at partial
lever positions. It does not snap to a binary mode. Lower working detent
−4.9425 mm is distinct from the lower housing stop −6.9425 mm; the upper spacer
stop is +3.9075 mm. Scoped native/faceted bank, follower, transition and first
retained-history checks pass, as do all 24 shifted-operation cases and scoped
hosted gestures. Complete pointer and mid-cycle-restraint acceptance remain explicit.
See `simulation/docs/reverser-fork-and-follower-2026-09-20.md` and the
consolidated `simulation/docs/author-review.md`. Trials, rejected alternatives,
remaining checks and source invariants stay explicit; no upstream CAD changes.

## Findings for the framework

- The isolated higher-result restraint passes both geometry representations
  and browser/Python action-order checks, but its full-tree trial triggers
  `LandingInvariantError` on an ordinary carry preparation. A CAD-free
  reduction using the actual shaft/dial/lever laws completes without the
  constraint and fails with it. At the observed mixed-source cut the driven
  coordinate's displacement and the threshold crossing have opposite relative
  directions. See `simulation/docs/higher-result-lockout-2026-09-21.md` and
  `simulation/test_carry_constraint_repro.py`. No new framework correction is
  ratified or implemented by this project record, and adoption remains open.

- Exact printed groups can contain enclosed voids represented by disconnected
  negative-volume mesh shells. The project checks material connectivity, not
  surface-shell count, and separately requires one valid native solid. Every
  rigid body remains covered; no part is skipped.
- A placement joint on a Molejo leaf is counted in its required shape-parameter
  ports. A thin mounting assembly separates placement from wire deformation.
- Reusing a wrapped assembly render directly in a fusion crosses the assembly's
  simulation-phase boundary. Generated ordinary placement methods avoid that.
- STEP products with repeated human-readable names need identity-based import
  selection. The project uses a byte-audited ignored name-disambiguation copy.
- Two imported-part adjustments returned older built geometry than a fresh
  adjustment after changing helper constants. Explicit dimensional parameter
  identities and built/fresh equality contracts resolve the project cases;
  the cause is not established. Independent ignored verification artifacts use
  `SOLID_BUILD_DIR=_build_checks` with the same workspace environment, separate
  from the live preview's publication lock.
- OpenSCAD output in a nested inspection directory rebases rigid STL imports
  but leaves flexible snapshot STL paths relative to the flexible module's
  directory. The image silently omitted the two spring arms although their
  meshes existed. Moving inspection classes from `simulation/tools/views.py`
  to `simulation/views.py` restored both arms in the snapshot. This is an
  artifact-path finding, not permission to treat an incomplete image as proof.
- Nested measured profiles exceed an 8 GB export ceiling before schema-4
  expression sharing can run. After algebraic simplification, a result carry
  expression still expands to approximately 270 MB when fed through its hook
  profile, then repeats in six wire coordinates across ten stations. The
  reproducible `simulation/tools/expression_size.py` measures this without
  allocating the complete expanded model. At pause fresh export was blocked;
  the stale palette was rejected by browser preflight. A separate framework
  cycle was required to address construction-time sharing, not just final JSON
  size. See the measured resource limits and traceback evidence in the project
  measurements. Subsequent read-only framework inspection during the pilot's
  diagnosis confirmed ADR-080 and the late binding pass. No framework
  implementation was changed by this project. The handoff's suggested
  `construction-time-expression-sharing` became the framework-owned
  `expression-graphs` cycle, now integrated at `5e59147` under ADR-101.
  The fresh project export succeeds with 9969 bindings and all controls;
  calibration, six worked examples and layer controls pass in the current page.

These are evidence for an upstream finding record, not framework changes or
claims that a new API has been accepted. No framework implementation was edited.

## Risks / Trade-offs

- Nominal source fits may not operate without the manual's sanding and tuning:
  distinguish the nominal source inventory from verified moving interfaces.
- Arithmetic can be right while gears do not engage: require geometry contracts
  alongside the author's numerical calibration cases.
- STEP subassemblies sometimes describe separately modeled pieces printed as a
  group: preserve all constituents and verify connected rigid groups deliberately.
- A static spring cannot prove moving spring clearance: use a measured flexible
  representation where motion changes its shape, or record the interface as open.

## Migration Plan

Add only the simulation package, project manifest, build exclusions and records.
Commit this plan, implement from the frame upward, then sync specifications and
archive only after the required evidence passes. Upstream CAD remains unchanged.

## Open Questions

What causes the invalid cover/housing intersection, and
what is the faithful representation of its finished fit? What are the measured
engagement phases and operating clearances? Resolve these in the import and
single-channel increments before replicating the mechanism.
