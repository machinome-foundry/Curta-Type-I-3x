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
The analogous generated result-bank enclosing/root identity issue was then
reproduced and corrected separately; its dense measurements use the already
corrected rigid children. See the operating continuation record.

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

## Ordinary passage and independent contact timing

Freezing an engaged carry gear is a negative control, not ordinary motion.
At each higher counter's tooth midpoint (crank 204°, 224°, 244°, 264°, 284°),
the frozen initial shaft has approximately **2.9283 mm³** native contact;
advancing it by the source passage's 36° makes both complete-print kernels
clear. All five stations reproduce this contrast. Log:
`counter-carry-motion-control-probe.log`.

`test_counter_bank_lockout.py` now samples ordinary source tooth trajectories
for counts 0, 1 and 9, five starting flats and carry fractions 0, .5 and 1.
It includes input/carry entry, midpoint and exit angles as well as a 10° grid.
An initial candidate run is scoped to ones and tens through temporary test
patches, not production edits, in
`counter-trial-ordinary-motion-ones-tens.log`. It passes **2/2 tests in
1112.536 s**: the negative control and **4,125 complete-print poses** in both
kernels (90 flat/count/height cases). The corresponding run for stations
3–6 is now active in `counter-trial-ordinary-motion-stations-3-6.log`.
No whole-bank motion acceptance follows until that run also completes.

The counter's bell ingredients are not rigid copies of the result-side ones.
`tools/compare_counter_profiles.py` reads the original native parts and
compares candidate registrations without altering them:

| Native ingredient | Result volume, mm³ | Counter volume, mm³ |
| --- | --- | --- |
| upper locking disc | 2849.553368 | 2891.484231 |
| lower locking disc | 4511.217197 | 4572.692667 |
| carry ring | 2033.363220 | 2033.075111 |

The tested 0°, 180°, 181.25° and 182° registrations all retain material
differences. Some working surfaces could nevertheless coincide; whole-solid
non-equivalence does not establish every contact curve's shape. It means
rigid congruence cannot justify simply copying a result contact table. The
committed probe reproduces the initial readings byte-for-byte in
`counter-result-profile-shape-comparison-tool.log`.

`tools/counter_locking_envelope.py` therefore measures complete counter
prints independently. At ones shaft **167.6°**, the native closing bracket is
**174.885711670..174.885749817°**, while the mesh closes slightly earlier at
**174.884986877..174.885025024°**. At raised tens shaft **147.6°**, the sampled
opening and closing brackets are exactly 20° later in both kernels. This
single-pose agreement does not establish a shared profile. Logs:
`counter-ones-partial-envelope.log` and
`counter-tens-raised-partial-envelope.log`.

A coarse ones profile collection has completed over shaft 134..494° in 6°
steps, with a 5° crank grid and bracket refinement in both kernels, in
`counter-ones-upper-envelopes-coarse.log`. Each kernel has 61 shaft records:
55 have two boundaries and six indexed records have none. The terminal
completion record is present. This finite grid can miss narrow islands;
refined/between-knot checks and retained operating action-order evidence are
still required. No counter law is adopted or proposed as settled by this
collection. A 2° shaft-grid refinement, excluding the already measured 6°
knots, is active in `counter-ones-upper-envelopes-refine-2deg.log`.

## Indexed free-band measurement

The measuring tool now accepts `--bands` instead of `--shaft`, with an
explicit parked `--crank` (default 0). It brackets both complete-print
locking flanks around each of the station's five actual shaft indices in
both kernels. A blocked centre or a missing outer contact fails the probe;
every reported bracket retains its measured zero/positive endpoint volumes.
The 18 bisections give an angular bracket no wider than 5/2^18 degrees,
not a tolerated intersection volume. The instrument's missing-function
test failed first; all three bracketing/negative-control tests then pass
(0.003 s), including contact as small as 1e-20 mm³.

The complete ones run has ten verified records. The intersection of the two
kernels' measured free intervals at crank 0 is:

| Shaft index | Last free on lower side | Last free on upper side |
| --- | ---: | ---: |
| 134° | 131.304992676° | 134.311031342° |
| 206° | 203.303943634° | 206.311031342° |
| 278° | 275.303962708° | 278.307903290° |
| 350° | 347.310714722° | 350.063819885° |
| 422° | 419.518196106° | 422.308094025° |

These bands are asymmetric and differ among source flats. They are local
parked-crank measurements, not a continuous all-crank clearance certificate
or a reason to use identical repeated sectors. Logs:
`counter-indexed-band-tool-{red,green}.log` and
`counter-ones-indexed-bands.log`. The full bracket/volume records are also
committed as [numeric evidence](evidence/counter-ones-indexed-bands-2026-09-21.json).
The corresponding tens measurement at
carry 0, .5 and 1 is active in `counter-tens-indexed-bands.log`.

The first actual-root diagnostic reaches crank 170° and counter shaft
167.6°, but fails its measurement setup: its drum path omitted the enclosing
`main_axle_step_drum_1` node. This is not a geometry result. The failed log is
preserved as `counter-ones-wrong-order-root-probe.log`.

The durable `tools/counter_wrong_order.py` corrects that path and additionally
checks **all six** complete lower counter prints against both drum halves.
Its actual operating requests are crank lift to 9 mm, reverser to −4.9425 mm,
partial crank movement to 170°, separately sampled lever withdrawal toward
the lower housing stop, and a further crank request. The corrected run is
active in `counter-ones-wrong-order-root-corrected.log`. Its preparation,
complete upper/bell contacts and lower-input/both-drum contacts must be read
before declaring this a clear withdrawal path or a missing counter stop.
Neither this scope nor a successful diagnostic would certify every unrelated
interface in the operating root.
