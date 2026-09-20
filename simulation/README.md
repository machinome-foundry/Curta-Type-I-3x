# Curta simulation — implementation resumed

There are now three sibling models: `fast_curta` (prescribed poses),
`operating_curta` (`Time.running()`), and `clocked_curta` (event-committed
registers using the framework's clocked-machine support). The
[clocked model's record](docs/clocked-curta-2026-09-17.md) gives its Python
operation surface, running-oracle comparisons, timings and viewer limitations.
The manifest selects `operating_curta`. Its current verification and remaining
work are in the [operating completion record](docs/operating-curta-completion-2026-09-19.md).
The nested retained-joint pose defect is corrected in framework `b9b64dd`,
integrated with the pilot's approval. The unchanged operating-model subtraction,
carriage and clearing world-motion contracts pass both geometry kernels. This
removes that prerequisite; it does not certify the remaining mechanical stops,
whole-machine clearance or viewer pointer operation.

The simulation imports the complete standard STEP assembly: all 547 leaf
occurrences, plus the manual's three clearing-strip prints omitted from the STEP,
organized into educational show/hide layers. The operating root has independent
physical inputs and retained joint motion; it does not use the legacy page's
calculator or starting-register controls. Input, bevel, carry and clearing-tooth contact contracts pass,
as do the bell spring's full subtraction sweep, all seventeen register
detents and the spring-loaded clearing stop. **Whole-machine cover/frame
interfaces, the seat inventory and final demonstration verification remain
open; this is not a
delivered calculator simulation.** Follow the
[implementation tasks](../openspec/changes/simulate-the-curta/tasks.md).

The operating carriage stop pin now uses the author's unchanged printable STL,
seated .51 mm deeper to clear the frame while retaining its angular end stops.
Its original STEP gives contradictory native intersection/containment answers;
the reproduction and source comparison are in the operating completion record.
Pin-contact checks therefore use the faceted backend even on the exact runner.
This resolves that mounting interface. The separately verified
[carriage and clearing restraints](docs/carriage-interlocks-2026-09-19.md) now
stop seated shifting, between-slot seating and clearing against the fixed
frame. They preserve measured play and require the user to release each
restraint; they never lift, finish a sweep or seat the carriage automatically.
The record names the bounded simulation-owned tip and underside fits, their
source-fidelity tests and the negative-sweep follower correction. Upstream
CAD and the reversing-shaft detents are unchanged.

The [housing-thread fit](docs/housing-thread-fit-2026-09-20.md) now clears the
two installed printed covers while retaining their measured axial capture.
Three scoped clearance/fidelity checks pass under both runners; these STL
interfaces remain faceted. This does not complete the whole-machine inventory.

The [lower enclosure seat](docs/enclosure-seats-2026-09-20.md) now shares the
main-shaft axis. The correction carries its marker track and lower fittings
together; a separate .05 mm base seating clearance and finer sleeve
tessellation leave the native solids unchanged. The scoped seat and placement
checks pass on both runners.

The [operating rest inventory](docs/operating-rest-inventory-2026-09-20.md)
records the remaining positive contacts without exclusions. The
[reverser seating investigation](docs/reverser-seating-investigation-2026-09-20.md)
now includes the printable knob/yoke, ball bore, shaft fastening seats and
housing window. Counter reversal remains unimplemented pending a justified
working fit; no reversing-shaft geometry has been changed.

Framework `6954e7c` and viewer `038f74d` (API 22) pass the current hosted-browser
probe on the actual operating export: all 24 controls load, real drags operate
the selected crank lift and first selector independently, and seated shift
and clearing drags stop at their measured play without auto-lifting. This
is not yet the complete standalone/hosted pointer and wrong-order matrix.

Surface markings now use the framework's decal API: all 25 number rolls,
the lower input-place indices, sleeve branding and reversing arrows are
declared on their existing parts and exported. The pilot has visually accepted
the markings; the [original verification record](docs/markings.md) preserves
the producer checks and renderer limitations at that checkpoint. OpenSCAD does
not draw decals, and the conical upper-housing index sheet remains unsupported.
The Python retained-angle and changing-source prerequisites are now resolved.
The [implementation checkpoint](docs/direct-operation-implementation-2026-09-15.md)
records the initial running implementation and its then-open prerequisites. The
[movable-marker record](docs/direct-operation-markers-2026-09-16.md) adds ten
independent marker inputs and measured neighbour stops. Its ratchet failures
have since been corrected and verified across all 117 teeth for two revolutions;
the marker-track tessellation discrepancy is now corrected by finer housing
meshing, without changing its native solid or marker seating. Counter reversal, interlocks,
clearing-loop deployment and final whole-machine acceptance are still incomplete. The
[earlier prerequisite checkpoint](docs/direct-operation-running-checkpoint-2026-09-15.md)
preserves the original carry-association refusal.

The export memory blocker is resolved by machinome's `expression-graphs`
cycle, integrated at `5e59147`. The post-fit complete export takes 41.43 s
with 817216 KiB peak process RSS under the 8 GiB address-space guard, using
the existing CAD cache. The
calculator page passes calibration, all six examples, retained operations,
lift/shift guards, selector controls and layer checks against that fresh export.
The [pause report and framework-cycle handoff](docs/pause-report-2026-09-11.md)
preserve the initial 10h Astra/xhigh sprint and its historical stop condition.
The September 11 verification and remaining physical interfaces are recorded in the
[measurements](docs/measurements.md#resumption-after-expression-graphs) and
[resumption validation matrix](docs/resumption-validation-2026-09-11.md).
That baseline reran all 37 tested node modules: 142/144 faceted and 143/144 native
checks passed. Both runners then retained the housing-thread overlap; the
additional faceted bearing contact passed natively. The thread interface has
since been fitted as linked above. The historical matrix is not final
whole-machine acceptance.

Work starts from the previous [assessment](assessment.md). The new
[measurements and validation findings](docs/measurements.md) identify the invalid
spring, distinguish the hardware products sharing names, and document why the
rest assembly's integrity tests currently fail. The invalid spring has an
explicitly authorized, documented replacement; upstream geometry is untouched.

## Run

From this project's root, with the workspace venv active:

Run heavyweight jobs sequentially under the resource bounds in the pause
report. The current workspace framework is required; package metadata alone
does not distinguish its post-0.6 motion, expression-graph and markings changes.

```sh
machinome build
machinome snapshot -o snapshot-rest.png --autocenter --viewall
python -m unittest simulation.test_source
machinome test --faceted simulation/standard/assembly.py
machinome test --exact simulation/running.py
python -m unittest simulation.test_running.RunningCurtaTest
python -m simulation.tools.probe
```

Without activating the workspace environment, use `../../../.venv/bin/machinome`
and `../../../.venv/bin/python` in this checkout. The exact root test is
intentionally failing until the recorded source findings are resolved. A
successful build alone is not an assembly-validation result.

Independent subassemblies are inspectable by explicit class reference:

```sh
machinome build simulation/standard/assembly.py:UpperFrame1
machinome build simulation/standard/assembly.py:MainAxleStepDrum1
machinome build simulation/standard/assembly.py:LowerFrame1
machinome build simulation/standard/assembly.py:DigitSelectorAxle1
machinome build simulation/standard/assembly.py:Carriage1
machinome build
```

The last command restores the complete model as the published viewer document.
No floor or development server is launched by these commands.

### Legacy prescribed-pose calculator page

This page belongs only to `fast_curta`, not to the operating model. Its page-local
registers, automatic preparation and direct register setters are historical
teaching aids, not direct mechanical operation. To inspect that older study,
explicitly export the pose model and serve the project root locally:

```sh
machinome export fast_curta -o _build_export
python -m http.server 8766 --bind 127.0.0.1
```

Open `http://127.0.0.1:8766/simulation/viewer/`. Set the eight input sliders or
type an exact input, then turn the crank. Completed turns become the next starting
registers; repeated turns and decimal shifting support multiplication. “See
inside” hides the enclosure, frame and carriage covers/supports. The assembly
tree independently hides, shows and focuses every subtree. Session values live
in the page and reset on reload. A partial turn can be inspected but not committed.
The carriage-lift slider exposes the 6 mm disengagement stroke and compressing
spring. Changing decimal position lifts, shifts and reseats the carriage; crank
controls are disabled while lifted or between detents. Completed turns are kept
before manual lifting. The model has eight independent drivers; the eight digit
sliders are a convenient presentation of its single exact operand driver.

The readouts calculate with the verified arithmetic convention; they do not turn
the currently incomplete mechanical motion into a validated whole machine.

Six worked examples cover addition, carry, full overflow, subtraction, decimal
shifting and clearing. “Load and run example” replaces the current page registers;
pause at any point to inspect the mechanism. The underlying instructions are
`Rest`, `Set one`, `Turn crank`, `Lift carriage`, `Shift ×10`, `Seat carriage`,
and `Clear both`. Use lift → shift → seat in that order; `Rest` resets a
reproducible pose, not a claim that a physical crank can run backward.

## Source mapping

- `curta.py`: `fast_curta`, calculator controls and prescribed register-state relation.
- `running.py`: `operating_curta`, with history integrated through the mechanical laws.
- `clocked.py`, `clocked_parts.py`, `clocked_laws.py`: `clocked_curta`, with
  framework-owned register commits, request interlocks and closed-form poses.
- `assemblies.py`: seven educational layers, with separate result/turns registers,
  carriage covers, input banks, drive and carry subassemblies.
- `mechanism.py`, `drive.py`, `selectors.py`: named joints and drive relations.
- `arithmetic.py`: reproducible arithmetic; six calibration/operation tests pass.
- `registers.py`: seventeen radial dial joints and measured source clocking.
- `markings.py`, `artwork/`: surface decals, calibrated roll clocking and
  paint-only derivatives of the original drawings; no additional solids.
- `transmission.py`: result/turns banks with sliding inputs and keyed rotation.
- `cycle.py`, `carry_motion.py`: sub-turn input, decimal complement, measured pin
  approach, retained carry and reset-cam timing.
- `input_mesh.py`, `bevel.py`: exact-verified single-interface engagement benches.
- `bevel_bank.py`: the installed seventeen-channel interface, including all six
  carriage detents and lifted intermediate positions; both kernels pass.
- `demo.py`: stepped demonstrations and replay checks shared with the page examples.
- `engagement.py`: complete printed-drum contact sweeps, passing both kernels.
- `carry.py`, `standard/carry.py`: fifteen sliding carry levers and stationary bearings.
- `carry_spring.py`, `detents.py`, `carry_seat.py`: spreading U-wires, measured
  detent profiles and explicit mounting-groove fits; twelve tests pass both kernels.
- `clearing.py`: the manual's two opposed tooth strips and spacer, formed from
  the author's flat STLs into the measured cover groove, with a local retaining-
  screw relief. Every tooth remains unchanged; clearing contact passes both runners.
- `retaining_spring.py`, `bell_spring_motion.py`: the bell's native mounting plate
  and hooks, joined by measured ribbed flexible arms following the drum pockets.
- `views.py`: explicit inspection poses for snapshots at driver defaults.
- `spider.py`, `register_detents.py`, `dial_detent_motion.py`: the source ring
  and tips with seventeen tapered flexible fingers, driven by the actual dial
  joints and measured ball-rise profile. The compact `dial_cam.py` law now also
  passes both complete-bank runners, including carry/subtraction cascades and
  progressive clearing; its formerly pending native verification is complete.
- `covers.py`, `cover_fits.py`, `test_covers.py`: the corrected cover datum,
  inner ring-seat facing, shallow housing pockets and retained axle flats.
  Seven contracts pass on both runners, and three separate fit mutations fail
  as intended (then are restored). Source-STL interfaces remain faceted. The covers'
  mutual thread overlap now has the separately verified bounded fitting in
  `housing_thread.py` and `test_housing_thread.py`; the complete inventory
  remains open.
  `tools/cover_fit.py` and `tools/cover_neighbors.py` reconstruct the unfitted
  source geometry independently of these adjustments.
- `tools/expression_size.py`: actual standalone expression sizes on the shared-
  graph framework. It no longer mistakes multiplied token counts for emitted
  text; the old flat-expansion estimates remain historical pause evidence.
- `clearing_stop_spring.py`, `clearing_stop_motion.py`: the source stop pin
  follows the clearing-cover cam and compresses its eight-turn spring between
  measured seats. Seven contracts pass both kernels.
- `positioning.py`: moving spring seat and port-driven carriage spring compression.
- `zero.py`: retained zero cam, sliding drive pin, grouped roller/lever and moving
  spring terminal, with six passing contact/mount contracts on both kernels.
- `pawl.py`, `pawl_spring.py`: measured anti-reversal ratchet following, reverse
  blocking and a seven-turn spring fitted between the plate and moving pawl.
- `bearing.py`: bevel-tip/frame bearing clearance after the axial fit.
- `prints.py`, `standard/printed.py`: printed bodies from exact STEP ingredients.
- `fit.py`: explicit, documented assembly and tooth-outline fit corrections.
- `viewer/`: the educational calculator page and tested page-local accumulator.
- `flexibles.py`: the documented zero spring and source-sized carriage spring.
- `contracts.py`: material connectivity that distinguishes enclosed voids from
  detached positive-volume bodies; rigid bodies and flexible material patches
  are checked. A reconstructed spring still counts as one physical occurrence.
- `standard/parts.py` and `standard/assembly.py`: compacted output of
  `machinome import-step`, with source product names and all source placements.
- `source.py`: creates the ignored STEP import copy with unique names for
  otherwise ambiguous products. A restoration test proves every other byte
  remains upstream's.
- `standard/test_assembly.py`: verifies the world placement of every mesh against
  the source occurrence. A deliberate 1 mm crank misplacement was detected.
- `test_curta.py`: inventory, connectivity, source validity and interference
  contracts. Failed contracts are retained.
- `tools/probe.py`: reproducible measurements and housing-interface diagnostics.
- `tools/compact_import.py`: one-time mechanical cleanup of a fresh scaffold;
  do not rerun it over edited mechanism code.
- `tools/check_calculator.py`: reproducible headless browser calculation and layer checks.

The ignored import copy is prepared automatically when the parts module loads.
If the upstream CAD file changes during a live session, explicitly run
`python -m simulation.source`, rebuild, and run the placement contract. The live
watcher sees the generated import copy; it does not watch its upstream input
through this preprocessing step. Changes to hierarchy require reviewing the
generated source mapping, not just refreshing that copy.

## Current findings

The educational palette recalls a metal Curta: aluminum-silver structure and
drum, bronze gearing, brass guides and clearing teeth, steel springs/hardware,
black housing and controls, and ivory number rolls. `colors.py` is the single
palette; colors stay with parts when layers are hidden or isolated. This is a
display convention, not a material specification for the printable design.

The lighter spring tessellation retains the same spline and wire dimensions:
Molejo samples per spline span, so four samples per span provide 128 rings per
coil. The previous 1,000-per-span setting created almost eight million triangles
and stalled software-rendered browser interaction. A geometry/mesh-budget test
now passes below 50,000 triangles; the original exact wire shape is unchanged.

The invalid STEP product is the zero-positioning spring (#419219). Automatic
repair remains invalid and splits it into two native solids. The pilot authorized
the documented spring. Its installed shape uses the manual's 1.1 mm wire and five
counter-clockwise turns, with terminal placement and installed bore fitted to the
measured mounting parts. Native validity, wire-size and both faceted/exact mounting
contracts pass. The 11.5 mm winding mandrel is distinguished from installed bore;
springback and force are not predicted. See the measurements for the fit decision.

The original STEP digits-cover / upper-housing intersection returns invalid
geometry. The operating model now uses the author's original print STLs for
those two parts and the crank collar, whose STEP tessellations are not watertight.
The replacement files are valid, but a positive nominal housing overlap remains;
the complete nominal overlap inventory is not yet established. See the measurements
for the current diagnostic evidence. Working motion and arithmetic are not a
claim of complete physical validation or fabrication readiness.

The project-owned OpenSpec change is `simulate-the-curta`. Its planning commit is
`05165d3`; it remains active and unarchived. Current controls describe an operation
from explicit starting registers: changing crank progress is reproducible, rather
than accumulating hidden Python state. The calculation-facing page retains
completed operations while the underlying model stays scrub-friendly.

## Attribution

This simulation layer uses Marcus Wu's Curta-Type-I-3x source and retains this
repository's CC BY-NC-SA 4.0 license and acknowledgments. The standard design is
used; none of the optional modifications has been selected. The historical
assessment remains unchanged as the record of the earlier research session.
