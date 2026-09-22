# Counter browser comparison: one traced floating residual

The strict station 4/5/6 browser reports remain failed/pending exactly as
captured. They differ from their Python oracles at only
`carriage.registers.dial_detents.p_6mm_ball_419241_9.lift`:
browser `.08929057589867746`, Python `.0892905758986775`, three binary64 ULPs.
Every other stopped/idle coordinate, both stops and discrete outcomes agree;
each runtime's snapshot replay is exact. This is not a contact-volume tolerance.

The [preserved Python trace](evidence/counter-detent-python-trace-2026-09-22.md)
reproduces the same result before and after the latest framework optimization.
During preparation, a cam piece computes `from + (end-base)`, retaining
`.050000000000000044` instead of exact float `.05`. The following branch carries
that residual into its final lift. The direct endpoint expression is identical
in both runtimes. The viewer's independent trace, committed on its main at
`3414c42` and authority-wording correction `3b83bc0`, records its final branch
starting from `.05` and reaching the lower value. No source is stale and no
stop or arithmetic behavior was changed to hide the difference.

Viewer ADR-047 requires exact discrete agreement and float agreement under
the producer corpus's relative window (currently `1e-9`). Bitwise equality of
every project float was a stronger local check. Under the pilot's standing
autonomous authority, the repository agent classified this preexisting residue
and added an **explicit opt-in** `--allow-measured-detent-rounding` to the
counter browser checker. This was not a separately stated pilot design choice.
Default comparison stays exact. The option permits at most three ULPs for
this one named coordinate, records each difference, and keeps all other
coordinates exact. Four ULPs, any unrelated drift, missing state and nonfinite
values fail. Eleven checker tests pass after the new-interface red baseline.
Native/world64 zero-common checks, forced-contact controls, status and replay
checks are not relaxed. Neither runtime is rounded or patched.

Rechecking the existing complete reports with that explicit classification
passes their full validators. This is a new analysis of captured evidence,
**not a new browser run or bitwise-parity claim**. Each has exactly four
reported differences: p9 at stopped/idle for the short/long requests.

| Station | Original browser report | SHA-256 |
| --- | --- | --- |
| 4 | `_build_counter_bank_fourth_retry_d9c1833/counter-browser-acceptance.json` | `8b703f8afb79f43dca2038e0dda8f11bb668f7fc6bdb210fc675a857aa50ce62` |
| 5 | `_build_counter_bank_fifth_retry_d3309ff/counter-browser-acceptance.json` | `39fb31dca6d2d672e40c0d9a46b5ca137327d04c676a742ffcc88c3a000f0a2a` |
| 6 | `_build_counter_bank_sixth_c895dba/counter-browser-acceptance.json` | `4db0b62d672cef2ff5646c35aad9ee05742a95574bfdda46b3204550317f635d` |

All use program `4127d33c87f1501a024ee5c7391d1897ce3af65309b946c811d4244c7fd68da2`
and viewer bundle `8a03c3a3d3cb83c132059474092a15e7b2a085871d98d87cdcccbd40566bfe81`.
Python report hashes remain in the [bank acceptance record](counter-bank-operating-trial-2026-09-22.md).
The tens combined-bank browser retry and later production acceptance remain
separate obligations.
