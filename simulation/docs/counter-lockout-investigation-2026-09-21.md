# Counter lockout investigation

Tasks 6.2/6.3 require actual counter-side restraints as well as result-side
ones. This investigation does not adopt a counter restraint or fit in
`OperatingCurta`, and does not reuse the result-side contact table.

## Source-backed instrument

`tools/counter_lockout_probe.py` constructs each of the six existing counter
channels, retaining its source shaft pivot, upper-print placement and carry
stroke. Angles are actual machine shaft/crank angles, not normalized result
angles. The initial shaft positions are 134°, 114°, 94°, 74°, 54° and 34°.
The ones lockout is fixed; the five higher upper stacks have travel
−1.8..2.4 mm along their source downward axes. The normal lower input position
is retained at −4 mm, though it is not part of this upper-contact measurement.
The bell uses the already measured finer tessellation; its native material
is unchanged.

The fixture contract compares every upper print with the **actual retained
operating root**, using `Sim(..., meshes=True)`, and verifies identical native
material with zero native difference in both directions. The same comparison proves the
complete bell native-equivalent. Independent intermediate/full carry checks
prove the five upper stacks move down by 2.1/4.2 mm and the ones stays fixed.

The initial missing-instrument test is red. A first implementation check
also exposed an unassembled test oracle: mesh-free `Sim` does not prepare the
geometry tree. That test setup was corrected, not accepted as geometry evidence.
The first three geometry/selection contracts then pass (30.194 s).

The dynamic fixture factory initially gave all six root exports the same
artifact identity. Its regression fails **1 != 6** (0.641 s). The declared
`source_station` parameter now distinguishes them, and `trial_fit` additionally
distinguishes the unmodified and candidate instruments. No original printed
class or upstream file was changed. With complete-bell equivalence added,
the four-contract source fixture suite passes (121.106 s).

Logs under `_build_checks/`:

- `counter-lockout-fixture-red.log` — missing instrument;
- `counter-lockout-fixture-first.log` — unassembled oracle, not a machine defect;
- `counter-lockout-fixture-posed.log` — three contracts pass;
- `counter-lockout-export-identity-red.log` — export identity collision;
- `counter-lockout-fixture-green.log` — four source-instrument contracts pass.

Snapshot publication additionally exposed a shared identity on the trial's
enclosing channel, despite distinct roots and upper prints. An expanded
identity test fails **1 != 6** (1.656 s); the channel now declares its source
station too, and the test passes (1.667 s). Logs:
`counter-lockout-channel-identity-{red,green}.log`. Native/memory measurements
use each actual placed child and are unaffected by this SCAD-reference issue.
The analogous generated result-bank enclosing/root export identities need
the same check before result-bank instrument exports are relied on; its
ongoing dense measurements use the already corrected rigid child identities.

## Indexed contact before a candidate fit

The source-fit survey covers 120 poses: six stations, both carry seats,
five indexed flats and crank 0°/180°, measured natively and on the published
mesh. Fourteen poses have positive commons. At the parked crank, flat 3
contacts on every station:

| Station | Shaft | Raised native common, mm³ | Carried native common, mm³ |
| --- | --- | --- | --- |
| ones | 350° | 0.00004264142218 | unchanged fixed lockout |
| tens | 330° | 0.00001705656544 | 0.00005116969883 |
| hundreds | 310° | 0.00001705656680 | 0.00005116970292 |
| fourth | 290° | 0.00001705656566 | 0.00005116969952 |
| fifth | 270° | 0.00001705656885 | 0.00005116970906 |
| sixth | 250° | 0.00001705656783 | 0.00005116970601 |

The mesh misses several native contacts, including all five raised higher
stacks. The ones also contacts at crank 180° natively; its mesh reports zero
there. These findings concern the existing rigid simulation fits, not a claim
that the author's working printed calculator jams.

`CounterBankContactTest` pins parked-crank clearance over 60 poses and fails
with **19 kernel/pose failures in 15.715 s**. It deliberately defaults to
the installed fit and remains red until candidate adoption is justified.
Logs: `counter-lockout-indexed-source.log` and `counter-bank-indexed-red.log`.

## T08 candidate — not adopted

The isolated `--trial` substitutes only a .16 mm outer-profile relief for
the existing .15 mm counter lockouts and refines each complete upper print
to .01 mm linear / .1 rad angular tessellation. All six source class
identities, frames and carry relations remain explicit. This is a candidate
simulation fitting allowance, not a manufacturing recommendation.

The same 60-pose indexed-clearance test passes natively and faceted with the
candidate selected by a temporary test patch (**1/1, 41.645 s**). Log:
`counter-bank-indexed-trial.log`.

The candidate's material/identity/engagement suite passes **3/3 in 136.076 s**.
Every complete upper is one connected print and one valid native solid;
there is no added material, removal is confined to the original lockout and
bounded by its surface area times .01 mm, its R4 keyed core is untouched,
and the complete upper's axial extent is retained. Both locking flanks remain
present at all six stations, all five indexed flats and five carry heights:
**300 complete-print contact poses**, measured natively and on the mesh.
Log: `counter-bank-trial-material-flanks.log`.

Whole-profile
admission, ordinary counter motion, wrong-order retained stops and actual-root
Python/browser acceptance remain unproved; no counter contact law is proposed
from indexed clearance alone.

Fresh snapshots of counter ones at shaft 350° / carry 0 and counter tens at
330° / carry 1, both with the bell parked, were rendered and inspected.
The initial default views hid the upper interfaces behind the bell, so a
front-facing oblique view was rendered instead. The inspected final images
are `_build_checks/counter-ones-t08-contact-view.png` and
`_build_checks/counter-tens-t08-carried-contact-view.png`. They show the source
shaft, complete upper and lower prints, and bell in their separate installed
frames. Their pixels establish the assembly view, not clearance of the tiny
contacts quantified above.
