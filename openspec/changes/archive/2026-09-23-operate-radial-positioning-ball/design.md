## Context

The source sphere is R3.75 at (9.627860318, 0, 30), in a stationary radial
guide. A rejected orbit clears the bell but penetrates the frame by over
144 mm³. The measured radial bell/collar profiles use a .05 mm normal gap.
An ordinary self-read endpoint-difference law pulls the free ball back and
blocks the wrong instant; those failures motivated the separately integrated
framework `Follow` law and viewer parity work. The ring passage is already
verified and adopted at project `3f7e0c9`.

Current native bell enclosure proves all angles and retained radial slack;
native frame and conservative sphere/mesh hulls prove complete frame, ring,
collar lift/shift and bell interfaces. Candidate all-neighbour demonstration
checks are still running and remain an adoption gate. Source prints and other
moving-part fits do not change in this cycle.

## Goals / Non-Goals

Goals: make the existing physical ball move radially under the two measured
contacts, retain slack, stop incompatible crank/carriage movement, preserve
ordinary arithmetic and every other physical input, and match Python/viewer
retained state on the actual production export.

Non-goals: new UI controls, automatic action preparation or finishing, physical
forces/rolling/friction, modifying the ball or its neighbours, source-file
changes, and whole-machine completion by implication.

## Decisions

### Use the existing measured candidate, not a different contact model

Promote the existing parent-X prismatic ball with initial displacement zero.
Use public `Follow` with the actual bell turn and carriage lift as ordered
envelope sources and the retained ball coordinate as output/self-read.
Retain matching dynamic bounds so incompatible input movement stops at closure.
The measured finite profile is accepted only with the independent continuous
geometry proof; its table is not its own clearance oracle. No separate page
calculator, callback-assigned coordinate or endpoint-difference substitute.

### Preserve explicit historical references

Keep the current static-ball root available as a named reference, then derive
the default operating root by changing only positioning and its contact law.
Keep the orbit candidate based on the static reference, so adding the radial
law cannot silently erase its counterexample. Retain the pre-Follow law as a
negative. Ring/frame references must explicitly select their intended geometry
and corresponding motion model, not accidentally inherit an invalid mixture.

Existing fixture checks must verify the new coordinate is exactly zero at
rest and hash all original 213 coordinates against their existing digests.
Do not re-record those digests or drop the preservation assertion. Full-root
paired tests compare all other meshes and original coordinates over legal
motion; the only new retained coordinate is the radial ball.

### Verify contact, history and wrong-order operation

Keep the source sphere and actual guide frame as measured premises. Prove
zero native/world64 contact over the admitted profile domains, with no
hidden supports or overlap epsilon. Check transverse guide capture. Run all
six demonstrations against every rigid and flexible neighbour of the ball.
Check outward push, free retention, inward push, both incompatible request
directions, long/short stop, idle/retry, explicit relief and exact replay.
Reject static, orbital, reversed-axis and pulling-law variants through the
corresponding independent geometry or retained-state checks.

### Validate the current viewer artifact

Export the adopted root with the integrated producer/viewer pair. Check full
bank equality at rest, outward, retained return, raised-carriage stop, idle,
replay and relief through the hosted viewer's public run handle. Verify the
unmodified auto-mounted standalone page through real part-pointer gestures,
terminal outcomes, four-decimal input readouts and inspected images. The
standalone page intentionally exposes no public live-bank lookup; do not
remount it or extract hidden handles and call that standalone coverage. Both
surfaces use the exact same exported program and bundle. The earlier viewer-cycle
trial proves engine compatibility but does not substitute for current
production-geometry acceptance. Preserve exact bundle/export hashes. Use a
screenshot timeout sufficient for the already measured software-renderer
readback cost; do not change simulation behavior to capture an image.

This evidence-surface clarification changes neither the retained-state
requirement nor the viewer API. It avoids a speculative API solely for a test.

## Risks / Trade-offs

- Inherited contact declarations could contaminate historical negatives →
  keep an explicit static base and verify the expected coordinate sets.
- A table may clear samples but not intervening positions → use conservative
  full-domain native and mesh enclosures, not a volume threshold.
- Adopting a restraint can reveal a previously accepted wrong action order →
  retain physical stop/relief semantics and report the measured obstruction;
  do not automatically prepare the machine or weaken the bound.
- Green local mechanics can hide other moving collisions → keep the complete
  neighbour audit and umbrella whole-machine tasks separate and open.

## Migration Plan

Commit this plan with finished read-only enclosure evidence. Complete candidate
gates, then promote the radial declaration and wiring. Run preservation and
production geometry/behavior checks, rebuild the current viewer artifact and
validate it, sync/archive this local capability and commit. Reverting the
default root's inheritance/positioning selection restores the explicit static
reference without touching source assets or the separately completed ring fit.

## Open Questions

Are any ball contacts newly exposed by full subtraction, overflow, clearing or
shift demonstrations? Does the reverse contact direction require additional
admitted-travel evidence? Resolve these before completion, without expanding
the ring/frame fits or claiming undocumented physical forces.
