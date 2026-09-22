# Frame-fit implementation: protected-seat gate

Historical gate report, 2026-09-13. The pilot subsequently approved the
bounded seat-edge exception and continued fitting without repeated routine
confirmations; that planning revision is commit `9c58255`. The findings below
retain the reason for that revision, not a current request for permission.
No corrected-frame acceptance, full-path bound or regression acceptance was
claimed at this gate. The subsequent [verified correction](carry-frame-validation-2026-09-13.md)
records those results separately; integration remains pending.

## Result

The plan was committed as `7d39306b2e2e0e4d476ce137f670d1c171e1ead4`.
The new independent two-station bench reproduced six native frame-contact
failures, with three placement/travel/solid-validity guards passing. See the
[retained red test output](evidence/carry-frame-red-2026-09-13.md).

Native support mapping then identified an actual common guide/frame seating
land at each selected station. Both slider endpoint contacts reach its edge.
Even a 0.025 mm clearance neighbourhood, half the proposed running gap,
includes existing frame material supporting that land. This triggers the
ratified instruction to return a protected-seat conflict to the pilot.

This is not a proposal to omit the frame, move the bearing, change the slider,
shorten its stroke or waive a Boolean overlap. No such change was made.

## Independent native measurements

The [support inventory](evidence/carry-frame-supports-2026-09-13.json) records
native faces, full rigid placement matrices and the named spring/slider
contacts at four poses. It is a partial support map, not a full swept-envelope
certificate or a completed inventory of all protected features.

At station one, the frame's planar registration face is at world X = 52.8 mm,
Y = -11.01 to -6.39 mm, Z = -22.2 to -15.9 mm, area 29.106 mm². Its opposing
guide face is also at X = 52.8 mm and has area 45 mm². Their native face/face
intersection is one valid **20.43 mm² seating land**. The bodies share no
positive solid volume: this is an existing seating contact, not an overlap
being renamed as support.

The second station has the same measured geometry after expressing its source
placement in a coordinate frame rotated +20 degrees about world Z. This is a
diagnostic coordinate change only. Its own native placement is preserved;
small approximately 1e-9 mm residuals are reported, not rounded away in the
data. Both stations were measured independently.

The [seat-gate probe](../tools/carry_frame_seat_gate.py) selects the actual
native frame and guide faces by their measured planes/extents, requires a
unique match, and intersects those faces. It does not derive the protected
land from a relief cutter or a fitted frame. It applies no fuzzy Boolean or
overlap-volume threshold.

| Endpoint | Actual slider distance to seating land | Seat strip within the 0.025 mm witness, first-station coordinates | Strip area |
| --- | --- | --- | --- |
| Raised, drop 0 | Approximately zero | X 52.8; Y -7.89 to -6.42; Z -21.600 to -21.575 mm | 0.03675 mm² |
| Lowered, drop 4.2 | Approximately zero | X 52.8; Y -7.89 to -6.42; Z -16.825 to -16.800 mm | 0.03675 mm² |

The [complete gate results](evidence/carry-frame-seat-gate-2026-09-13.json)
show the same two strips at station two. Each is a valid native face. A
0.01 mm layer immediately behind each strip contains approximately
0.0003675 mm³ of valid native frame material inside the witness.

For this lower-bound witness only, the probe makes a copy of the raised
slider translated +0.025 mm in Z, and a copy of the lowered slider translated
-0.025 mm in Z. Every point of either copy is 0.025 mm from a point of the
actual slider, strictly inside a 0.05 mm clearance neighbourhood. Existing
seat material inside these copies therefore cannot coexist with that gap.
These copies are measurement geometry, **not new operating poses or changes
to an installed moving part**. No production cutter was constructed.

The original endpoint slider/seat intersections have zero area: they meet
the edges, not the land's interior. Consequently a passage cut that retains
the complete seat can at best retain zero clearance at those frame edges.
Calling a 0.05 mm face-normal allowance elsewhere a full running gap here
would conceal this contact. Accepting such endpoint contact instead would
also require an explicit design decision.

## Inspected visual evidence

- [Support sections](../../_build_evidence/carry-frame-supports.png): six native
  sections showing the unchanged frame, fixed guide, slider or spring, and
  the measured overlap. The Y/Z views show the guide's lower support; the
  XY views distinguish the two slider contacts from the two spring legs.
- [Seat-edge close-ups](../../_build_evidence/carry-frame-seat-gate.png): actual
  native guide/frame seating outlines and the two witness strips. Vertical
  scale is deliberately enlarged and labelled; these are measurements, not
  an after-fit rendering.

Both images were opened and inspected. They show station one; station two's
independent native geometry and measurements are retained in the JSON. No
complete assembled or after-fit image is claimed.

## Decision returned to the pilot

Recommendation at the gate, **subsequently approved by the pilot**: permit an explicitly dimensioned local
exception at these two seat edges per selected station. Keep the guide itself
and its placement unchanged, and require preservation/contact tests for the
remaining registration land. Measure the complete 0.05 mm pocket boundary and
remaining land before fitting; the witness strips above are only a lower
bound, not finished pocket dimensions or proof of structural adequacy.

This is narrower than relocating a support or changing a moving part, but it
does revise the current promise that every protected seating surface remains
unchanged. All other stop conditions, the two-station scope and the unsampled
clearance proof remain in force. The remaining M4, support/nut, shaft/bearing
and non-selected-station checks had not been completed at the gate and were
not waived; their later full measurements are in the correction's record.

The proposal/design/spec/tasks have since been revised coherently and pass
strict validation. Fitting and verification subsequently proceeded under that authority.
The running-engine/viewer cycles remain pending; the pilot explicitly asks
to be consulted again when ready to start actual solid-node feature development.

## Historical commands and provenance

These commands were run sequentially from the Curta `WTs/open-run-simulation`
directory with the gate-era bench/test/tool hashes listed below:

```sh
ulimit -v 8388608
export PYTHONPATH="$PWD:/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation"
export SOLID_BUILD_DIR=_build_open_run_evidence
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
timeout 300 /home/asa/devel/libresolid-studio/.venv/bin/solid test --exact simulation/carry_frame.py
timeout 300 /home/asa/devel/libresolid-studio/.venv/bin/python -m simulation.tools.carry_frame_supports
timeout 180 /home/asa/devel/libresolid-studio/.venv/bin/python -m simulation.tools.carry_frame_seat_gate
```

The first command exited 1 for the six named contacts at that historical
checkpoint. It now passes against the fitted operating frame; rerunning it
in the completed checkout is not a reproduction of the red state. Both
diagnostics exited 0; their current versions explicitly select the raw
`MainBody` so they still measure the source seat, not the fitted adapter.
The historical tool/test hashes below identify the earlier versions, whereas
the completion regression records the full final source hashes.
`openspec validate clear-result-carry-frame-contacts
--strict` and `openspec validate simulate-the-curta --strict` pass; planning
validation is not mechanical acceptance. The original simulation remains 7/17.

Framework import: `solid-node/WTs/open-run-simulation`, unchanged content
`6e41f2da132a8604f9b68895967247fb8876fc4d`. Other import origins are in the
red record. At this checkpoint, project production geometry and source
placements remained at the planning commit; only the bench, tests,
diagnostics and records had been added.

SHA-256:

| File | Hash |
| --- | --- |
| Original `CAD/Curta Assembly.step` | `943ec7545d9cbcbe69266f0e8b1b65e912f80fa46cad0c974dea164bdcbbbee3` |
| `simulation/standard/carry.py` | `8c6f502312ec657c12ccd0d7f20f6b47b98f09cef3fac1625dfaa02d00f4afa6` |
| `simulation/carry_spring.py` | `68cff8e1e2b819d37d8ac6e6124ec3809ea52f6aecd0e204ada6b9ec37f07836` |
| `simulation/carry_seat.py` | `8456d02f6229650a0906f45005a89701b4d2f1e30be48735002fe17c3930f41c` |
| `simulation/detents.py` | `124a1fa4f33de578ccc2857ef3df8285755d451fbb301d3c9fa4b23de1ea46a5` |
| `simulation/carry_heads.py` | `44436a3f07a99ffae6e62236fc20e3dbf7475a60bb1d3477b57c1ad8023c5e8d` |
| `simulation/carry_fits.py` | `15a9538b97b278422b9d71afe1efe6f56c2262c2b88a691920b3106adf527510` |
| `simulation/tools/carry_frame_supports.py` | `aca3cfa154f80ff3ecb80ca51dba26c17d03073f46350203cc0259f9256b2dea` |
| `simulation/tools/carry_frame_seat_gate.py` | `d0945241d49b479a357e5df025ba1049ce016ac55de7995ba4dcf27e284c2c5b` |
| `simulation/carry_frame.py` | `76f61b61ed803ed99195513a2bdd605f2e1f222b42570d4705a575d742ff738b` |
| `simulation/test_carry_frame.py` | `9f0f3e947f4fd9ec5c68bd001c7153d0bc246992019a44cf4ce108225dd12019` |
| Support section image | `fd7ac3cc982a6d08778f4a7e23a31a6c4d7eac575ee4f0366d83fec5d50e6bfd` |
| Seat-edge image | `79de60373d7f9e475be4a60cbb5cd94a48e2e00b4a01fe24571cee9f10c27d65` |
