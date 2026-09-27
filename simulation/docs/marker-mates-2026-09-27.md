# Decimal-marker frame adoption

This increment follows central-assembly commit `6810577` and uses integrated
framework `fabfc3d`. The ten marker/ball/spring assemblies now have
parameterized track seats, with their existing neighbour-bound `turn` joints
and all ten operator controls retained. No new framework API is proposed.
Source marker placements and the diagnostic geometry banks remain unchanged.

Each project-owned marker adapter carries its source track frame. Lower
seats add the original radial seating to `LOWER_CENTER`; upper seats use the
recentered shaft datum. Their frame difference replaces exactly the old
parent translation. The unchanged `marker()` helper continues to declare the
site joint and neighbour Bounds; a named mount references that same joint.
Both banks keep the `.06` mm `radial_seat` default, evaluated by each frame's
callable against its realized bank. No render method also places a mated child.

`test_marker_mates.py` independently restates the old joints, neighbour Bounds,
and original source assemblies, and retains the old track-placement classes.
At radial seats 0, .06 and .12 mm it compares all thirty physical leaves,
bank ordering and values, request status and exact snapshot replay. Non-default
seats are numerical placement witnesses, not clearance claims. Requests reach
neighbour stops, open space, traverse a full turn and repeat a stopped request.

Before any marker production edits, the legacy comparison passes; each bank's
structural adoption test fails with zero mates instead of five (2 tests,
2.393 seconds).

After implementation, all twenty marker/core/zero/selector/register/crank
adoption and running-marker tests pass in 20.928 seconds. This includes the
historical bank hash, actual-root independent marker operation, every neighbour
stop in both directions, full-turn travel and exact replay. In-memory +.2 mm
shifts of lower marker 1 and upper marker 6 seats fail the independent witness
on their actual `position_marker` leaves by .20000000000000284 mm. Both
mutations are restored automatically; no tolerance was changed.

The seven existing installed `running_motion.py` contracts pass in 95.79
seconds on the faceted kernel (volume epsilon zero) and 97.59 seconds on the
exact kernel. In particular, every installed marker body, ball and spring
moves independently around its track, and the upper bank follows carriage
lift/shift and clearing-ring rotation without changing the registers. The
other existing stop, spring and drum movement assertions also remain green.

The full `machinome build operating_curta` succeeds without a framework
override. Its export keeps document version 13, the exact same 216 coordinate
identifiers and 26 controls as the central-assembly checkpoint, and 301 program
sources. All 417 model references resolve to existing assets.

Native full-machine views `_build/marker-mates-rest.png` and
`_build/marker-mates-set.png` were inspected. The second requests +20 degrees
for marker 1 and marker 6; those two markers remain on their lower and upper
tracks while the other eight remain at their original positions. These are
untimed input-pose views, not stepped-operation evidence or a marking-artwork
check. The stepped tests above prove independent motion and retained values.

The correctly selected twenty running limit/ratchet/carriage/clearing/loop
tests pass in 367.949 seconds on this complete marker-adopted root:

```sh
python -m unittest -v simulation.test_running_limits \
  simulation.test_running_ratchet simulation.test_running_interlocks \
  simulation.test_operating_loop
```

These are scoped adoption and regression proofs. Transmission stacks, carry
sliders and several spring/detent attachments still await migration, and
the project's existing whole-machine geometry acceptance remains open.
