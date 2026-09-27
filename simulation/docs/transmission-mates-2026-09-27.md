# Transmission channel frame adoption

This increment starts from marker adoption `92c9c8c` on integrated framework
`fabfc3d`. It attaches the eleven result channels and six counter channels
through their existing `turn` joints. The new `channel_frames.py` adapters
name each source-local motion datum from that channel's original joint; they
add no geometry, parameter, fit correction or motion coordinate. Matching
parent seats preserve identity rest placement, including the tens channel's
existing internal translation. The two internal sliding groups of each
channel are unchanged and not claimed as migrated by this increment.

## Independent evidence

`test_transmission_mates.py` freezes the old fitted banks, original retained
phase initialization and source-based ones channel. Each of seventeen
channels receives a different angle/setting/carry ratio. The witness compares
all transformed basis points at the existing eight-decimal precision, asserts
that all seventeen actual gear-tip leaves were visited, checks bank order and
values, and replays complete snapshots exactly. A separate tens probe checks
its existing self-translation during rotation and axial movement.

Before adoption, the two-bank and self-translation witnesses pass and the two
structural bank checks fail with zero mates instead of eleven and six (3 tests,
1.944 seconds). A first test-authoring draft assigned whole non-coordinate
bank references to a reused class-body temporary and failed during definition;
the fixture was corrected to state each joint end directly before collecting
this red baseline. No production behavior was changed for that fixture error.

The initial adoption passes 23 focused tests, but review finds that adding
mates to the shared `ResultShafts` base breaks the historical
`TrialResultShafts`, which replaces fitted children. Importing that trial
reproduces the documented inherited-moving-child refusal. The correction
preserves `ResultShafts` unchanged and adds a dedicated `MatedResultShafts`
production specialization, selected by `RetainedTransmission`. Historical
trial banks remain independent and unmated; no inherited mate is silently
retargeted and no framework rule is relaxed. A new regression imports and
checks both historical banks. All 24 focused transmission/marker/core/zero/
selector/register/crank and running-marker tests then pass in 23.308 seconds,
including the unchanged historical 216-coordinate bank hash.

In-memory +.2 mm shifts of the result-tens and counter-ones seats fail the
independent bank witness. Their actual gear-tip basis points shift by
.20000000000000284 and .1999999999999993 mm respectively. Both seat patches
are restored automatically and each restored gear tip matches its prior
points exactly.

The candidate production blobs are `bda6ff300f67999f032346b90f950eb3cb437ee5`
for `channel_frames.py`, `0e4b83f79667384e8af2885ae6dc4bc4184d07f6` for
`running_parts.py`, and `d507500902e6a14a7203f27e350d685923884140` for
`reverser_operating_parts.py`. These pin the candidate imported by the longer
regressions; final commits can include record-only updates.

`machinome build operating_curta` completes on the integrated framework,
without an override. The export keeps document version 13, the exact same
216 coordinate identifiers and 26 control names as the marker checkpoint,
and 301 program sources. All 417 model references resolve to existing assets.
The build used its separate `_build/operating_curta` artifact tree and a
4 GiB address-space cap while the contact tests retained `_build/simulation`.
The production source stayed frozen. The inspected host had 9.5 GiB available
before starting that bounded overlap; measured availability remained 9 GiB.

All six full-root `simulation.test_running.RunningCurtaTest` arithmetic
cases pass in 988.360 seconds on that frozen candidate: independent inputs,
successive additions, manual calibration carries, partial-stroke replay,
carriage-shift reassociation and subtraction/borrow followed by addition.
The run used the workspace environment, one BLAS/OMP thread and an 8 GiB
address-space cap. This is fresh actual-running-root arithmetic evidence,
not the separate clocked model's result.

Native snapshots of `MatedTransmissionBench` were inspected at rest and at
`angle=12, setting=9, carry=1`, using automatic full framing at 1200 by 900.
Both complete banks remain on their shafts; the driven view shows the
independently scaled turns and axial movements. Images are
`_build_transmission_mates_views.kH8RcJ/rest.png` and `set.png`. This isolated
pose bench is visual attachment evidence, not a clearance claim for those
arbitrary simultaneous settings. Its separate artifact directory was seeded
from the completed export so it did not write into the contact tests' cache.

Actual-root contact tests are in progress. The eighth-result, hundreds-result
and counter-ones cases have passed completely; counter tens and the four
higher counter stations remain in progress. This is a checkpoint, not yet a
completed transmission increment. The candidate source stays frozen in the
primary checkout while subsequent work uses a separate project worktree.
