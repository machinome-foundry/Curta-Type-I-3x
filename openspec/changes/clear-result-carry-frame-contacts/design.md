## Context

Status: ratified by the pilot, 2026-09-13 ("ratify, go on"). No repair was
implemented at ratification. This is a project-owned prerequisite in the existing Curta
`open-run-simulation` worktree, not a framework/viewer change or a shop sprint.

Seat-edge revision also approved on 2026-09-13: "yes, and then try, you don't
need so many confirmations from me". The pilot authorizes the bounded
exception below and continued fitting/verification without repeated approval
of routine implementation steps. No broader moving-part or support redesign
is authorized.

The source assembly and the operating layer share the STEP's millimetre world
frame and vertical Z axis. The frame remains fixed. Define lever drop `d` as
millimetres downward from the raised endpoint: `0 <= d <= 4.2`; the existing
engagement fraction is `d / 4.2`. The `099`, input-one, seated-carriage fixture
has `d = 1.1630815` at both selected stations, not zero drop.

### Physical scope

| Station | Carry assembly under `Curta.carry_mechanism.result_carries` | Coupled sleeve |
| --- | --- | --- |
| Ones → tens | `results_tens_lever_assembly_1` | `Curta.transmission.result.tens.p_10220_410003_1_419227` |
| Tens → hundreds | `results_tens_lever_assembly_2` | `Curta.transmission.result.hundreds.p_10220_410003_1_419086` |

Each assembly contains `tens_slider_for_results`, `tens_slide_bearing` and
`carry_lever_spring.wire`. The only proposed production geometry change is to
`Curta.frame.upper_frame.main_body`. The rest of the assembled machine stays
present as neighbouring geometry, even where its motion is held fixed.

### Evidence and source reconciliation

The [native evidence report](../../../simulation/docs/open-run-evidence-2026-09-12.md)
records all 428 physical bodies and four nine-pose transition probes. Both
stations show the same three contact families:

| Contact family | First-station native observation | Interpretation |
| --- | --- | --- |
| Spring / frame | About 0.4734 mm³ at `099`, about 0.4738 mm³ at trip | Present before a carry; not an event-timing artefact |
| Lowered slider edge / frame | 0.099225 mm³ at `d = 4.2`; 0.075 mm-wide overlap | A frame passage conflict at the lower endpoint |
| Raised slider shoulder / frame | 4.626578 mm³ at `d = 0` | A separate passage conflict at the upper endpoint |

Manual pages 30–31 were read and visually inspected. They specify approximately
57 mm blanks of 0.6 mm wire, show the closed U mounted on the bearing's lower
support with free hooks at the slider detents, place the fork between the
transmission-sleeve flanges, and require free snap/reset motion. Those figures
support the installation topology; they do not specify a clearance-pocket
dimension or prove the fitted wire's exact elastic shape.

The [source comparison](../../../simulation/docs/evidence/open-run-transitions/frame-source-comparison.json)
checks the first station at four drops with both the original source parts and
the fitted operating parts. All 16 native and 16 source-STL-interface results
are valid. The original static STEP wire intersects the native frame by
0.510484 mm³; restoring it is not a solution. Original and fitted sliders have
the same native endpoint frame contacts. The supplied `main body.stl`, loaded
in its existing coordinates without alignment or repair, also reproduces the
contacts (about 4.640764 / 0.099226 mm³ for the raised/lowered slider).
It is not a drop-in clearance fix. This is a local comparison, not proof of
complete STEP/STL equivalence or a verdict on a physically assembled Curta.

The existing twelve isolated carry tests omit the frame; installed carry-bank
tests cover pins. Their green results do not contradict these new findings.
The original `simulate-the-curta` change already leaves frame/guide interfaces
open. Its 7/17 task state, prescribed arithmetic behaviour and unresolved
whole-machine findings remain untouched.

## Goals / Non-Goals

Goals:

- Clear the three named contact families at the two selected stations, from
  the raised endpoint through the complete 4.2 mm travel to the lower endpoint.
- Preserve the currently measured spring seats, detent contact, guide
  placement, fork/sleeve capture, pin approach and reset geometry.
- Bound every frame change by independent source-derived geometry and retain
  actual before/after failure, clearance and visual evidence.
- Make the correction reusable by the later running slice without introducing
  new controls, arithmetic state or a runtime dependency.

Non-goals:

- Repairing other carry stations, changing the mechanism's timing, extending
  motion admission, or solving spring force, strain, friction or impact.
- Redrawing upstream parts, adopting optional modifications, changing source
  files, or certifying a manufacturing process or structural strength.
- Completing the existing simulation, accepting a full initial snapshot or
  closing the open-run home-window, outgoing-boundary or runtime requirements.

## Decisions

### 1. Prefer a stationary, local frame fit

Introduce a `MainBody`-derived fitted adapter in a project-owned frame-fit
module and use it only as `mechanism.UpperFrame.main_body`. Its build-time
adjustment removes material in three separately named passage families at
each of the two selected stations. The cut geometry is fixed: it must not
depend on the currently displayed lever pose or cut a new hole during motion.
The raw `standard.parts.MainBody` and source assembly stay unchanged.

Do not alter `carry_spring.py`, `carry_seat.py`, `detents.py`, `carry_heads.py`,
`carry_fits.py`, installed carry placements, sleeves or measured motion
profiles as part of this design. The source comparison does not prove the
spring model perfect; it does show that reverting the wire or swapping the
frame representation does not solve these contacts. Preserving the working
interfaces gives this first correction a narrow, testable boundary.

Alternatives considered:

- **Translate the station or frame:** changes several measured mounts and
  contact relationships to address one passage; no source datum supports it.
- **Replace or bend the spring differently:** could be a later supported
  solution, but it affects the seated fold and hook/detent proof and does not
  address the two slider contacts. Not authorized by this proposal.
- **Trim the slider:** could damage a guide or transmitted-contact surface
  already protected by the existing fit tests; not the selected first remedy.
- **Use the print STL or original wire:** the measured substitutes still
  intersect. Source-STL inspection remains evidence, not a representation swap.
- **Treat it as a fixed overlap or omit the frame:** conflicts with the
  manual's moving interface and the ratified no-hidden-obstacle requirement.

### 2. Measure and constrain the relief before cutting

Use a named running gap of **0.05 mm** per contacting surface,
consistent with existing project fit conventions. It is a simulation fit
allowance, not an upstream drawing tolerance, a force prediction or a permitted
Boolean overlap. Declare it once as a dimensional parameter and derive the
cutters from measured source features; do not duplicate it as unexplained
offsets in tests.

The first-station contact regions supply the starting measurements, not
finished cutter boxes:

- Lowered edge: world X 52.725–52.8, Y -7.89–-6.42, Z -16.8–-15.9 mm.
- Raised shoulder: X about 48.573–52.8, Y -9.535–-6.42,
  Z -22.2–-21.6 mm.
- Spring: two lower-leg/fold-side regions around X 53.8 and 60.8,
  Y -11.10, Z -16.98 mm. Use each region separately, not a box that removes
  the entire bridge between the two legs.

Before implementing the adjustment, measure the full moving envelopes and
nearby support features in their native source frames, including the second
station's own transforms. Record named permitted-removal regions and their
dimensions independently of the implementation cutter. Map and protect guide
seating/registering lands, the M4 fastening features, structural support and
nut seats, main-shaft/bearing surfaces, and all non-selected station passages.
Apply the explicitly approved seat-edge exception below when defining the
remaining protected registration lands.
Do not use a whole-station box, full annular groove or total mass budget as a
substitute for these spatial bounds.

Acceptance requires one valid connected frame solid, no added material, no
removed material outside the permitted regions, and unchanged protected
features outside that exception and unchanged assembly placements. A cutter derived from an already fitted
frame would be circular evidence. Gap checks need independent upper and lower
bounds in the documented local normal directions, not merely a nonzero
distance or an endpoint volume total.

If the required envelope/gap reaches a protected seat outside the approved
edge exception, breaks continuity,
requires relocating a support, exceeds a local passage fit, or requires a
moving-part change, stop and return the measured conflict to the pilot.
Ratifying this plan authorizes measuring/dimensioning a fit within those
bounds, not choosing a different repair when they fail.

#### Approved seat-edge exception

The [native gate report](../../../simulation/docs/carry-frame-gate-2026-09-13.md)
measures a 20.43 mm² guide/frame registration land at each station. At the
raised and lowered endpoints the slider meets its boundary; even a 0.025 mm
clearance witness occupies a 0.03675 mm² strip of that land at each end.
Preserving every point of the land and providing a real local gap are
therefore incompatible at these edges. The pilot has approved local
frame-side edge relief, not a relocation or change of the guide.

Independently bound permitted seat changes around the measured contact
segments: first-station X = 52.8, Y = -7.89 to -6.42, at Z = -21.6 and -16.8
mm. Account for adjacent corner faces where the running gap wraps around
the segment endpoints. Dimension the bounds from these source features and
the declared gap; do not exempt a whole face or station. Require unchanged
geometry and native support contact on the remaining land, and report the
actual removed/retained seating area. A trial fit that overreaches this
exception fails its preservation tests and is corrected before acceptance.

The 0.05 mm target is measured in the named local relief directions; it is
not a claim that every pre-existing noncontact passage elsewhere in the
station already has at least 0.05 mm play. Positive-volume intersection is
still forbidden everywhere on the supported path. Record any smaller
unchanged clearances honestly.

Dimensioning and reversible fit trials proceed under this approval. Keep
the unsampled-path proof as an acceptance gate: trial geometry is not a
verified correction until that bound and all preservation checks pass.

### 3. Prove motion clearance, not just endpoint clearance

Promote the retained diagnostic counterexamples into named regression tests
before changing the frame. First reproduce native red at each station for
the preloaded spring and both slider endpoints. Confirm driver-owned updates
and installed-frame identity; the old direct-port cached-pose prototype is
not a usable motion probe.

After fitting, independently check the full lever stroke, all detent-law
knots and the `099` preload, plus both trip/reset transitions with crank and
driving dial frozen at their recorded events. Start dense checks at 41 or
more lever poses and add contact-sensitive samples. For the frame interface,
also establish a conservative swept/interval envelope and its numerical
bound; a denser sample grid alone does not prove an unsampled path clear.
If that bound cannot be established, report the limitation and leave the
clearance gate open rather than weakening the ratified fidelity.

Reuse the complete 428-body diagnostic inventory for moving-neighbour checks;
keep the six source-mesh interfaces explicitly faceted. Native bounding-box
rejection may accelerate disjoint tests, but mesh boxes cannot certify native
clearance. Any positive shared native volume fails, however small; invalid
geometry or a missing body fails as well. Preserve independent contact/capture
tests so a roomy but disconnected mechanism cannot pass.

Negatives must independently remove each relief family, omit or misplace the
second-station relief, and enlarge a relief across a protected surface. The
intended contact or source-preservation test must fail, then pass again after
restoration. Vary the declared gap and verify its measured effect to catch an
inert parameter. No intentionally broken production state is committed.

### 4. Keep the prerequisite and later running work separate

The old prescribed model supplies frozen background poses only. Neither it nor
these tests demonstrates history-dependent running. Keep the input, subtraction
mode and carriage fixed as recorded; do not grant new arbitrary pose admission.

The correction changes a shared frame body but only two spatial regions of
station fit. Check the frame's complete protected-source difference and its
unchanged contacts at other stations; do not generalize the relief to all ten
result stations or five turns stations. If the implementation instead requires
a shared moving-part change, bring that scope back before doing it.

No ADR is needed for this local fit. The new capability can eventually be
promoted independently, while the original broader assembly/operation deltas
remain with `simulate-the-curta`. The later running proposal must cite this
change's accepted result, not infer that the whole Curta is validated.

## Risks / Trade-offs

- A local frame pocket may disturb an unmeasured support → map and protect
  source seating and fastening features before fitting; preserve the remaining
  land under the approved edge exception and stop on a materially broader conflict.
- Preserving current spring geometry may leave an unsuitable shape → retain
  wire, seating and hook tests plus the full sweep; change the design only
  with explicit evidence and pilot approval.
- A nine-pose negative record could be mistaken for a path certificate → use
  it only to reproduce failure; require bounded swept evidence for clearance.
- CAD caches may hide a changed adjustment → compare fresh and built native
  geometry and validate from the worktree with explicit framework imports.
- Full regressions have known unrelated failures → retain named existing
  findings and fail on any new/changed one; no whole-machine green claim.
- Heavy CAD jobs previously exhausted memory → run sequentially with the
  recorded 8 GiB address-space guard, one numerical thread and bounded jobs.

## Migration Plan

After pilot ratification, validate and commit planning-only artifacts and their
project evidence before implementation. Preserve unrelated dirty state; do not
stage the shop, framework, viewer, source caches or generated pictures.

Write/run the new native failures, dimension the permitted fit and protected
surfaces, implement only the frame adapter, then validate its complete installed
effects. Build the root and inspect both close-up before/after views and an
assembled view with all relevant supports present. No live shop/server launch
is needed for this correction.

Run affected local and bank regressions on both kernels, and the complete
project regression under the known-failure accounting. Only after the focused
requirements pass, sync this capability and archive this change in its own
completed implementation record. Do not check off or archive the original
`simulate-the-curta` tasks. Integration, push and publication remain separate
pilot decisions. Rollback consists of reverting this focused frame adapter
and its wiring as a normal reviewed change, not resetting the worktree.

## Open Questions

- Do the complete spring and slider envelopes admit the proposed 0.05 mm
  local gaps within the approved seat-edge exception and without touching any
  other protected support? Dimensioning is the
  first gated implementation step, not an already measured clearance claim.
- Which conservative native/interval envelope gives a defensible unsampled
  clearance bound for the existing fitted spring? Failure to establish one
  leaves the evidence gate open; it does not authorize a fidelity downgrade.

The pilot ratified the frame-only repair direction, its two-station scope,
0.05 mm gap target and these stop conditions on 2026-09-13. Neither a different
spring mounting nor a guide/slider redesign is bundled into that decision.
The later seat-edge approval changes only the frame-side preservation boundary
described above; the other stop conditions and acceptance obligations remain.
