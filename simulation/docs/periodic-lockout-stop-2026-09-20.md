# Periodic closing surface: project-owned framework reproduction

Framework main: `8d2bd71171be81f13ba5dd492851ed8b3a9ababb`.
Project starting checkpoint: `331081436ed3d4e79890e07843f93f82e2d71f2a`.
No framework source changes or new framework cycle have been made here.

## Physical caller and expected result

The source-backed `ResultActionOrder` contains the complete bell and result
ones stack, using the same retained tooth law as the operating model. Set
digit 3, crank height 0, turn to 120°, then withdraw the selector to zero.
The actual ones shaft remains at 189.6°. Its measured next closing contact
is about 125.33066° natively / 125.32082° on the current published mesh.
The 125.22° stop used below is on the free side of both.

Both a request to 150° and a request to 840° must stop at that **first**
closing surface. The latter cannot pass through the closed land merely
because its endpoint is in a later revolution's open window.

## Small reproduction on the actual parts

`simulation/periodic_lockout.py` contains two deliberately local diagnostics,
neither selected by the manifest. Both constrain the existing bell joint.
The periodic version reads the actual co-rotating drum and retained ones
shaft. At the prepared shaft phase its lower bound is:

```python
-360 * floor((-drum - 10.8) / 360) - 125.22
```

Outside the certified shaft neighbourhood its algebraically free branch
follows the co-rotating drum. There is no synthetic coordinate. The comparison
uses the earlier fixed local stop with its explicitly limited one-turn free
fallback; that fallback is **not** proposed as the operating solution.

Run from the project root with the integrated framework on `PYTHONPATH`:

```text
python -m unittest simulation.test_periodic_lockout -v
```

Result: **3/4 pass, 80.320 s**:

| Existing source parts and request | Outcome |
|---|---|
| Fixed local stop, immediate 120 → 840 | Blocks correctly at 125.22° |
| Periodic stop, immediate 120 → 150 | Blocks correctly at 125.22° |
| Periodic stop, timed 120 → 840 over 2 s, dt .1 | Blocks correctly at 125.22° |
| Periodic stop, immediate 120 → 840 | Raises `StopInvariantError` |

The exception reports that `bell.turn` left its declared bound and locating
the stop stopped no moving input, after one stop event. It explicitly calls
this a broken run invariant rather than a coarse-timestep issue. The log is
`_build_running/periodic-lockout-reproduction.log`.

## Alternatives checked before escalation

The broader measured five-flat candidate first expressed the forbidden
region as a signed gap added to the actual co-rotating joint. It stops the
short request at 125.220816° but the immediate long request raises the same
error (20.288 s test). Stating the next periodic closing surface directly
also raises it (19.562 s test). The small reproduction removes the measured
table, interpolation, five-flat selection and their performance cost while
retaining the failure on the real parts.

Splitting every user request into hidden small moves, retaining the old
one-turn cap, or accepting the timed-only case would conceal the missing
admission behavior. None is adopted. The production operating restraint is
unchanged; only the separately documented .01 mm ones-lockout fit is present.

## Continuation boundary

The contact-profile geometry refinement is recorded in
[result locking](result-locking-2026-09-20.md). Its acceptance is separate from
this run defect. Project tasks 6.2/6.3 remain open. A new, pilot-authorized
framework cycle is needed to investigate/fix first-contact location for this
periodic moving-read bound, with this Curta reproduction as empirical
acceptance. No new interface is proposed by this finding, and no framework
implementation, integration, or remote publication is authorized by it.
