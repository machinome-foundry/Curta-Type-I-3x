# Register-detent frame adoption

Following carry commit `96775f6`, the production carriage selects
`FramedRegisterDetents`: seventeen ball seats from the unchanged source
assembly, each mated through its original `lift`, and a rigid spider seat.
The spider's seventeen fingertip joints, all shape laws, the carriage's
recentring/clocking and all fits remain unchanged. The source orientation of
each spherical ball is retained too. Original `RegisterDetents` remains an
independent legacy witness.

The source-axis conversion helper moves unchanged from `carry_frames.py` to
`source_frames.py`, shared with this increment. It supplies both explicit
directions using the ratified precision contract. No new API is needed.

## Evidence

Two draft fixture errors were corrected before the valid red: child-declaration
records were not node classes, and resolving a child type inside a declaration
body produced a path reference. The corrected tests resolve production types
outside class bodies. The valid red runs two tests in .759 seconds: adoption
fails with zero rather than eighteen mates; the independent witness passes.

The witness compares six requests (0, .25, .7, 1.4, .5, 0 mm), with each ball
receiving its own index/17 fraction. It asserts all seventeen physical balls,
tips and arms plus the spider mount exist, compares every transformed basis
at eight decimal places, exact bank order/values, all twelve shape controls
per arm, and exact snapshot replay. All 29 focused adoption/running-marker
tests pass in 24.178 seconds, including the historical 216-coordinate hash.

After the unmodified witness passes, +.2 mm seat mutations independently move
ball twelve by .20000000000000284 mm and the spider's counter-six tip by
.20000000000000007 mm. Both fail the witness; automatic restoration returns
the complete selected basis exactly.

The unchanged existing seventeen-ball capture assertion passes before adoption
(faceted: one test, 59.73 seconds). `DetentMateCaptureBench` delegates only that
assertion, not the separate integer/carry/clearance sweep. After adoption it
passes faceted (18.30 seconds, volume epsilon zero) and exact (4.49 seconds).

Fresh `machinome build operating_curta` passes. Compared with frozen checkpoint
`7ee005f`, the entire program differs in exactly seventeen `stated_by` fields:
`RegisterDetents` becomes `FramedRegisterDetents` for the inherited ball-to-finger
relations. After asserting precisely those replacements, program content is
equal, including identity, coordinates, sources, limits and profiles. All
control definitions are equal; all 417 mesh/marking occurrences have identical
STL bytes. Version 13, 216 coordinates, 26 controls and 301 sources remain.

Native candidate and independent legacy snapshots at rise=1.4 mm were inspected
at 1200 by 900: `_build/detent-mates-set.png` and
`_build/detent-legacy-set.png`. Their decoded RGB bytes are identical. The full
ring and seventeen independently deflected fingers/balls are visible. This is
attachment evidence, not an arbitrary-setting clearance claim.

Validation used the workspace environment, one BLAS/OMP thread, isolated build
caches and 4 GiB address-space limits for CAD jobs. The separately frozen
outer-channel eight-test contact suite subsequently passes in 3878.007 seconds;
it is not relabelled as testing this increment. Whole-machine geometry remains
open, and the simulation umbrella is not archived.
