# Reversing-shaft mounting-seat trial

This records the initial candidate at `fe02911`. The
[fork/follower continuation](reverser-fork-and-follower-2026-09-20.md) records
the revised fastening end, local fork fit, differentiated counter profiles
and radial spring-loaded follower. Initial failures below remain historical
evidence, not the current trial's complete status.

Pilot authorization, 2026-09-20: test the mounting-seat modification in the
simulation and document all proposed fixes for review with the author.
**Experimental, not adopted in OperatingCurta.** Upstream CAD, both detent
pockets and their 12 mm spacing remain unchanged. The previous
[insertion-only probe](reverser-insertion-trial-2026-09-20.md) shows why merely
pushing the original shaft farther into the frame cannot pass rigid contact.

## Exact candidate, not an instruction to sand a real part

[TrialReversingShaft](../reverser_seat_trial.py) intersects the original solid
with a stepped cylindrical envelope, removing material only above local
Z115.05. It raises the installed body 1.9 mm. It also shortens the upper end,
so that the fastening neck/stud retain their original installed end heights:

| Feature | Original local geometry | Trial local geometry | Installed consequence |
|---|---|---|---|
| Main shaft shoulder, R3.693 | Ends Z117 | Ends Z115.05 | World Z−22.25, .05 mm below original frame underside |
| Neck, R2.9375 | Z117..121.5 | Z115.05..119.6 | Neck end remains world Z−17.7 |
| Stud, R2.1 | Z121.5..127.5 | Z119.6..125.6 | Stud end remains world Z−11.7 |
| Detent centres | Z78.6 and 90.6 | Unchanged | Both move upward 1.9 mm with the shaft |
| Lower flats and bearing land | Original surfaces | Unchanged surfaces | Installed lower end also moves upward 1.9 mm |

Native source volume is 4826.543416 mm³; trial volume 4744.349171 mm³.
The native removed-solid measurement is approximately 82.193929 mm³,
bounded by local Z115.05..127.5 (Boolean mass-property sums have a small
numerical discrepancy). The fitted shape is valid and one solid. Tests
check no added material and preservation of the whole local Z0..110 region,
including pockets and lower flats. This does not certify strength, thread
engagement under load, printability or retention after shortening.

The tested body rise is specifically **1.9 mm**. Other `seat_rise` values
are exploratory build parameters, not validated alternatives; the diagnostic
driver defaults and tests below deliberately specify this one candidate.

## Lever endpoints and the remaining detent question

Source-coordinate driver positions, in millimetres:

| Pose | Knob/ball height | Input-gear height | Reason |
|---|---:|---:|---|
| Lower | −4.9425 | −4.85 | Ball aligned axially with the raised lower pocket; pinion centred in the .185 mm fork play |
| Upper | +3.9075 | +4.0 | Existing upper frame/spacer limit; same .0925 mm mid-play offset |

Travel is **8.85 mm**, not an assumed 9 mm or 12 mm. At the lower pose the
tens pinion's 1.5 mm tooth band aligns with the nine-tooth row. An independent
12° pinion perturbation now meets the drum, where the original lower-detent
placement missed it. This proves reach at that sampled position, not a
complete driving cycle or successful counter arithmetic.

The upper pocket centre would require knob height **7.0575 mm**, which is
3.15 mm above the tested upper stop. Thus the candidate does **not** establish
two centred detent positions. Whether the upper position can be retained on
the pocket flank requires radial ball following, spring compression and a
retention assessment. The inherited diagnostic does not model those effects;
its prescribed ball/spring pose must not be mistaken for a solved contact law.

## Red-first checks and results

The unchanged shaft, translated upward before cutting, failed all four initial
mounting/fidelity tests: upper-frame overlap 24.872984 mm³ faceted, stud end
1.9 mm too high, no localized removal, and failed axial free play. The profile
change makes all four pass on the exact runner.

Final [trial tests](../test_reverser_seat_trial.py) cover the shaft mounting,
source preservation, both knob stops, lower-row reach, and all six input
stacks at both lever endpoints with both 0 and 9 mm drum lift, crank 101.25°.
Each bank check tests both drum halves, both frames, fork clearance and fork
capture. All failures are accumulated so a first-channel failure cannot hide
later channels. An initial exact test mistakenly passed the drum assembly to
a solid-only assertion; it was corrected to test its two rigid prints. Those
initial API failures are not mechanical evidence.

| Result | Exact | Faceted |
|---|---:|---:|
| Shaft vs both frames | Clear | Clear |
| Shaft vs fastening nut | Clear | **0.038002314 mm³ overlap** |
| Shoulder free ±.025 mm, blocked +.1 mm | Pass | Pass |
| Original installed stud-end height and protected geometry | Pass | Pass |
| Knob vs frames/spacers, both endpoints | Pass | Pass |
| Lower tens tooth reaches nine-tooth row under perturbation | Pass | Pass |
| Sixth input print vs fork, all four endpoint/drum combinations | **1.585791236 mm³ overlap** | **1.723612089 mm³ overlap** |

The other five input prints clear the tested neighbours, and all six show
axial capture under the .3 mm perturbation. The sixth print's overlap is a
pre-existing local fork/input finding, not cured by moving their common
height. No fork material is removed in this trial. The nut's exact/faceted
disagreement is preserved, not waived or called a proven manufacturing defect.

The exact final suite is **7/11 passing** (6.41 s); the faceted suite is
**6/11 passing** (21.22 s). Existing source-assembly red acceptance tests remain
unchanged. There is no new successful operating-reversal claim.

## Reproduce and review

Run from the project with the workspace environment and `PYTHONPATH="$PWD"`:

```sh
machinome test --exact simulation/reverser_seat_trial.py:ReverserSeatTrial
machinome test --faceted simulation/reverser_seat_trial.py:ReverserSeatTrial
machinome snapshot simulation/reverser_seat_trial.py:SeatProfileComparison -o _build_running/reverser-seat-profile.png --camera 35,-60,-7,6,0,-7 --imgsize 1200x900
```

The comparison places the unchanged shaft on the left (grey) and trial on
the right (green), with fastening ends aligned. The generated OpenSCAD image
was inspected: both stepped fastening profiles remain present, with no added
collar or detached sliver. It is a cropped profile-detail view,
not an installed full-assembly certificate. Logs are under `_build_running/`:
`reverser-seat-trial-{red,exact,faceted}.log` and
`reverser-seat-snapshot.log`. The current interactive inspection, operating
model and manifest default are untouched; the trial is an explicit class
reference, not a replacement of the pilot's current view.

Conclusion: the modified mounting seat **resolves the sampled lower axial
engagement mismatch**, but does not finish reversal. Next requirements are
the sixth-channel fork fit, upper detent retention, the nut mesh discrepancy,
installed enclosure/fastening checks and the full driving sweep. Consult the
[author-review register](author-review.md) before treating any trial as a
physical design change.

Strict validation of the active `simulate-the-curta` OpenSpec record passes.
No task is marked complete by these partial mechanical results.
