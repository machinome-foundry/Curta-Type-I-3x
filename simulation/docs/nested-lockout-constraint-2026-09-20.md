# Nested cross-assembly lockout constraint

This is a project finding and reproduction, not a ratified framework API or
an implemented operating restraint. No framework or viewer source is changed.
Tested framework content: `9fb5127fad62e6c66067b34e7d02dd389471fa2d`.

## Mechanical evidence

The [partial-result continuation](result-partial-engagement-2026-09-20.md)
identifies a real closing-disc contact after a selector is withdrawn mid-turn.
At crank 120° and selector 3, the ones shaft is at 189.6° and still clear.
Withdrawing the selector to zero leaves that angle retained. Continuing to
150° puts the ones lockout 1.080401810 mm³ into the actual bell. The existing
run admits the request; it has not enforced this mechanical restraint.

The native isolated ones-disc measurement at the same phase modulo 72°
(45.6°) brackets closing contact at crank 125.335121..125.335169°. It retains
source disc geometry and the already documented fitted pentagon. This first
boundary is not yet a complete constraint: validate the complete bell, the
free indexed band, opening/closing transitions, multiple revolutions and
all higher-channel carry positions before adopting a law.

## Public composition limitation

In `OperatingCurta`, the actual crank coordinate is
`main_drive.crank.turn`; the bell follows it in
`carry_mechanism.tens_bell.turn`. The shaft being locked is in
`transmission.result.ones.turn`. These are nested real joints in distinct
mechanical/educational assemblies, not interchangeable proxy coordinates.

`tools/cross_assembly_bound_probe.py` reproduces the public declaration issue
without importing framework internals. Its deliberately simple `120 + phase`
bound tests scope only; it is **not** the proposed mechanical contact law.

- A flat positive control puts the two actual joints at a shared declaring
  parent. Its 150° request correctly stops at 124°. Cross-coordinate bounds
  themselves work; this is not a claim that every cross-assembly constraint
  is unsupported.
- Referring directly to the sibling shaft class from the nested drive's
  bound is rejected at declaration: the shaft is not a child of that declarer.
- Relaying its actual joint through a public drive port constructs the tree
  but `Sim` rejects the bound: a plain port is not banked state.
- Passing a replacement nested disc child from the ancestor is rejected:
  the drive has no `disc` constructor parameter.

The final output is
`_build_running/cross-assembly-bound-probe-final.jsonl`. This is consistent
with the documented bound-read scope, not a demonstrated regression of that
contract. It leaves no supported declaration shown here for attaching this
restraint to the existing **nested** joints from their common ancestor.

## Decision needed before framework work

One project-only alternative is to reorganize ownership so the relevant
physical moving parts are jointly declared at a common level. That would
change the established assembly tree, paths, controls and many validated
relations; it is not a harmless parameter adjustment. Giving a stationary
assembly a fake moving joint, copying shaft state into a dummy joint, or
silently treating a derived port as banked state would not model this contact.

The narrower product question is whether machinome should support a
common-ancestor-owned constraint on those existing descendant joints while
preserving their mechanical ownership. The pilot was asked for authority to
open that separate framework change. Any proposal still needs the framework
workflow's explicit ratification and caller proof before implementation or
integration. No new API spelling is assumed, no issue has been filed, and
the current operating task remains open.
