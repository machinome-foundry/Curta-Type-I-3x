Ratified on 2026-09-13 ("ratify, go on"). No production implementation task
was complete at ratification. The existing diagnostics are starting evidence,
not the correction's passing acceptance tests. Validate and commit this
focused planning record and its evidence before task 1.1.

Implementation status, 2026-09-13: planning commit `7d39306`; task 1.1
completed. The protected-seat gate was triggered before any production cut:
both endpoint gaps reach an existing guide/frame seating land at both
stations. See `simulation/docs/carry-frame-gate-2026-09-13.md`. Tasks 1.2–1.4
remain incomplete. The pilot subsequently approved the bounded seat-edge
exception and instructed "yes, and then try, you don't need so many
confirmations from me". The revised artifacts authorize dimensioning and
fitting under that exception; no further routine confirmation is required.

## 1. Reproduce the failures and bound the repair

- [x] 1.1 Add independent native frame-contact contracts for both selected stations at `099` preload and the raised/lowered slider endpoints; run them red against the unchanged model and retain pair names, volumes, exact import origins and frame/travel guards. Recorded in `simulation/docs/evidence/carry-frame-red-2026-09-13.md`: six intended failures, three guards passed.
- [ ] 1.2 Measure the full slider/spring envelopes, both station transforms and the nearby guide lands, M4 fastening features, support/nut seats and shaft/bearing surfaces; record independent permitted-removal regions for each relief family and the proposed 0.05 mm gap.
- [ ] 1.3 Add source-preservation, connected-frame, no-added-material, unchanged-placement and protected-feature contracts, including the bounded seat-edge exception and remaining registration contact; establish source hashes and retained mechanical contact tests as the repair's comparison baseline.
- [ ] 1.4 Verify that trial reliefs stay within the approved seat-edge exception and avoid other protected features; develop the conservative unsampled-clearance method alongside reversible fitting, retaining its complete proof as task 3.1's acceptance gate. Return only materially broader repair/fidelity decisions to the pilot.

## 2. Fit the first station, then the second

- [ ] 2.1 Implement a source-derived frame adapter with the three separately identifiable first-station relief families and one declared gap parameter; wire it into the operating upper frame without changing the raw source assembly or any moving part.
- [ ] 2.2 Make the first-station frame-contact tests green while preserving spring seats, wire geometry, guide placement, fork/sleeve capture, pin approach and reset behaviour; compare fresh and built native geometry.
- [ ] 2.3 Add only the second-station reliefs using its verified source transform; make its native contact tests green and demonstrate that non-selected station features and protected frame geometry outside the approved seat-edge exception remain unchanged.
- [ ] 2.4 Independently measure upper and lower clearance bounds at the named gap sites, verify their response to at least two declared gap values, and retain the dimensional drawing/measurement record for the actual fit.

## 3. Verify complete movement and challenge the fit

- [ ] 3.1 Check full lever travel at both stations, including all detent knots, `099` preload and at least 41 discrete poses; establish and record the separate conservative swept/interval proof and numerical bound for frame clearance between samples.
- [ ] 3.2 Rerun both installed trip and reset transitions against the complete 428-body inventory, with the source-mesh interfaces named; preserve partial preload, event backgrounds, coupled sleeve movement and the reset after 360 degrees.
- [ ] 3.3 Run negative controls removing each relief family and omitting/misplacing the second-station fit; confirm the intended contact failure in each case, then restore and rerun green.
- [ ] 3.4 Run an excessive-relief mutation crossing a protected feature and a gap-application mutation; confirm the preservation/dimensional contract detects each fault, then restore and rerun green.

## 4. Regression and inspected evidence

- [ ] 4.1 Run the affected carry, spring, fit/head, pin/contact, sleeve/bell and installed-bank regressions on both kernels; compare against the pre-repair mechanical interface baseline and retain failures by name.
- [ ] 4.2 Run the full project's faceted and native regressions sequentially under the resource guard, reporting the existing unresolved failures separately and requiring no new or changed regression; do not present this as whole-machine acceptance.
- [ ] 4.3 Build the root with the explicit framework worktree, inspect the published document and referenced artifacts, and confirm the corrected frame reaches the operating assembly without changing controls or profiles.
- [ ] 4.4 Generate and inspect before/after close-up sections and an assembled view showing both stations with relevant supports and neighbours; retain hashes, captions and reproduction commands, and document the final relief dimensions and fidelity limits.

## 5. Close only this prerequisite

- [ ] 5.1 Update project measurements and the simulation README with the bounded verified correction and remaining findings; validate this change and confirm its focused acceptance requirements are met without checking off `simulate-the-curta` tasks.
- [ ] 5.2 Sync the new `result-carry-frame-clearance` capability and archive only this completed change; commit its implementation, tests, accepted evidence and completion record in the Curta repository, excluding generated artifacts and unrelated work.
- [ ] 5.3 Record the accepted correction commit in the open-run campaign handoff and resume the remaining transition, home-window and setup evidence work; report integration as pending unless separately authorized.
