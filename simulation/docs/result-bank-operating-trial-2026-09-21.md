# Remaining result-bank operating trial

**2026-09-22 follow-up:** the separately approved viewer cache repair now
passes this trial's four browser stop/relief/retry/replay cases. Both captured
eighth-station stopped/relieved bank pairs match Python exactly, all 213
coordinates. See [the resumption record](resumption-2026-09-22.md#viewer-blocker-retired--remaining-result-bank-trial)
and [saved browser report](evidence/result-bank-browser-acceptance-2026-09-22.json).
The mount failure below is historical. This trial is still not adopted and
its interrupted arithmetic/native acceptance is still outstanding.

Status: isolated candidate for tasks 6.2/6.3, not the manifest default and
not whole-bank acceptance. Production still has the proven result ones/tens
and pawl restraints; counter work has its separate isolated trial.

## Actual missing hundreds stop

The new production test uses only actual controls: set `digit_3` to 3,
turn to 160°, withdraw that selector to zero, then request 190°. The
prepared shaft is 149.6° and the complete upper/bell pair passes clearance
in both kernels before that last request. The unmodified operating model
then completes 190° instead of stopping, leaving **0.30868623164229286 mm³
native / 0.3235355698386036 mm³ faceted common**. The test fails the intended
`completed != blocked` assertion in **268.120 s**:
`_build_checks/result-bank-hundreds-operating-red.log`.

This proves a missing restraint on the named complete-print interface; it
is not a whole-machine interference inventory. The eighth-input test also
fails as intended in **317.047 s** (`result-bank-eighth-operating-red.log`):
set digit 8 to 3, turn to 260°, withdraw it, then request 290°. The prepared
shaft is 49.6° and the prepared upper/bell pair clears both kernels, but
the request completes through **0.3086862316418869 mm³ native /
0.3235354171748899 mm³ faceted common**. The last three result shafts have
no direct selector, so those cases cannot simply invent inputs 9..11.
They still need operating carry/action-order coverage.

## Coordinate law and full-tree fixture

`result_bank_closing_limit` intersects the nine remaining station limits,
keeping the already adopted ones/tens constraints separate. For station
`s`, the local crank angle is actual crank minus `20*(s-2)` and the local
shaft angle is actual shaft plus that offset. Every returned bound is
translated back to the actual physical crank coordinate before intersection.
It reads each actual retained shaft turn and upper travel, not a global
register value or calculator setting.

Axial normalization is also required. The source channels 3, 4, 5, 6 and 8
have a raised raw travel of **0 mm**; channels 2, 7, 9, 10 and 11 use **−4.2 mm**.
The candidate now converts actual travel to the tens-local height as
`actual - RESULT_RESTS[station-2] - 4.2`. It does not move the source print
or replace its existing carry relation.

The numeric test fails first on the missing function. Both tests then pass
in **1.421 s**, exercising all nine limiting stations at three upper heights,
mixed banks, later revolutions and incomplete coordinate-pair rejection.
A temporary wrong-sign offset mutation fails **19 assertions in 1.131 s**;
the source was not modified by that test patch. Logs are
`result-bank-law-{red,green,phase-mutation}.log`. These tests prove the
angular coordinate transformation and intersection, not geometric admissibility.
That initial test assumed common raw axial origins and was incomplete.
After the fixture finding below, the actual source rest positions produce
**11 failing assertions** in `result-bank-law-axial-rest-red.log` (1.123 s).
The corrected normalization passes **2/2 in 1.447 s** in
`result-bank-law-axial-rest-green.log`. The independent geometric admission
checks always used each source bench's physical carry position; their inputs
and profiles are unchanged by this correction.
With correct axial normalization retained, the repeated wrong-sign angular
mutation still fails **19 assertions in 1.245 s**
(`result-bank-law-axial-rest-phase-mutation.log`). Fourteen neighbouring
law/browser-validator/support tests also pass in **104.547 s**
(`result-bank-neighbour-numeric-regression.log`); that invocation preceded
the axial correction and is not its regression evidence.

`ResultBankOperatingTrial` installs the existing source-specific T07 candidate
upper prints at stations 3..11 and adds that combined lower crank bound.
It inherits all production controls and retained relations, keeps the original
assembly paths, and changes no counter channel. The bench's channel factory
is now shared explicitly with this trial; source print identity, pivot and
placement remain per station.

The fixture test fails first because the trial module does not exist
(`result-bank-operating-fixture-import-red.log`). Its first implemented run
fails five station comparisons in **92.591 s**
(`result-bank-operating-fixture-first.log`): approximately **174.879800 mm³**
of differing material at each of stations 3, 4, 5, 6 and 8. The initial-bank
and export-identity checks pass. The fixture had inverted every raw travel
using the tens −4.2 mm rest, putting these five independent bench references
4.2 mm too low. This also exposed the same missing axial conversion in the
candidate bound, now pinned red and corrected above. No source fit changed.

The corrected fixture checks the source bench's own zero-carry travel against
each recorded rest before inverting the actual operating travel. Its rerun
passes **2/2 in 97.778 s** (`result-bank-operating-fixture-axial-rest.log`). It compares every
complete upper against its measured source-specific bench in both native
difference directions and requires the entire initial bank to equal the
production bank. Export/channel identity checks pass alongside it. The first
trial hundreds short/long stop test now passes **1/1 in 1112.808 s**
(`result-bank-trial-hundreds-operating.log`). The 190° request stops at
**165.22323837279146°**, and the 880° request stops at
**165.22323837227304°**. Both have zero native/faceted common, positive
.2° overtravel common, a held shaft, exact snapshot replay and admitted
.05° relief followed by another stop. Its log SHA-256 is
`b221e689dcdf37fafc6951f92799aeae5c14fc663dda80b86c37ca420d5634b0`.

The trial's eighth-input case passes **1/1 in 1166.542 s** in
`result-bank-trial-eighth-operating.log`: 290° stops at
**265.22323837279146°**, and 980° stops at **265.22323837227304°**.
Both clear in both kernels, contact at .2° overtravel, retain the shaft,
replay exactly and admit .05° relief followed by another matching stop.
Its log SHA-256 is
`6186f95bd85246bb25e4def0b3784c90e4f6bec597bfae94ad95a49648b13d99`.
The test records full stopped/relieved banks through
`CURTA_RESULT_ACCEPTANCE_REPORT`; only this eighth invocation uses the capture,
not the completed hundreds run. The [saved Python banks](evidence/result-bank-eighth-python-acceptance-2026-09-21.json)
contain all 213 manifest coordinates in each of four states (SHA-256
`d1dbc4c056c13e9ed8a9ba0eb45bf9627055745340ad50b002aa690a6897f08e`).
They are not browser parity: mounting that trial still fails below.
The isolated export completes in `result-bank-operating-export.log`, retaining
213 coordinates, 24 inputs and 25 controls. Browser mounting fails as recorded
below. The ordinary page-53, subtraction/borrow-and-undo and successive-addition/
selective-clearing regressions are now running against this isolated class
(`result-bank-operating-trial-arithmetic.log`), without modifying the production
test class or root. No arithmetic or successful browser result is claimed yet.

Independent dense profile checks continue per station and kernel. Faceted
stations 2..11 have completed **23,556 admitted poses each**, zero positive
commons; native stations 2..7 and 9 have the same completed result. After the
interruption, process inspection found no native workers for 6..11 or faceted
worker for 11, and no logs for those unstarted checks. New native queues now
run 6/8/10 and 7/9/11. The last faceted station 11 has since completed;
its log SHA-256 is
`e18c6e46630b1ee74606296bcfd00fd003016e1cf6bb3aace82b436a419fbec9`.
Native 6 and 7 also complete and their queues advance to 8 and 9. Their log
hashes are `38fe038bbdb9709cbce66d66501b1170331c7dd086e11a22fb4293dbf78bb556`
and `dc05955f3c7230eee813fc0dd5f93c3d64c0324a60933cd48e766b18ad2a15c4`.
Native station 9 subsequently completes **23,556 poses, zero failures**,
log SHA-256 `d864266e4b520320753ba3038fb3e55b80927e99587d7afa2988dfd9ad8d4fd6`,
and that queue advances to station 11. Station 8 remains running with 10
behind it. A completed station 9 does not stand in for the unfinished 8.
The live arithmetic and operating tests were left alone. No process is
restarted merely because it is quiet. These are finite samples, not a
continuous contact certificate. Default-root adoption remains gated on the
remaining geometry and actual operating acceptance, not the numeric law alone.

## Browser mount failure: expression-pool lifetime

The new `tools/result_bank_operating_browser.py` uses the same public mount,
snapshot, restore and running-request surface as the accepted counter probe.
It prepares stations 3 and 8 independently and requires both short/long
stops, replay, relief/retry and complete coordinate banks. Optional Python
comparison names its exact station/request scope; it cannot claim station-3
parity from a station-8-only report. The four report-validation tests first
fail on the absent module, then pass **4/4 in .001 s**. These are validator
tests, not browser acceptance.
The combined result/counter report-validator regression passes **8/8 in
.004 s** (`result-counter-browser-validators.log`). Playwright's documented
promise-awaiting evaluation and finite screenshot timeout informed the
probe; they do not alter the running program or its contact semantics.

The unmodified fresh bundle fails during `MachinomeViewer.mount`, before
any operating request or screenshot, with `Cannot read properties of
undefined (reading 'kind')` in expression-shape classification. The partial
report remains `validation: pending`, with the exception recorded and zero
cases; it is not accepted. The document/bundle identities and original log
hashes are preserved in the [mount evidence](evidence/result-bank-browser-mount-2026-09-21.json).
Reproduce against the existing isolated export (without the geometry tests'
virtual-memory limit) using the workspace Python:

```text
python -m simulation.tools.result_bank_operating_browser --build _build_result_bank_trial
```

Inspection of the delivered bundle shows a 50,000-node expression-pool
reset threshold. A bounded diagnostic loads that bundle with an in-memory
assertion around the classifier's expression-root/binding-root acquisition.
It observes generation **1 → 2** while acquiring the **30,159 bindings**:
the expression root was obtained in generation 1, but classification would
continue in generation 2. Its numeric ID 7742 happens to exist in the new
pool; index existence therefore does not establish reference validity.
The diagnostic stops at that generation change and does not alter the
cache limit, any expression, or the saved original failure report. No
viewer/framework file was edited, and no instrumented execution is used
as acceptance evidence.

This is a separate viewer-owned lifetime finding exposed by the real Curta
bank, not evidence that reducing geometry or dropping restraints is valid.
The pilot authorized preparation of a separately governed viewer proposal,
`keep-expression-references-valid`. Its planning artifacts and strict validation
are complete in the viewer repository; implementation still awaits approval.
Python operation and independent geometry checks can continue;
browser adoption cannot pass this failure. The earlier Python CPU profile
remains a distinct investigation, not a fix for this mount error.

## Geometry-worker interruption checkpoint

The later station-8 and station-11 native workers terminated before their
terminal summaries, at 22,455 and 5,439 admitted poses respectively. Their
process absence and terminal tool results were verified; the cause is not
known. These are incomplete runs, not passes. The
[termination evidence](evidence/geometry-worker-terminations-2026-09-21.json)
pins both logs alongside the counter workers interrupted at the same
checkpoint. Previously completed native stations 2..7 and 9 are unaffected.
A separate full-matrix retry queue now schedules result 8/10/11 after the
counter-tens retry, writing `result-station-N-profile-certified-native-retry-1.log`
without overwriting the old logs. Those retry queues subsequently terminate
again before completion, as recorded in the
[second interruption checkpoint](evidence/geometry-worker-terminations-second-2026-09-21.json).
The isolated arithmetic worker later also terminates with exit 143: page-53
calibration passed, subtraction/undo was unfinished, and the third case had
not started. No batch acceptance is claimed. At the final 19:39:40 UTC check,
no Curta test process remains live; long retries await clarification of the
repeated unexpected termination rather than overwriting or trusting partial logs.
