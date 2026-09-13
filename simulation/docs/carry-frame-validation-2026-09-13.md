# Two-station frame fit — verified local correction

The approved local correction is implemented and satisfies its focused
acceptance checks. Planning: `7d39306`, revised with the
pilot-approved guide-seat-edge exception in `9c58255`. This is a Curta-owned
prerequisite, not implementation of the solid-node/viewer running feature.

## Actual fit and independent measurements

`frame_fits.CarryPassageFrame` derives from the unchanged source `MainBody`.
Only `mechanism.UpperFrame.main_body` uses it. Four fixed tools implement three
contact families at angles 0 and -20 degrees: the source-outline shoulder
offset, the lowered edge and two separate spring-leg windows. The bridge
between the spring legs is retained. No cutter depends on the current pose.

The named `running_gap` defaults to 0.05 mm; construction admits only the
measured 0.04–0.06 mm trial range. Before adding these bounds, all four
out-of-range witnesses (0, 0.039, 0.061, 0.1) were incorrectly accepted; after
the change they all raise. This is a simulation fit, not a print tolerance.

The [native measurement record](evidence/carry-frame-fit-report-2026-09-13.json)
contains both stations and three gap values. At the default:

| Independent measurement | First station | Second station |
| --- | ---: | ---: |
| Lowered-edge normal gap | 0.050000 mm | 0.050000 mm |
| Raised-shoulder normal gap | 0.050000 mm | 0.050000 mm |
| Left spring-window normal gap | 0.050096 mm | 0.050096 mm |
| Right spring-window normal gap | 0.050511 mm | 0.050511 mm |
| Original guide/frame registration contact | 73.575 mm² | 73.575 mm² |
| Retained registration contact | 73.415 mm² | 73.415 mm² |

The complete native contact map has six lands per station, including corner
faces omitted by the initial feasibility probe. The loss is 0.160 mm² per
station, confined to the approved edge neighbourhood; over 99.78% remains.
The exact source-difference contract protects everything outside the eight
independently recorded passage regions. Total removal is 15.303152 mm³;
that number is a report, not an allowed mass budget.

The [protected-feature map](evidence/carry-frame-protected-2026-09-13.json)
locates 53 installed native references relative to the complete removed
volume: 23 M4 fasteners (minimum separation 17.253 mm), ten supports/nuts
(23.225 mm), three fixed frame/bearing neighbours (100.722 mm), four shaft/drum
references (6.298 mm), and every one of the 13 non-selected carry guides
(13.985 mm). The other two guides have the separate approved seat-edge map.
All 105 original cylindrical frame surfaces are checked: only the R49.5 mm
inner frame wall loses area, 4.211119 mm² where the two approved shoulder
passages reach its lower rim. Its remainder, the bores and all other geometry
outside the bounded passages are unchanged. This is spatial preservation,
not structural-strength certification or acceptance of existing hardware fits.

The independent maximum trial envelope uses 0.08 mm outward bounds. The
source shoulder vertices, lower-edge coordinates, separate spring bounds and
seat-edge exceptions are recorded separately in `test_frame_fits.py`; that
test does not import the production cutter definitions.

Twelve local-shape negative controls detect omission of each of the four
tools at both stations, omission/misplacement of station two, a protected-seat
overcut and an ignored gap parameter. They do not write broken production
code. Subsequent normal reruns pass all 17 new contracts on both runners.

## Continuous clearance, not a denser-grid assumption

The rigid-slider certificates cover every point of the native slider over
the complete 4.2 mm translation. They partition its source box, exclude cells
only with a valid zero-volume native source intersection, and require occupied
cells' complete swept boxes to clear the frame. Each swept box includes a
1e-6 mm guard. Every unresolved, invalid or negative-volume Boolean fails.

The [first certificate](evidence/carry-frame-swept-first-2026-09-13.json) passes
13,907 frame checks in 103.05 s; the [second](evidence/carry-frame-swept-second-2026-09-13.json)
passes 13,949 in 102.08 s. Both finish with no unresolved or queued cell. The
second certificate applies the same rigid 20-degree coordinate rotation to
the complete frame and slider: no obstacle or relative placement changes.
The first unoptimized run timed out; the second-station world-axis trial was
stopped after over 59,000 checks to use station-local axes. Neither incomplete
trial is counted as passing evidence.

The spring interval method encloses the published analytic centreline across
the full detent spread range, including the interior minimum of clamped
tangent chord norms. It subdivides curve parameter and spread, surrounding
each interval by a full native ball containing the 0.3 mm wire radius plus
2e-6 mm native-approximation allowance and 1e-8 mm rounding allowance.
Every ball must clear the frame. Independent analytic coordinates agree with
Molejo mesh ring centres at every detent knot and the preload within
2.85e-14 mm. A reviewed source hash and fixed-axis/angle checks bound the
supported spring law; this is not a certificate for arbitrary Python code.
Final guarded-source reruns pass: [first](evidence/carry-frame-interval-first-2026-09-13.json)
370 native checks / 229 clear enclosures in 12.15 s;
[second](evidence/carry-frame-interval-second-2026-09-13.json)
374 / 231 in 13.43 s, both with no unresolved interval.

The installed coupled sleeves also pass full-stroke native swept enclosures:
[first](evidence/carry-frame-swept-first-sleeve-2026-09-13.json) and
[second](evidence/carry-frame-swept-second-sleeve-2026-09-13.json). Each entire
source bounding box, translated through 4.2 mm and expanded by the same
1e-6 mm guard, clears the complete frame in one native check. The actual
installed preload is undone before taking that raised-position bound.

These are frame-clearance certificates, not force, friction, strain, impact
or whole-neighbourhood certificates. The 0.05 mm readings are in the named
relief-normal directions, not a global minimum for every unchanged passage.

## Installed transition reruns

All four 41-pose sweeps pass with zero positive, invalid or signed-negative
contacts. Each uses all 428 bodies (422 native, six source meshes), retaining
inventory hash `af09629ffdd781d4b798e8a0edc400c149d3fbc43139dfab99ccbb3044eac6cb`.
The complete inventory was already retained with the pre-fit evidence; the
new records retain its hash, all candidate neighbours and mesh-only identities.

| Event | Crank degrees | Native / faceted comparisons | Sweep seconds |
| --- | ---: | ---: | ---: |
| [Trip 1](evidence/carry-frame-trip1-41-2026-09-13.json) | 117.060440 | 1066 / 123 | 93.59 |
| [Trip 2](evidence/carry-frame-trip2-41-2026-09-13.json) | 149.935440 | 1517 / 123 | 84.23 |
| [Reset 1](evidence/carry-frame-reset1-41-2026-09-13.json) | 355.016337 | 1074 / 123 | 76.89 |
| [Reset 2](evidence/carry-frame-reset2-41-2026-09-13.json) | 375.016337 | 1585 / 123 | 83.47 |

Each background is the frozen prescribed `099 + 1` fixture; moving slider,
coupled sleeve and spring are independently swept. This proves the sampled
installed transitions, not causal running or continuous neighbour clearance.

## Inspected images

The native before/after sections use identical moving parts and guides in
each column. At both stations, the red source intersections disappear at the
spring lower leg, lowered edge and raised shoulder; the retained guide land
stays visible. These are cropped sections with equal axis scales, not full
part silhouettes or force evidence.

Both OpenSCAD assembly views use `CarryFrameInspection`: `099 + 1`, with only
the enclosing shell hidden for inspection. The frame, carriage, guide supports,
fasteners, springs and neighbouring stations remain. The close-up shows both
selected slider/spring passages; the wider view shows their support blocks
and adjacent shafts/stations. The upper carriage cover still occludes the
upper mechanism. No obstacle is omitted by the collision checks, which always
use the complete `Curta`, and submillimetre gap claims come from measurements.

| Inspected image (ignored generated artifact) | SHA-256 |
| --- | --- |
| [First-station sections](../../_build_evidence/carry-frame-sections-first.png) | `e816223849630118e870bf25cb4075ebe9df79a143e22d603d57af05641fa20c` |
| [Second-station sections](../../_build_evidence/carry-frame-sections-second.png) | `f89a4f3b878f1817915da3576742d598249e478d288d0f93dffedad612204298` |
| [Assembled close-up](../../_build_evidence/carry-frame-assembled.png) | `b5e555fc06d80ae6b93ec90dec63c07332de6a9ad8ecb53d311744c6fbae102f` |
| [Assembled context](../../_build_evidence/carry-frame-context.png) | `bb665309981dfa12ed8f5fb744c71a607d3330af1ea8e4dc17cc32406bc1826c` |

Reproduce sections with `python -m simulation.tools.carry_frame_sections`.
For assembly views, use `solid snapshot simulation/views.py:CarryFrameInspection`
with `--imgsize 1600x1200 --projection ortho` and respectively
`--camera 120,-55,-10,48,-18,-12` and `--camera 190,-100,50,40,-18,-35`.
Leave the renderer at its OpenSCAD default and provide `-o` with an ignored
image path. The full-root build is restored after inspection.

## Root publication

The finite full-root build passes in 56.61 s, then the
[artifact inspection](evidence/carry-frame-publication-2026-09-13.json) passes.
The schema-4 document retains 9969 bindings, eight drivers, seven instructions,
390 rigid occurrences and 38 flexible occurrences. Every referenced artifact
exists and is nonempty, all references stay inside the build directory, and
there is no retained build-error record. The frame's published artifact path
matches the actual operating `CarryPassageFrame(running_gap=0.05)` instance;
its native volume is 199441.6249710615 mm³ and its STL hash is
`3e522b2b272233c6748108955a61d5dba8df2dd195566ff95e7714b34ce68187`.
The document hash is
`6e8b0eb44a3ba79475767e56597a77a2b3b4641789b7aa4cd27f2d78820ddee2`.
The generated inspection manifest retains a hash for every rigid occurrence.

The first inspector launch failed because the helper created an unbound
`Curta` before assembly. Explicitly binding the existing default drivers fixes
the helper; no framework or model change was involved. An initial regression
launch was stopped when that helper changed and its failure-name parser was
corrected to keep `.FAIL!` separate from a test name. Three parser cases pass.
Those incomplete launches are not counted as a full regression.

## Environment and reproduction

Run inside this Curta worktree with the workspace `.venv/bin/python` / `solid`.
Set `PYTHONPATH` to this worktree followed by
`/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation`, and
`SOLID_BUILD_DIR=_build_open_run_evidence`. Each CAD job is sequential, with
`ulimit -v 8388608` and `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
MKL_NUM_THREADS=1`. Diagnostic jobs have bounded timeouts; the regression
runner allows up to 2400 seconds per module, including the long native bell
spring sweep, and stops on any unexpected result or source drift.

Framework content is `6e41f2da132a8604f9b68895967247fb8876fc4d`, not merely the
installed metadata's `solid-node 0.6.0`. No framework feature code is changed.
Molejo's clean checkout is `e76c9039cf906cfc0005324d78ccee7116e0ff4a`.
The interpreter is Python 3.12.3; package metadata records CadQuery 2.7.0,
cadquery-ocp 7.8.1.1.post1, molejo 0.2.0, NumPy 2.2.6, manifold3d 3.5.2 and
trimesh 4.4.9. Source checksums accompany the native and regression records.

Commands under that guarded environment:

```sh
python -m simulation.tools.carry_frame_fit_report
python -m simulation.tools.carry_frame_protected
python -m simulation.tools.carry_frame_interval --station first
python -m simulation.tools.carry_frame_interval --station second
python -m simulation.tools.carry_frame_swept --station first
python -m simulation.tools.carry_frame_swept --station second
python -m simulation.tools.carry_frame_swept --station first --part sleeve
python -m simulation.tools.carry_frame_swept --station second --part sleeve
python -m simulation.tools.open_run_transitions --event trip1 --samples 41 --kernel exact --inventory
python -m simulation.tools.open_run_transitions --event trip2 --samples 41 --kernel exact --inventory
python -m simulation.tools.open_run_transitions --event reset1 --samples 41 --kernel exact --inventory
python -m simulation.tools.open_run_transitions --event reset2 --samples 41 --kernel exact --inventory
solid build simulation/curta.py:Curta
python -m simulation.tools.carry_frame_publication
python -m simulation.tools.carry_frame_regression
```

## Full regression

The [complete regression record](evidence/carry-frame-regression-2026-09-13.json)
retains all 78 module runs, commands' log paths/hashes, named failures,
resource readings and SHA-256 hashes of all 191 simulation source files.
Every module matches the recorded baseline plus the new passing contracts;
the source list and every source hash remain unchanged throughout the run.

| Runner | Modules | Passed / total | Summed process seconds | Maximum process RSS, KiB |
| --- | ---: | ---: | ---: | ---: |
| Faceted | 39 | 159/161 | 1064.91 | 822576 |
| Native | 39 | 160/161 | 3078.32 | 1275384 |

The complete sequential controller takes 4149.91 s, including its source
checks. Its exit is zero because there is no new or changed regression, not
because every individual test is green. The two existing findings remain:

- `ShaftBearingTest.test_tip_clears_frame_through_a_turn`: faceted volume
  `3.240210274700639e-06 mm³`; its native rerun passes.
- `CurtaTest.test_assembly_integrity`: source-STL `digits_cover` /
  `upper_housing` volume `224.32750533797636 mm³`, failing on both runners.

No contact epsilon or hidden part is used. The regression controller's success
criterion is matching the named baseline plus green new contracts, not zero
failed tests or whole-machine acceptance.

## Accepted scope and remaining running work

All 17 new contracts pass on both runners, including the dense motion grid,
gap bounds and source preservation. Source/gap contracts use native geometry
in either runner; the collision contracts also exercise the faceted path.
The complete faceted/native regression preserves the named bearing-facet
and housing/thread findings. The lightweight rerun passes 30 Python and
five calculator JavaScript tests. All focused implementation and evidence
requirements are met; only this prerequisite is eligible for closure.

No `simulate-the-curta` task is completed by this report. Home-window,
initial-snapshot, outgoing-slice and causal running evidence are separate.
The pilot must explicitly authorize actual solid-node feature development
once the readiness evidence and coordinated proposals are ready.

### Next evidence step after this correction

Return to the existing acceptance dossier, not a wider frame-repair campaign.
First verify the selected input's complete 0–9 travel while stopped in a
measured home window. Include both the `099` start and the post-carry home
configuration whose second reset is still pending beyond 360°; a selector
change must not manufacture a reset of that retained state.

Do not sweep this state by changing the old root's `operand`: the existing
`transmission.channel_values` recomputes `previous_transfer` from that value,
and `carry_motion.engagement` uses it to reconstruct the retained second
carry. A pure, no-CAD evaluation of
`channel_values(11)(None, None)(100, operand, 1, 0, 0)` confirms this:
with operand one its first/second carry fractions are `(0, 1)`; with operand
zero they are `(0, 0)`, even while the completed result is held at `100`.
This is existing prescribed behaviour, not a failure introduced by the fit.
Freeze the selected start/post-carry assembly once, then independently
move the actual selector knob group and keyed input group through 0–54 mm,
and the selector shafts/number roll through their corresponding 0–324°.
Check their source-frame bindings at the existing seated settings first.
Keep the drum, output shafts/dials and carry parts fixed during each travel
probe, retaining every installed neighbour in the collision inventory.
The earlier two-phase pinion/drum check does not cover these other bodies.

Then close the selected slice's initial-state record and locate its outgoing
boundary at the first unsupported physical interaction, not merely at a
calculated decimal overflow. Keep all neighbouring obstacles and state the
fixed boundary conditions. The outgoing interface is the hundreds dial's
`ResultRegister.p_10205_1.number_roll_carry_pin_half` against
`ResultsLever3.tens_slider_for_results`. Its `Type2HalfPin` has 189° local
clocking, whereas the first two `HalfPin` mounts use 180°; verify the actual
installed third frame rather than copying a first-station threshold.
These are the existing running campaign's evidence
obligations, not additional claims proved by the frame fit or a requirement to
repair unrelated whole-machine findings first. Complete the coordinated
repository-owned proposals and ask the pilot before actual solid-node feature
implementation; no such permission is inferred from this prerequisite's tests.
