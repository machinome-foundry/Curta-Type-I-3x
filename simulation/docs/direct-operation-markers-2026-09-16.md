# Movable decimal markers — Python implementation

The running development root now exposes all ten original decimal markers as
independent physical inputs. This is separate from the visually accepted
surface markings: no decal artwork or marking declarations changed.
The default manifest remains the earlier pose model; this is not completion
of direct operation or permission to archive the active OpenSpec change.

## Physical ownership and fit

Each source marker's body, 3 mm ball and spring travel together on one real
revolute joint. The five lower markers belong to the enclosure. The five upper
markers belong to the clearing plate, so carriage/plate movement carries their
track while each marker retains its own position. No marker drives an input
digit, arithmetic register or hidden annotation state.

The source placement origins fit circular tracks about
`(-0.406900356, 0.745841949)` for the lower bank and
`(0.386511579, -0.028412332)` for the upper bank. Their placement radii are
72.9734198 and 54.5886435 mm. The lower track retains its source center;
the upper bank is recentered to the shaft like its already-fitted clearing
cover. Rotating the lower bank about the nominal shaft would be incorrect.

Native solids expose small body/track overlaps in the original radial seat:
0.743088347 mm³ lower and 0.226733511 mm³ upper. Moving each complete marker
assembly radially outward by **0.06 mm** clears both tracks through a full
turn, sampled every five degrees. This is a placement fit, not an edit to the
printed body, ball, spring or housing. Independent structural-parameter probes
at seats 0 and 0.5 mm intersect the respective track on opposite sides; the
accepted seat lies between them. The body/ball/spring radius test verifies that
all three parts follow the same center through a quarter turn.

## Neighbour contacts

The joint bounds retain cyclic marker order without imposing an artificial end
of the circular track. Each neighbour pair is declared once. Moving either
participant into a held neighbour stops the pushing input; it does not move
that neighbour. Moving a neighbour away opens the corresponding free travel.
All five markers can also travel together through a complete revolution.

Native contact discovery, rounded downward to 0.001 degree, gives these
clockwise free intervals from the fitted rest arrangement:

| Pair in each bank | Lower bank (degrees) | Upper bank (degrees) |
| --- | ---: | ---: |
| 1→2 / 6→7 | 0.076 | 0.139 |
| 2→3 / 7→8 | 0.226 | 0.316 |
| 3→4 / 8→9 | 0.149 | 0.346 |
| 4→5 / 9→10 | 0.149 | 0.286 |
| 5→1 / 10→6, across the back | 328.808 | 318.039 |

`python -m simulation.tools.marker_tracks --native` reproduces contact
bracketing on the fitted assemblies. Its default mode instead measures the
original, unseated source meshes; those are not the adopted stop values.
The coarse meshes overstate some neighbour gaps by about 0.02 degree, so the
joint stops use native contacts. Each stop is independently checked against
all nine cross-assembly rigid-leaf pairs; a further 0.05-degree body rotation
must intersect the neighbour.

## Evidence

Before implementation, ordinary running requests admitted travel through the
neighbour, and the integrated root lacked marker inputs. These tests were red
before adding the ten joints, cyclic contact bounds and controls.

- Four running marker tests pass, including both directions for all ten
  markers, opening space, snapshot replay and an integrated root request
  that leaves both registers and all eight input digits unchanged.
- A fifth test passes for simultaneous full-circle travel of both banks,
  followed by contact against a neighbour's retained angle.
- The first four marker tests and the six existing contact/lift-limit tests
  pass together: 10/10 in 62.966 seconds after removal of an unsuccessful
  ratchet experiment. The full-circle test separately passes in 0.419 seconds.
- The integrated successive-additions/selective-clearing/repeated-clearing
  and snapshot-replay scenario also passes after marker integration
  (1/1, 148.095 seconds). This is not a rerun of the complete arithmetic matrix.
- Native marker geometry: 4/4, final rerun 58.11 seconds. This includes every neighbour
  pair, full-turn track clearance, shared radii and radial capture.
- Faceted marker geometry: **3/4**. The full-turn lower-track clearance
  reports a 0.023397085 mm³ overlap at marker 1, angle 0, that is absent in
  the corresponding native check. No epsilon or skipped assertion hides this
  discrepancy. The final faceted rerun repeats it (3/4, 1.35 seconds).
- `_build_running/direct-operation-markers.png` was rendered and inspected:
  the first lower and upper markers have each moved 30 degrees away from
  their four neighbours; the remaining assembly is unchanged. This is a
  posed OpenSCAD geometry check, not viewer/pointer or elapsed-run evidence.
  OpenSCAD does not display the accepted decals.
- A fresh development-root build succeeds at framework `0b0f02a`. Its
  document version is 7, with ten marker controls and ten neighbour-bound
  expressions in the published program. All 28 accepted marking occurrences
  remain present: the three published-artwork tests pass. The separate
  material-baseline test is skipped because no before/after baseline was
  supplied; it is not counted as evidence of material identity.
- The builder correctly warns that the installed viewer only supports
  document versions 1–6. No viewer acceptance is claimed or attempted;
  that independently ongoing work is outside this Python increment.

Reproduce the running and native checks from the project root with the
workspace environment:

```sh
PYTHONPATH="$PWD" ../../../.venv/bin/python -m unittest -v simulation.test_running_markers
PYTHONPATH="$PWD" ../../../.venv/bin/solid test --exact simulation/decimal_markers.py:MarkerGeometryBench
```

Use the resource guard and single-threaded settings in the implementation
checkpoint for heavy geometry jobs. Build/snapshot artifacts are ignored and
are not committed.

## Other mechanics remain open

The forward-running pawl law is unchanged. New red diagnostics in
`test_running_ratchet.py` show that reverse play reopens a seated pawl and
that repeated reverse crank requests are not blocked. Native seated-pawl
bracketing at seven regular/closing stations finds contact about
0.20005–0.20008 degree before each release. The rounded free-side position
`release - 0.2` is clear; another 0.001 degree in reverse meets material.
`solid test --exact simulation/tools/ratchet_stop.py:StopProbe` passes that
geometry contract (1/1, 0.74 seconds).

A candidate crank-only stop was rejected: recomputing the last release after
backlash can forget the captured tooth and let successive requests walk
backwards. Candidate pawl-own-read laws also regressed ordinary forward
return. None of those experiments remains in production. The two running
ratchet diagnostics remain explicitly red, not skipped or counted as passing.

Counter reversal, clearing-loop deployment, measured interlocks, the complete
arithmetic mode matrix and the existing whole-machine contact findings also
remain open. This increment changes neither the framework nor the viewer and
does not introduce a Python handoff.

The updated counter diagnostic passes the 12 mm stroke's full-turn clearance
sweep but fails driving engagement at crank 101.25 degrees (1/2, 3.04 seconds).
Clearance alone is not sufficient to adopt that source stroke as an operating
reverser. The 9 mm candidate's separate clearance finding remains in the main
implementation checkpoint; its rerun fails at crank 114 degrees while the
driving-contact test passes (1/2, 1.79 seconds).
`openspec validate simulate-the-curta --strict`
passes; validation of the record does not complete its open tasks.
