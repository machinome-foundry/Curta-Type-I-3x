# Operating Curta: resumed after interruption

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

## Outstanding work

- Task 1.3: whole-machine rest/frame contacts, including collar shoulder,
  collar nut/pins and other recorded interfaces. The shoulder-facing trial
  remains separate; seating the thrust ring does not adopt it.
- Tasks 6.2/6.3: remaining higher-result and counter restraints, interrupted
  arithmetic and geometry gates, and complete action-order coverage.
- Task 6.4: the printed clearing-loop clip/release path is unresolved;
  its swept contact must not be suppressed or turned into an invented hinge.
- Tasks 5.1–5.5 and 6.5/6.6: complete operating demonstrations, full regression,
  real-pointer matrices, final visuals/documentation and OpenSpec closeout.

The remaining-result-bank browser export exposes a separate viewer
expression-cache lifetime bug. Viewer change `keep-expression-references-valid`
was approved for implementation by the pilot on 2026-09-22, after its
planning-only preparation. Work continues in the viewer repository under
that change. No result-bank browser pass is inferred from its proposal or
from the default-root browser acceptance above.
