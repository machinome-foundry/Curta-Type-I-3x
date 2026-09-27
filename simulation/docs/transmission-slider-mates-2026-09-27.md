# Transmission sliding-group frame adoption

Starting from the outer-channel checkpoint `7ee005f` on framework `fabfc3d`,
this increment attaches the two sliding prints inside each of seventeen
channels: 34 existing `travel` joints, without new coordinates. It is project
adoption of the existing interface, not a framework extension. Work takes
place in the isolated `curta-frame-continuation` project worktree while the
primary checkout stays frozen for the outer-channel contact regressions.

The shaft-line guide on each print and the matching channel seat have the
original channel's XY datum, source Z=0 and negative-Z direction. Source
prints receive thin adapters; already fitted uppers and counter inputs get
frames beside their existing fit declarations. No shape, tolerance, site-joint
axis, relation or source placement changes. Both fixed-height ones uppers
retain their zero-ratio carry binding.

## Red-first and ownership correction

Before implementation the structural test fails all seventeen channel
subcases (zero internal mates rather than two), while the four independent
outer-bank tests pass: 5 tests, 17 expected failures, 1.838 seconds in the
worktree. The original primary-checkout reproduction took 2.779 seconds.

An initial attempt to attach inherited print declarations was refused at
class creation by the documented ownership rule. The correction explicitly
redeclares each moving child at its mate owner. The existing station factories
now expose their fitted upper constructors separately, so those declarations
do not duplicate fits or inspect generated joint-specialization internals.
Their qualified helper names change artifact identity, not geometry. The
historical channel factories remain unmated. Counter ones declares both mates
on its final protected-input owner, not on an ancestor it later replaces.

All 25 focused adoption and running-marker tests pass initially in 19.397
seconds, and again in 20.173 seconds with the strengthened physical-leaf
coverage below. The historical 216-coordinate bank hash is unchanged.

## Independent physical evidence

The legacy bank witness retains the original source/fitted channels, their
phase initialization, and an independently declared protected counter-ones
input. It compares all basis points at eight decimal places during distinct
per-channel rotations, input settings, carries and exact snapshot replay.
It explicitly requires seventeen shaft gear tips and all 34 sliding groups
with their actual gear or pentagonal-lockout leaves.

The first coverage assertion incorrectly expected a gear inside both ones
uppers, which contain sleeves and a pentagonal lockout instead. That assertion
and an exploratory mutation probe's nonexistent leaf path were corrected;
those failing probe attempts are not accepted evidence. With the unmodified
witness explicitly green first, separate in-memory +.2 mm changes to the
result-digit-seven and counter-ones guide seats each fail the pose comparison.
Each selected input-gear and upper-lockout origin moves
.1999999999999993 mm. Automatic restoration returns every selected basis point
exactly to its prior value.

Fresh `machinome build operating_curta` succeeds without a framework override.
Compared with the frozen outer-channel checkpoint:

- The complete exported motion program is equal, including its identity,
  coordinates, intermediates, edges, spans, sources, limits and profiles.
- All control definitions are equal: 26 controls, 216 coordinates,
  301 program sources, document version 13.
- All 417 mesh/marking occurrences resolve and have byte-identical STL data.
- The entire exported root tree is equal after replacing each model filename
  with its asset SHA-256 and excluding only freshness timestamps. Thus the
  comparison also checks every rest placement and exported motion operation.

The full-root independent-selector and partial-crank/replay regressions both
pass in 152.643 seconds. The six-case arithmetic result recorded for the
outer-channel checkpoint is not relabelled as a fresh six-case run here.

The native snapshot `_build/slider-mates-set.png` was inspected at
`angle=12, setting=9, carry=1`, with full automatic framing at 1200 by 900.
Its decoded pixels are identical to the separately inspected checkpoint view
`_build_transmission_mates_views.kH8RcJ/set.png`. It shows both complete shaft
banks with their independently moved sliding groups; this isolated pose is
not an arbitrary-setting clearance claim.

Validation used the workspace environment with one BLAS/OMP thread. The
build, snapshot and two running cases used 4 GiB address-space caps. Build
artifacts stayed in the isolated worktree; the primary contact run continued
against its frozen source and separate cache.

Integration still waits for the outer-channel contact suite. Whole-machine
geometry acceptance remains open; no OpenSpec archive is claimed here.
