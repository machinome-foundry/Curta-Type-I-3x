# Remaining result-bank operating trial

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

The trial's eighth-input case is now running in
`result-bank-trial-eighth-operating.log`. The test optionally records full
stopped/relieved banks through `CURTA_RESULT_ACCEPTANCE_REPORT`; only that
new eighth invocation uses this capture, not the completed hundreds run.
An isolated export is also running in `result-bank-operating-export.log`.
No arithmetic or browser result is claimed yet for this bank trial.

Independent dense profile checks continue per station and kernel. Faceted
stations 2..10 have completed **23,556 admitted poses each**, zero positive
commons; native stations 2..5 have the same completed result. After the
interruption, process inspection found no native workers for 6..11 or faceted
worker for 11, and no logs for those unstarted checks. New native queues now
run 6/8/10 and 7/9/11, and the last faceted station 11 runs separately.
The live arithmetic and operating tests were left alone. No process is
restarted merely because it is quiet. These are finite samples, not a
continuous contact certificate. Default-root adoption remains gated on the
remaining geometry and actual operating acceptance, not the numeric law alone.
