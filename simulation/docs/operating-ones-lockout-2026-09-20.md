# Ones-lockout adoption in the operating assembly

Project starting point `2a9aa84`; framework `e63700e`; viewer `e82b521`.
This increment serves tasks 6.2/6.3. It adds the measured fixed-height ones
restraint to the actual operating crank, not to a substitute driver or a
flattened demonstration tree. It does not complete the whole interlock matrix.

## Red and implementation

The new full-root test prepares selector 1 at 3, turns the actual crank to
90 then 120 degrees, and withdraws that selector to zero. The shaft retains
189.6 degrees. On the unchanged operating root, both subsequent requests to
150 and 840 incorrectly completed: two red subtests, 246.093 s.

`OperatingCurta.main_drive.crank.turn` now intersects its original pawl bound
with the measured closing-surface bound. It reads the actual co-rotating bell
and retained ones shaft across their existing assembly boundaries. The common
profile law moved unchanged from the diagnostic into `locking_laws.py`; the
diagnostic still consumes exactly that law. No driver, tree, default, print
geometry, phase or manufacturing fit was changed.

The first full-root rerun passes both formerly red cases in 263.174 s, stopping
at 125.22323837227304 degrees and holding the shaft. The expanded regression
adds replay, reverse relief, retry, native/published-mesh first-contact and
overtravel controls, and preservation of the original reverse-pawl stop.
The installed stop has zero native and zero published-mesh common volume;
.2-degree overtravel gives 0.0020016976789634286 mm³ native and
0.00251322971894858 mm³ faceted contact. Both long/short replays, relief and
retry passed before a final test-record assertion used the clocked field
`side` instead of the running Stop's documented `bound` field. That test typo
is corrected. The complete rerun passes in **836.661 s**, including the
original reverse-pawl stop after the contact/relief/retry sequence. The
historical ancestor diagnostic also passes with the stricter parent bound.
Two unchanged numerical profile/tooth-passage checks pass in **42.693 s**
after the common-law extraction. The four-turn page-53 calibration regression
also passes on the complete operating root, as does subtraction through both
full register banks followed by addition back to zero. Partial-input replay
and reversing-counter history remain in progress at this checkpoint,
not claimed green prematurely.

The historical `AncestorLockoutCurta` diagnostic still declares its original
125.32-degree local bound. Its parent now supplies the stricter certified
125.223238-degree stop, so its regression correctly expects the intersection.
The old measurement and old export evidence are not rewritten.

## Complete export and real pointer

The full operating export builds against framework main. Browser comparison
against the pre-change operating document proves identical 608 descendant
paths, 25 controls, program coordinate declarations and document version 7.
All 155 distinct referenced model assets exist and are nonempty. The document
contains 24 driver inputs; the extra control is the crank instruction button.

The public hosted request 120→840 stops at **125.22323837227304°**, exact
snapshot replay passes, and .05-degree relief completes and holds at idle.
A real horizontal pointer drag on the crank's selected turn handle stops at
**125.22323837279964°**, retaining the shaft at 189.6°. No page errors occur.
The inspected close-up shows the complete bell's closing edge alongside the
ones upper stack, and the visible control reports blocked at 125.2232°.
This screenshot is wiring/pose evidence, not a substitute for Boolean contact
checks or a whole-machine clearance certificate.

Content hashes:

- Export: `cd39f339b89a803da515f1dcd3e7ff1d2af9d09e84ee981b8ae60c3d85a4b66c`.
- Pre-change document: `a15c92eb9dc0b8e6e2c8bfa820a101a9a1ef379d06f86b1802d2d0765c411586`.
- Viewer bundle: `8acaf5989e5fa99bb5f3314c2080016603893ca8e665569a4d707ff24f8de751`.

Reproduce with the workspace environment, from this project's root:

```sh
machinome export simulation.running:OperatingCurta --no-widget -o _build_operating_lockout
python -m simulation.tools.ancestor_lockout_browser \
  --build _build_operating_lockout --baseline _build/operating_curta/viewer.json \
  --stop 125.22323837227304 --target 840
python -m simulation.tools.periodic_lockout_browser \
  --build _build_operating_lockout --operating
```

The baseline is the preserved pre-adoption build, not a document rebuilt after
the change. CAD uses single-threaded BLAS/OMP and the 8 GiB virtual-memory cap;
the separate browser process must not inherit that cap. Reports and images
are ignored generated evidence under `_build_operating_lockout/`.

The first broader full-root browser run passed the 0th, 1st and 2nd later-turn
cases, then its **setup** request from zero to 1200° was refused by the
existing pawl's 1,000-surfaces-per-law-per-tick guard (1,176 surfaces). That
guard is unchanged, and this is not a first-contact failure. Later-case setup
now reaches complete turns one at a time before the partial withdrawal; the
challenged 720-degree instantaneous request is unchanged. The full-root legal
three-turn controls use a six-second request at dt=.1, matching ordinary
operation, rather than demanding an arbitrarily large instantaneous tick.
The reduced diagnostic still tests immediate 1080-degree requests unchanged.
The complete-root matrix now passes **seven stops and four legal moves**.
Every case passes exact snapshot replay, .05-degree reverse relief, idle hold,
retry at the same boundary, and unchanged retained shaft. Stop coordinates are
125.22323837227304°, 485.2280105590762°, 845.2050994865567°,
1205.2280067446554°, 1565.2280067446554°, 120.38810729947272° and
129.82507171577254°. The legal cases all complete 1080°: selectors 0, 3 and 9
at zero lift end at shaft angles 4°, 652° and 1948°; selector 0 at 9 mm lift
ends at 2164°. No browser page errors occur. The final inspected screenshot
shows the complete assembly at 1080°, the raised crank at 9 mm, and the
unchanged control surface. It does not certify the unresolved rest overlaps.

## Scope kept open

The .1-degree free-side profile stand-off and original F18 fit retain their
existing seven-pose and 1,888-boundary-samples-per-kernel certification. There
is no new author-review geometry correction in this increment. The profile
represents measured geometry, not force/friction or continuous collision
dynamics, and the executor retains its finite sampling limitations.

Only the ones upper stack has this fixed axial seating. Higher result and
counter channels slide with their carry latches; copying this law onto them
without those measurements would assert an unproved restraint. Their action
orders, selector/lift/reverser restrictions, printed-loop deployment, final
pointer matrix and complete-machine geometry remain open. No task is marked
complete solely by this adoption checkpoint.
