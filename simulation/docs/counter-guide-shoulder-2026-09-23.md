# Counter guide shoulder: isolated trial

Status: scoped shoulder fit adopted and production checks passing. The whole
operating model remains unfinished; this does not certify the complete guide.
Plan `70c6694` scopes only the measured .30 mm shoulder/ledge obstruction;
nominal guide-face contact and open-direction retention remain separate.

Before implementing the cutter, all four prospective preservation checks pass:
the independent maximum removal leaves one valid solid, adds no material,
preserves all curved native surfaces (including detents), both measured running
planes and pin tip, and the protected fork/reset shoe/stem/back volumes.
The all-five-station source ledge contract fails in both native and world64
geometry: ten expected subtest failures, five tests total in 1.563 s.
Log `_build_checks/counter-guide-ledge-source-red-70c6694.log`, SHA-256
`c0746619eaf769fa2cdf949dd6d14d8c5536a66f1df1b278d607790e8829de19`.

The earlier test measured and asserted the whole guide; it also failed ten
times. Before implementing any fit, its assertion was corrected to the planned
independent ledge window while retaining whole-guide measurements explicitly.
That earlier log is `counter-guide-shoulder-source-red-70c6694.log`, SHA-256
`e201d3b37fe6b543cab04ecfd7fe7404e61dd602730d7bef1733fcc0b60b3aa5`.
No positive whole-guide residual is waived by the localized contract.

The trial raises the underside .35 mm using a named box wholly inside the
independent maximum-removal region. It changes no guide, placement, travel,
spring or motion law. Source geometry remains a retained negative fixture.

The first candidate run has seven tests, five failures in 30.651 s. All
preservation tests and native ledge checks pass; all five world64 ledge checks
remain positive, approximately 1.4–1.7e-15 mm³. Complete-guide world64 commons
remain approximately 5.7–6.0e-6 mm³. No value is rounded down or excused.
Log `counter-guide-shoulder-candidate-70c6694.log`, SHA-256
`b1f0731ee5b471c319b61942f9e513188a177ab69ba7d6075208df61fc59bd40`.
An earlier launch failed to import `Prismatic` from the wrong module; the
correct import uses `machinome.motion.joints`. It is not a mechanical red.

The inspected native sections in
`_build_checks/counter-guide-shoulder-first-sections-70c6694.png` show the
source's .30 mm ledge penetration and candidate's .05 mm gap at full drop,
alongside the unchanged stem and guide. These pixels support the native result,
not acceptance of the still-failing mesh gate. A first-station diagnostic
locates the mesh remnant at the cutter/window corner near station X=60.30,
Y=-7.89, extending down to Z=-17.10000019; both Boolean parenthesizations retain
it. The native shoulder within that window starts at Z=-16.75. The source of
this native/mesh discrepancy is under investigation.

## Refined candidate

Design refinement `e8d3612` moves only the cut's lower X bound from 60.30 to
60.275, still inside the original independently tested maximum region. The
working stem ends at 60.225; the unchanged ledge begins at 60.375. This leaves
.05 mm from the stem and .10 mm lateral clearance to the ledge. Neither the
verification window nor the positive-volume rule changes. Direct float64
tessellation reduced but did not eliminate all first-candidate remnants, so no
framework precision feature was claimed as a fix. The published mesh is still
the same ordinary STL pipeline.

The refined candidate passes nine endpoint/preservation/native-enclosure tests
in 25.356 s (`counter-guide-shoulder-refined-e8d3612.log`, SHA-256
`b31e42ce660e3704d413de8fb809a60318ca3bb25fffa39a2765b6e565d8e240`).
The extended suite passes all eleven tests in 26.048 s, including conservative
continuous native and published-world64 shoulder enclosures and all-five-station
source/.2 mm insufficient-relief negatives on both kernels. Log
`counter-guide-shoulder-continuous-e8d3612.log`, SHA-256
`fd1cc154c5aa40670f25f92f58e598fb37c2d6f25ac6984a5a968a26ffacf9f1`.
The enclosures bound every point throughout the unchanged axial stroke and
have a strictly positive Z separation from the independently measured ledge;
they are not a finite pose sample substituted for a continuous proof.
Whole-guide residuals remain recorded separately and unaccepted.

## Neighbouring and complete-root gates

The unchanged six carry contact contracts pass on the isolated fitted bench:
6/6 faceted in 31.22 s and 6/6 native in 124.28 s, including full two-turn
pin/reset/fork clearance and the same free/blocked working-contact probes.
The unchanged three all-station spring contracts pass 3/3 faceted in 2.26 s
and 3/3 native in 180.51 s, including fixed folds, hook capture and guide seats.
Logs under `_build_checks/`, with SHA-256:

- `counter-shoulder-contacts-faceted-e8d3612.log`:
  `725d9ad11f24d85a631a1e987751da8a381a86e31a6cdaf01fa8dc03abcd84a7`.
- `counter-shoulder-contacts-native-e8d3612.log`:
  `4710164e76208013280f2df08262230dfc25f28cfe60e4b6b9e54c36b1a4bffa`.
- `counter-shoulder-springs-faceted-e8d3612.log`:
  `30c03df57505717bb0b0c6b4883e67072a6e8e95dc16975d46acf7dd013c180c`.
- `counter-shoulder-springs-native-e8d3612.log`:
  `df1bf8bdbbc62dcc6c330004723757c838b1855d13fc6c32d821a7616f11a872`.

The five-test complete-root/frame batch passes in 150.146 s. All 214 bank
coordinates match the explicit pre-fit reference exactly at rest and after
180 degrees of actual crank motion. Every other rigid mesh and all flexible
meshes are byte-coordinate identical; exactly the five counter slider shapes
have confined removal. Frame endpoints, spring/frame clearances, fixed-support
motion and installed fixture identity also pass. Log
`counter-shoulder-operating-trial-restored-e8d3612.log`, SHA-256
`406f4044bc4d774937bf6a2f5dd47039e35c7cf9bb17b8ceb09509c98b65a687`.
The first batch was 4/5 with 30 fixture-identity failures because its override
forgot to restore the shared bench to rest after the preceding stroke test.
The correction restores that required setup, not a tolerance or geometry change;
the first log remains `counter-shoulder-operating-trial-e8d3612.log`, SHA-256
`9cd656868ede3ee2b9c3a69d4ca09c2ad6b648747eeea9b3c499b49e7e93c1f0`.

Before adoption the production-facing shape test fails at all five stations
with .7460249920407725 mm³ of the original material still present. Log
`counter-shoulder-production-red-e8d3612.log`, SHA-256
`8d0300afc998c6b5d7982d370453fcdd38607c87b204c460b24a6052c9960599`.
Adoption substitutes only `OperatingCurta.carry_mechanism`'s counter slider
shapes through the same retained bindings. The explicit pre-fit reference and
all source/insufficient-relief negatives remain.

The first production import refused stale declaration references to the parent
class's replaced carry child. Both radial-ball references now name the current
class's actual `carry_mechanism` child, preserving their paths and laws. This is
an ordinary declaration correction, not a framework change. The failed launch
remains `counter-shoulder-production-green-e8d3612.log` despite its premature
filename; SHA-256 `656666d03d562057631343f84e1f0a322471b3ee59a51d8cf38c9600a228f010`.
The actual production-facing shape and full-bank/other-geometry tests then pass
2/2 in 74.086 s: `counter-shoulder-production-bound-ref-e8d3612.log`, SHA-256
`bf5e6cb55d0f6f5fb1b0575dad536c466e7042bec6b5dc52f6b4e5bd7f399d35`.
The eleven independent shoulder contracts rerun green in 8.764 s; log
`counter-shoulder-post-adoption-contracts-e8d3612.log`, SHA-256
`e89a71b5221fd184b92b55b4f0f5a5dc85096a9b61fedfdf3c3d626f021fe01e`.

The radial-ball preservation test correctly detects the newly changed shoulder
meshes against its historical all-old-shape reference (one failure in 14.498 s;
`counter-shoulder-radial-shape-red-e8d3612.log`, SHA-256
`51b79a697725cbf11104c5cf99f3f33d741c2c94123510cb5c9220ba545fa3db`).
It now compares the ball-only change with the accepted shoulder shape on both
sides, via explicit `ShoulderFittedStaticBallReference`; no mesh is skipped and
the original static-ball root is retained. That unchanged full bank/mesh
assertion passes in 83.204 s through quarter turn, full turn and raised shift:
`counter-shoulder-radial-preservation-e8d3612.log`, SHA-256
`407bfb68c70942e1e55eaffb2c76678636bf35575e4ef2e3f4821814f8f46cd7`.

Final inspected native section image
`counter-guide-shoulder-final-sections-e8d3612.png`, SHA-256
`8df2ae1a5e48f6109f5321793500e582b963a07efce62abad6e532ae1af045bf`,
shows the .05 mm vertical and .10 mm lateral ledge gaps while retaining the
working guide stem. It makes no full-guide capture claim.

The fresh export `_build_checks/operating-shoulder-82bf530-a92541d/` pairs the
adopted root with framework `82bf530` and viewer `a92541d`. It builds successfully,
keeps the exact original program identity
`b81b2ce7af6556c12a68829fa3444d1dc6efc7c110d2cd88aff57fff0b9700f4`,
24 inputs and 25 controls. Manifest SHA-256 is
`0b8f70d9c276f4517df28c629734f020ea266ac5d7051b7714acf78483474a79`;
bundle `feeaed32febb1ede3b267e9f47a6a0fd0a6b39bc149453af338011489b68ff86`;
index `16238dda75b0b88224bd1bcaf0c9dfd77a6f43d75652b2972f4af5ed00111bb2`.

On that fresh export and final bundle, the hosted browser passes all eight
frozen Python-oracle stages with exact equality of every one of 214 coordinates,
including raised-carriage stop, replay, relief, outward motion and retained return.
There are no page errors; exit zero and the final screenshot are observed.
The inspected image shows the complete assembly and final 360.0000-degree
readout. Report `operating-shoulder-eight-stages-e8d3612.json`, SHA-256
`2e0bd4a89a1481d9094579b989e8f7b2b58d55e2f5fd08c7bffa5dd6b31bc314`;
PNG SHA-256 `4f41e684fd752739fa75459bd1ada5dbe92bfd688531d19303dab87e46165c8d`.
This public-handle oracle is not a new all-control pointer matrix.

The fresh whole-root rest survey records 389 rigid occurrences, 236 positive
world64 pairs and zero refused intersections. Every positive remains a finding;
the count is not a list of accepted contacts or a paired attribution to this fit.
Report `operating-shoulder-rest-world64-e8d3612.json`, SHA-256
`e011c78cec8552f51dbf4864230b96f2407d29f479dc16e68af6f1ad6958a1e0`.
The shoulder cycle closes only its named ledge interface. The umbrella remains
12/23; guide retention/tangencies, clearing-loop, zero-clip, selected-input and
whole-machine demonstration/contact obligations remain open.

## Reproduction

Using the configured workspace environment from this project:

```sh
python -m unittest -v simulation.test_counter_guide_shoulder simulation.test_counter_shoulder_adoption
machinome test --faceted simulation/counter_shoulder_contacts.py
machinome test --exact simulation/counter_shoulder_contacts.py
machinome test --faceted simulation/counter_guide_trial.py
machinome test --exact simulation/counter_guide_trial.py
python -m unittest -v simulation.test_counter_shoulder_operating_trial
```

Framework validation used the isolated `cache-folded-law-graphs` worktree at
`82bf530`, not modifications in the framework primary checkout. All five main
project specs validate strictly. The new shoulder spec is synced and the
completed `clear-counter-guide-shoulder` cycle is archived; no whole-machine
task checkbox is changed.
