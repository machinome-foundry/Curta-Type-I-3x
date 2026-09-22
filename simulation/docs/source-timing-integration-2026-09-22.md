# Carry timing: integrated prerequisites and project continuation

## Working authority and scope

The pilot directed autonomous, evidence-led correction and continuation, and
then answered “go” to the explicit request to rebase the framework cycle and
integrate both fixes. Routine local fixes, regression checks, reconciliation
and integration within this work do not need another approval question.
Preserve unrelated work. Do not infer permission to push, publish, contact
the author, change the machine's purpose or weaken its acceptance contracts.

Both separately owned source-timing cycles are archived and fast-forwarded
into their local `main` branches:

- Framework: `5d5ba18454837b6a0cab951f6ca117c12fb89a0b`, planning `4569c7e`,
  based on `b0fb36957ddb054463b2b4b3da7ac2689b4f4955`. The pilot authorized
  rebasing the two-commit cycle from e6a42c8 over the intervening documentation
  commit. Range-diff confirmed identical patches before the completion record
  was amended with renewed authority and validation. The unrelated untracked
  `docs/examples/v8-engine/` directory was preserved in place; no incoming
  change touches it.
- Viewer: `684c58338800ad300e0d2594cc8d17d61cb3a7f5`, planning `46fea1d`,
  based on `c8da56e77f7653a06b335459e7759c6b24152e69`. Its primary bundle was
  rebuilt after integration. The workspace environment loads both primary
  checkouts, and `machinome-viewer describe` reports API 24, documents 1–11.

Nothing was pushed or published. Existing exports and saved runs must not be
silently treated as corrected: re-export running models to v11, and use new
source-timing run identities. Clocked models retain their separate semantics.

## Framework regression and unchanged project reproduction

Post-rebase producer checks pass **790 tests and 797 subtests**, 58.91 s,
three warnings. The single skip is the opt-in real viewer capture, previously
run separately and passed on the identical paired source. Viewer completion
records contain its 1,456 TypeScript and 196 Python/browser passing tests.
Those are package checks, not complete Curta physical acceptance.

On the integrated primary framework, the unchanged project command
`python -m unittest simulation.test_result_carry_graph_repro -v` passes all
**four tests in 87.462 s**. This retains the six-station control, newly failing
seven-station case and both complete-result-bank cases, constrained and
unconstrained. The unchanged bulk request reaches crank 180°, ones 724°,
tens 704° and first lever 0 mm. No law, oracle, bank or contact restraint was
removed, and the request was not split to pass.

Project source at the start of this check is
`885267751eb4870d8a3ded51cce96aa471eca34f`. The author's untracked assembly
video and `screenshots/reverser_inspection.png` remain untouched.

## Recovered terminal results from the earlier continuation

The old checkpoint described two workers as pending. Their logs now contain
terminal summaries; neither is still running:

- Native result station 8: **23,556 admitted poses, zero failures**, including
  all configured knots, carry heights 0/.5/1 and six-degree base shaft grid.
  Profile SHA-256 is
  `1cf2bed3b1be41ba66bccc2eb788fb24ddc5c21698853478e8d0f02813e10529`.
  Log `_build_checks/result-station-8-profile-native-2026-09-22.log`, SHA-256
  `6d0508712111ad3a929d690c6899bd925e954491b54cc80ece4fd1c5efca5c44`.
- Unadopted **ResultBankOperatingTrial** arithmetic: **3 tests passed in
  8,209.898 s** (page-53 calibration, subtraction/undo, successive additions
  and clearing). This ran against the earlier framework e6a42c8, not the
  integrated correction. Log
  `_build_checks/result-bank-arithmetic-resumed-2026-09-22.log`, SHA-256
  `239efb7dad6264efdbc43ebc40fcefb46658089bde6c471560b661184322eb9b`.

These three arithmetic passes do **not** belong to the collar trial. That
trial's final exact log still reports **2 passed, 2 failed**. Neither result
adopts a trial or completes the whole-machine inventory. Native result
stations 10/11, wider counter acceptance, clearing-loop contact and final
operating matrices remain open. OpenSpec stays at **12/23 tasks complete**.

## Actual-machine continuation

The unchanged seven-request `simulation.tools.higher_counter_wrong_order`
diagnostic completes on the actual **213-coordinate OperatingCurta**. The
formerly blocked 90°→180° request completes with result ones 724° and tens
704°. Subsequent 190°, lever withdrawal and 200° requests also complete.
All seven rows retain 213 coordinates and report zero complete counter-tens
upper/bell common on both native and faceted kernels. Its log is
`_build_checks/higher-counter-source-timing-integrated-2026-09-22.jsonl`,
SHA-256 `a77e19c55fd3a25be1e235ea3574878331cba7eeed5400d1e4304dd7bf67b9ae`.

This is a carry-correction result, **not** evidence of a counter restraint.
Counter tens stays at its indexed 114° throughout: the original combination
of 9 mm crank lift and reversed counter position engages one tooth on counter
ones and zero on the higher inputs. That is independently pinned by
`test_reverser_modes.test_all_four_working_combinations`. The earlier trace
never actually prepared the intended partial higher-counter tooth passage.

The diagnostic keeps that default sequence unchanged and adds a separate
`--partial-input` sequence: at zero crank lift, lever −3 mm engages the
measured single-tooth row on all counter inputs; crank 180° then 190° enters
the tens tooth's 184.75°..196° window. Moving the lever to +3.9075 mm withdraws
that higher input before requesting 200°. No model declaration or retained
coordinate is assigned. The expected pre-withdrawal shaft is independently
114 + (190 − 184.75) × 72 / 11.25 = **147.6°**.

The new trace test fails first on the absent sequence, then passes alongside
the three unchanged trace tests and three engagement-mode tests: **7/7 in
.001 s**. These lightweight tests prove diagnostic request routing and
existing engagement classification, not actual geometry or a missing stop.
The real partial-input trace completes and confirms the preparation: at 190°
the shaft is **147.6°**, and stays there after upward withdrawal. Both complete
upper/bell kernels clear those poses. The default root then wrongly completes
200° with **.3222787564319185 mm³ native / .33989275719740286 mm³ faceted common**.
Its log is `_build_checks/higher-counter-partial-input-integrated-2026-09-22.jsonl`,
SHA-256 `84b0cc448e95bc763982155d05551a989e979e1e77009a611b558e46373bb882`.
The [compact measurement record](evidence/counter-tens-partial-input-2026-09-22.json)
retains all five request outcomes and both complete-print readings.
This is now a real missing counter-tens restraint, not the earlier result
carry failure or a conclusion drawn from a disengaged input.

The new actual-root regression
`simulation.test_operating_counter_tens_lockout` fails **completed != blocked**
in **60.044 s**, after proving the prepared held shaft and clearance in both
kernels. Red log `_build_checks/counter-tens-operating-red-2026-09-22.log`,
SHA-256 `55c85db1efdda1f1248548fe39cca3756e21f69fe4d2c5afd2c7365933dc0035`.
This intentionally red production contract remains until a verified adoption.

The isolated `CounterTensOperatingTrial` now challenges the already measured
counter-owned T08 fit and `higher_counter_closing_limit` against this concrete
case. It replaces only the counter-tens upper print and adds its independent
crank bound, reading the actual bell, shaft and axial travel. Existing result,
pawl and carriage restraints remain inherited. This is a scoped behavioral
experiment ahead of full-profile acceptance, **not** permission to adopt the
candidate while its complete native matrix remains unfinished. The new trial
test first fails on the missing module. The implemented trial then passes
**2/2 tests in 540.543 s**, covering exact initial-bank/fixture equivalence,
short/long stops, both contact kernels, positive overtravel, exact replay,
reverse relief and retry. The 200° request stops at **194.7853836059494°**;
the 920° request stops at **194.78538360544917°**. Both hold the shaft at
147.6°, have zero native/faceted upper/bell common, and collide under a
deliberate .2° overtravel. Each replays its complete snapshot exactly,
admits .05° reverse relief and stops on retry. Log:
`_build_checks/counter-tens-operating-trial-2026-09-22.log`.
Its SHA-256 is
`cd5822ba93a74c1ed66e31039b87195db03ceb30bec7b5dbd93f1619e08523e0`.
The checked contact pair is the complete upper stack and bell. It does not
certify the six lower input gears against the drum during axial withdrawal,
nor the full path between sampled contact poses; those remain separate gates.

The focused diagnostic/mode/law/sampling/compiler regression passes **22/22
in 24.327 s**, retaining the 40 measured collision refusals, five false-stop
controls, all five ordinary input/carry flats, axial support sampling and
source-registration checks. Log
`_build_checks/counter-tens-source-timing-regression-2026-09-22.log`, SHA-256
`0385f33f94b722ca9504404ad918e454b9b7e1e71deb9ac9a55505fe19b1795e`.
This is not a replacement for the unfinished whole-print native matrix.

The trial's full-assembly rest snapshot also renders successfully through
the default OpenSCAD renderer and was inspected at
`_build_checks/counter-tens-trial-rest-2026-09-22.png`. Assembly placement is
coherent; OpenSCAD does not display the decal markings. The enclosed rest
view cannot prove a .01 mm fit or the retained stop, which are established
by the separate fixture/contact tests, not by the image.
The independent counter-tens bench was also rendered and inspected along
the Z axis at the measured held shaft 147.6°, crank 194.7853836059494° and
carry 0 (`_build_checks/counter-tens-trial-stop-axis-2026-09-22.png`). It shows
the source-relative stack/bell placement. This is an explicitly posed
measurement fixture, not a replay of operating history; its native geometry
equivalence is the separate passing fixture test.

## Next acceptance gates

Keep the production counter-tens regression red until adoption is justified.
The next work is complete native candidate admission, intermediate-height and
carried-operation cases, lower-input/drum withdrawal clearance, ordinary
arithmetic and actual-browser stop/replay parity. Other counter stations,
native result stations 10/11, the collar trial, clearing-loop passage and
whole-machine regression remain independent open obligations. No new pilot
approval is needed for this scoped evidence-led continuation. The active
OpenSpec change is not ready to sync/archive.

## Fresh operating build and browser interaction

The finite build succeeds in ignored `_build_source_timing_2026_09_22/`
using the integrated primary pair, under the existing 8 GiB address-space
guard and single-threaded BLAS/OpenMP settings. The new operating document
is v11 with 24 inputs, 25 controls and 213 bank coordinates. All **155 unique
rigid/marking assets** it references are present and nonempty. Program identity:
`0aac38742fcad90b0818ed07bd2bd4e239873169ffa9d207b3a18f869a732ca3`.
Document SHA-256:
`cdbb284e56672aa905e38a25c7efd1f3169fc8f128cd3195f27baf7745a9c28b`.

`python -m simulation.tools.operating_browser_probe --build
_build_source_timing_2026_09_22/operating_curta --screenshot
_build_checks/operating-source-timing-browser-2026-09-22.png --interlocks`
passes with no page errors. Actual pointer gestures lift the crank 1 mm
without rotation and change only selector 1 to one (its shaft reaches 36°).
Seated carriage shifting stops at .18°, and clearing at 1.437226368040361°
without lifting the carriage. The final screenshot was inspected: assembled
body, visible markings, controls and blocked-request readout are coherent.
This is the real geometry export, not the package's CAD-free carry drawing.

Bundle SHA-256:
`a84304064f0cdbcebf896e343525eb703d4ac3463cb0612b5896be749c710d6e`.
Browser report `_build_checks/operating-source-timing-browser-2026-09-22.json`,
SHA-256 `4d06f8489421ce65acd39d2ba43d51f859982e1e82b2c54ce111547e4a8629fb`.
These scoped gesture/interlock checks do not establish the complete pointer
matrix, browser carry parity for all 213 coordinates, or whole-machine
clearance. No geometry, material, joint, law or control declaration changed.
