# Collar seat completion after branch reconciliation

This continuation starts from project `5f101ae`, framework `c81a585` and
viewer `fcecb1a`. The earlier [clocking and shoulder investigation](collar-seating-investigation-2026-09-21.md)
remains the source of the pin-bore, threaded-phase and shoulder measurements.
The upstream STEP/STL files are unchanged. These are bounded simulation fits,
not instructions to modify a physical calculator or whole-machine acceptance.

## Reproduced failures and bounded corrections

The old `OperatingCollarBench` again failed its rest-neighbour and moving-seat
checks before editing: collar/main-body common was 5.536428033e-6 mm³ and
collar/washer common was 4.884981308350689e-15 mm³. No overlap epsilon was used.

The collar's bottom is local Z0, installed at world Z7.8 against the fixed
frame. `SeatedCollar` removes only the bottom .05 mm in addition to the
already-tested .72 mm annular spider-shoulder facing. The collar stays at its
measured source height and corrected -90° world clocking. The unchanged nut
retains its 40° phase and Z12.3 height. Pin bores, inner ledge, threaded stem
and flange remain in place.

The washer's local Z0 and Z3.2 planes are installed, upside down, at world
Z60.3 and Z57.1. They meet the collar lip and clearing cover respectively.
Facing its first end alone exposed a second residual washer/cover common of
5.360099922e-6 mm³. `SeatedCollarWasher` therefore removes .05 mm from each
axial end, leaving local Z.05..3.15. Its radial profile, middle, installed
transform and neighbouring solids are unchanged.

The source-bounds test failed before the second washer facing (Zmax remained
3.2 instead of 3.15). Both preservation tests then passed, including connected
collar material after binary-STL encoding, no added washer material and removal
confined to the independently bounded end skins. Coplanar mesh-difference
scraps must lie on both preserved source surfaces within source-STL length
precision; this is not an overlap-volume tolerance.

## Correct motion and retention

The old trial attempted to seat the carriage with the clearing ring at 180°.
That is not one of the source cam's rest pockets: the existing independent
clearing-interlock tests and measured `PIN_DROP` place them at 0° and 230°.
The corrected test traverses those actual seats at all six carriage positions
and explicitly requires a 180° request to stop seating at lift 4.810085 mm.
The motion laws and stop dimensions were not changed to accommodate the test.

Moving checks retain the previous spider, nut and pin capture assertions and
add washer free/captive tests: .04 mm toward either axial neighbour is free,
while .1 mm reaches the retaining face. The trial's four checks pass on the
faceted runner in 177.77 seconds and exact runner in 173.45 seconds, with
volume epsilon zero. The collar is source-STL geometry on either runner,
not a newly exact solid.

The independent all-neighbour diagnostic checks 1,161 distinct pairs involving
the collar, nut and washer against the 389 rigid occurrences. Both float32 and
float64 diagnostic representations report no residual common. All 213 bank
coordinates remain unchanged. Flexible wires and other rigid-pair combinations
are outside that scoped survey.

The section image `_build_checks/collar-seat-facings-2026-09-22.png` was
inspected: both pins are inside the original bores, the nut retains its thread
engagement, and the spider stays below its faced shoulder. The section alone
does not resolve a .05 mm gap; the free/captive and removal checks measure it.

Before adoption, the default root's 213-coordinate initial bank was captured
as canonical sorted compact JSON. SHA-256:
`ea39d95d50f06580db66c894f5b3f700ab6ed930cee113b2b9ffe4689935f5b7`.
The acceptance test uses that fixed witness instead of comparing two models
which would become aliases of the same fitted root after adoption.

## Reproduction and acceptance state

Use the workspace venv, `PYTHONPATH=.`, `SOLID_BUILD_DIR=_build_checks`, single
BLAS/OpenMP threads and the existing 8 GiB address-space guard. Relevant logs:

- `reconcile-collar-red.log`: original trial failure.
- `collar-washer-two-seats-red.log`: missing lower washer facing.
- `collar-washer-two-seats-final.log`: both source-preservation checks pass.
- `collar-seated-operating-v2-faceted.log`: all four trial checks pass.
- `collar-seat-facings-neighbours.log`: complete 1,161-pair survey.
- `collar-pre-adoption-bank.log`: unchanged default-root bank witness.

## Production adoption

The named `OperatingCollarBench` is now an unchanged subclass of the default
`OperatingCurta`, not a separately fitted carriage. Before changing production,
that wrapper failed its first rest-neighbour assertion with collar/main-body
common 5.980170458e-6 mm³ (one test, one failure, 18.61 s). A prior misdirected
test-file invocation discovered zero tests and was discarded; the accepted
commands explicitly target `simulation/operating_collar.py:OperatingCollarBench`.

`RetainedCarriageStructure` now installs the verified collar and washer and the
measured collar/nut phases. The same four production contracts pass on both
runners: **4/4 faceted, 123.71 s; 4/4 exact, 133.48 s**, zero volume epsilon.
The default's complete initial bank matches the pre-adoption hash above.
Its collar/nut/pin meshes match the independent source-datum seating fixture.
Logs: `collar-production-wrapper-red.log`,
`collar-production-adoption-faceted.log`, `collar-production-adoption-exact.log`.

The [compact evidence](evidence/collar-seat-adoption-2026-09-22.json) pins source,
log and inspected-image hashes. This adopts only the scoped collar fitting;
no motion law, control, upstream asset or OpenSpec checkbox changes. It does
not resolve the rest of the whole-machine overlap inventory.
