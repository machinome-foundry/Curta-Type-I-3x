# Central assembly frame adoption

This increment starts from Curta `5203fbd` on integrated framework `fabfc3d`,
without a worktree override. It uses the existing frame and existing-joint
mate interface; it does not require a framework or operator-interface change.

Four complete assemblies now attach through their original `turn` joints:
the stepped drum in the main drive, the tens bell in the carry mechanism,
the operating register carriage, and the complete clearing-ring assembly.
Each already uses the central shaft's Z datum in its assembly coordinates.
Matching parent seats and child spindle frames therefore preserve identity
rest placement. The drum's and carriage's independent lifts remain unchanged,
as do the loop's separate deployment joint, all bounds, laws and source parts.
Internal fitted placements are not removed or approximated.

The carriage and clearing mates live on the project-owned classes that
declare those children, rather than on an ancestor whose moving child is
replaced later. No generated-source class is edited. Mount handles reference
actual joint declarations, not name strings.

## Independent witnesses

`test_core_mates.py` restates the pre-migration bell and operating-carriage
attachments without any mates. Its source adapters may expose connector
frames, but the legacy fixtures never consume them for placement. It compares
every physical leaf's transformed basis points at the existing eight-decimal
precision, bank values and ordering, and exact snapshot replay. It checks bell
rotation/subtraction, carriage lift/shift, loop deployment and clearing sweep.
The existing crank witness independently covers the drum in both lift modes.

Before production edits, the two new moving-pose witnesses pass and all four
structural adoption subcases fail (3 tests, 3.936 seconds). After adoption,
all 13 core/zero/selector/register/crank tests pass in 12.281 seconds, including
the unchanged historical 216-coordinate bank hash.

Temporary in-memory +0.2 mm seat shifts fail the new bell/carriage/clearing
witnesses. A separate actual-leaf check measures 0.2 mm on the drum, bell and
counter body and 0.20000000000000284 mm on the clearing ring. Every patch is
restored automatically, and each restored leaf matches its original points
exactly. This verifies that the witness reaches installed parts, not only
empty assembly nodes.

## Installed motion

The seven existing `running_motion.py` contracts pass on both kernels:
faceted in 125.08 seconds at volume epsilon zero, exact in 118.09 seconds.
They verify installed carriage/indexing and clearing stops, marker movement,
spring endpoints, clearing-cover direction, the drum/crank's 9 mm lift and
the stationary bell/transmission. The eleven separately selected
`ClockedOperationsTest` cases pass in 32.877 seconds. That clocked model is
a separate existing regression, not proof of all running-root arithmetic.

The first clocked invocation selected the whole test module, which also
contains CAD-runner cases; two of those errored under plain unittest because
their `node` had not been realized. The corrected invocation selects only
`simulation.test_clocked.ClockedOperationsTest`, as intended. No production
fix or weakened assertion was made for this command-selection error.

All twenty running lift-limit, ratchet, carriage/clearing interlock and
operating-loop cases pass (361.455 seconds). That invocation also named the
nonexistent module `simulation.test_clocked_operations`, so its overall exit
was failure with one loader error, not a green 21-test suite. The corrected
eleven-case clocked invocation above passes separately. No running test failed.

The seven existing `crank_coupling_seat.py` contracts also pass on the exact
kernel in 109.49 seconds: complete drum clearance, source bore coaxiality,
retaining-pin clearance/capture, unchanged bounded relief, retained bank and
actual turn/lift motion. No test tolerance or geometric correction changed.

`machinome build operating_curta` completes on integrated main. The export
keeps document version 13, exactly the same 216 coordinate identifiers and
26 control names as before this increment, and 301 program sources. All 417
model references resolve to existing assets (389 mesh plus 28 marking
occurrences). This is contract preservation, not a byte-identical export claim.

Native carriage views are inspected at `_build/core-carriage-rest.png` and
`_build/core-carriage-set.png`. The latter requests elevation 6 mm, carriage
angle 40 degrees, clearing 30 degrees and deployment 45 degrees on the
independent mated bench. The clearing assembly, markers and loop remain
attached and compose their orientations. These are untimed input-pose views;
the retained movement and stop evidence comes from the stepped tests above,
not the still images. Native snapshots omit marking artwork.

These scoped proofs do not close the existing whole-machine geometry
acceptance tasks or claim that every attachment is migrated.
