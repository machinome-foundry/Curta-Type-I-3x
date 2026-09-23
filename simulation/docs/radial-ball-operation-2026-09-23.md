# Radial positioning-ball adoption

Status: scoped radial-ball operation is verified and adopted. The whole
operating Curta remains unfinished. This record
continues the [rejected orbit and measured contact investigation](positioning-ball-following-2026-09-22.md)
and the separately completed [ring passage](thrust-ring-passage-2026-09-23.md).

## Scope and preserved references

The source sphere remains R3.75, centred initially at (9.627860318, 0, 30).
`StaticBallOperatingCurta` preserves the previous root. `OperatingCurta` derives
from it and adds only the radial positioning declaration and its two-contact
`Follow` law. `RadialBallTrial` is independently based on the static root;
the rejected orbit cannot accidentally inherit the new radial coordinate.
`ReversedRadialBallTrial` and `PullingBallTrial` retain incorrect-axis and
endpoint-difference negatives. Original/fitted ring fixtures explicitly select
either the static or radial motion model.

There is no new ball control, source edit, resized ball, added support, force
model or automatic action preparation. Original 213-coordinate rest digests
remain unchanged. Updated fixture assertions require exactly 214 coordinates,
check the named ball displacement is zero, then remove only that new coordinate
before hashing the original bank. They do not replace the historical digest.

## Prerequisites and red evidence

Framework `f4c48f61a88f183f7e11ccb3e0bbc7158b8e6b9d` and viewer
`fe1a7082d1f4e7907ae50c0268e6d26fd19e444b` are separately integrated on their
main branches. This project uses the pinned framework worktree
`machinome/WTs/follow-two-clearance-surfaces`; the framework primary's
untracked `docs/examples/v8-engine/` is untouched. Neither package was pushed
or published. Project plan `a139fe0` follows the adopted ring at `3f7e0c9`.

The production-facing geometry test fails twice against the static root:
missing radial coordinate and unmoved sphere after a quarter turn. Log
`_build_checks/operating-radial-ball-production-red-a139fe0.log`, SHA-256
`98792070f48274ae9dfa6083c73e78b13d1a4f41ba5f9d5c3de721f9b357fec2`.
The earlier native/world64 static and orbit collision witnesses remain in the
linked investigation. Its continuous native bell and conservative mesh
enclosure proofs remain prerequisites, not replaced by endpoint samples.

All six candidate demonstrations passed every ball-neighbour comparison:
389 rigid occurrences plus 39 flexible leaves means 427 neighbours per pose.
Addition/carry/subtraction had 135 samples in 819.671 s; overflow/shift/clearing
had 163 in 799.140 s. Both reports have zero positive samples and no missing
neighbour, with arithmetic and command outcomes checked. Logs:

- `positioning-ball-all-neighbours-group1-3f7e0c9.jsonl`, SHA-256
  `d8f9f567f7a31aa054151dc5a98be279bb2bc1c59c39072e64f9ae81c33074ab`.
- `positioning-ball-all-neighbours-group2-3f7e0c9.jsonl`, SHA-256
  `f90a368c67645acfc6d4dd81b662fb131e245cd5f2879882475920b1b579e7f8`.

These are finite admitted-motion samples beside continuous proofs of the four
critical interfaces. They do not waive any contact between other parts.

## Contact and history

With the carriage raised to 6 mm, a crank request stops near
0.36119713971311285 degrees, ball displacement -1.2252018554755857 mm.
At crank 90 degrees the ball is outward at 2.213142830078919 mm; raising the
carriage then stops near 1.2183680966576502 mm without turning the crank.
Explicit relief permits continued action; free return does not pull the ball.
The candidate reverse-contact test, including idle, retry and exact replay,
passed in 110.600 s. Log `radial-ball-candidate-reverse-contact-a139fe0.log`,
SHA-256 `3f550bb6f3c3240d84cca469d7f7cea5e08d71a21f7538dda13b563f3199a779`.

The initial long/short test incorrectly required bit-identical banks for
different per-tick input trajectories. Sol's read-only framework review found
the existing running-bound specification explicitly promises the same contact
within its agreement tolerance. For .1/.5-second requests, eight crank-driven
coordinates differ by at most 5.275074821398107e-11 degrees; four lift-driven
coordinates differ by at most 2.1826984664130578e-12 mm. The ball and every
unaffected coordinate are identical. Both authored contact gaps remain
non-positive. The corrected test uses the existing 1e-9 relative/absolute
agreement only on the explicitly identified dependent coordinates, checks
physical feasibility without an epsilon, and retains exact same-command
snapshot replay. No framework mutation or geometry tolerance was justified.

The first transverse capture test exposed a native/mesh discrepancy at the
outer radial position: at Z+.2 the native Boolean reports valid empty while
world64 reports 0.16039406966617248 mm³. The 72-row guide diagnostic preserves
these results and invalid native commons rather than treating them as proof.
Sol's independent review confirmed a strict interior point in both exact
solids, using classification tolerance zero. At the upward .2 mm displacement,
the point (11.541571853564232, 3.0652117978127276, 32.321879856111245) is inside
the frame and ball, whose centre-to-point radius is 3.739994196 mm <3.75 mm.
The exact surfaces also yield a 9.05659788 mm intersection curve. Thus native
empty is a false negative, not merely tessellation disagreement. Rotating the
equivalent source sphere did not cure it; a fresh analytic sphere could return
the whole ball, which is also wrong. No reparameterization is an accepted
clearance proof.

The separate framework correction is now integrated at `83aad09` (planning
`c5ec9c0`, archived `refuse-false-empty-exact-common`, ADR-142). The public
`intersect_shapes` helper refuses an empty common when its bounded native
section search finds a strictly interior witness in both solids. Unknown
classification and failed section verification also refuse acceptance. This
finite guard does not certify every empty Boolean and invents no overlap
volume. The original native source sphere and frame remain unchanged.
Framework validation passed 3,595 tests and 2,131 subtests, with four skips;
98 post-archive focused tests and seven subtests also passed. The primary
checkout still contains only the untouched untracked V8 examples.

The initial integrated guard source SHA-256 is
`9eb6be3b251ec92473a99096f884f323d6086e690e315a309bf38c7c4d8b2e93`.
Production geometry passed all three tests against this source in 60.824 s,
including strict interior witnesses for both outer axial capture directions.
Log `operating-radial-ball-final-guard-geometry-9eb6be3.log`, SHA-256
`0aa829e771868d9eb5273679e4e557c2723d4cc71cdbd56bbb1e074c750907b3`.
The continuous native bell/ball proof passed 2,467 checks covering 1,264
certified intervals in 560.754 s, refining 200 refused coarse enclosures;
the retained bank stayed unchanged. Log
`operating-radial-ball-final-guard-interval-9eb6be3.jsonl`, SHA-256
`70966f9b18cb10d42c31d66d10273a947f1d7174c19071ad266f85c34403702f`.
The conservative mesh/native-frame proof passed 667 checks covering 604
intervals in 18.797 s. Log
`operating-radial-ball-final-guard-mesh-enclosures-9eb6be3.jsonl`, SHA-256
`86d419e9c75801ec0ef6e3aa691f20df6bc7dac6891e504d90be291b1d6e87c2`.
Earlier partial audits against an intermediate guard were stopped and kept
as partial evidence, not counted as completed acceptance.

The production root also passed all six full guarded ball-neighbour audits:
135 samples for addition/carry/subtraction (877.153 s), 163 for
overflow/shift/clearing (873.106 s), each against all 427 other rigid/flexible
occurrences, with zero positive samples and expected arithmetic/outcomes.
Logs `operating-radial-ball-final-guard-neighbours-group1-9eb6be3.jsonl`
and `operating-radial-ball-final-guard-neighbours-group2-9eb6be3.jsonl`,
SHA-256 respectively
`8a972edb62c4616c2841f344c3a0e980e764cbc3948efd6598220d8b6a1b98cd`
and `3ca5e196eb7829a29e8e088b81644d1ef1cbef786f4ad2aa67fcd075d7377764`.

### Boundary-witness correction and repeated proof

The later [carry-guide diagnostic](carry-guide-contact-2026-09-23.md) exposed
zero-tolerance native classification calling a nominal boundary point IN.
Framework `5e1404e` resolves this by requiring a witness's distance from every
face to exceed that face's native uncertainty. It does not zero a positive
common or introduce an overlap allowance. The corrected guard source SHA-256
is `1529c4c75fff7e1879752dee2d22597d0afb2262ebdfeeebf72cc09ea6ffc7dc`.

The unchanged production ball passed all three geometry tests again in
56.727 s, retaining the two strict-interior negative controls. The continuous
native bell/ball proof passed 2,441 checks over 1,251 certified intervals in
528.065 s, refining 187 refused coarse enclosures. The conservative
mesh/native-frame proof again passed 667 checks over 604 intervals, in
16.930 s. Both interval proofs leave the retained bank unchanged. The lower
refinement count reflects resolved boundary candidates, not fewer requested
path intervals or changed ball/profile geometry. Logs and SHA-256:

- `operating-ball-resolved-witness-616c7bd.log`:
  `ba46c9c6f25534238b3af51a6c0b6112ef9bbf4f686e76938a321b2b68171e95`.
- `operating-ball-resolved-witness-interval-616c7bd.jsonl`:
  `d57230f6de6d5a4d874ffec1fa337db3e3efefb84e4e568107fb72a2065fc1b3`.
- `operating-ball-resolved-witness-mesh-616c7bd.jsonl`:
  `8f2001e8c2060b63cb4ffe79b0dbf5790b9e56c008e78937d1c6a271b3efc827`.

The six-demo neighbour audits above remain explicitly pinned to the earlier,
more conservative guard; they are not relabelled as runs of this correction.

## Current production viewer artifact

The export in `_build_checks/operating-radial-ball-a139fe0/` uses the production
root from `a139fe0` plus this recorded implementation, document version 12,
214 coordinates and the integrated API-25 viewer bundle. SHA-256:

- `manifest.json`: `bab5b1248bf8f100b764bf37bfd00065770df876bb83ec191b44549a9727569b`.
- `machinome-viewer.js`: `732087f7dd8ef22d51b3c2cb45f30b085966eab5d5e090485626cb0d50fe8530`.
- `index.html`: `16238dda75b0b88224bd1bcaf0c9dfd77a6f43d75652b2972f4af5ed00111bb2`.
- Python eight-stage complete-bank oracle:
  `0c6d2409d50a8cd5f9e7071a32d20c7018bcbfee39d6034b7481bfc310b38962`.

Exact production source hashes used by this export:
`running.py` = `337f3ae77b70d5e5138787a706b6bb8f528001d4102c2bfdf4b52f5fb47d800f`,
`positioning.py` = `2c757f98f9bcde3d55430f0fd1cb1a4a8567940628313faf56e28002554ea2a5`,
and the unchanged profile =
`cf0382d6cea269bff7c66dfdf8651bd857f5457396ffec80778fe6ca7d591af4`.

The hosted public handle passed all eight stages with bit-identical complete
214-coordinate banks: rest, lift, blocked crank, restored replay, relief,
post-relief turn, outward turn and retained return. All 25 controls and the
canvas were present; no page errors. Report
`operating-radial-ball-hosted-a139fe0.json`, SHA-256
`6ca3802180684addd266cbf4917a2c0565cb9dcbf4b8f3fbba85f0db178413c4`.
The reusable viewer-owned archived `trial_browser_probe.py` checks actual
exported assets despite its historical trial name. Its current invocation is
against this production artifact, not the older trial. The final full-assembly
image was inspected with the visible crank readout at 360 degrees.

The unmodified auto-mounted standalone page passed a real crank-part pointer
gesture: visible crank readout 0.0000 to 1.0000, terminal `completed`, observed
pointer release, all other visible inputs unchanged and no browser errors.
The screenshot was inspected: coherent complete assembly, crank controls and
the expected readout/outcome. This is visible four-decimal evidence, not hidden
full-bank inspection. The standalone page has no documented live-bank lookup;
the hosted public `run().state()` is the complete-bank parity surface. No
remount, hidden handle or speculative viewer API is used to disguise that limit.
The capture harness's explicit 180-second screenshot cap changes no simulation
or command deadline; prior paired viewer evidence measured slow software-renderer
readback on both v11 and v12 exports.
Standalone report SHA-256:
`ff80a8d44ffe5c0e47e853fd552ab9ec738ecfb06bdc02b6ae95e7a4fbf9b396`.

The five-panel native/source-mesh section image was also inspected: actual
admitted rest, outward 90 degrees, retained return 360, raised-carriage crank
stop and outward-bell lift stop. It shows the sphere's fixed axial height,
radial displacement, retained return, ring passage and approaching collar.
These are poses reached by normal requests, not manually shifted drawing
copies. Image `operating-radial-ball-sections-a139fe0.png`, SHA-256
`6113731982a679908215da09a02b5a1817c0c90eb1a3f12691c2bef09cd643c6`.

Paired preservation and negative tests passed 5 tests in 502.312 s: all other
rigid/flexible meshes and original coordinates remain identical through legal
motion; original source-ball material is unchanged; static and reversed-axis
models retain positive geometric counterexamples; the pulling-law variant
fails retention; both explicit static and production radial ring comparisons
pass. Eight legacy native/orbit tests passed in 221.321 s, including the
unchanged initial-bank digest and independent installed result-bank geometry.

## Final acceptance and remaining work

The final focused gate on integrated framework `83aad09` completed 24 tests
in 87.637 s: 23 passed, while the browser async-barrier test could not launch
Chromium under the CAD process's 8 GiB virtual-address-space cap. This is not
a green combined run. All 14 pointer/standalone-report tests, including the
same browser case, passed in 0.813 s without that cap. No code or assertion
changed between runs. Logs `operating-radial-ball-final-focused-83aad09.log`
and `operating-radial-ball-final-reports-no-vm-cap-83aad09.log`, SHA-256
respectively `245b7b44a5f306ae4fd6b054980610a10528f7a3d7634bebcd7caf141a6a8c2e`
and `dcad22b5bdf97b6355dc7de75350fa6d8405699d40cc564439f9761328dc607f`.

Production history passed four tests in 432.608 s, including both contact
directions, retention, explicit relief, idle/retry and exact snapshot replay.
Log `operating-radial-ball-history-green-a139fe0.log`, SHA-256
`7d6bb68792da7e0ab1ce61464bd838c5cf8c9552ebdf3a8580ea60ca9c6da3d6`.
Twenty affected faceted fixture tests passed. Their final guarded-native
rerun also passed all 20: collar 4/4 (247.10 s), clearing carrier 3/3
(52.56 s), lower frame 6/6 (10.70 s), crank coupling 7/7 (131.24 s).
Log `operating-radial-ball-old-fixtures-final-guard-exact-9eb6be3.log`,
SHA-256 `63208506f3474664be84ba69ec37d06f1ca3e050f37faf94c14861386446e016`.
A stale test-only crank/lift
bench lacked the independently operated reverser binding; its red unbound-port
error was repaired in that fixture, without changing production controls.
The seven focused ratchet/limit tests then passed in 32.214 s.
All 15 carriage/clearing interlock, operating lockout and marker tests also
passed in 1,298.878 s. Log `operating-controls-interlocks-a139fe0.log`,
SHA-256 `73289610e7ac18cad102834bb7f1ebff97f3358e9061a11a524b5eb39ace0054`.
The separate 14-test arithmetic/law/partial-input process loaded the old
crank/lift fixture before its repair. It completed with 12 passes and exactly
the two known unbound-reverser fixture errors, not a green batch; all six
production arithmetic tests and the partial-input history test passed.
The corrected seven-test ratchet/limit batch above supplies the focused
replacement evidence. The original log is retained as
`operating-controls-arithmetic-a139fe0.log`, SHA-256
`1dd2137cf0625bb2fcf39928f44a93816b1360edfbf12f3b6832d7818c57aa93`.

The exact six-demo replay gate passed: both tests completed in 2,531.238 s,
including two complete executions of every demonstration from the same
initial snapshot, with identical terminal outcomes and retained snapshots.
Log `operating-radial-ball-six-demo-replay-a139fe0.log`, SHA-256
`6526b6d041723c5b4c18466fb9d6f890e3dc48e2ba33502dc140bbb41ce282fd`.
This closes the local radial-ball acceptance, not overall operation speed:
Sol's no-mesh measurement found five production crank ticks took 37.18 CPU
seconds versus 4.55 with the static reference. Independent framework/viewer
performance work remains in their own repositories and must preserve this
verified behavior.

The later expanded reverser/clearing process also completed successfully:
eight tests in 3,189.725 s, including all 24 carriage-position × subtraction ×
counter-reversal combinations and the all-digit/all-station bidirectional
clearing-law matrix. Log `operating-controls-reverser-clearing-a139fe0.log`,
SHA-256 `67343c5b266e66c13795e5f1477c19a0e82be3c7e4fd1ea23729508825343779`.
It used the frozen production graph and pinned prerequisite framework
`f4c48f6`; it is not relabelled as a performance-candidate run. The subsequent
paired package optimization and its exact-state gates are recorded in the
[reconciliation continuation](reconciliation-2026-09-22.md).

The new full-production ratchet case reaches 10 degrees with input 3, then
requests reverse travel to zero. It checks the independent measured stop
9.342758620689654 degrees, physical crank sign, seated pawl, unchanged operand,
bit-identical complete bank on three retries, and exact snapshot replay.
The same contract fails at the blocked-status assertion when a declarative
negative-control root omits only the crank's pawl restraint. The two paired
tests pass in 50.778 s on integrated framework `23857e9`; neither production
geometry nor its graph changed. Log
`operating-full-root-ratchet-paired-262378b.log`, SHA-256
`80254f7084a72ffbb4ed60202cf226c7e20152281ebe521b1098ba873310f1a7`.
The first negative-fixture attempt defined CAD classes through stdin and
failed construction because no source path existed; that is a harness error,
not the required mechanical negative. Its failed log is retained separately.

After this local completion, carry-guide contacts, clearing-loop release, zero-cam clip,
input-selector fit and whole-machine interaction/geometry acceptance remain
separate open work. The umbrella's 12/23 tasks are not advanced by this record.

The project-local change `operate-radial-positioning-ball` is completed under
the pilot's standing autonomous instruction, with its three requirements
synchronized to `radial-positioning-ball-operation` and strict validation.
Its archive is `openspec/changes/archive/2026-09-23-operate-radial-positioning-ball/`.
The later carry-guide diagnostic is separate read-only investigation, not a
fit included in this adoption or an exemption for existing contacts.
