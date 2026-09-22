# Clearing cover / counter-body outer seat

Status: implemented in `OperatingCurta`, with scoped production verification.
Upstream source assets are unchanged. This is not a finding
that the author's working print fails or a manufacturing recommendation.

The refreshed operating rigid-rest survey retains a 468.059392 mm³ faceted
common between the clearing cover and counter body. Independent native
placement gives 468.259260 mm³, confined to world Z44.2..45.0 and the annulus
R46.8..48.75. The source cover's R46.8 wall and Z12.9 local face become that
world seat. The body top is local Z0; its outer flange continues to Z3.3.

`ClearingSeatCounterBody` removes only the outer top land, local Z0..0.85
outside R46.75. The extra .05 mm in each direction is a declared seating
gap, not a contact tolerance. The existing underside fits remain unchanged.
The body is not translated; its complete inner geometry, bearing/indexing
regions, bore, overall extents and remaining flange are preserved. The
clearing cover, clearing teeth and their datums are unchanged.

The new production-wrapper test fails first on both runners, at
468.059591 mm³ faceted and 468.259261 mm³ exact. Its separate material-removal
assertion also fails because no fit exists yet. These are
`clearing-carrier-seat-red-{faceted,exact}.log` in `_build_checks/`.

The isolated fitted tree passes the bounded-removal, one-solid/connected-mesh,
unchanged-extents and native no-addition assertions. Its first clearance test
used world-down as a local perturbation and incorrectly tested lifting the
upside-down source cover away from its seat. Those two failed runs are
retained as `clearing-carrier-seat-first-{faceted,exact}.log`; the test now
uses source-local +Z, which is world-down. No geometry was changed to make
that correction pass.

The corrected pair of tests passes on both runners (52.49 s faceted,
54.25 s exact). The cover clears at nine sampled sweep angles at all six
carriage positions, remains free for a .04 mm downward perturbation, and
still meets the body at .1 mm. A separate fixed 213-coordinate initial-bank
witness is included in the final verification. These are scoped checks, not
the whole-machine interference or operating-action matrix.

The inspected world Y=0 section
`_build_checks/clearing-carrier-seat-trial-2026-09-22.png` shows the retained
flange, unchanged inner body and both .05 mm seat gaps. Its independently
transformed complete native solids have exactly zero common; inspection
leaves all 213 bank entries unchanged. The reusable section tool is
`python -m simulation.tools.clearing_carrier_section --output <png>`; after
adoption it inspects the default operating root.

## Production adoption

The final isolated suite passes 3/3 on both runners (47.88/50.80 s), including
the fixed pre-fit bank witness. Then the acceptance wrapper was returned to
the unmodified default root: it fails again at the measured cover/body
contact, with one bank test passing and two geometry assertions failing
(`clearing-carrier-seat-production-red.log`, 7.37 s).

`RetainedAxleCarrier.counter_body` now selects the same fitted part. The
thin wrapper adds no fit or motion of its own. All three production checks
pass, 56.75 s faceted and 58.12 s exact, on framework `471d00a`. A fresh
production section was inspected at
`_build_checks/clearing-carrier-seat-production-2026-09-22.png`; its complete
native common is zero and its 213-coordinate bank is unchanged.

The full faceted rigid-rest inventory changes from 253 to 252 positive pairs:
only this cover/body pair disappears, no new positive pair appears, and no
intersection is refused. The 252 remaining pairs are not waived or certified
by this scoped fit. The [evidence index](evidence/clearing-carrier-seat-2026-09-22.json)
pins both inventories, test runs, source files and inspected images.
