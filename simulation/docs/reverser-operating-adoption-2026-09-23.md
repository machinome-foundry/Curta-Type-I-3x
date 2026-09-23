# Operating reverser adoption

Status: scoped production acceptance passed in an isolated project worktree;
ready for local integration. Overall operating-machine completion remains open.

This continues `simulate-the-curta` tasks 6.2–6.5 under the pilot's instruction
to finish the operating model. It does not close those tasks, the clearing-loop
requirement or whole-machine geometry acceptance.

## Evidence and dependency gates

The default root at `85c8710` still admits the reproduced crank-90 lever
penetration and retains the reversed crank-82.432377 tooth contact. The fresh
two-test red run, candidate five-test green run and first complete hosted
endpoint pass are recorded in
[the contact-cover investigation](reverser-profile-cover-2026-09-23.md).
The same record preserves the earlier six arithmetic checks, four complete
crank modes, source-cover proof and inspected pinion views.

The candidate uses .43 mm relief only inside R6 on the three ones pinions,
preserving the existing .36 mm outer capture tips and keyed core. The five
higher channels retain their .42 mm fit. Installed outward covers feed ordinary
absolute bounds on the existing reversing-knob joint; no CAD executes in a
running law. These are sampled geometric restraints, not swept-volume or force
certification. The upstream CAD remains unchanged.

Absolute-target endpoint corrections passed their separate final framework
and viewer validation and the paired Curta gate below. Their reviewed commits
are now on local framework main `34b3de127165ec7c2ff9429e24fc01ab39416e5f`
(implementation `7ba9deb`) and viewer main
`80d58d499e3f411fe972bb793ce2d29459e3d1a4` (implementation `63fec79`).
The framework final suite passed 3,680 tests, four skipped and 2,230 subtests;
its merged-state gate passed 319 tests and 599 subtests. The viewer final
widget suite passed 1,556 tests with two skipped; merged running/typecheck,
bundle and documentation gates passed. Both clean integration worktrees are
retained for stable project validation. Nothing was pushed or published.
No trial pass is substituted for fresh default-root acceptance.

### Final endpoint candidate hosted check

On project `85c8710`, the fresh hosted report
`_build_checks/reverser-asymmetric-browser-85c8710-06.json` completed with
exit 0 and `validation: passed`. All nine statuses agree with the expected
completed/completed/blocked/blocked/blocked/completed/completed/completed/completed
sequence. All nine complete 214-coordinate Python/browser banks agree at the
IEEE-754 bit level; retry, restored replay and relief also pass.

The real pointer starts on the visible knob at (800.8670112326427,
479.7954355163532), moves 100 pixels down, and produces completed, completed,
blocked admissions of -1, -1 and -0.8480000000000061 mm. Its final lever height
is 1.0594999999999941 mm. Pointer-up is observed, no command remains active,
all other driver and turn-coordinate bits stay unchanged, and no page error is
reported. The fresh screenshot was inspected: black housing, visible hardware
and selectors, crank readout 90 degrees and clock 0.67 seconds. These pixels
show placement/interaction, not hidden internal contact clearance.

Pinned candidate content (not yet integrated package commits):

- Framework `run.py`: `95a7f23420fa9e67c1b94d1e3446bead1f07380e0ac94b2cc322f1f239d5fa01`.
- Framework `trajectory.py`: `96483106789792d99a9413beb9e585b2eab5e64063778ec583d327d46d2bd679`.
- Viewer bundle: `41bd9f1ea95162e8cbbaafef8a247f84cada95ff63082533dce2cdc91e77d58e`.
- Export manifest: `3388020498a62ea4d75b4adfa7acd1b995e098d47bc101dfd9b8e6c0cc6c3587`.
- Report JSON: `3a77aeec6f3779b11fa6aaf23602aaecdd23e3a3782ce82ab2b15e311d0cc433`.
- Screenshot: `71aed3d5e7182aa9d824ec5f74483a82d2765f4d47e3b30bf342db730a18d97b`.
- Terminal log: `ed24b500ddfc2c656772e8eec8f2f7f73f89091d76e4ee34936d7a8e620a102f`.

During this run the framework owner briefly changed and reverted a source-line
movement flag. Independent timestamps establish that the process had already
imported the frozen module (bytecode 12:42:31 UTC; temporary source edit
12:46:44 UTC); all nine Python cases finished before the discrepancy was
observed. The original source hash was restored exactly, and no source reload
occurs in this tool. The temporary edit therefore is not part of this result.
The owner's read-only follow-up found no reproduced defect: actual restricted
points come from `Sources.along()`, not that movement flag. Full-suite and
latest-main integration gates remain separate from this hosted result.

## Integration shape

- Move the proven pinion and retained transmission subclasses into a production
  parts module; preserve the existing counter-ones upper-lockout fit.
- Preserve the pre-restraint radial-ball operating root as an explicitly named
  diagnostic base. The historical ones-fit trial uses that base, so adding the
  production restraint does not silently change the trial's question.
- Keep `simulation.running:OperatingCurta` as the public default. It combines
  the fitted transmission with exactly one pair of compiled reverser bounds.
  Keep the current controls, joints, paths, follower and shoulder carries.
- Make the combined trial a compatibility fixture of the adopted model rather
  than attaching a duplicate bound. Historical measurements remain historical.

## Production acceptance

The first implementation step extracts the existing candidate's identical
pinion adjustment and retained transmission into `reverser_operating_parts.py`.
Historical trial imports remain compatibility aliases. Both unchanged native
`OnesFlankFidelityTest` contracts pass after extraction (2 tests, 21.948 s,
exit 0): the 25-pose .01 mm minimum-gap survey and the protected outer-tip,
keyed-core, one-solid and no-added-material checks. This is a refactor gate,
not production adoption or the final installed contact matrix.

The unchanged long-request/replay contract is now inherited from the actual
default-root test class instead of existing only in the trial class. Before
root adoption it fails as intended: the crank-90 lever request to -3 returns
`completed`, not `blocked` (1 test, 120.974 s, exit 1, fresh worktree CAD cache).
This supplements the already recorded native/faceted penetration red; it
does not replace that geometric failure with a status-only assertion.

After wiring the default root, all five unchanged production contact/path
contracts pass (178.715 s, exit 0) against framework integration `34b3de1`:
actual native/world64 penetration prevention, precontact free play, a distinct
retained history's withdrawal, long-request retry/replay/explicit relief, and
the reversed crank-82.432377 passage. No expected status, volume assertion,
request size or timestep was relaxed. All six unchanged `RunningCurtaTest`
arithmetic/replay checks also pass on the actual default root (997.697 s,
exit 0): independent selectors, successive additions/selective clearing,
manual calibration carries, partial crank release and exact replay, shifted
register association, and full-bank subtraction/borrow undone by addition.
The log `_build_checks/reverser-production-arithmetic-01.log` has SHA-256
`7334de1b9c5e306007c2486bc0f6094b0720954a6234de3b9a61d4fa6fb25cac`.

The fresh public-root export completed (exit 0):
`_build_checks/reverser-production-v13`, document version 13, 214 coordinates,
identity `086dc890a67f5867fb57162207386852149ae4ca1b383399fd7aab377c985805`.
Its manifest SHA-256 is
`67d81ef23aaac58f1b503a8ebdf0ab2e1f4f083f20cdeac3918716fd68502773`;
the embedded viewer bundle is the endpoint bundle pinned above. Export success
alone is not browser acceptance.

Production hosted report `reverser-production-browser-07.json` is preserved
as **failed**, exit 1. All nine expected statuses and complete bitwise banks,
the visible-part blocked gesture and command release passed before screenshot
readback exceeded 120 seconds. Its JSON hash is
`8db7b99295b3b6bc5b735380d8864a87da4fb1fef7ab8e4252e2c3b64c73b3d0`;
log hash `dd3c7aefc9a1c0a993582804ac717c43c36c870ee74c4b98256ef771e9f650a1`.
The retry uses an explicit 180-second screenshot-only allowance, matching the
standalone probe. Physical requests, command deadlines, timestep and assertions
are unchanged. A screenshot timeout is not counted as a complete browser pass.

The twenty unchanged profile compiler, footprint/cover and installed-law tests
plus six standalone-report validation tests pass (26 tests, 1.034 s, exit 0)
against framework `1b136de`, whose law-error correction is now integrated.
The new report test failed first: a requested blocked gesture was incorrectly
accepted when its terminal UI said completed. The guard now distinguishes those
outcomes. The combined log hash is
`36f3dd01fc4bc363325068b2d78a6732009ad35ef6a4690b7f7db2baae1454bd`.
This report-validation unit test is not itself a physical browser gesture.

Production hosted report `reverser-production-browser-08.json` completed with
exit 0 and `validation: passed`, using the same production export and endpoint
package pair. All nine expected statuses and all 214 coordinate bits in each
case agree with Python. The actual knob drag again admits -1, -1 and
-0.8480000000000061 mm, stops at 1.0594999999999941 mm, observes pointer-up,
leaves no command active and preserves every other driver and turn coordinate.
There are no page errors. The fresh screenshot was inspected: assembled black
housing and hardware, crank 90 degrees, and a visible `blocked after -0.848 mm`
outcome. The picture proves that visible interaction, not internal clearance.

- JSON SHA-256: `223ef60dc00207f8b7a4f7397b3b004d5bcab9b799d21af6c02f0e6b5985d9b3`.
- PNG SHA-256: `56609eb750913919d3ef6e93dff21511043fa236433de4ef34bc5b9a98dda079`.
- Log SHA-256: `ed24b500ddfc2c656772e8eec8f2f7f73f89091d76e4ee34936d7a8e620a102f`.

An unrelated viewer test batch briefly launched additional Chromium processes
during report 08 and was stopped to restore the serial browser window. No bundle
or export changed. This is functional acceptance, not a controlled performance
measurement; no timing claim is derived from the run.

After framework law-error integration, the same five production contact/path
tests pass again on `1b136de` (165.235 s, exit 0). This checks the current
framework against both geometric representations and the retained-history,
precontact, retry/replay/relief and reversed-path cases. Log
`_build_checks/reverser-production-law-integration-01.log` SHA-256:
`14a3a1db7449d8399cf903f9e5c68a8cabe19ef04e4fd631bae37531181e3fac`.

The unchanged four-prepared-mode contract is promoted to the actual default
root and inherited by the compatibility trial. It passes (one test/four mode
subcases, 465.136 s, exit 0) on endpoint framework `34b3de1`: normal/reversed
counter crossed with lowered/raised crank, each completing an entire 360-degree
stroke. The log is `_build_checks/reverser-production-four-modes-01.log`,
SHA-256 `4f9e65e663e706401acf856fdb0a16b16f3cef0125e019953854775e87314529`.

On framework `1b136de`, all nine unchanged carriage/clearing interlock tests
and five decimal-marker tests pass (14 tests, 307.821 s, exit 0). They include
all working shift slots, partial lift, independent stop release, retained
partial clearing, bidirectional ring stops, independent marker travel and
snapshot replay. Log `_build_checks/reverser-production-interlocks-markers-01.log`
SHA-256 `f28534e9880a9e484168fae5e1969daac6c5dbff02e1204d9d3601cb59bc5fb2`.
This does not include clearing-loop clipping or whole-machine clearance.

Standalone attempt `reverser-production-standalone-01.json` is a failed
acceptance run (exit 1), although the old exception path left `validation`
incorrectly at `pending`. That reporting defect is corrected for later runs;
the original is preserved. The visible crank nudge prepared 90 degrees,
the actual `reverse counter` part was acquired after an ordinary camera drag,
and a 100-pixel downward pointer drag moved the lever from 3.9075 to 1.9075 mm.
The UI correctly reported `completed`: that 2 mm movement never reached the
1.0595 mm contact. Every other input readout stayed unchanged and pointer-up
was observed. Its inspected screenshot shows the standalone assembled model
and crank readout; it does not prove a blocked request.

- JSON SHA-256: `31c50c183723fef1cb3ec19a59eff67489bb53513cfd64db4d003a7fd04dbd18`.
- PNG SHA-256: `2a938fb7d644c112b6386d7a0eae4852dca03e214e55630e6b1ce89b617fce9b`.
- Log SHA-256: `9c34c6e6be7565c31e8fd7ec2ceac7a24aa0345e18d5342430c98df4062faf52`.

Attempt 02 increases only the physical drag to 200 pixels, keeping the blocked
assertion and command deadline. Chromium may use CPU 9 and 14 instead of only
14, for functional capture; neither attempt establishes a performance result.

Standalone attempt 02 completed with exit 0 and `validation: passed`. The
unmodified auto-mounted page used only the visible crank nudge controls for
preparation, an ordinary camera orbit, and the actual lever at (867, 577) for
the 200-pixel drag. Its UI reports `blocked after -0.848 mm`; the lever readout
is 1.0595 mm, crank 90.0000 degrees, every other input readout unchanged and
pointer-up observed. There are no page errors. No hidden handle, remount or
register setter is used. The screenshot was inspected: complete assembled
model and prepared crank readout; the four-decimal UI evidence is separate
from hosted report 08's complete bitwise bank proof.

- JSON SHA-256: `b7c7ebcd56962bcfe1c14590683a48c5c473e4f996885fdcc471fdfb50902d15`.
- PNG SHA-256: `036ed54451d92b34c7fa17bd4f6a3e63a94f432ef488e6f80e180e4df0563383`.
- Log SHA-256: `7993eb45949b53970bb435c507c406868d926c26d2ed3b6763e108c1c431bb8f`.
- Unmodified index SHA-256: `16238dda75b0b88224bd1bcaf0c9dfd77a6f43d75652b2972f4af5ed00111bb2`.

The production geometry/contact, arithmetic, four-mode stroke, interlock,
marker, exported-bank and actual hosted/standalone reverser gates above are
accepted for this focused adoption. They do not close the printed clearing-loop
path, remaining rest contacts, every-node geometric regression or the entire
OpenSpec change. The separately owned viewer performance candidate still owes
its final integrated package/browser validation; its timings are not claimed
by these endpoint-bundle runs.
