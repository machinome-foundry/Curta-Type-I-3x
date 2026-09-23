# Remaining carry/frame contacts

Project `d6f298f` still uses the verified first-two-result-station frame fit.
A new read-only probe measures each of the fifteen installed carry sliders
against the complete production frame at initial position and 2.1/4.2 mm
downward stroke witnesses. No root state changes or new fit are applied.

| Stations | Native raised common (mm³) | Native lowered common (mm³) | Sampled midpoint |
|---|---:|---:|---|
| Result 1–2, previously fitted | 0 | 0 | Clear |
| Result 3–10 | approximately 4.626578 | approximately .099225 | Clear |
| Counter 1–5 | approximately 3.370756 | approximately 3.741717 | Clear |

All 45 native commons are valid; world64 checks independently reproduce the
same obstructed/clear classification. Every station's exact values, frame
displacements, initial travel and native common bounds are retained. The
213-coordinate bank is unchanged. This 9.763-second diagnostic is not an
admitted motion replay, a spring survey or a full-path clearance certificate.

The first diagnostic incorrectly transported the site-declared axis through
the imported leaf's frame. It completed, but its nonzero-stroke values are
invalid as carry-stroke evidence. The corrected version uses the station's
parent frame, as required by the existing public site-joint contract. The
`world_frames` helper now optionally exposes assembly frames; its default
leaf inventory is unchanged. A dedicated rotated-leaf test fails against the
old helper's missing option and passes with the extension. Neither this
harness error nor its correction is a framework limitation.

The existing frame fitter explicitly lists only stations `(0, -20)`. Thus
these remaining contacts are unfinished work, not a missing prior merge.
Counter endpoint volumes differ materially from result endpoint volumes;
the [new project plan](../../openspec/changes/extend-carry-frame-passages/proposal.md)
requires independently measured supports and local removal bounds before any
cut. No symmetry-based bank-wide cutter or source-overlap waiver is adopted.

Artifacts under `_build_checks/`:

- Corrected `carry-bank-parent-frame-witnesses-d6f298f.jsonl`, SHA-256
  `97b68752d24a8f7d55c7a052b8a7d66d41fda7466e4d8afe1ce12f6d60d8c678`.
- Invalid stroke-frame attempt `carry-bank-frame-witnesses-d6f298f.jsonl`,
  SHA-256 `466eb1bcd9e9c1d3adfe22c36dcd31e278d3565a9b0b97f39f3d6f9020560e13`.

Reproduce the corrected inventory with
`python -m simulation.tools.carry_bank_frame_contact`, explicitly pinning the
verified framework worktree used here (`cache-standing-bound-bind`, `a500a99`).

## Red contracts

The independent full-bank driven fixture passes two guards: its native frame,
fifteen sliders/guides/springs match the installed operating root at rest with
zero material difference in either direction, and actual driver updates move
every slider through 4.2 mm while all rigid supports remain fixed. Its two
clearance tests fail at 104 named kernel/station/pose subtests: both slider
endpoints and spring preload/maximum-spread witnesses at each of thirteen
unfinished stations. The first two result stations stay clear. The four-test
run takes 48.894 seconds and exits one, as expected before fitting.

Log `_build_checks/carry-bank-frame-red-4cd6ec4.log`, SHA-256
`ce6c72428d1075b336a01189c41688a7dc56863625d9f3f056c7a394da694ea3`.
No production frame geometry has changed at this checkpoint.

## Independent removal limits and source support

Every installed guide has six mapped native contact lands, totalling about
73.575 mm². Result stations are measured at 0, −20, …, −180 degrees; counter
stations at 130, 110, 90, 70 and 50 degrees. Actual native transforms retain
their source floating-point residuals. Nominal rotations only select the
independently bounded station regions; they do not reposition any part.

The counter upper shoulder is a rectangle at Z=−21.6 mm. Its lower shoulder
is a different five-sided outline at source Z=−11.7 mm, reaching −15.9 mm
after the full 4.2 mm stroke. It cannot use the result's thin lower-edge cut
at −16.8 mm. Counter spring extrema are also wider. Each family has separate
source-derived bounds in `carry_bank_regions.py`, with no whole-station box
or annular relief. The two leg windows leave their intervening bridge intact.

Before constructing the fit, three prospective maximum-removal tests passed
in 23.817 seconds: a single valid solid without added material, unchanged
small cylindrical bore surfaces, and zero lost native contact area outside
the independently named .08 mm seat-edge strips. More than 99.63% of result
lands and 99.81% of counter lands remain. The maximum removed material stays
strictly apart from all 49 selected installed hardware/frame neighbours; the
closest is `frame.fasteners.m4_nut_2` at 1.9004724457572808 mm. This is a
geometric preservation bound, not a strength claim or whole-machine check.

All fifteen continuous slider enclosures pass against these maximum regions:
172,403 native checks, no unresolved cell. All fifteen spring enclosures also
pass: 4,784 checks, no unresolved interval, maximum independent centreline
cross-check error 2.842170943040401e−14 mm. These certify feasibility inside
the permitted regions, not clearance of the smaller production candidate.

The first spring run stopped at the source hash guard. Comparing its pinned
`3afcac9` source with current main establishes exactly three changed import
lines (`solid_node` → `machinome`, commit `a6e6a9f`), and no changed geometry,
constant, affine parameter law or placement. The guard now pins current
source SHA-256 `2f8501ea46e12d1319428a225dc14a819c95c791670b54322fd1274f4045e623`.
Both legacy first/second slider and spring certificates were then rerun and
passed with separate output names, preserving the historical artifacts.

Native before-fit sections of both distinct station families were inspected:
raised/lowered shoulders and maximum-spread spring, complete frame and guides
present, positive contact highlighted. The image is scoped to those sections,
not an assembled-root acceptance picture.

Artifacts under `_build_checks/` (SHA-256):

| Artifact | Hash |
|---|---|
| `carry-bank-support-areas-4cd6ec4.jsonl` | `5459a1f7c388008c5bb787fc392b33f9617a3bdb1fdc76714c3c7109a5ebeb31` |
| `carry-bank-min-spread-4cd6ec4.jsonl` | `48415f756fb9592cccd01c9b499445662137e3d56e5bc097be7a13ddfb29b2c5` |
| `carry-bank-region-gate-4cd6ec4.log` | `442328dbf3a3bdec156f73760b33e8a33c0cc337f166076f9770fd8860591ead` |
| `carry-bank-protected-hardware-4cd6ec4.jsonl` | `afac97c5adf5e1659a932a3b100dd975cf136946ad53e4b5264ab820273f5708` |
| `carry-bank-sections-before-4cd6ec4.png` | `8b2645f42b9df7f8dec01d25e65c21e3decae12b11ee4d671f8bfc72d734af9a` |
| `carry-bank-region-sweep-group-1-4cd6ec4.log` | `5fe6abb0f35e090453622ed09374a5403ea8e7896794e6009658225d1c326896` |
| `carry-bank-region-sweep-group-2-4cd6ec4.log` | `80ed10be9426a9ff06a45ea040e5508c9cd7e748d39799bd11d4beb4ede59db4` |
| `carry-bank-region-sweep-group-3-4cd6ec4.log` | `a75a0dd53dfeaaa074554b4988a1017535bf5be3b2334948845706c5da5940d7` |
| `carry-bank-region-sweep-group-4-4cd6ec4.log` | `7b3fca30a2928deeac6871b93a192cc6271dcb2f90aa910ea40bc8e83eb0e0b2` |
| Stopped `carry-bank-region-spring-bound-4cd6ec4.log` | `15daf4c7bf612b42680b20bf13eb61f474263ec35ae85981d9201808fb1d04ef` |
| `carry-bank-region-spring-bound-reaudited-4cd6ec4.log` | `330eb8f9611e81b2a3f19f4c6d9302ae2d08f357a98fca33eaf734e6adf28193` |
| `carry-frame-legacy-certifier-regression-4cd6ec4.log` | `1779863aa2a4d89ed6a71e8aa271154b771069565ac35a71ab01907db49a5420` |

The earlier `carry-bank-supports-4cd6ec4.jsonl` incorrectly labelled native
face area returned by `Face.Volume()` as volume; it is superseded by the
explicit-area report above and is not used for material-volume claims.

## Isolated candidate checkpoint

`CarryBankPassageFrame` retains the old two-station adapter and adds eight
result stations and five separately measured counter stations. The counter
cuts derive their wires directly from the original counter slider, never
from the acceptance regions. The existing .04–.06 mm trial gap remains, with
.05 mm default. Neither a moving part nor the operating root is edited.

Ten initial candidate tests pass in 159.715 seconds. These check all slider
endpoints and spring preload/extremum contacts in native and world64 geometry,
actual full stroke and fixed supports, exact unchanged native geometry of
every other fixture body, one valid frame, no added material, zero removal
outside independent regions, unchanged protected lands/bores, exact fresh/
built material parity, and measured shoulder gaps at .04/.05/.06 mm for all
stations. Result lands retain about 99.7825%, counter lands 99.8913%. Since
all candidate removal is contained by the independently checked maximum
regions, the 49-neighbour separation bound also applies to this smaller cut.

Log `carry-bank-fit-initial-4cd6ec4.log`, SHA-256
`b949941780ac154ae0fe155f087a4eb2d9e8398f81c6cd9291a9fed27ad0bebe`.
Dense/continuous candidate motion, negative controls, capture, root adoption
and assembled visual acceptance remain separate gates, not implied passes.

## Candidate motion, negative controls and inspected geometry

All fifteen stations pass 78 native/world64 poses each, covering the 41-point
stroke grid, both families' detent knots and the preload. There are 2,340
part/pose rows (slider and spring), all exactly zero in both kernels. The
result-bank run takes 619.877 s; the counter-bank run takes 327.744 s.
The actual .05 mm candidate also passes every continuous enclosure: 235,763
native occupied-slider-cell checks and 5,592 spring interval checks, with no
unresolved region. These are independent of the candidate cutter geometry.

Five negative tests pass in 33.691 s. Restoring each of eight distinct
omitted result/counter shoulder or spring-leg cuts restores a valid positive
native obstruction. Rotating additional passages by one degree leaves both
families obstructed. Excessive central drilling violates independent removal
bounds; an empty frame is rejected before clearance; an actual 3.9 mm stroke
fails the 4.2 mm displacement guard, while 4.2 mm passes. The original
two-station adapter's seven material/gap tests remain green in both kernels
(40.27 s exact; 37.01 s faceted).

All fifteen original spring seats and hooks pass three capture contracts in
both kernels (145.20 s exact; 2.84 s faceted): fixed closed-fold centres,
.01 mm free/.2 mm blocked hook play at three engaged positions, and spring/
guide clearance at six stroke positions. The first harness launch used a
test-class path where the CLI requires a node reference. A second launch
discovered zero tests because imported cases are not locally defined cases;
neither is counted as validation. A local companion subclass registers all
three tests. An initial incorrectly pre-rotated perturbation direction then
fails capture; the public API already transports node-local directions. The
corrected local-X check is the passing evidence, not a mechanical change.

The candidate's six native station sections were inspected and show the
separate shoulder and spring-leg reliefs with guides retained. An initial
plot attempt tried to section an empty common; skipping empty solids fixes
only the plotting instrument. The inspected assembled view shows the frame
lands, guide blocks, shafts and adjacent supports. Its outer shell is hidden
for inspection only; the upper cover still occludes part of the mechanism.
It is a support-context view, not evidence that every tiny gap is visible.

Artifacts under `_build_checks/` (SHA-256):

| Artifact | Hash |
|---|---|
| `carry-bank-candidate-dense-result-4cd6ec4.log` | `2c95a3a55a234ce6b6f391cf18f66beac703a1d01ae172ce5d5e9120ad2e6cbb` |
| `carry-bank-candidate-dense-counter-4cd6ec4.log` | `61a619bf74736e9c301256dc698f372a2c4726c5f9efa7bf2ea48401ad95aeee` |
| `carry-bank-candidate-sweep-group-1-4cd6ec4.log` | `1b09f68a609f2af783198b5f64a9ef34b90ceef02b1cc992ef1e292abe2d382e` |
| `carry-bank-candidate-sweep-group-2-4cd6ec4.log` | `1924f44b3d78de7447eaa664844630b6b70dc739a0709b06c2c545874c886a84` |
| `carry-bank-candidate-sweep-group-3-4cd6ec4.log` | `fa515d0d37a05db1d049e44bbaf62c3044c92cff848013655cc4cf8f68a89fc0` |
| `carry-bank-candidate-sweep-group-4-4cd6ec4.log` | `cb563a40514baff0dd21fce5a02df4242fb9dd6252eca640a380b7a0a36ec384` |
| `carry-bank-candidate-spring-bound-4cd6ec4.log` | `b5ddf4823fa82ca209126c80d606940f548e601938c835779e9e00111a7637a2` |
| `carry-bank-candidate-negatives-4cd6ec4.log` | `5e8bd3b56fda60e57d540647a2a1895be7bd1210463f99f3b1b95f19698072ba` |
| `carry-bank-first-pair-fit-exact-4cd6ec4.log` | `15a1f1d52e4ed375d93d79f3d64e25a4680100e847a380f0607766dbb595b2b7` |
| `carry-bank-first-pair-fit-faceted-4cd6ec4.log` | `16c249f474ffa181694f1bc1c1fb0ff618bba8f0b713c8c318fd0b3fbc9d357f` |
| `carry-bank-candidate-capture-exact-local-axis-4cd6ec4.log` | `c7fe9e246622a87161c3677bdb02d6511bea9ea7bda4b5e0e2bcba45a1bee16e` |
| `carry-bank-candidate-capture-faceted-local-axis-4cd6ec4.log` | `645b8107af3eac8677186ec209ff42b57dcd68524eab8da6d4195a436ed15a9a` |
| Wrong-axis exact attempt | `14f078a6279527966b95a3385a1f0650bf52b164b1ea2505f6635bb009a92911` |
| Wrong-axis faceted attempt | `2fdbed7cea8512f2a34b5f0b776272482f23d18cd748c2890930026de8bb1c99` |
| `carry-bank-sections-candidate-4cd6ec4.png` | `fdf596c77bf432e099c7c80c0ef5e20e39b90d54ea96d1610d347c53338b200b` |
| `carry-bank-assembled-candidate-4cd6ec4.png` | `9ad907f16c53b931eeb0c6f969e778b952237db7382b5db147d534b8b8baa4bf` |

## Whole-root trial and unresolved guide finding

A paired rest/half-turn test passes in 62.387 s: all other 388 rigid meshes
and all flexible meshes are array-identical, and the complete 213-coordinate
bank is identical. Only the frame loses material, inside the independent
bounds. The baseline classes subsequently pin the old first-pair frame
explicitly so future production adoption cannot silently erase this comparison.
The final explicit-reference rerun passes in 53.686 s after production adoption.

The complete rigid-pair addition inventory finishes 44 samples in 198.011 s,
with the expected (5, 2) result/counter. Paired with the pre-fit grip-seat
inventory, it adds no pair and removes only the thirteen intended slider/
frame pairs. All non-frame pair volumes are bit-identical. Some existing
frame/guide/fastener/support common volumes change numerically; these are not
claimed bit-identical or waived. The native protected-material proof above
still establishes that removal does not reach those hardware bodies.

The unchanged guide-play diagnostic records 450 native/world64 perturbation
measurements at 0, 2.1 and 4.2 mm drop, including radial/tangential ±.01 and
±.2 mm offsets. No native Boolean is invalid. It exposes an independent
pre-existing obstruction: every counter slider at full drop enters its guide
by approximately .595350 mm³ natively (.595357 mm³ world64). All unperturbed
guide/slider world64 questions are positive, including much smaller result
contacts; these are not excused as rounding. This fixed-frame correction
does not alter those guide/slider interfaces. Their working-clearance finding
remains open under the overall operating-machine task, and guide motion is
not certified clear by this record.

Further artifacts (SHA-256):

- `carry-bank-candidate-root-identity-4cd6ec4.log`:
  `01c0d15907764b33ef200ba13c79f92b092ac0a1f8c27a8d4cbaa843d137c493`.
- `carry-bank-candidate-addition-contacts-4cd6ec4.jsonl`:
  `0c550e5429041d77434b4ebb88015f82baefdb3eec60403445089f1508234a8d`.
- `carry-bank-unchanged-guide-play-4cd6ec4.jsonl`:
  `78f796f5a1320a02bcc587ad30dcb14a2cb4301150624a0ab5392b8686440da2`.

## Production adoption and operating regression

`UpperFrame.main_body` now uses `CarryBankPassageFrame`. The original
`CarryPassageFrame` remains unchanged and is explicitly installed in the
reference fixtures, preventing the comparison from following production edits.
Fourteen production/candidate material, support and stroke tests pass in
251.081 s. The explicit whole-root rest/half-turn identity check passes in
53.686 s. All six operating demonstrations, each replayed with exact bank
equality, pass in 764.842 s. All fifteen fork/sleeve interfaces retain .01 mm
free/.2 mm blocked play in native and world64 questions (9.948 s).
The original first-pair full-motion companion also passes all ten tests against
the adopted production frame: native 131.25 s, faceted 13.30 s, zero volume
epsilon. The change and both synced baseline specs pass strict validation.

These runs use the frozen framework `cache-standing-bound-bind` worktree at
`a500a99`. They prove only the adopted frame correction; the subsequently
integrated Follow law and the positioning-ball trial are separate work.
No moving geometry, carry/reset law, driver, upstream source or attribution
changes in this correction. Overall `simulate-the-curta` remains 12/23 tasks
complete, including its open full-assembly and viewer acceptance gates.

Final artifacts under `_build_checks/` (SHA-256):

| Artifact | Hash |
|---|---|
| `carry-bank-production-material-and-stroke-4cd6ec4.log` | `66263869f5abfbc212ebc9ef6c8785564a4b4684d7bfc42d2eac1a9e2a6a6603` |
| `carry-bank-production-root-reference-4cd6ec4.log` | `a117380abb06c884f18b4954be632aa0184e8392b5886d852717c963cfb8322d` |
| Six-demo exact replay log | `a00ff055ea6f243a72ed4fae358e7b55f5be09ca64a992f7839b4f2607893cbc` |
| All-station fork/sleeve capture log | `5d154d95b6cc287b5e5bb41999580cc72a6a19dea6ba90bd0ad94c3f16015cf2` |
| `carry-bank-production-first-pair-motion-exact-4cd6ec4.log` | `f2b2c6af8a3f4b4a727eef209cecf9ccdde4fe471aa1400a572a12470f241210` |
| `carry-bank-production-first-pair-motion-faceted-4cd6ec4.log` | `187463e2d2457822a7111c74bf5003af388bbeb7cc4867f4a21109c036894c90` |
