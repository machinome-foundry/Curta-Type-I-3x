# Actual standalone-page interaction evidence

## September 23: fitted-shoulder production continuation

All **25 currently declared controls** now have passing independent physical
gestures on the same unmodified fitted-shoulder export and viewer bundle.
The [consolidated evidence index](evidence/standalone-current-controls-2026-09-23.json)
matches the manifest's exact control-name set and all 24 driver names; each
raw report passes the shared release/terminal/independence validator. All
reports use the same manifest, index and bundle hashes. This is complete
baseline pointer reachability for the currently implemented controls, **not**
completion of task 6.5: the required clearing-loop deployment is still absent,
and full strokes and all wrong-order/mid-cycle sequences remain separate gates.

The final refresh adds independent crank lift (2.0000 mm), carriage lift
(1.0000 mm), partial crank (1.0000 degree), and the actual part-button's full
revolution (exactly 360.0000 degrees). Each completes after observed release,
leaves other visible inputs unchanged, has no page errors and exits zero.
All four complete-assembly screenshots are inspected. The full button reaches
its terminal readouts at 177.443 s and finishes capture at 191.073 s, with the
normal timestep and two simulated seconds; this is not real-time performance.
The index records exact report/image hashes, physical points and per-stage
timings for all 25 cases. No hidden run handle or host motion request is used.

The subsequent marker continuation on project `9f0f9c1` uses the same pinned
export below. All ten actual marker controls pass independent, serial
standalone gestures. Each starts from an untouched page, requires the actual
part hover, receives a 60-pixel leftward drag and observes release before
terminal readout checks. All other 23 input readouts remain unchanged and
there are no page errors. Every process exits zero; all ten screenshots are
inspected and show the complete assembly. Some marker rows are below the
viewport: the report captures their actual DOM readouts, not visible pixels
of every numeric row. This is not full-bank or full-track-travel acceptance.

| Marker | Final readout (degrees) | Terminal outcome |
| --- | ---: | --- |
| 1 | -0.0760 | blocked after -0.076 deg |
| 2 | -0.2260 | blocked after -0.226 deg |
| 3 | -0.1490 | blocked after -0.149 deg |
| 4 | -0.1490 | blocked after -0.149 deg |
| 5 | -1.0000 | completed |
| 6 | 1.0000 | completed |
| 7 | 0.1390 | blocked after 0.139 deg |
| 8 | 0.3160 | blocked after 0.316 deg |
| 9 | 0.3460 | blocked after 0.346 deg |
| 10 | 0.2860 | blocked after 0.286 deg |

[The evidence record](evidence/standalone-current-controls-2026-09-23.json) pins every
report and inspected image, physical gesture point, exact asset hashes and
timings (terminal checks 8.701–14.506 s, captures 23.496–27.346 s). All ten
reports pass the shared validator and use byte-identical export assets. The
initial marker-1 attempt hit marker 5 instead and was rejected before any
gesture; its failed report is preserved and excluded from acceptance.

The reversing knob also passes on the same export. An ordinary empty-canvas
camera drag from (1299.3, 150) by (-300, 0) first exposes its actual part;
the harness checks that this camera action changes no input. A real downward
60-pixel knob drag at (867, 577) then changes `reverser_height` from 3.9075
to 1.9075 mm and completes after observed release, with unchanged other
23 readouts and no page errors. Terminal / capture times are 22.312 / 37.328 s;
exit zero is observed and the full-assembly screenshot is inspected. Report
`operating-shoulder-standalone-reverser-visible-9f0f9c1.json` SHA-256
`45a40bbf93a943b028080e173887d32b6c0e783c76f53a84ec6b041f39361689`;
PNG `a24729cd7fa4c34a08402a45db74edf86c2c336f3a169a425ea8649faa1b5b42`.
This proves independent partial knob travel, not the complete throw or a
mid-cycle locking contract. The first post-orbit guess (736, 500) did not
hit the knob and was rejected before any gesture. That failed report remains
`operating-shoulder-standalone-reverser-orbit-9f0f9c1.json`, SHA-256
`e994a5bec6bd2cbbfcf5126f08ecb1162bae30e306d11a13fee68b0b84c43fa2`.

The unmodified `_build_checks/operating-shoulder-82bf530-a92541d/` export
contains the accepted counter-shoulder geometry at project `4256778`, framework
`82bf530` and viewer `a92541d`. Its manifest SHA-256 is
`0b8f70d9c276f4517df28c629734f020ea266ac5d7051b7714acf78483474a79`,
bundle `feeaed32febb1ede3b267e9f47a6a0fd0a6b39bc149453af338011489b68ff86`
and index `16238dda75b0b88224bd1bcaf0c9dfd77a6f43d75652b2972f4af5ed00111bb2`.
The 214-coordinate program identity remains
`b81b2ce7af6556c12a68829fa3444d1dc6efc7c110d2cd88aff57fff0b9700f4`.
These fresh standalone cases use the normal timestep and serial browsers.

An actual seated-carriage shift gesture passes: hover at (800, 480), selection
of the real `shift carriage` handle at (757.484375, 432.4375), then an
80-pixel leftward drag and observed release. The carriage reaches 0.1800 degrees
and the visible outcome is `blocked after 0.18 deg`. Its elevation remains
0.0000 and every other visible input is unchanged. No page error occurs;
the process exits zero. Terminal readouts are verified at 16.182 s and capture
finishes at 29.584 s. The inspected screenshot shows the complete assembly,
selected physical handles and matching blocked outcome. Report
`operating-shoulder-standalone-seated-shift-left-4256778.json` SHA-256
`8a3e15e38349b73d5c5f91e77364da84a87d87805eca36eeb491e831f2f092dd`;
PNG `6ebf233e823cb9fe95f54ab71862f6b1dbdcafdc5c35b6eaa832a85b4fda5469`.

The preceding rightward drag reached `blocked after 0 deg` with unchanged
inputs. It correctly fails the harness's admitted-movement gate and is not
counted as passing movement coverage. Its failed report and inspected image
are preserved: `operating-shoulder-standalone-seated-shift-4256778.json`,
SHA-256 `1679017427bddbd618983eb7e53ba3d3e71275302b6578d36fb9edbd980a55b5`.
Neither gesture lifts the carriage or uses a host motion request. This remains
four-decimal visible-state evidence, not full-bank or hidden-command inspection.

Independent selector cases 2–5 also pass on this export. Each starts from the
untouched page, finds its actual knob by nearest-hit hover, receives a 60-pixel
downward drag, observes release and reaches 2.0000 with `completed`. All other
23 visible inputs are unchanged and no page error occurs. Each process exits
zero and each screenshot is inspected: complete assembly, matching selector
and readout, and a completed outcome. Timings below are seconds from launch.

| Selector | Actual hover/drag start | Terminal readouts | Screenshot complete |
| --- | --- | ---: | ---: |
| 2 | (800, 635) | 14.100 | 28.169 |
| 3 | (750, 635) | 15.680 | 27.869 |
| 4 | (698, 635) | 14.124 | 27.638 |
| 5 | (653, 635) | 15.704 | 29.846 |

Reports are `_build_checks/operating-shoulder-standalone-digitN-4256778.json`
and their sibling `.png` images. SHA-256, report then image:

- 2: `3023588565e2dd727e1806d74555508fc2665fd6effc8985cc2e47a8271d5573`;
  `b07308ce947f938faef330d6b7483b0203169c55bd3e63f839355d80c2a454d3`.
- 3: `9dad0359eea621fe821c0bce7b6f131c1774109f9d43b0996fae8dfce234d4df`;
  `b57585a169e9ca078ca25f96f2c2ec56eaa990e8c382e6a960f62b091dfa479f`.
- 4: `0c9f05300d12b44895ae1caadd2d2e0f8701233efcfdb8214b19c66a6bef352d`;
  `a1666f59999e57734ce0ea10695747928c04c0e5444d519f456156bb5aeca7e2`.
- 5: `40e4778d4a09112a4f0675d4dab5ad4eaed83192bf02911956dd50860c710ba8`;
  `87fd7570d9cff841006cfda8df6f34c9d5622d7ee9a0b9d602d1bb8019d108f8`.

Selector 6 passes from its actual visible knob at (622, 598), with the same
60-pixel downward drag: 1.0000, completed, all other readouts unchanged, no
page errors, inspected screenshot and exit zero. Terminal verification is at
11.838 s and capture at 25.845 s. The report
`operating-shoulder-standalone-digit6-visible-4256778.json` hashes to
`38a0d0079dc40380d6919540a94e48ce3be378f51283dba49655fe530cf59b0c`,
its PNG to `6be76621e0e938103f1c9ade2139943fd7de7a5152852b5b609c4946582fa58f`.
The earlier point (620, 620) hit no control; that failed attempt performs no
gesture and remains `operating-shoulder-standalone-digit6-4256778.json`,
SHA-256 `90d42fdbe517685c500d70c7ef226d918e6796c900bc6f38b3cc4b1dd9570166`.

Selectors 7 and 8 pass at their visible edge knobs, respectively (601, 577)
and (599, 547). Each 60-pixel downward drag reaches 2.0000, completed, with
observed release, unchanged other visible inputs, no page errors and process
exit zero. Both complete-assembly screenshots are inspected. Their terminal /
capture times are 13.600 / 27.460 s and 14.914 / 28.805 s. Reports follow the
`digitN-4256778` pattern above; SHA-256, report then image:

- 7: `b2e45fa7e9241a5a44d2d5cb6c08504a18f3f19655e8cd10ae72d968b9ecd562`;
  `739b34b7ae845f3b48809e95a84e76fae2b4aa8c7d58f1483a0ff888e5bc4b12`.
- 8: `94d55a9565c19fb676ccfd02225e325989f5b96d88bb4c80af106fdae6aec62d`;
  `dcdc52aae9c7328a703ba5365e993f7895042534564a436fbb5233ba9c1e9ed8`.

The first selector is refreshed on this same export, completing standalone
independent-motion coverage for all eight selectors on the pinned current
geometry and bundle. A real drag at (842.025, 620) reaches 1.0000, completed,
with the same release/independence/error checks, inspected screenshot and
process exit zero. Terminal / capture times are 9.658 / 24.283 s. Report
`operating-shoulder-standalone-digit1-4256778.json` SHA-256
`44a957212ccfdcc5bd1a42d9116766682860bf7497241644320fc54983bad1c8`;
PNG `c57203427fd0efff0c53d41a8a3a26969ca6a719fbab9471d76aa7d239d0fa64`.
This does not prove every selector's full stroke or mid-cycle mechanical
restraint, nor does it complete the remaining standalone control matrix.

The physical clearing ring at (830, 360) also accepts an 80-pixel rightward
drag while seated: 1.0000 degree, completed, unchanged other inputs, observed
release and no page error. The complete-assembly screenshot is inspected and
the process exits zero (terminal 10.516 s; capture 23.753 s). This request
stays inside the measured seated play and **does not reach the restraint**.
Report `operating-shoulder-standalone-seated-clearing-4256778.json` SHA-256
`1cc38e2d5ffa4a49ab66acf65ed7625a04c979ea75f952950fc629e840796e01`;
PNG `9a4eeb7cb65c1a22b1fce0f31fe6b536744e03d5a4d3df2ab55e796f5f14e973`.
The ten passing current-export reports above are revalidated together and
their manifest/index/bundle hash triples are identical. This includes eight
distinct selectors and two seated controls, not ten independent mechanisms
cleared of all contact or action-order obligations.

The independent 400-pixel rightward drag from the same physical clearing
ring reaches the seated restraint: final visible angle 1.4372 degrees,
`blocked after 0.437226 deg`, carriage elevation 0.0000 and all other visible
inputs unchanged. The outcome describes the final pointer command's admitted
travel, not the total angle reached by the gesture's sequence of commands.
Observed release, no page errors, inspected complete-assembly screenshot and
exit zero pass; terminal / capture times are 13.472 / 26.948 s. Report
`operating-shoulder-standalone-seated-clearing-stop-4256778.json` SHA-256
`d2ad0b622e75a619b5baf97cdba737f06dde4e1ee5913db8ea0f7bf309428a5f`;
PNG `d29888ffc2a80ce3a2a7304341af897e9404786b691dc83c3b0de10e32b1d06e`.
The complete-bank hosted stop at 1.437226368040361 degrees remains separate
evidence; this standalone page only exposes four-decimal input readouts.

The existing standalone/hosted report validators also pass all 14 tests in
1.033 s on this project head. This includes rejection of unretired commands,
missing release, unrelated movement and no-op attempts; it is harness
validation, not additional physical-control coverage.

## September 23: current retained-ball export

The fresh `_build_checks/operating-prefix-23857e9-572648f/` export pairs
framework `23857e9` with viewer runtime `572648f` (later viewer `08d70fb`
adds rejected-experiment history only). It has the production 214-coordinate
program `b81b2ce7af6556c12a68829fa3444d1dc6efc7c110d2cd88aff57fff0b9700f4`.
Its manifest and index are byte-identical to the earlier radial-ball export;
only the separately verified viewer bundle changes. SHA-256:

- Manifest: `bab5b1248bf8f100b764bf37bfd00065770df876bb83ec191b44549a9727569b`.
- Index: `16238dda75b0b88224bd1bcaf0c9dfd77a6f43d75652b2972f4af5ed00111bb2`.
- Bundle: `0d602f50532ffe3c906b0bea285352cf60c5165da9b77d818d948f75f5e113df`.

On the unmodified auto-mounted page, an actual first-selector drag at
(842.025, 620) reaches digit 2, reports completed after observed release,
leaves the other 23 visible input readouts unchanged and produces no page
error. Process exit zero is observed. The screenshot is inspected: complete
assembly, changed selector and matching visible 2.0000 readout. This is not
the full standalone control matrix or sub-readout bank parity. Report
`operating-prefix-standalone-selector1-262378b.json` SHA-256
`56862d315d3ade178dd671d7a09e5ae37544c3f7344aecc5ea21f51f652e6ffd`;
image SHA-256 `a9adee9dbe265769cb2e0957b47dd122e66cd2c6d943a8e87d483512fc3af1b0`.

Three further current-export attempts reached their required visible terminal
states without page errors, but **exited one on screenshot timeout**. Their
reports remain pending, not passing visual acceptance:

- `operating-prefix-standalone-revolution-55846d3.json`: actual crank button,
  completed 360.0000 degrees, other 23 input readouts unchanged; SHA-256
  `2b35d0c98fdf8574d6046f9eda32172e4b488dce4a71fe33c1d96ed51306702e`.
- `operating-prefix-standalone-lift-carriage-94f0ce2.json`: actual labelled
  carriage-lift handle, completed 2.0000 mm, other readouts unchanged; SHA-256
  `d40d3481894972fd8789b43835111bc6e2f663b9e74abf3d742e7937be814616`.
- `operating-prefix-standalone-partial-timed-94f0ce2.json`: actual partial-turn
  handle, completed 1.0000 degree, other readouts unchanged; SHA-256
  `5826dd134ff928e38e2f09b511699140387f568c4b5c3fb55f3fa80b8fed4a1b`.

The timed partial case reached page-ready at 6.342 s, observed pointer release
at 22.427 s, verified terminal readouts at 85.385 s, then exhausted the
180-second screenshot deadline (and a separate fallback). These runs overlapped
other SwiftShader browsers. Contention is a hypothesis, not an established
viewer defect: the hosted non-crank screenshot subsequently succeeded and a
read-only idle-render comparison showed no reliable improvement from suppressing
animation frames. Serial same-bundle reproduction is the next gate; no timestep,
render behavior or visual acceptance requirement has been changed.

The serial same-bundle reruns now pass for partial crank and carriage lift,
including successful screenshot capture, inspected pixels and observed exit zero:

- Partial crank: actual labelled handle at (805.875, 254.25), completed
  1.0000 degree; terminal readouts at 25.626 s and screenshot at 72.831 s.
  Report `operating-prefix-standalone-partial-serial-e8d3612.json`, SHA-256
  `5dff547a5ee8b3981ba2ddd68931365b7f739839acf1a6f3bdb8e4aa011ac307`;
  PNG SHA-256 `19af63abf0560fd9b9ba81eb612ef42f6ee6671cc8f26ad6cf4ae33f4467c83c`.
- Carriage lift: actual labelled handle, completed 3.0000 mm; terminal
  readouts at 47.974 s and screenshot at 95.494 s. Report
  `operating-prefix-standalone-carriage-serial-e8d3612.json`, SHA-256
  `1837ec8d7f67f44838c6929140fcf23377ae930b5e26ce8849134499b540bce9`;
  PNG SHA-256 `f07f6047507e803ce625422600cd2a19377cc01f977e30654a20506c07a9e4db`.

Both retain all other visible input readouts and have no page errors. The
images show the complete machine, actual selected handles, matching values
and completed outcomes. Gesture quantization can produce a different admitted
amount under different load (the earlier carriage attempt reached 2 mm);
these probes assert independent admitted movement, not a fixed mouse-to-millimetre
delta. No viewer repair was needed for these serial captures. This supports
contention as the earlier capture explanation without proving it uniquely.

The serial full-revolution retry also passes on that same pinned export:
actual button press/release, completed exactly 360.0000 degrees, unchanged
other 23 visible readouts and no page errors. Terminal readouts are verified
at 201.573 s and screenshot capture finishes at 251.570 s; exit zero is
observed. The inspected image shows the complete machine and matching
360.0000/completed UI. This is not a real-time result. Report
`operating-prefix-standalone-revolution-serial-e8d3612.json`, SHA-256
`7dc22a32af313c30d971418d5b016a593abd3beb19b318e3ab0b1c2585f974cc`;
PNG SHA-256 `e9c787f4bc2f5f9d917e66ea2b6b7d8a4963a4a5fd3203bfa03b031d8c11b2a8`.

`tools/operating_standalone_probe.py` serves the unmodified exported index,
manifest, bundle and contained model assets. It never remounts the viewer,
obtains a hidden run handle, modifies the page implementation, or submits
host movement requests. A hover-only search requires the actual nearest-hit
canvas title to name the intended part control. For overlapping freedoms,
the gesture uses the viewer's real labelled handle. Pointer release is
observed, then the visible outcome is awaited and readouts are recorded.

The ordinary timestep is unchanged. The page exposes 24 root input readouts
and one instruction row, but its auto-mount does not expose the full run bank.
Readouts have four decimal places: this gate does not prove sub-readout
independence, empty hidden command state or 213-coordinate parity. The
[hosted terminal tests](pointer-terminal-acceptance-2026-09-22.md) are separate
evidence for those stronger state checks. Neither declaration count nor a
hover hit alone is accepted as successful movement.

The report helper first fails red for the missing module, then its three tests
pass. They reject missing hover/release/outcome, no movement, missing inputs,
changed other readouts and page errors. The logs are
`_build_checks/standalone-report-{red,green}-e5636f8.log`.

## First production case

The actual default export `_build_counter_bank_production_bound_7107b1c`
passes the crank-lift drag with observed process exit zero. The canvas title
names `lift crank`, `one revolution` and `turn crank`; the distinct lift
handle is dragged upward. Crank elevation reaches 3.0000 mm, the UI outcome
is completed, and all other visible input values are unchanged. No page
error occurs. The final screenshot is inspected. This is one physical control,
not completion of the full standalone matrix.

Report `_build_checks/standalone-crank-lift-e5636f8.json` SHA-256:
`7e9f04a4aab11186f725c4db8031ddb0a0ae0078e802ca1bd6f4ed0f9fa509a5`.
The report pins the original index, manifest, bundle, hover attempts and exact
screen coordinates. Its bundle is `8a03c3a3...`, manifest `03099125...`, and
program `3e1d5051...`; these are the existing production export, not a newly
built viewer candidate. Other controls remain to be tested.

## Selector and next controls

The first coarse hover search misses selector 1 and exits one. Its untouched
pending report/image remain `standalone-selector-one-e5636f8` under
`_build_checks/`. A denser search over the visible selector band finds the
actual `set digit 1` hit at (842.025, 620). A 60-pixel downward drag passes:
digit 1 reads 4.0000, its outcome is completed, other visible inputs remain
unchanged and no page error occurs. The screenshot is inspected and the
process exits zero. Report `standalone-selector-one-dense-7a620d9.json` has
SHA-256 `76b66ec38efbc8442d4c85f6cc56efa6ac0de1abddb3dac39f92685c716d525a`.
No control proxy or hidden-part shortcut was added to find it.

The diagnostic now also supports an ordinary empty-canvas orbit gesture
(asserting no input changed), and physical button presses. A full-revolution
report may require an exact 360.0000-degree visible delta; a new red-first
test rejects 359.9999, then all four report tests pass. The button case is
running with an explicit 600-second observation deadline because normal
default-timestep execution is still slow. That deadline does not change
the simulated timestep or instruction duration. It is not yet a passing case.

The physical one-revolution click subsequently passes with observed exit zero.
The actual crank-bearing part at (842.025, 200) receives a press/release,
without a drag or an instruction-panel click. The instruction outcome is
completed, crank rotation reads exactly 360.0000 degrees, other visible input
readouts remain unchanged, and no page error occurs. The screenshot is
inspected. Report `standalone-crank-revolution-7a620d9.json` has SHA-256
`60ade952592bdd867e5f0fc6a4596d0fe43353cc45a665987138d0eed35d87a8`.
This proves the click reaches its specified visible endpoint at the default
timestep, not that the two simulated seconds execute in two wall-clock seconds.

The distinct partial-turn handle also passes on the same unchanged production
export. The actual labelled handle at (805.875, 254.25) receives a 60-pixel
rightward drag; crank rotation reads 1.0000 degree with a completed outcome.
All other visible input readouts are unchanged, no page error occurs, the
process exits zero and its screenshot is inspected. This is a partial turn,
not another full-turn button action. Report
`_build_checks/standalone-partial-crank-3fefd59.json` has SHA-256
`22816a000fb8f0ea0adfd929484d5c16181025540800979437787faf51b4fa02`.
Resume/wrong-order cases and the remaining standalone controls are still open.

## Fresh paired standing-cache export

Export `_build_operating_standing_cache_884b01e` uses framework `a500a99` and
viewer runtime `5149fe1` (later evidence-only `c5541f1` changes no bundle).
Its program is exactly equal to the prior production export, identity
`3e1d505123b75832f6e1b4353d7e9d7f5c5856375bcb67454ca15b602f140c20`,
with 213 coordinates. Manifest SHA-256 is
`001469d01ad5113b5620db782be3ca26b8f3280bb8751d168ef9888639811495`;
bundle SHA-256 is
`0d16382708d1672904572bf8f20277c5af60ed0ba8befc1c6cd53723423fdf84`.
The rejected ball-orbit candidate is not included.

A fresh physical partial-crank drag passes: 2.0000 degrees, completed,
unchanged other visible inputs, no page error and observed process exit zero.
The actual screenshot is inspected. Report
`_build_checks/standing-cache-standalone-partial-range-884b01e.json` SHA-256:
`261dec8087ea40542c38def6a7c08a1480ba0df9d479b44cba8ecbffead5be89`.

Two preceding failed harness attempts remain intact: one confused the later
labelled-handle location with the part's initial hover point; the next reached
2 degrees but incorrectly demanded the previous run's timing-specific 1-degree
quantum. A physical partial drag does not promise a fixed delta for identical
screen displacement at different runtime speeds. The diagnostic now explicitly
requires a finite positive partial turn below 360 degrees, preserving the
separate full-revolution button's exact 360-degree requirement. The added test
fails red before implementation, then all five report tests pass; negative,
zero, full-turn, beyond-full-turn and nonfinite values are rejected. Logs are
`_build_checks/standalone-partial-range-{red,green}-884b01e.log`.
