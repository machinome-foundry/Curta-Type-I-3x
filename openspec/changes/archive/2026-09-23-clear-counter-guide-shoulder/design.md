## Context

The inspected longitudinal section places the counter shoulder's underside at
station Z=-12.9 mm at rest, descending to -17.1 mm. The guide ledge is at
-16.8 mm. Its positive common occupies X=60.375..61.725, Y=-7.89..-6.42,
Z=-17.1..-16.8 mm. These are independently measured source faces, not a
Boolean common reused as a production cutter. Station axes rotate the first
counter by -130 degrees about world Z, without axial translation.

Routine bounded fitting is authorized by the pilot; source modification,
unmeasured loss of support and a blanket whole-machine clearance claim are not.

## Goals / Non-Goals

Goals: remove the measured shoulder obstruction with a named .05 mm endpoint
gap, preserving all other working interfaces and the full original stroke.

Non-goals: change guide placement/material, resolve the nominal running-face
tangencies, model friction/forces, change detents, or certify fabrication.

## Decisions

1. Work on a simulation-owned counter-slider subclass first. Keep a frozen
   pre-fit reference and an all-five-station candidate fixture. Do not alter
   production while current retained/browser checks are running.
2. Bound the maximum allowed removal in the counter's normalized rest frame
   to X=60.25..61.80, Y=-7.95..-6.35, Z=-12.95..-12.55 mm. The refined trial cut uses
   X>=60.275 within this box, leaving the running stem at X<=60.225 untouched.
   It raises only the underside by .35 mm (.30 interference plus .05 gap).
   Before cutting, establish that the maximum region preserves one connected
   solid and the guide faces, detent curves, reset sole, fork and pin tip.
   If that fails, reject the trial; do not enlarge its allowance.
3. Use the measured source placement to transform the named box to local
   slider coordinates. Do not move the part, shorten its 4.2 mm travel, cut
   an expanded copy of the guide, or derive a cutter from the overlap solid.
   Guide relief was rejected as the first option because the outer ledge is
   narrow and belongs to the fixed guidance/support, whereas the offending
   shoulder has a localized underside distinct from its working stem.
4. Verify the ledge interface independently on native and published world64
   geometry over the whole stroke, including endpoint and continuous swept
   enclosure where available. A source/insufficient-relief fixture must retain
   the positive obstruction. Report the complete guide common as well: its
   separate nominal-face mesh findings cannot be subtracted or thresholded.
5. Preserve the original state/control graph. Adoption changes only the named
   shape adjustment after exact outside-region/source comparisons and the
   existing spring, head/fork, frame and operating-state checks pass.

## Risks / Trade-offs

- Relief could weaken a working surface → prove protected native surfaces and
  material outside the independently named maximum region before adoption.
- Native zero could hide a Boolean failure → use integrated resolved-witness
  guard and independent world64 measurements; refusals remain failures.
- Finite samples could miss a shoulder contact → use conservative swept
  geometry for the simple translational stroke and retain explicit limits.
- This fit could be mistaken for complete guide capture → keep the remaining
  guide-face contact and open-direction retention investigation separate.

## Migration Plan

Plan, source red and maximum-removal proofs; isolated fitted candidate;
preservation/contact checks; then a production-only shape substitution with
unchanged state/control identities. Retain source and insufficient-fit
negative fixtures. Revert the substitution if any required interface fails.

## Open Questions

The maximum region passes all four protected-interface checks before the cutter
is implemented. The first X>=60.30 candidate passes native endpoint and
continuous-enclosure checks, but its published mesh retains a positive sliver
where its lower cut edge meets the unchanged X=60.30 verification window.
The direct float64 tessellation comparison reduces but does not eliminate every
remnant, so a framework precision change is not a proven solution.

Refine only the cut's lower X bound to 60.275: this leaves .05 mm from the
protected running stem and .10 mm radial clearance from the independently
measured ledge at X=60.375. It removes .025 mm more of the nonworking shoulder
strip, entirely within the original preservation-tested allowance. Keep the
verification window and strict-zero tests unchanged. This is a material fit,
not a tolerance or a waiver of the separate full-guide residual. The original
failed candidate and source red remain recorded. Routine trial refinement is
covered by the pilot's explicit autonomous authority; no interface or scope
change is proposed. Rejection still follows if the refined candidate fails.
