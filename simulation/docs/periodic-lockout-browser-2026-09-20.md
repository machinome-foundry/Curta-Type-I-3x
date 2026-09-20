# Periodic lockout: integrated producer and browser parity check

## Framework integration

The pilot approved integration and continued Curta work on 2026-09-20.
Framework main was verified clean at `8d2bd71171be81f13ba5dd492851ed8b3a9ababb`,
then fast-forwarded through planning `c2023b146856c0b6516f04e69a6e92fb7bc152a0`
to implementation `e63700e4fdb90e066d47f358e9de0ea935ac1be9`.
Post-integration focused validation passed **233 tests + 153 subtests, 9.45 s**.
The exact clean cycle worktree was removed through the shop's managed teardown;
the branch remains. Nothing was pushed or published.

The framework archive is
`openspec/changes/archive/2026-09-20-periodic-lockout-first-contact/`.
Its `evidence.md` and `evidence/curta-contact.jsonl` record:

- Actual Curta periodic-stop reproduction: **4/4 pass, 77.521 s**.
- Broader ones-lockout motion suite: **6/6 pass, 466.480 s**, covering five
  flats, later turns, withdrawal phases, relief/retry/replay and legal 1080°
  requests, including subtraction height.
- Seven actual long-request stop poses: **14/14 zero overlaps** across native
  and faceted kernels; .2° posed overtravel produces **14/14 positive overlaps**.
- Framework full suite: 3,488 passed, 4 skipped, followed by the expanded
  focused matrix. ADR-135 records push attribution at the located contact.

Those checks ran during the completed framework cycle against the same code
now integrated. They do not certify a browser consumer or the whole Curta.
After integration, `python -m unittest simulation.test_periodic_lockout -v`
was rerun against primary main: **4/4 pass, 83.319 s**. The project OpenSpec
change also validates strictly; its completion remains 12/23 tasks.

## Browser reproduction on the actual source-backed bench

Project base: `c76f230836ce3a91cc960564a1e1f0b3a7e9232b`.
Viewer remains clean at `4355da1a7f64dacd7d86eb27dbdfdf7ced94598f`, API 23,
version 0.2.0 unreleased. No viewer source was changed.

`simulation/tools/periodic_lockout_browser.py` opens an isolated local Chromium
page and mounts the exported `PeriodicLockoutBench` using the public viewer
API. The actual browser worker executes the requests. Nothing touches the
pilot's live Studio session, uploads assets, or rewrites a model coordinate.
Reset between cases is explicit test setup, not a mechanical operation.

Each case sets crank height 0, digit 3, turns to 120°, then withdraws the digit
to zero. The ones shaft retains **189.60000000000002°**. The expected next
free-side stop is 125.22°.

| Request | Actual browser result |
|---|---|
| 120 -> 150° | Blocked at **125.21999999999935°**, shaft unchanged |
| 120 -> 840° | Invariant refusal; crank stays **120°**, complete snapshot unchanged |

The long request reports that `bell.turn` left its declared bound and locating
the stop stopped no moving input. No uncaught page errors occur: this is the
run's transactional refusal. The acceptance script deliberately exits nonzero
because that refusal is not the required first-contact stop.

Read-only inspection confirms the matching cause in the viewer's
`machinome_viewer/widget/src/run/run.ts`: `searchedConstraint` discards the
outside end of its contact bracket, while `constraintGroup` compares the
candidate's complete-request endpoints. The framework correction retains both
bracket ends and attributes push there. The viewer is an independent executor;
integrating Python cannot update this browser code.

The browser screenshot was inspected. It shows the complete bell, drum and two
source shaft assemblies, with the panel still at crank 120° / digit 0 after
the refusal. It is not an image of a successfully stopped long request, nor
proof of geometric clearance.

### Reproduction

From this project root, use the workspace venv and the integrated framework
first on `PYTHONPATH`. Export with single-threaded BLAS/OMP and an 8 GiB CAD
virtual-memory cap; do **not** inherit that cap into Chromium:

```sh
machinome export simulation.periodic_lockout:PeriodicLockoutBench \
  --no-widget -o _build_periodic_lockout
python -m simulation.tools.periodic_lockout_browser --build _build_periodic_lockout
```

The browser probe writes ignored `browser-acceptance.json` (including full
readbacks and refusal) and `periodic-browser.png` in that export directory.
The same unmodified probe must pass after a viewer correction.

Tested content SHA-256:

- Viewer bundle: `427e5090bc8119fa0e4cf80e0ca2366a72567cb5c945adddfc60631d5dc6944d`.
- Actual bench manifest: `7b6f259e4bf5e51e8439a1d52ef0681899a76f5d2d95072bf6d2fff891a3bd48`.
- Framework running corpus: `4d937550b5fb5d5d6bc6b9e5f51428cb4cc106edab2286bb54975470c0005cc1`.

## Next boundary

The minimal next dependency is a separately authorized viewer correction:
carry the first-contact bracket through its executor, attribute each candidate
at that bracket, and consume the producer's unchanged exported corpus. Preserve
atomicity, relieving/disengaged-input behavior, existing time-drive handling
and the public API/document shape. Validate red-first unit/corpus tests plus
this actual Curta browser reproduction and the broader measured restraint.
Do not hide the defect by splitting user requests or imposing a turn cap.

The general restraint remains unselected. Full-root operating adoption,
other channels/action orders, complete pointer acceptance, clearing-loop work
and the whole-machine overlap inventory remain open. Tasks 6.2/6.3 and overall
12/23 completion are unchanged. No upstream CAD or author-review fit changed.
