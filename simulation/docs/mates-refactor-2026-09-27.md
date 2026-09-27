# Curta mates migration: operating crank

This is the first adoption step, not a claim that every Curta joint or source
placement has been converted. The generated source tree, printable geometry,
fitted clearances and arithmetic laws are unchanged. Whole-machine geometry
acceptance remains open under the existing project record.

## Attachment and contracts

`AttachedCrank.spindle` and `RunningMainDrive.crank_seat` name the existing
central Z motion datum. `RunningMainDrive.turn` now mates those frames with a
revolute freedom. The crank's independent 0..9 mm lift remains a child joint;
the two coaxial freedoms commute. The mate generates the same physical
`main_drive.crank.turn` coordinate that the old site declaration generated.
It replaces the former plain `turn` port and explicit port-to-crank relation.

The pawl-dependent `Bound` lives on the mate's freedom and reads the
anti-reversal pawl in the declaring drive assembly. The five ancestor crank
constraints, the crank's Turn/Button coordinate selections, arithmetic source
relations and the reversing-lever Bound now name `main_drive.turn`. They do
not create another retained coordinate, change input units or change the
operator's controls. The negative ratchet fixture independently restates the
same mated drive without its pawl bound; it does not bypass mate inheritance
checks by replacing an inherited moving child.

## Framework requirement and ownership

On framework `49a8fc5`, a moving mate rejected Bound reads in its freedom,
could not be constrained through its own coordinate, and could not be selected
explicitly by a control. The pilot ratified the additive extension before
OpenSpec proposal. The separately owned `mates-in-mechanical-contracts` cycle
uses one Sol proposer, another Sol implementer, and root adversarial review
before spec sync/archive. No compound freedom or viewer schema is introduced.

The framework cycle has planning commit `956d063` and implementation commit
`163afcc868155eba94dac16ab10345662d3ce5bc`, integrated locally into framework
main after root review. Its three specs are synced and the record is archived
at `openspec/changes/archive/2026-09-27-mates-in-mechanical-contracts` in that
repository. ADR-153 records the decision. The separately owned Studio API
companion `c0f2bfd6dacc9008e7766ecbac24d148294b82aa` is integrated into Studio
main. Both completed worktrees were removed cleanly; commits and branches
remain. Nothing was pushed or published. The workspace environment now uses
the integrated framework without a worktree override.

## Evidence

Starting project: `fb5505d`. Starting framework: `49a8fc5`.

- Original `simulation.test_running.RunningCurtaTest`: 6 passed in
  1009.671 seconds, before migration.
- New adoption tests first failed because `RunningMainDrive` had no mate and
  the crank controls selected `main_drive.crank.turn` instead of the mate.
- The independent joint-declared witness passed before implementation. It
  compares the complete drive subtree's transformed basis points, every bank
  entry, pawl stops, repeated requests and snapshot replay in both lift modes.
- Initial migrated focused run: 6 tests passed (adoption/twin and stroke
  limits). Full-root retained-bank and positive/negative pawl checks: 3 passed.
  The 216-coordinate bank retains the previously pinned historical hash;
  it was not regenerated to accommodate the refactor.
- Framework review reproduced and corrected foreign same-name read acceptance
  and inferred-node aliases evading self/duplicate read checks. A separate
  control-declaration cache mutation was also corrected before completion.

- Fresh `machinome build operating_curta` passes. Its document retains version
  13, all 216 coordinate ids, all 26 control names and 301 program sources.
  All 389 mesh occurrences resolve to existing assets. The graph identity
  changes with the new declarations; this is not a byte-identical export claim.
  Crank lift/turn operation order changes, but their coaxial transforms agree
  in the independent subtree witness in both modes.
- `machinome test simulation/crank_coupling_seat.py --faceted`: seven passed
  in 114.87 seconds, with volume epsilon zero. The default exact runner:
  seven passed in 97.42 seconds. These cover the actual crank/drum/pin
  interface, coaxial bore datum, unchanged bounded relief, capture, retained
  bank and actual turn/lift geometry. They are not whole-machine acceptance.
- Isometric and axial native snapshots were inspected at
  `_build/operating_curta/mates-iso.png` and `mates-axial.png`; no detached or
  displaced crank assembly is visible.
- The hosted browser probe passes on the fresh export with no page errors:
  a pointer lift reaches 1 mm without turning the crank, and dragging the
  first selector moves only that selector and its shaft. The screenshot is
  `_build/operating_curta/mates-browser.png`. This is a scoped pointer check,
  not a repetition of the earlier all-26-control acceptance campaign.
- A deliberate 0.2 mm spindle-frame mutation exposed that the initial pose
  helper walked empty `children` lists in a non-meshed Sim. It now walks
  public child declarations too, asserts the real crank leaf is present,
  and fails on that mutation with a measured 0.2 mm crank displacement.
  The deliberate source mutation was restored; the corrected four-test
  adoption suite passes in 6.824 seconds.
- After framework integration, the same four tests passed in 6.937 seconds
  with no `PYTHONPATH` override.

The migrated batch passed all 30 tests in 1347.230 seconds:

```sh
python -m unittest -v simulation.test_running.RunningCurtaTest \
  simulation.test_mate_refactor simulation.test_running_limits \
  simulation.test_running_ratchet simulation.test_running_interlocks \
  simulation.test_operating_loop
```

This includes all six existing arithmetic cases, actual production ratchet
and negative-control behavior, carriage/clearing interlocks and loop replay.
Tests used the workspace venv, the framework cycle through `PYTHONPATH`,
an 8 GiB address-space cap and one BLAS/OMP thread. The corrected four-test
pose suite was rerun separately after the batch had imported its earlier
test definition. Framework final validation passed 933 tests and 954 subtests;
all 37 baseline specs passed strict validation. The strict manual build has
the same five unresolved-reference warnings as the unchanged framework base,
recorded in the archived evidence rather than waived as a successful build.

## Next finding: repeated dial coordinate names

`ResultDials` has eleven sibling dials and `TurnsDials` six, each with a local
`turn` joint. `register_reading` consumes those seventeen retained paths,
as do the existing arithmetic laws and replay witnesses. A separate two-dial
authoring probe confirms that uniquely named `ones_turn` and `tens_turn`
mates currently generate `ones.ones_turn` and `tens.tens_turn`, not
`ones.turn` and `tens.turn`: the assembly's mate name also names its child's
generated joint.

The choice was presented to the pilot before another OpenSpec change:
optionally let `.on(..., joint_name="turn")` preserve a local physical name
while the assembly mate has a distinct name, retaining today's default;
or keep separate dial joints and use rigid mates only for frame placement,
with no new API. The pilot rejected the naming-string approach. On
27 September the pilot ratified the declaration-reference alternative:
`ones_mount = ones.axle.on(ones_seat, ones.turn)`, with both frames defined
and the dial's `turn` an existing declared joint. That next framework cycle
is separate from the completed crank adoption and is not implemented here.
