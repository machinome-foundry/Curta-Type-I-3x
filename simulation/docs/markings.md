# Curta surface markings — 2026-09-15

The pilot directed this project to defer direct-operation clearing, record its
framework requirement for another agent, and implement markings next. The
clearing handoff is `machinome/workflow/docs/curta-retained-angle-clearing.md`
in the workspace (framework commit `3045600`); it is pre-spec evidence, not a
ratified new API. The existing calculator remains pose-driven.

## Implemented surface declarations

`simulation/markings.py` supplies plain mixins to the original rigid leaf
classes. Fitted descendants inherit them. There are six distinct decal
artifacts, carried by 28 existing occurrences: 17 register dials, eight input
rolls and three housing parts. No glyph becomes a child, printed piece or
interference solid. No upstream STEP, STL or drawing is edited.

| Part / marking | Placement in its own source frame | Registration |
| --- | --- | --- |
| Both fitted register dial types / `digits` | R9.45 cylinder, band z=.9..11.4 mm, axis +Z | Artwork zero x=-3.2388 mm at -124°; artwork y=0 at z=11.4 mm. |
| Input number roll / `digits` | R9.3 cylinder, z=0..15 mm, axis -Z | Artwork zero x=55.5123 mm at local azimuth -175.6°; artwork y=0 at z=15 mm. White digits on a black roll. |
| Lower housing / `input_places` | R68.1625 upper collar, z=36..49.8 mm | Sheet x=190.27 at -72° compensates the part's +72° source placement; sheet y=0 at z=49.4 mm. |
| Upper outer sleeve / `branding` | R71.25 outer cylinder, z=2.55..64.5 mm | First arrow x=119.10667 at 0°; sheet y=0 at z=14.41233 mm. CURTA spans the input bank; the other arrow is approximately 130° away. |
| Bottom housing / `reversing_arrows` | R68.1 cylinder | Dot at z=95.1925 mm, beside the reversing knob's exposed pad, offset 10 mm circumferentially from the 72° station. |

The whole strip is wrapped once; `pitch` is not used. All placements state
`zero=(1, 0, 0)` explicitly. Vertices sit on nominal surfaces with no project
offset. Any anti-z-fighting treatment belongs to the future renderer.

The assembled part operations independently give the same zero direction for
every register dial (-124° local azimuth faces world +Z) and every input roll
(-175.6° faces radially outwards). Register artwork increases 0→1 with local
+36°, matching the joint's -36° advance. Input artwork descends 9→0 along
the strip; wrapping around -Z both rights the upside-down source roll and
makes its +36° world advance show the next digit. The glyphs follow the
existing joints and carriage placement, not a second display state.

The lower index collar must not be confused with the tall `BottomHousing`:
putting that sheet on R68.1 would bury it behind the R68.1625 collar. The
reverse arrows, by contrast, belong on the tall shell. Housing registration
is an explicit simulation placement, not a certified vinyl-cutting template
or a manufacturing tolerance recommendation.

## Artwork preparation

The source result strip and reversing arrows are used directly. The other
three supported sheets have paint-only derivatives under `simulation/artwork/`.
See [their provenance and reproducible extraction](../artwork/README.md).
The original paths and transforms are preserved, not substituted with a font.
The upper-sleeve sheet's inch metadata is corrected to millimetres in its
derivative. Cutting borders and screw-registration circles are not paint.

## Explicitly remaining

`Drawings/upper_housing_numbers.svg` is an **annular-sector development of a
conical surface**, not a cylindrical strip or a flat label. Its approximately
112.4/102.2 mm development radii correspond to a 45° cone at approximately
79.5/72.3 mm model radii. The supplied upper housing includes a sloping rim.
Current `Flat` and `Wrapped` placements do not map that sheet faithfully.
The eleven upper-housing place numbers therefore remain unimplemented;
they have not been flattened onto a cylinder, floated on tangent planes,
turned into solids, or approximated by a cloud of small markings.

The **browser viewer does not yet draw decals**, and the OpenSCAD renderer
does not draw them. The framework publishes and exports them correctly for a
future consumer. The project adds no alternative browser renderer. Diagnostic
triangle plots below are evidence for artifact placement and readable artwork,
not a claim of viewer support, window visibility or a running direct-operation
calculator. Existing mechanical/thread findings remain open.

## Verification commands

Run CAD jobs sequentially from this repository, with the workspace environment,
one BLAS/OpenMP thread and the recorded 8 GiB address-space guard:

```sh
python -m simulation.tools.prepare_marking_artwork --check
machinome build
python -m simulation.tools.check_markings
python -m simulation.tools.check_marking_poses
python -m simulation.tools.render_markings
machinome export -o _build_export
python -m simulation.tools.check_markings _build_export/manifest.json
```

`check_markings` inspects the public document, referenced STL surfaces, their
radii and axial bands. Its `--record-baseline <json>` and `--baseline <json>`
compare every material occurrence's artifact, STL/BREP bytes and piece ID.
Use a fresh unmarked control build, not an old cached document, for this check.
`check_marking_poses` checks actual decal glyph extents through all 25 parts'
operations for 0–9, then lifted/shifted zero (275 checks). The root test suite
includes the same check, plus a separate check that the reversing label is
centered on the exposed operating pad. Independent glyph measurements catch
incorrect phase, order and orientation, rather than comparing declarations
to themselves.

`render_markings` writes `markings-digits.png` and `markings-housings.png` under
`_build_evidence/`: orthographic projections of the actual solid and decal
triangles. The first covers all ten digits on both register types and the
input roll; the second covers the three supported housing sheets. Polygon
edge antialiasing is disabled to avoid artificial seams between triangles.

## Validation record

Framework at the start of verification: `30456007d65aae5d1b31bba2d711e72c2eb416a6`
(the requirement-document commit above the integrated markings API). Generated
meshes, snapshots and raw logs stay ignored.

- Red publication check: no `markings` entries and no referenced decal surfaces,
  failing two assertions. The material baseline assertion passed.
- Red pose check on an unmarked control: failed because `number_roll` had no
  digit decal. After restoration, all 275 actual glyph-position checks pass.
- Green publication check: 25 digit markings and three housing markings,
  six distinct portable surface meshes, all vertices on the measured cylinder
  radii and within the intended axial bands.
- Fresh unmarked/marked control: all 390 material occurrences (148 distinct
  model paths; 384 occurrences have exact BREPs) retain their model path,
  STL/BREP hash and piece ID. The older cached pre-task document
  differed on the seventeen occurrences of one **unmarked** fitted axle; a
  fresh unmarked build reproduced that same difference. That old cache was
  therefore not used as the paired-markings baseline. Neither its source nor
  its fit was changed for markings.
- The three derived SVGs pass exact reproducibility checks against selected
  upstream paths. All 30 standalone unit tests pass, and the project-owned
  active OpenSpec change passes strict validation.
- The digit and housing triangle plots were inspected: 0–9 are upright and
  ordered on all three band variants, their counters remain open, and the
  CURTA, input-place and reversing artwork is legible without cutting borders.

- Reversing-label red: the first placement used the internal lever origin,
  not the visible pad. The new geometry assertion measured a 27.00000084 mm
  height error. The label was moved from housing-local z=68.1925 to z=95.1925,
  centered on the exposed pad's world z=-55.2575 mm.
- Phase mutation: changing the register decal from -124° to -88° (one whole
  digit) failed `check_glyph` for digit 1 with a 0.45018 mm extent mismatch.
  The mutation is reverted; no parameter default or test expectation was
  changed to make that mutated placement pass.

- The complete faceted matrix ran all 37 node modules. After correcting the
  reversing placement and the input-palette expectation, root and display
  were rerun: root 14/15, display 2/2, including both new root checks. Combined
  final coverage is 144/146. The only remaining findings are the unchanged
  bearing contact (`0.0000032402102747 mm³`) and the source-STL cover/housing
  thread overlap (`224.32750533797636 mm³`). No epsilon was introduced.
- The complete exact matrix ran the same 37 node modules: **145/146 pass**,
  including both new markings checks. The bearing contact passes with native
  geometry. The sole failure is the same source-STL cover/housing thread
  overlap, at exactly the volume above. The sequential processes took
  3216.31 seconds in total; the largest recorded process RSS was 1256608 KiB.
  The framework remained clean at the same content commit throughout.
- Final build publication passes all four marking checks, including the
  fresh unmarked-control material comparison. Export passes its three
  applicable marking checks; its optional before/after baseline check is
  skipped, since that comparison was made on the build's STL/BREP artifacts.
  An independent build/export comparison matches all 390 material occurrence
  hashes and piece IDs and all 28 marking-reference hashes and colours.
  After the full regression, the complete root was rebuilt (53.66 seconds,
  614240 KiB peak RSS). All four checks passed again; the artifact comparison
  matched the tested export, including relocation beneath `models/`.
- The full OpenSCAD assembly snapshot was inspected. As expected, it shows
  the existing machine with blank digit surfaces; it does not render decals.
  Camera: `0,0,0,55,0,25,650`, orthographic, autocentered/view-all, 1400×1100.
- The refreshed browser export passes calibration, all six worked examples,
  retained state, lift/shift guards, eight selectors, layers and capture.
  `calculator-checked.png` was inspected; the browser still ignores decals.
  This check runs without the CAD virtual-memory limit because Chromium
  reserves large address ranges; its own browser and loopback server close.
  The tested `solid-widget.js` SHA256 is
  `42e214cb1d3cc0483548f53d4a8c27324d4ebca816f1b29ae9b66789800733b7`.

Raw evidence: `_build_evidence/markings-{faceted,exact}-matrix.json` and
per-module logs, `markings-final-faceted-{curta,display}.log`, `markings-reversing-red.log`,
`markings-phase-mutation.log`, `markings-final-build.log`, `markings-handoff-build.log`, `markings-export.log`,
`markings-calculator.log`, `markings-assembly.png`, `markings-digits.png`, and
`markings-housings.png`. All remain generated, ignored files.

These checks complete the supported-markings continuation, not the whole
machine. Direct operation, conical markings, viewer rendering and the existing
mechanical findings remain open.
