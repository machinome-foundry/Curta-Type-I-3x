# Mid-cycle counter reversal: confirmed missing restraint

The operating root is **not finished**. A physical reversing request at crank
90° admits a positive gear/drum common. This is a project-law gap, not evidence
of a framework admission failure: `RunningReverser` declares only the fixed
housing/spacer range, with no drum-dependent bound. No production law, print,
placement, source asset or accepted requirement changes in this checkpoint.

## Pinned reproduction

Project content `e4ef8755e80e25e677aa40072d06c97dda21746b`, framework main
`82bf530cacae1fd7b841a47a35c961eb438b79f8`; viewer main remains `a92541d` and is
not used by this native/Python diagnostic. Framework CI commits `a87abc5` and
`e05d9c5` were independently reconfirmed as ancestors of framework main.

An untouched `Sim(OperatingCurta(), dt=.1, meshes=True)` receives an ordinary
crank request to 90°, duration .5 s, followed by .5 s of running. The command
completes. The counter-ones shaft remains 134°, crank lift is zero. Subsequent
requests move only the reverser and its connected axial/follower coordinates;
the probe never seeds a register, poses a gear independently or prepares the
crank for the reverser.

The complete printed pair is:

- `Curta.transmission.turns.ones.p_10218_1`
- `Curta.main_drive.stepped_drum.main_axle_step_drum_1.main_axle_step_drum_top_1`

Native checks use `machinome.exact.intersect_shapes`, including the resolved
interior-witness guard. Faceted checks use the published local meshes with
their retained world placements in `Manifold.Mesh64`. No positive volume is
waived by an epsilon.

## Observed contact

The native nine-tooth drum band's top is world Z = −48.2 mm. The descending
ones pinion's bottom reaches it when the knob is at 1.0575 mm. This is a
fixture-specific first-contact height, **not a universal reverser bound**.

| Requested knob height (mm) | Native common (mm³) | World64 common (mm³) |
| --- | ---: | ---: |
| 1.0675 | 0 | 0 |
| 1.0575 | 0 | 0 |
| 1.0475 | 0.02353507611251452 | 0.023458419217706056 |
| 1 | 0.1353266876469794 | 0.13491142006933782 |
| 0 | 2.4888342988989 | 2.481290385366863 |
| −4.9425 | 3.530261416877793 | 3.519563077511023 |

Every request currently reports `completed`, including the penetrating ones.
At 1.0475 mm the positive native common spans Z = −48.21…−48.2 mm,
X = −24.4627565819035…−22.957519635462795 mm and
Y = 25.19387598931957…27.489809721425278 mm. The reviewed native section at
Y = 26.3 shows the .01 mm gap and .01 mm penetration on opposite sides of
the same contact. Its axial scale is explicitly expanded.

An earlier exploratory probe checked only the ones pair at crank 171.25°
and 180° and six lever heights; its zero faceted samples do not certify a
clear path. The subsequent 90° probe checked all six counter inputs against
both complete drum prints at nine heights. Only the pair above was positive
at those samples. These terminal observations narrow the finding; they are
not an all-angle, continuous-path or whole-machine certificate.

## Red-first regression and retained evidence

`simulation.test_running_reverser_wrong_order` runs **two tests in 47.697 s**:
the free-play test passes; the penetration test fails in both geometry checks
and its terminal-status assertion (**three failures, exit 1**). This is an
intentionally open acceptance regression, not a passing implementation.
The test checks actual material before asserting `blocked`, so its failure
does not depend solely on an assumed command status.

Reproduce from the project with the workspace Python:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=. \
  /home/asa/devel/machinome-studio/.venv/bin/python -m unittest -v \
  simulation.test_running_reverser_wrong_order
```

The separate section tool completes with exit 0; that means its diagnostic
ran, not that the operating mechanism passed:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=. \
  /home/asa/devel/machinome-studio/.venv/bin/python \
  -m simulation.tools.reverser_wrong_order_sections \
  --image _build_checks/reverser-wrong-order-e4ef875.png \
  --report _build_checks/reverser-wrong-order-e4ef875.json
```

Use new filenames on a rerun; the tool refuses to overwrite evidence. The
report retains both full 214-coordinate banks, independently restored from
the prepared 90° snapshot before each request.

- JSON SHA-256: `826727a408247be94b008d598f39fc2d403f04141f64af6b131c63623ca4dda0`.
- Inspected PNG SHA-256: `a1b79ff2c82c37305c24ce1deef0b26f4c601e5fdcd754ab3a4918b532b3d2f7`.

The table and test outcome above are reconstructed from completed terminal
calls, not claimed to be a raw saved transcript. The two-pose JSON is emitted
directly by the checked-in tool. Exploratory volumes are not silently promoted
to a regression matrix.

## Phase-envelope continuation

On project `8ca74d5`, `tools/reverser_tooth_envelope.py` adds an independent
pose instrument from the **complete installed prints** in an untouched
production root. It rotates each input about its declared shaft axis, rotates
both complete drums about their installed main axis, and applies the lever
and drum axial displacements. It does not mutate the run, change print material
or normalize the source to an assumed ideal gear. Each report names its station,
crank, shaft, lever height, drum lift and kernel. All five shaft sectors are
measured over a full 360°; no sector is silently repeated.

Two fixture tests pass in **91.604 s**. They compare the instrument with real
requests at the near-contact heights, at crank 171.25° with a nonzero retained
shaft phase, and at crank 90° after raising the drum 9 mm. Native and mesh
world bounds match within coordinate-rounding precision (1e−10 mm); contact
classification must match exactly, and every zero common must remain exactly
zero. Comparing the final digits of two positive volumes is not an overlap
tolerance. The initial tool attempt mistakenly read the axis off the bound
value instead of the class joint declaration and stopped before measurement;
that local diagnostic error is corrected, not a framework limitation.

An additional real-history test passes in **25.530 s**: lower the reverser at
home, then turn to 90°. The ones shaft is now 231.6°, instead of the red
fixture's 134°. Requests to −3, 0, 1.0675 and 3.9075 mm all complete with zero
native/world64 common in the ones pair and without changing crank or shaft
phase. This is a sampled withdrawal counterexample to a home-only lock, not a
whole-bank continuous-clearance certificate. The original penetrating-history
test remains red; this passing test does not replace it.

The first world64 survey samples nine crank angles (0, 75, 90, 100, 120, 150,
170, 180, 270°), two lever heights (0 and −3 mm), and 181 shaft angles from
134° through 494° at 2° spacing. All **3,258 rows** complete; 790 have a positive
common and none has a negative volume. At crank 90° / lever 0, the first shaft
sector's free samples are 154…174°; at lever −3 the whole sampled sector is
clear. At crank 170°, both heights have free samples 160…178°. These are
observations, not interpolated bounds or evidence of all intervening points.

The boundary instrument retains every observed transition and both its free
and positive endpoints. It performs 16 bisections within each observed bracket;
it explicitly does **not** claim to exclude unsampled islands. Three unit tests
pass, including two disconnected contact islands, preservation of a positive
1e−30 mm³ common, and refusal of unordered, negative or nonfinite measurements.
The nine-angle survey yields 18 records and 70 boundary brackets; each active
row has ten boundaries across the five shaft sectors.

Native checks at crank 90°, lever 0 confirm the first sector's angular gap:
shaft 152° overlaps by 0.008850995541473169 mm³, 153°, 154° and 174° are clear,
175° overlaps by 0.004657491704910437 mm³ and 176° by 0.018376175081854292 mm³.
Refinement gives these **clear-side endpoints**, with positive commons retained
on the other side of each bracket:

| Kernel | Lower clear shaft angle | Upper clear shaft angle |
| --- | ---: | ---: |
| Native | 152.23562622070312° | 174.0721435546875° |
| Published world64 mesh | 152.22329711914062° | 174.07217407226562° |

Thus mesh-only admission would be too permissive at the lower boundary.
The limiting native positive samples are 3.7497067733704725e−9 and
8.213639765078992e−13 mm³; neither is waived. Combining measured bounds must
use the stricter free side of both kernels, then validate interpolation and
the full retained path. No runtime table is adopted from this coarse survey.

Raw generated JSONL under `_build_checks/` (all producer processes exit 0):

- `reverser-angular-survey-8ca74d5.jsonl` — SHA-256
  `355c2885cca1151c1bef1d1018979a1e08b3fcf7eb6f1e73da23ceb7e8726c8c`.
- `reverser-angular-boundaries-8ca74d5.jsonl` — SHA-256
  `d011c41ca6f75738e7e2f12c5c15409533914d33a05d8c52142e23c501d4799e`.
- `reverser-angular-native-brackets-8ca74d5.jsonl` — SHA-256
  `933cedc3f462c7d16588018bbea8b864615fed26e0626e3d70e9122edc185816`.
- `reverser-angular-native-boundaries-8ca74d5.jsonl` — SHA-256
  `9787162f1ba0e0413939ca49860cb60f50f8db8ae74d3bf3ad236350c260fe37`.

For example, reproduce native refinement with the workspace Python, from this
project, setting `PYTHONPATH=.` and one BLAS/OpenMP thread as above:

```sh
python -m simulation.tools.reverser_tooth_envelope --crank 90 --height 0 \
  --shaft 152 --shaft 153 --shaft 174 --shaft 175 --boundaries --kernel native \
  --output _build_checks/reverser-angular-native-boundaries-rerun.jsonl
```

For the faceted survey, supply the nine `--crank` values above,
`--shaft-step 2 --height 0 --height -3`, and a new output path. Adding
`--boundaries` retains/refines the observed transitions. Every existing evidence
file is preserved. The instrument supports stations 1…6, but the current
fixture and phase evidence are explicitly **station 1**, not proof of the
five different higher-counter prints.

## Remaining implementation

Measure the axial admission envelope against **actual retained shaft phase**,
crank rotation and crank elevation for all six inputs and both request
directions. An input may be free in the same crank pose after a different
physical history. Neither a global `crank == 0` lock nor a universal 1.0575 mm
floor follows from this witness. Crossing a blocked band must stop even when
the requested endpoint lies in another clear band.

Express the measured restraint on the existing connected reverser joint;
preserve available play, register history and ordinary parked-crank reversal.
Require red-to-green actual-root contact, long/short requests, relief, repeat,
snapshot/replay and viewer parity before adoption. Tasks 6.2–6.5 remain open;
this finding does not waive the clearing loop or whole-assembly contacts.
