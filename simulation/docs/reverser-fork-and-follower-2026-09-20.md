# Reverser continuation: fork, fastening end and spring-loaded follower

Continuation of the pilot-authorized mounting-seat trial, under the request
to finish the operating Curta and retain all fits for author review.
Upstream files and detent geometry remain unchanged. The candidate is now wired
into `OperatingCurta`; the trial classes remain independently testable. This
record distinguishes tested interfaces from the remaining acceptance work.
The [initial trial](reverser-seat-trial-2026-09-20.md) describes commit `fe02911`,
not the revised candidate below.

## Local fork relief

`tools/reverser_fork.py` places the source actuator and sixth input in their
common frame. The input axis is (35.074028853, 20.25); the source fork's R5
seat is centred at (33.878198, 19.6613403), about 1.333 mm away. The fitted
R3.85 sleeve therefore enters one edge, giving 1.585791236 mm³ native /
1.723612089 mm³ faceted overlap. Its contact spans the fork's 4.5 mm thickness.

`FittedReversingActuator` removes material only inside an R3.9 cylinder centred
on that input, through local Z−2.25..2.25. It preserves the other five seats,
knob shoulder and axial fork faces. The first rotating check then found a
separate far-wall contact at crank 195°/240°: .012566394 mm³ native, confined
to the 1.5 mm tooth band. A second cutter opens only the existing 1.685 mm
tooth slot to R6.28 around that same input. The initial .36 mm fitted tooth
reaches R6.226210; neither slot face is moved. The source .185 mm total axial
play remains, and independent ±.3 mm capture checks remain mandatory.

The initial sleeve-only relief left .038824682 mm³ faceted contact because
the coarse curved-wall tessellation crossed its .05 mm gap. Refining only
the actuator's mesh to .01 mm linear / .1 rad angular deflection resolves
that representation issue. It does not excuse the separately measured
native far-wall contact. Source-fidelity tests require a valid, single solid,
no added material and no removal outside the union of the two named cutters.
The native fork changes from 6579.695121 to 6577.077948 mm³, removing
2.617173 mm³ in total.

## Finished M4 end, not the unthreaded blank

Manual page 28 explicitly instructs cutting threads into the shaft with an
M4 die. Its printed blank is R2.1. The trial now represents the finished
nominal M4 major envelope as R2.0, confined to the already-shortened stud;
no thread helix or fastening-load rating is claimed. Neck and installed
stud-end heights retain the original trial's datums. This makes the nut
clear on both kernels instead of waiving the previous .038002314 mm³ faceted
contact. The shaft/pocket mesh is separately refined to .01 mm / .1 rad;
that changes tessellation, not the native detent.
The revised shaft has native volume 4736.620867 mm³ versus source
4826.543416 mm³; its removed-solid measurement is approximately 89.922247 mm³.

## Counter tooth profiles: why the isolated result was insufficient

The full-bank sweep reaches the higher counters at phases absent from the
old one-pinion trial. At upper gear height +4 mm, drum lift 9 mm and crank
123°, the hundreds input's tooth itself overlaps the upper drum. The
independent native profile probe gives:

| Outside-profile relief (mm) | Native overlap (mm³) |
|---:|---:|
| .36 | .004154118 |
| .37 | .002775206 |
| .38 | .001672006 |
| .39 | .000845759 |
| .40 | .000297740 |
| .42 | 0 |

The trial uses .42 mm for the five higher counter inputs only. Applying it
to the ones counter's three teeth lost fork capture at crank 75°; that trial
was rejected and the ones stack retains its existing .36 mm fit. No result
input, keyway, tooth thickness or sleeve changes here. Drum-clearance tests
and unilateral driving/capture tests are separate: making an undersized gear
that merely avoids collision cannot pass.

## Radial ball and spring following

The native source measurements are reproducible with
`tools/reverser_spring.py` and the source-drift test:

- Ball radius 2.7 mm (the CAD value, still distinct from the manual's 5 mm
  diameter hardware specification).
- Shaft R3.693, two +X conical pockets with apex X.81, half-angle 63°, centres
  Z78.6/90.6 in the shaft frame. Their spacing and surfaces are unchanged.
- Spring wire radius .255 mm, coil-centre radius 2.295 mm, 6½ turns, free
  centreline height 11.1 mm; knob blind-bore end 16.7 mm from the shaft axis.

`reverser_detent_motion.py` derives radial contact from the cone, its rim and
the cylindrical land, with a named .05 mm surface gap. It is not a fitted
table or a different detent. The source's fixed radial ball position first
failed the independent original-print seating and restoring-direction tests.
The analytic law passes clearance and inward-blocking checks at 92 positions
against the original printable shaft, plus native source-dimension checks.

`FollowingReverser` gives the ball its own radial joint and drives a
source-sized analytic spring between that ball and the knob's blind end.
The original fixed ball/free-height spring failed all four initial mounted
tests. Refining the ball and shaft meshes preserves the small clearances;
the first coarse sphere's bounding-box centre was off by .0204 mm. A mistaken
spring perturbation direction was also corrected to the wire's local axis,
not treated as evidence to alter a seat.

The lower pocket centre is a minimum in required ball radius. At the upper
working stop the ball lies 3.15 mm below the upper pocket centre, on a flank
whose radius decreases upward. A compressed spring therefore has a restoring
direction toward that upper stop. The spring remains compressed throughout
travel, with pitch greater than wire diameter; the knob is independently
blocked upward by its spacer. This establishes geometric seating and the
restoring direction, **not holding force, friction, automatic snapping,
fatigue, print strength or a dynamic detent simulation**.

| Position (shaft-local ball Z) | Ball-centre radius (mm) | Coil centreline height (mm) |
|---|---:|---:|
| Lower centre, 78.6 | 3.896397 | 10.558757 |
| Between pockets, 84.6 | 6.443000 | 8.012155 |
| Upper working flank, 87.45 | 5.501402 | 8.953752 |

Native sphere/shaft pocket commons remain unreliable as documented earlier.
The shaft/ball contact test deliberately uses the actual fitted shaft mesh
on either runner, with explicit Boolean status checks and no volume epsilon;
the independent original-print test prevents that representation from being
its own reference. Native tests still verify the other exact interfaces and
spring validity/wire section.

## Verification checkpoint

- Original-print/profile/source tests: 4/4 pass, now including 112 sampled
  ball positions extending below the lower working pocket.
- Mounted follower: 6/6 faceted (3.23 s) and 6/6 exact (25.79 s) pass over
  the expanded housing-stop-to-spacer travel, including spring capture and
  the upper restoring-direction stop.
- Six-input bank: **15/15 faceted (30.03 s) and 15/15 exact (249.00 s)** pass
  with the differentiated tooth fits.
  This includes all four mode combinations through crank 0..360° at 3°
  intervals, unilateral contact at first/middle/last active tooth passages,
  all-six fork capture at 15° crank intervals and both endpoints, shaft
  fastening and protected geometry. These are sampled full-revolution checks,
  not a mathematical continuous-collision certificate.
- Working-stroke transition: 1/1 faceted and 1/1 exact (68.49 s) pass across 37 heights at parked crank, both
  drum lifts, with both drum halves, both frames, fork and housing-window
  neighbours. The expanded transition through 45 heights, including the lower
  housing stop and its independent .01 mm free/.1 mm blocked probe, subsequently
  passes 2/2 faceted (5.08 s) and 2/2 exact (85.80 s).

The lower and upper close-up OpenSCAD images were inspected. They show the
ball at the lower pocket centre and upper pocket flank with the changing coil
length. The opaque knob is deliberately omitted to reveal the spring; these
images alone do not certify its bore or the complete assembly. First render
still contained the knob because omission was applied from the wrong owning
assembly; the corrected inspection subclass omits it at its owner and both
final images show the wire.

Evidence logs under `_build_running/`: `reverser-fork-red.log`,
`reverser-fork-{faceted,exact}.log`, `reverser-fork-refined-faceted.log`,
`reverser-profile-measurements.jsonl`, `reverser-bank-differential-faceted.log`,
`reverser-detent-law-{red,green}.log`, `reverser-detent-source-green.log`,
`reverser-follower-{red,faceted}.log`, `reverser-follower-refined-faceted.log`,
`reverser-follower-final-exact.log`, and `reverser-transition-{faceted,exact}.log`.
Images: `reverser-follower-{lower,upper}.png`.

No broad roadmap checkbox is completed by these scoped results. The
[author-review register](author-review.md) remains the consolidated agenda.

## Engagement between working positions

The actual source top drum has seven **adjacent 1.5 mm bands**, beginning at
Z−54.2, −52.7, −51.2, −49.7, −48.2, −46.7 and −45.2 mm; the nine-tooth band
starts at −49.7. An initial 4.5 mm-pitch assumption in the new draft was
discarded after reading the source assembly. A geometry-bound test now checks
all seven transformed row extents. This was a diagnostic mistake, not an
upstream geometry defect.

`reverser_modes.py` derives active tooth count from positive axial overlap
between these bands and the actual pinions. All three ones pinions contribute;
each higher counter has one. A nine-tooth engagement includes the final single
tooth passage, so simultaneous overlap with a one-tooth row is not counted twice.
The source-height clearance and driving-contact checks are independent of this
counting law. With the lever unseated at −3 mm, all six channels meet one-tooth
rows. Initially suppressing those higher-channel passages produced a measured
.919736969 mm³ tens-input collision at crank 192°. The corrected mapping passes
the faceted sweep through ten lever heights, both drum lifts and 61 crank poses.
Three contracts pass on both kernels (16.11 s faceted / 418.67 s exact),
including source bands and unilateral driving contact at unseated positions.
The added full-revolution sweep at four heights below the working pocket also
passes: final **4/4 faceted (23.40 s) and 4/4 exact (660.16 s)**. Thus the
sampled matrix covers fourteen lever heights, both drum lifts and 61 crank
poses per height/mode, plus the separate unilateral contact checks.

This is not a midpoint switch or automatic detent snap. The lower working
pocket at knob −4.9425 is also not a hard stop. The source housing-window edge
is flush near −6.9925 mm; the candidate lower travel limit is −6.9425 mm with
a named .05 mm gap. The expanded transition and follower checks above verify
that extra travel. A reduced running-limit test first failed because the draft
incorrectly stopped at the lower pocket; with the actual window limit it passes,
including synchronous knob, ball and spring admission at both hard stops.
The upper working position remains the measured spacer stop at +3.9075 mm.
The 8.85 mm separation of working positions must not be confused with total
admissible travel to a housing stop.

The operating integration adds a physical `reverser_height` input on the actual
knob and derives all six gear heights from that knob's retained joint, with
the measured .0925 mm fork mid-play offset. Counter motion reads actual axial
engagement independently of result inputs. Its first acceptance test failed
before implementation because the operating model had no reversing input
(`operating-reverser-red.log`). No register is written directly, and neither
the crank nor carriage is automatically prepared. Mid-cycle reverser/crank
restraint and whole-machine interference acceptance remain separate work.

The first integrated retained-operation test passes (359.526 s, `dt=.1`). With
operand 3, successive user-requested turns give `(result, counter)`:
`(3, 1)` → lower lever → `(6, 0)` → raised crank → `(3, 1)` → upper lever →
`(0, 0)`. Moving the lever alone does not change the preceding total. The all-six
carriage-position matrix uses `dt=.2` as an additional subdivision check; its
result is recorded separately when complete, not inferred from this first run.
The full operating-root lower-overtravel/hard-stop test and partial-movement
snapshot/replay test also pass. They issue physical requests and verify that
the crank, carriage and register history are not silently prepared or reset.
The unseated-height characterization passes too (84.228 s, `dt=.2`): at knob
−3 mm, one crank revolution leaves the zero operand/result unchanged and puts
`111111` in the counter, as the six local one-tooth engagements predict. The
lever stays at −3 mm. This proves the current modeled engagement is not
silently coerced to ±1; it is **not** proof that no separate, still-unvalidated
whole-machine interlock could restrain that action.

Additional logs: `reverser-law-and-limits-final.log` (8 tests),
`reverser-overtravel-{red,green}.log`, `reverser-overtravel-{faceted,exact}.log`,
`reverser-follower-final-faceted.log`, `reverser-follower-overtravel-exact.log`,
`reverser-mapped-final-{faceted,exact}.log`, and
`reverser-mapped-overtravel-{faceted,exact}.log`,
`operating-reverser-first-green.log`, and `operating-reverser-matrix.log`.
Browser-test API usage was checked against
the [Playwright input guide](https://playwright.dev/python/docs/input); the probe
uses actual pointer events and public viewer readback, not direct run movement.

## Installed geometry and hosted control

`running_reverser_motion.py` instantiates the complete operating root, not a
substitute bank. Its retained requests pass on both kernels (1/1 faceted,
32.88 s; 1/1 exact, 18.32 s). Vertex comparisons show that knob, fork and all
six input prints translate together while the shaft, spacers and frame remain
fixed. They also check actual radial ball position, fork clearance/capture,
spring/ball/knob contacts and enclosure clearance through working and overtravel
positions. This remains a scoped interface test, not the full overlap inventory.

`machinome build operating_curta` succeeds; all 155 unique model/decal artifact
paths referenced by its tree exist. The version-7 export has **25
controls**, including a Z-axis Slide on the actual reversing knob, with its
selected retained lift joint. `operating_browser_probe --interlocks --reverser`
passes against that ordinary hosted export. Real down/up pointer gestures
produce retained knob heights 3.2408333333 and 3.9075 mm in the final run;
all six gear travel coordinates equal `-(height + .0925)`. Crank, carriage and
all selectors remain unchanged. The existing crank/selector and seated
carriage/clearing drag checks pass too; page errors are empty.

These are **partial gestures and committed-frame readbacks**, not full-stroke
pointer certification or a full standalone/hosted interaction matrix. The
close-up images were inspected: the external knob is visible and operable
through its housing window. The probe uses its own browser and camera; it
does not change the pilot's Studio navigation.

The first browser launch inherited the CAD job's 8 GiB virtual-address limit
and Chromium exited with SIGTRAP before loading the page. Running browser
checks separately without that address-space cap resolves launch; CAD jobs
retain their cap. The next probe reached both gestures but its assertion
incorrectly looked for a computed `setting` Port in the retained bank. Reading
each actual input-print `travel` joint fixes the fixture; no production change
was required for either issue.

The updated fork reproducer keeps an independently placed original actuator
alongside the candidate. It reproduces 1.585791236 mm³ source overlap and zero
candidate overlap even after adoption (`reverser-fork-source-and-fit.jsonl`),
so the original finding is not lost when the trial class changes.

Observed framework head `9fb5127fad62e6c66067b34e7d02dd389471fa2d`, viewer head
`c6df93ddd1723f1b9be0fb7e73f19d6f6c2daffa`, viewer API22. The ordinary build
refreshed the stale local viewer bundle through its normal build mechanism.
Final bundle SHA-256:
`329015221a9e2968a2c7dccc80af30f2890d6365a8f19639bcde54db182ef4fd`;
document SHA-256:
`c355f68405435048c9fef949cc78719fce82ac800bbad40dcde0bbea7594d146`.
No framework/viewer source was edited by this work.

Logs: `reverser-installed-{faceted,exact}.log`, `reverser-operating-build.log`,
`operating-reverser-unseated.log`, `operating-reverser-browser-final.json`.
Images: `operating-reverser-browser-reverser-{down,up}.png` and
`operating-reverser-browser.png`. Earlier failed browser reports remain as
environment/fixture evidence, not evidence of a failed mechanical control.
