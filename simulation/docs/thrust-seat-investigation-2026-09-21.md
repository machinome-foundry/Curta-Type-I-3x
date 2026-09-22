# Thrust ring and carriage spring: placement-only candidate

**2026-09-22 follow-up:** adopted in the operating root by `1fc3e00` after
red-first root tests, source/mutation negative controls, faceted/exact
interface and motion checks, a fresh build and inspected browser images.
See [resumption evidence](resumption-2026-09-22.md). The original investigation
below records the earlier isolated candidate; its "not adopted" status is
historical. The collar-shoulder facing candidate remains separate.

Status: **isolated, not adopted**. The source ring, collar and sleeve need no
material removal for this candidate. Their operating placements and the
production spring law are unchanged. This advances task 1.3's seat investigation,
not whole-machine acceptance or a force/preload calculation.

## Measured support surfaces

The initial source positioning instrument reproduces the collar/ring common
of 225.523065076 mm³. The ring starts at world Z25.5225, inside the collar's
lower tapered bore. Its native thickness is 1.5 mm and outside radius 16.35 mm.
A source-derived section shows the collar's internal supporting ledge at Z33.
Raising only a measuring ring by 7.45 mm still leaves 1.446655633 mm³ overlap;
7.5 and 7.5275 mm clear. The exact-contact sample, +7.4775 mm, produces a
negative faceted common (-0.000001383272149 mm³) and is **refused**, not rounded
to a passing zero. The full scan finishes with that refusal explicitly recorded.

The unchanged sleeve has a downward-facing native annular seat at Z54.3.
The old analytic spring ends at centreline Z51.0225 and its mesh reaches only
Z51.919999521, leaving a gap below that seat. At its lower end it overlaps the
thrust ring by about 6.5992 mm³. The earlier endpoint-motion tests correctly
checked transport of the old endpoints, but did not establish physical seating.
The old and candidate stack sections were rendered and visually inspected.

Using the project's named .05 mm seat gap gives:

| Quantity at zero carriage lift | Old placement | Candidate, mm |
|---|---:|---:|
| Thrust-ring underside | 25.5225 | 33.05 |
| Thrust-ring top | 27.0225 | 34.55 |
| Lower wire cap centre | 27.0225 | 35.5 |
| Upper wire cap centre | 51.0225 | 53.35 |
| Coil centreline height | 24 | 17.85 |

The source-sized wire radius is .9 mm. The lower cap centre is ring top plus
.9 + .05; the upper is the sleeve seat minus (.9 + .05). The lower ring and
wire cap then rise with the 6 mm carriage stroke while the upper cap and sleeve
stay fixed. At full lift the coil height is 11.85 mm. The existing four-turn,
R13.2 centreline, 1.8 mm-wire analytic spring is reused. Its constant-pitch
shape remains an approximation to flattened source ends, not an inextensible
wire or a stress, spring-rate, preload or durability model.

Manual page 48 shows this stack but leaves its written spring instructions
unfinished. These dimensions therefore come from the source seats and tested
geometry, not from an invented manual instruction or a manufacturing recommendation.

## Red/green and full-root evidence

Before correction, the new seat tests produce three physical/position failures:
the lower endpoint is 8.4775 mm below the candidate seat-derived coordinate,
the ring meets the collar, and the wire meets the ring. Wire connectivity
already passes. The first candidate run then exposed an invalid test argument
(`directions='reverse'`); that is a test setup error, not a new mechanical
failure. The corrected tests express negative travel with a negative axis and
the public `forward` direction.

All five final tests pass on both runners: **1.75 s faceted, 20.34 s exact**.
They cover:

- Ring clearance, ±.04 mm axial free play and positive downward capture at
  .1 mm overtravel, across five lift heights and eleven collar rotations
  (-100..100 degrees in 20-degree increments).
- Spring clearance against ring, collar and sleeve; free play and blocking
  at each real seat through the five lift heights.
- Independently checked lower/upper endpoint positions and an unmoved sleeve.
- Connected source-sized wire through full compression, with native validity
  and one-solid checks where native geometry is available.
- An unchanged source-placement negative control reproducing both contacts.

Collar contacts necessarily remain faceted on both runners because the collar
is the author's STL. Ring, sleeve and spring provide native geometry for the
corresponding exact-runner checks. These are sampled checks, not a continuous
whole-machine trajectory certificate.

`tools/thrust_root_probe.py` compares the source instrument with the actual
`OperatingCurta` rest meshes before substituting anything. The ring, collar,
spring wire, sleeve and clip match exactly at vertices and face centres.
It then checks measuring copies of the relocated ring and reshaped spring
against all 389 rigid occurrences plus that wire: **777 distinct pairs per
case**, with bounding-box rejection before Boolean intersection. The original
has three positive pairs:

- Ring/collar: 225.523065076 mm³.
- Spring/ring: 6.599188000 mm³.
- Spring/positioning ball: .473498071 mm³.

The candidate has **no positive pair in that scoped rest check**, no refused
common, and leaves all 213 run coordinates unchanged. The newly found spring/
ball contact was outside the previous rigid-only inventory; no inventory
entry has been silently waived or reclassified. Other flexible wires and
moving full-root states remain outside this diagnostic.

Logs, source hashes, native face measurements, rejected samples and complete
probe output are in [the evidence record](evidence/thrust-seat-trial-2026-09-21.json).

## Reproduce and continue

Use the workspace Python environment and `SOLID_BUILD_DIR=_build_checks` as in
the [collar investigation](collar-seating-investigation-2026-09-21.md#reproduction):

```sh
/home/asa/devel/machinome-studio/.venv/bin/machinome test --faceted simulation/thrust_seat_trial.py:SeatedThrustBench
/home/asa/devel/machinome-studio/.venv/bin/machinome test simulation/thrust_seat_trial.py:SeatedThrustBench
/home/asa/devel/machinome-studio/.venv/bin/python -m simulation.tools.thrust_seating --seated --section _build_checks/thrust-seated-trial-section-final.png
/home/asa/devel/machinome-studio/.venv/bin/python -m simulation.tools.thrust_root_probe
```

Without `--seated`, the diagnostic retains the original ring-height scan;
its exact-contact refusal intentionally makes the command exit 1. The first
candidate plotting invocation also failed because it omitted the new shift
driver's setup; the corrected probe explicitly binds both drivers and exits 0.

The separate [collar-shoulder trial](collar-seating-investigation-2026-09-21.md#isolated-shoulder-facing-trial)
addresses the spider, not this internal seat. The collar nut and carrier pins
remain unresolved. Neither trial is wired into production. Before operating
adoption, verify the combined placement/fit in the retained root and preserve
the independent mechanical controls and source identity. Task 1.3 remains open.
