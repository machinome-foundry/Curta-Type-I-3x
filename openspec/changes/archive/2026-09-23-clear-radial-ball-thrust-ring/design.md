## Context

The source ring is a 1.5 mm annulus, radii 12.3..16.35 mm, installed at
Z33.05 above the collar ledge. Its upper plane at 34.55 supports the existing
spring with the previously verified .05 mm gap. The unchanged ball is a
native R3.75 sphere at Z30 despite its source name saying 6 mm. Measured
radial centre limits span 8.332135..11.949091 mm. Source ring placement has
a 35.717779468-degree phase; radial travel is in the parent X direction.

The quarter-turn radial Follow trial penetrates the ring's lower inner lip.
Existing desired regression is red natively and world64. The independently
inspected section suggests a passage can remain below half the ring thickness
and inside its outer collar-support annulus; those bounds require proof.

## Goals / Non-Goals

Goals: remove this obstruction with independently bounded local material
removal; preserve both seats and source motion; prove the entire ball/ring
relative travel, not just the witness; retain source, negative and root checks.

Non-goals: ball size changes, new forces/preload, different collar/ring/spring
heights, changes to Follow or operating controls, production ball-motion
adoption, whole-machine clearance, or manufacturing/strength certification.

## Decisions

### Protect support material before cutting

Map the ring/collar supporting common at the existing downward .1 mm capture
probe, at all indexed carriage angles and intermediate angles. Measure the
ring's upper plane and the actual spring/ring retaining common. All such
material must survive exactly. Independently cap permitted local removal
in ring coordinates by the source thickness's lower .8 mm and installed-frame
X12..14.3, Y±2.4 mm. These deliberately rounded geometric limits come from
the measured contact and sphere reach, not the production cutter. If source
or mapped support lies inside a proposed removal, stop and revise the design
instead of weakening the preservation check.

### Sweep a spherical running gauge through radial travel

Use the unchanged R3.75 sphere plus a named .05 mm radial gap. A capsule
along X8.332135..11.949091 at Z30, transformed into the original ring frame,
is a candidate passage. Test .04/.05/.06 mm gaps inside the .08 maximum
independent allowance. No whole annular thinning or top-face change is allowed.
Changing the ring height would disturb two verified seats; shrinking the ball
would change its bell/frame/collar interfaces. Neither is a fitting option.

### Bound unsampled motion analytically and check both representations

The ring rises 0..6 mm while the ball stays at Z30. In ring coordinates the
ball centre therefore moves downward from Z=-3.05. Every ball cross-section
inside the ring is enclosed by the same-centre-height radial capsule: lowering
the sphere can only decrease its positive-Z section. Verify the source sphere,
actual parent-frame motion and retained radial bounds as premises. Native
source and complete published world64 ball/ring meshes must clear dense
radial/lift samples; tessellation must not create an inward shortcut across
the concave passage. Refine the local ring mesh if needed, retaining geometry.

### Stage adoption separately from ball motion

First use an isolated fitted positioning and radial-root trial. Require one
valid connected ring, no addition, exact protected material, fresh/built parity,
measurable gaps, restored/misplaced/excessive-cut negatives, existing seat
contracts, full other-mesh/bank identity and no new neighbour pair. Then replace
only the ring in the seated production positioning assembly. The original
source-pose negative and explicit unchanged-ring reference remain available.
The Follow trial is evidence, not an adopted production control.

## Risks / Trade-offs

- A concave passage's mesh may bridge into its gap → native and world64
  clearance, mesh validity and source-to-published comparison remain gates.
- Ring phase or carriage shift may rotate the relief incorrectly → inspect
  actual root placement and test the full declared shift/lift domains.
- Geometric support does not prove strength → make no force or physical-build
  recommendation; report removal volume and remaining section explicitly.
- Finite bell/collar profiles remain a separate ball-motion gate → do not
  claim this capsule proves those other contacts or whole-machine clearance.

## Migration Plan

Commit the plan and existing red/research evidence. Implement the isolated
adapter with red-first tests, then adopt only after preservation and motion
gates pass. Sync/archive the local capability with evidence. Reverting the
production adapter choice restores the original ring without altering sources.

## Open Questions

Does the whole measured supporting common remain outside the independent
removal region at every collar phase? Can the published mesh preserve the
named small gap? Resolve both experimentally before adoption.
