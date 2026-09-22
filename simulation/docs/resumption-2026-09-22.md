# Operating Curta: resumed after interruption

**Latest continuation:** [integrated carry-timing correction](source-timing-integration-2026-09-22.md).
Both package fixes are now on local main; all four unchanged carry-graph
regressions pass. That record also recovers the terminal native station-8
and isolated result-bank arithmetic results. Pending-worker and approval
statements below describe earlier checkpoints, not the current state.

The pilot requested a status check and continuation of the operating Curta.
The project is **unfinished**. `simulate-the-curta` is the active, validated
spec-driven change, with **12/23 tasks complete**. Its planning artifacts
being complete does not mean the implementation is complete. The default
manifest selects `simulation.running:OperatingCurta` on `direct-operation`.

## State recovered

The starting project commit is `a5be5ce`. No Curta test process was still
running. The stopped agent left the thrust-seat investigation, its tests,
tools and evidence uncommitted, plus three corresponding documentation edits.
Those are preserved in checkpoint `ec1ad52` and continued. The untracked assembly video and
`screenshots/reverser_inspection.png` are unrelated user assets and stay out
of the implementation commit.

The September 21 handoff is historical: its T07 tens-adoption instructions
were subsequently completed. The default root now has both ones and tens
restraints. Their completed arithmetic and Python/browser results are in
[the continuation record](operating-continuation-2026-09-21.md).
The remaining result-bank and counter candidates are still separate trials.
Their interrupted native and arithmetic logs are **not passing acceptance**.

Framework content remains `e6a42c80e6dcc686c180b8a6d94037301c4213a5` and
viewer content `1995aa1f58d44dfeea7bfa62502d71349891327a` for the seat
acceptance below. The pilot subsequently authorized the separate viewer
repair; framework content is unchanged.

## Thrust-seat integration

The inherited [seat investigation](thrust-seat-investigation-2026-09-21.md)
found a placement-only correction using the collar's existing Z33 ledge and
the sleeve's Z54.3 underside. Its five independent bench tests pass again.
A new full-root regression fails before integration: the spring intersects
the ring by **6.599205817 mm³** on the faceted runner.

`SeatedCarriagePositioning` now connects that measured placement to the
operating root. Ring underside is Z33.05, lower wire cap Z35.5, upper cap
Z53.35; lifting the carriage by 6 mm compresses the coil from 17.85 to
11.85 mm. The source ring and sleeve geometry, wire radius, coil radius and
turn count remain unchanged. The historical source-pose positioning bench
and independent seat bench remain available.

The two full-root faceted checks pass: all rigid neighbours at rest, measured
seating and capture through five lift heights and all six carriage positions,
and exact bank/endpoint replay. This is scoped interface acceptance, not a
whole-machine interference result or a spring-force calculation.

Validation on 2026-09-22 (logs and images in ignored `_build_checks/`):

- `operating_positioning`: 2/2 faceted (60.22 s restored), 2/2 exact
  (202.42 s). Lowering the production ring 1 mm made the same test fail
  on its ball contact (0.310682361 mm³); restoring it returned green.
- Historical positioning: 2/2 on each kernel; independent seat bench:
  5/5 on each kernel; nearby `running_motion`: 7/7 faceted (90.02 s),
  7/7 exact (103.36 s). These are scoped suites, not full-project acceptance.
- Fresh root neighbour probe: 389 rigid bodies, 777 candidate pairs,
  zero positive/invalid operating intersections. All five fixture meshes
  match the independent seated bench exactly. The reconstructed source
  negative control still reports ring/collar 225.523065 mm³, spring/ring
  6.599188 mm³ and spring/ball 0.473498 mm³. The 213-coordinate bank is unchanged.
- Built `_build_operating_seats_2026_09_22/operating_curta`: 155 nonempty
  unique rigid/marking assets, 24 inputs, 25 physical controls, 213 bank
  coordinates. Program identity remains
  `67e67c324e3bbf98811a97a69104751c3ddf658009b0a3acb7ff573fa47ab9da`;
  only two program provenance labels change. Flexible height is now
  `(-1 * carriage.registers.lift) + 17.85000000000001`.
- Inspected rest, elevated/shifted and public-browser screenshots.
  The browser mount, selector pointer, crank lift, seated-shift stop and
  clearing stop all pass with no page errors. This is the default root,
  not the larger result-bank trial. Browser document SHA-256:
  `020ab020a64821485c7b2f609527509388a673314999c47e7b80801feb5b41f8`;
  bundle SHA-256:
  `5f3ec29aede4934106bb0cbbdaa7454dcec39d2ba04a233f431a4ce279fef610`.
- `openspec validate simulate-the-curta --strict` and `git diff --check` pass.

Commands use the workspace `.venv/bin/machinome test --faceted|--exact`
with each of `simulation/test_operating_positioning.py`,
`simulation/test_positioning.py`, `simulation/test_thrust_seat_trial.py`
and `simulation/test_running_motion.py`. The root probe is
`python -m simulation.tools.thrust_root_probe`; browser acceptance is
`python -m simulation.tools.operating_browser_probe --build
_build_operating_seats_2026_09_22/operating_curta --screenshot
_build_checks/operating-seats-browser-2026-09-22.png --interlocks`.

## Resumed investigation checkpoint — 2026-09-22 12:44 UTC

Two focused project commits retain this continuation:

- `1c3dfde`: the seven-station carry failure, passing six-station control,
  original full-bank failures and fresh-process 7→6→7 order control.
- `cdf33c5`: isolated collar pin/thread clocking acceptance and the separate
  combined trial. Six isolated tests pass on each runner. The final full-root
  exact trial has two passes (initial bank, mesh fixture) and two interface
  failures; it is not adopted. No default-root source change remains.

Strict OpenSpec validation and `git diff --check` pass. The author-provided
assembly video and `screenshots/reverser_inspection.png` remain untracked and
untouched. Task count remains **12/23**.

**Two workers are still live at this checkpoint, not completed results.**
Inspect these processes and their existing logs before any retry; do not
restart a quiet worker or overwrite either log:

| Worker | PID at checkpoint | Log under `_build_checks/` | Last observed state |
| --- | ---: | --- | --- |
| Native result station 8, full knot matrix | 3218297 | `result-station-8-profile-native-2026-09-22.log` | 17,513 admitted poses, zero failures so far; carry=1, shaft=84°; no terminal summary |
| Isolated result-bank arithmetic batch | 3228593 | `result-bank-arithmetic-resumed-2026-09-22.log` | Page-53 calibration test running; no completed case or batch result yet |

The native command is
`python -u -m simulation.tools.check_higher_locking_profile --kernel native --station 8 --knots`.
Native stations 10 and 11 have **not** been restarted by this continuation.
The arithmetic worker runs the unchanged `RunningCurtaTest` methods below
under a scoped `unittest.mock.patch.object(test_running, 'OperatingCurta',
ResultBankOperatingTrial)`, without changing the production file:

1. `test_manual_calibration_carries`
2. `test_subtraction_borrows_through_both_registers_and_addition_undoes_it`
3. `test_independent_inputs_and_two_successive_additions`

Both jobs use the unchanged framework content `e6a42c8`. No terminal success
is inferred from partial progress. The framework correctness investigation
awaits the pilot's permission to create an isolated bench from committed main
while preserving its unrelated untracked `docs/examples/v8-engine/` directory;
the framework-change skill treats a dirty selected base as a stop condition.
No framework worktree or proposal has been created, and no framework/viewer
file has been edited in this continuation.

## Outstanding work

- The [complete-result carry discrepancy](result-carry-graph-finding-2026-09-21.md#resumption-after-viewer-repair--2026-09-22)
  still reproduces after the viewer repair. A new source-law diagnostic
  narrows its first failing prefix to seven active result stations. Both
  original failing tests remain; counter-tens operating acceptance cannot
  proceed through that preparation until this separate correctness gate is
  resolved. The viewer repair does not fix Python retained arithmetic.
- Task 1.3: whole-machine rest/frame contacts, including collar shoulder,
  collar nut/pins and other recorded interfaces. The shoulder-facing trial
  remains separate; seating the thrust ring does not adopt it. The new
  [clocked collar/pin/thread bench](collar-seating-investigation-2026-09-21.md#resumption-pin-and-thread-clocking--2026-09-22)
  passes six isolated contracts on both runners. Its combined operating-root
  trial remains unadopted: rest-neighbour and moving-seat tests are red at
  nominally flush main-body/washer interfaces. The default root is unchanged.
- Tasks 6.2/6.3: remaining higher-result and counter restraints, interrupted
  arithmetic and geometry gates, and complete action-order coverage.
- Task 6.4: the printed clearing-loop clip/release path is unresolved;
  its swept contact must not be suppressed or turned into an invented hinge.
- Tasks 5.1–5.5 and 6.5/6.6: complete operating demonstrations, full regression,
  real-pointer matrices, final visuals/documentation and OpenSpec closeout.

The remaining-result-bank browser export exposes a separate viewer
expression-cache lifetime bug. Viewer change `keep-expression-references-valid`
was approved for implementation by the pilot on 2026-09-22, after its
planning-only preparation. The repaired bundle now passes the original
result-bank browser acceptance below. This does not adopt that trial into
the default root or complete its interrupted arithmetic/native gates.

## Viewer blocker retired — remaining-result-bank trial

The pinned export is unchanged: SHA-256
`c545d8807846ec9c8ba404bc253e39e0b98418b50062e49ce006ef25313a5884`,
program `c693fd960131c22da87b2afb9111536a04bb344ea50d18719234536d7377f24c`.
Final repaired viewer bundle SHA-256:
`20880099c6490adca932f7152c987751a645dddd1bf089ff197342db3c81727c`.
Viewer implementation commit: **`9a755e5`**. Its complete widget suite passes
1,423 tests; Python/browser validation passes 193 tests plus 20 subtests,
with both optional Curta drawing tests enabled and no skips. Build and
typecheck pass. The viewer OpenSpec change remains active solely for its
pending pilot sync/archive confirmation; nothing was pushed or published.

All four public running-request cases pass, with no page errors:

| Station | Requested crank target | Admitted crank stop |
| --- | ---: | ---: |
| Hundreds | 190° | 165.22323837279146° |
| Hundreds | 880° | 165.22323837227304° |
| Eighth | 290° | 265.22323837279146° |
| Eighth | 980° | 265.22323837227304° |

Each case blocks, replays its complete snapshot exactly, admits .05° relief
and blocks the retry at the same stop. The complete initial/idle banks are
unchanged. The eighth station's two stopped/relieved bank pairs match the
saved Python report **exactly: four states × 213 coordinates**. Hundreds
stop angles match its recorded Python test, but no captured hundreds Python
full-bank oracle exists, so that comparison is not claimed.

Both final station screenshots were inspected: the assembled calculator,
readable markings, crank pose and displayed request state are coherent.
They remain generated artifacts in `_build_result_bank_repaired_2026_09_22/`.
The [complete numeric report](evidence/result-bank-browser-acceptance-2026-09-22.json)
has SHA-256 `ca8a84e07b330cf70964d8126b8804709d1f922fbf0893f297c68508ef646b39`.
The report validator was extended red-first to reject incomplete initial/idle
banks; all five report tests pass, and the saved real report was revalidated
against that guard and its Python oracle.

Reproduce from this project with the workspace Python and this command:

```sh
python -m simulation.tools.result_bank_operating_browser --build _build_result_bank_repaired_2026_09_22 --python-report simulation/docs/evidence/result-bank-eighth-python-acceptance-2026-09-21.json
```

Mount took 28.334 s, first idle step .737 s, first move 1,666.9 ms in the
final run, initially concurrent with other validation. These are observations,
not speed requirements. The separate source census peaked at 94,854 nodes
during load and returned to zero on disposal. No Python speedup is claimed.

The **default seated OperatingCurta** was also rerun with that same final
bundle: mount, crank-lift and first-selector real-pointer prerequisites,
seated carriage-shift and clearing interlocks all pass with no page errors.
Its fresh screenshot was inspected. JSON/image evidence is in
`_build_checks/operating-seats-browser-repaired-viewer-2026-09-22.*`.
This remains scoped pointer coverage, not a complete action-order matrix.
