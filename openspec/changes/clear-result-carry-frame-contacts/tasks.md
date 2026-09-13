Ratified on 2026-09-13 ("ratify, go on"). No production implementation task
was complete at ratification. The existing diagnostics are starting evidence,
not the correction's passing acceptance tests. Validate and commit this
focused planning record and its evidence before task 1.1.

Implementation status, 2026-09-13: original planning commit `7d39306` and
approved seat-edge revision `9c58255`. The protected-seat gate was triggered before any production cut:
both endpoint gaps reach an existing guide/frame seating land at both
stations. See `simulation/docs/carry-frame-gate-2026-09-13.md`. The pilot subsequently approved the bounded seat-edge
exception and instructed "yes, and then try, you don't need so many
confirmations from me". The revised artifacts authorize dimensioning and
fitting under that exception; no further routine confirmation is required.
Both station fits are implemented and locally verified. All 17 new contracts pass
on both runners; full-stroke slider/spring/sleeve enclosures, dimensional and
negative controls, installed transitions and inspected completion images pass.
The complete regression finishes all 39 modules on each runner: 159/161
faceted and 160/161 native, with only the named pre-existing failures and no
source drift. Actual solid-node feature work
requires the pilot's explicit go-ahead once the campaign evidence is ready.

## 1. Reproduce the failures and bound the repair

- [x] 1.1 Add independent native frame-contact contracts for both selected stations at `099` preload and the raised/lowered slider endpoints; run them red against the unchanged model and retain pair names, volumes, exact import origins and frame/travel guards. Recorded in `simulation/docs/evidence/carry-frame-red-2026-09-13.md`: six intended failures, three guards passed.
- [x] 1.2 Measure the full slider/spring envelopes, both station transforms and the nearby guide lands, M4 fastening features, support/nut seats and shaft/bearing surfaces; record independent permitted-removal regions for each relief family and the proposed 0.05 mm gap. Complete native enclosure, six-land contact, 53-reference support and 105-cylinder source maps are retained with independent spatial limits.
- [x] 1.3 Add source-preservation, connected-frame, no-added-material, unchanged-placement and protected-feature contracts, including the bounded seat-edge exception and remaining registration contact; establish source hashes and retained mechanical contact tests as the repair's comparison baseline. All seven fit contracts and ten contact/placement contracts pass on both runners; source hashes and 53 protected references are retained.
- [x] 1.4 Verify that trial reliefs stay within the approved seat-edge exception and avoid other protected features; develop the conservative unsampled-clearance method alongside reversible fitting, retaining its complete proof as task 3.1's acceptance gate. Return only materially broader repair/fidelity decisions to the pilot. Spatial and remaining-seat contracts pass, with continuous native enclosure methods for sliders, springs and sleeves.

## 2. Fit the first station, then the second

- [x] 2.1 Implement a source-derived frame adapter with the three separately identifiable first-station relief families and one declared gap parameter; wire it into the operating upper frame without changing the raw source assembly or any moving part. First-station trial: all three contact cases green; second-station cases remained red. Four native preservation checks passed before extending the fit.
- [x] 2.2 Make the first-station frame-contact tests green while preserving spring seats, wire geometry, guide placement, fork/sleeve capture, pin approach and reset behaviour; compare fresh and built native geometry. All 17 new contracts pass both runners, as do the retained carry/spring, installed carry bank, carry-contact, carry-fit, slider-head and carry-mesh contracts. Moving source and profile hashes are unchanged.
- [x] 2.3 Add only the second-station reliefs using its verified source transform; make its native contact tests green and demonstrate that non-selected station features and protected frame geometry outside the approved seat-edge exception remain unchanged. Native and faceted contracts pass; the complete source difference is bounded and all 13 non-selected guides are protected.
- [x] 2.4 Independently measure upper and lower clearance bounds at the named gap sites, verify their response to at least two declared gap values, and retain the dimensional drawing/measurement record for the actual fit. Native readings at 0.04, 0.05 and 0.06 mm, both stations: `simulation/docs/evidence/carry-frame-fit-report-2026-09-13.json`.

## 3. Verify complete movement and challenge the fit

- [x] 3.1 Check full lever travel at both stations, including all detent knots, `099` preload and at least 41 discrete poses; establish and record the separate conservative swept/interval proof and numerical bound for frame clearance between samples. The dense native/faceted contract passes; final continuous certificates cover both sliders, both coupled sleeves and both springs, with no unresolved interval or cell.
- [x] 3.2 Rerun both installed trip and reset transitions against the complete 428-body inventory, with the source-mesh interfaces named; preserve partial preload, event backgrounds, coupled sleeve movement and the reset after 360 degrees. All four 41-pose native sweeps pass; the six source-mesh interfaces remain explicitly faceted. Records: `simulation/docs/evidence/carry-frame-{trip1,trip2,reset1,reset2}-41-2026-09-13.json`, sharing the original 428-body inventory hash.
- [x] 3.3 Run negative controls removing each relief family and omitting/misplacing the second-station fit; confirm the intended contact failure in each case, then restore and rerun green. Ten intended contact negatives detected; all 17 normal contracts subsequently passed on both runners.
- [x] 3.4 Run an excessive-relief mutation crossing a protected feature and a gap-application mutation; confirm the preservation/dimensional contract detects each fault, then restore and rerun green. Both faults detected; all 17 normal contracts subsequently passed on both runners.

## 4. Regression and inspected evidence

- [x] 4.1 Run the affected carry, spring, fit/head, pin/contact, sleeve/bell and installed-bank regressions on both kernels; compare against the pre-repair mechanical interface baseline and retain failures by name. Carry, bell-spring, carry-fit/head/contact/mesh, carry-bank, bevel-bank and dial-detent-bank checks all pass both kernels with unchanged mechanical source/profile hashes; all 17 new local contracts also pass both runners.
- [x] 4.2 Run the full project's faceted and native regressions sequentially under the resource guard, reporting the existing unresolved failures separately and requiring no new or changed regression; do not present this as whole-machine acceptance. All 78 module runs match the baseline: 159/161 faceted, 160/161 native. The 191-file source list and hashes are unchanged. The retained JSON names the bearing-facet and common housing/thread failures; no overlap is waived.
- [x] 4.3 Build the root with the explicit framework worktree, inspect the published document and referenced artifacts, and confirm the corrected frame reaches the operating assembly without changing controls or profiles. Root build passes; schema 4, 9969 bindings, eight drivers, seven instructions, 390 rigid and 38 flexible occurrences. All referenced artifacts exist and the frame artifact matches the operating adapter.
- [x] 4.4 Generate and inspect before/after close-up sections and an assembled view showing both stations with relevant supports and neighbours; retain hashes, captions and reproduction commands, and document the final relief dimensions and fidelity limits. Both native section sheets and two OpenSCAD assembled views inspected; image hashes/captions/commands are in the validation record and final dimensions in measurements.

## 5. Close only this prerequisite

- [x] 5.1 Update project measurements and the simulation README with the bounded verified correction and remaining findings; validate this change and confirm its focused acceptance requirements are met without checking off `simulate-the-curta` tasks. The completion record covers all four focused requirements; full/lightweight tests, source hashes, publication artifacts and inspected images are retained. Both active changes and the new baseline spec pass strict validation; the original change remains at 7/17.
- [ ] 5.2 Sync the new `result-carry-frame-clearance` capability and archive only this completed change; commit its implementation, tests, accepted evidence and completion record in the Curta repository, excluding generated artifacts and unrelated work. The four requirements are synced and strict-valid; implementation commit, archive and final completion commit follow.
- [ ] 5.3 Record the accepted correction commit in the open-run campaign handoff and resume the remaining transition, home-window and setup evidence work; report integration as pending unless separately authorized.
