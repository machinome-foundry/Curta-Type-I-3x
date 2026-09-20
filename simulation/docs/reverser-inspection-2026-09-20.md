# Interactive reverser inspection

The pilot requested controls to inspect the alleged mismatch together, after
manually isolating the operating model proved insufficient: that model does
not expose the diagnostic's lever/gear pose. `reverser_inspection` is a separate
manifest model; `operating_curta` remains the default and is unchanged.

## What is shown

Four short root branches: `drum`, `pinion`, `fork`, `detent`. The last holds
the unchanged source shaft and ball. The upper drum and tens-channel input
print reuse exactly the existing diagnostic's solids, including the previously
recorded pinion fits; this increment changes no solid geometry. Knob, spring,
spacers, frames, other channels and lower drum are omitted for inspection, not
certified clear. The ball follows lever height only, NOT radial pocket contact.

All four sliders and five preset buttons belong to the root. Keep the root
focused so both bodies and their controls remain visible. To inspect tooth
height, hide only `detent` and `fork`, then view the small bronze pinion beside
the silver drum horizontally, with the shafts vertical. Restore those two
branches to see how the fork and ball follow the lever.

| Control | Meaning |
| --- | --- |
| `lever_height` | Axial displacement from the imported STEP pose; moves fork, ball and input print together. |
| `gear_offset` | Additional input-print height relative to fork. Source slot play is only 0–0.185 mm. Larger values are diagnostic disassembly, not permitted working clearance. |
| `drum_angle` | Clockwise crank angle, rotating only the drum. |
| `pinion_probe` | Independent rotation of the input print about its own shaft, relative to the complete diagnostic's phase at crank 101.25°. |

Presets reset both angles except the two probe buttons:

- **Lower centre:** lever −6.8425 mm, offset 0; axial tooth-band gap 0.4925 mm.
- **Best slot play:** lever −6.8425 mm, offset 0.185; gap 0.3075 mm. Initial pose.
- **Align teeth - unseated:** lever −5.035 mm, offset 0.185; pinion and nine-tooth
  row occupy the same 1.5 mm axial band. This lifts the ball off the lower pocket
  centre; it is a comparison pose, NOT a validated alternative endpoint.
- **Probe -12 deg / Probe zero:** perturb or restore the input gear at either
  height. The perturbation misses the drum below the row, intersects it when
  raised. An intersection is allowed to remain visible; the viewer does not
  automatically stop at contact.

The drum deliberately does not animate the pinion. Imposing a gear ratio would
make a separated pair look as though it drove. These are prescribed inspection
poses, not a force/contact simulation, operating reversal or arithmetic test.
The original complete assembly's failing acceptance checks remain unchanged.

## Verification

The manifest test failed before registration, and the inspection test module
failed before the model existed. The completed ten checks cover world-vertex
equivalence with the complete bench, the numerical gap, coupled axial motion,
independent offset and rotation, own-axis rotation, preset/replay endpoints,
miss/contact contrast, connectivity and rest interference.

Exact runner: **10/10 pass**. Faceted runner: **9/10 pass**, with the strict
root interference contract reporting 0.000000597499 mm³ at the flush maximum
gear/fork play endpoint. No epsilon, geometry adjustment or exclusion is used.
This mesh/native disagreement remains visible; the native rest common is clear.
The pinion's enclosed cavity shell uses the project's existing material-
connectivity check, paired with one valid native solid, not surface-shell count.
These are scoped diagnostic checks, not a rerun or completion of the full
operating-model regression. Tasks 5.1 and 6.4 remain open.

The finite build publishes schema 2, four drivers, five instruction buttons
and five existing rigid artifacts. No service is launched and no upstream CAD,
operating implementation or default model is modified. Logs and screenshots
live under ignored `_build_running/reverser-inspection-*`.

The finite local Chromium check mounts the actual published document with the
installed viewer's standard inspector, without a server or upload. All four
sliders respond independently to real keyboard input; all five preset buttons
reach their numerical endpoints, including returning to the initial pose.
The navigator's actual checkboxes hide `detent` and `fork`. Browser screenshots
of both the gap and unseated alignment were inspected, as were OpenSCAD side
and oblique snapshots. No page errors occurred. The first browser attempt
incorrectly matched a button's accessible name rather than its visible text;
the corrected test clicks the visible button and does not bypass its handler.

Reproduce the scoped checks from the project root:

```sh
python -m unittest simulation.test_reverser_inspection_manifest
machinome test --faceted simulation/reverser_inspection.py:ReverserInspection
machinome test --exact simulation/reverser_inspection.py:ReverserInspection
machinome build reverser_inspection
python -m simulation.tools.reverser_inspection_browser
```

The faceted command intentionally exits nonzero for the recorded flush-contact
finding; do not chain the remaining commands behind its success.
