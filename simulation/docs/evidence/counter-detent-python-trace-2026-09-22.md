# Preserved framework diagnostic

Copied from the isolated framework investigation's `diagnostics/counter-sixth-detent-float-trace.md` for durable project evidence. The following is the trace at its recorded checkpoint; the separate viewer trace subsequently confirmed its final branch starts from exact `.05`. No framework source change follows from this trace.

# Sixth-counter detent: exact Python path trace (read-only)

2026-09-22. This is a diagnostic artifact in an isolated framework worktree,
not a framework or Curta source change. Framework baseline
`acebc48800e30f340d1ef74e832c0b676f5b8d52` and integrated candidate
`4bff28ead06f88c6b897326f6efe8e227d8c861a` give the **same** result.
The project checkout was at `d3309ff52f2c27e2a9ad3c42814e9c73f9957266`;
`git diff d903dd7..HEAD` is empty for the trial, mechanism and cam-law files.
The `CounterBankOperatingTrial` program identity is
`4127d33c87f1501a024ee5c7391d1897ce3af65309b946c811d4244c7fd68da2`.

The exact public preparation is `Sim(CounterBankOperatingTrial(), dt=.1)`,
`reverser_height → -3`, then `crank_rotation → 260` (station six is the
counter-tens recipe shifted by 80°). The first request leaves the source
`carriage.registers.turns_register.p_10205_3.turn` at `-145.4500831` and the
detent `carriage.registers.dial_detents.p_6mm_ball_419241_9.lift` at
`0.08929057589867746`. The 260° request moves that source to `-181.4500831`
and the detent to `0.0892905758986775`. Later preparation to 270° and
`reverser_height → 3.9075`, and the blocked 280° request, leave both unchanged.

An instrumenting wrapper around the target law edge's `increments` during
the 260° request captured the actual source, graph endpoint evaluations,
returned `Motion`, increment and committed bank:

| Quantity | Python float hex |
| --- | --- |
| Source before | `-0x1.22e6714ac5f6fp+7` |
| Source after | `-0x1.6ae6714ac5f6fp+7` |
| Detent before | `0x1.6dbbf4753694dp-4` |
| `GraphValue.evaluate` at source before | `0x1.6dbbf4753694dp-4` |
| `GraphValue.evaluate` at source after | `0x1.6dbbf4753694dp-4` |
| Actual `law_motion` start | `0x1.6dbbf4753694dp-4` |
| Actual `law_motion` end | `0x1.6dbbf47536950p-4` |
| Target edge increment | `0x1.8000000000000p-55` (`4.163336342344337e-17`) |
| Committed detent | `0x1.6dbbf47536950p-4` |

The actual cam motion has 24 path pieces. Its piecewise continuation changes
from `0x1.6dbbf4753694dp-4` to `0x1.6dbbf47536bcdp-4` across piece 15
(`t=0x1.86a56a56a56a6p-1` to `0x1.9333333333334p-1`), rises and falls,
then finishes piece 18 at `0x1.6dbbf47536950p-4`; pieces 19–23 retain that
last value. Thus the movement is a real, explicitly represented modulo/cam
path. Its sequential IEEE-754 piece accumulation need not equal one direct
evaluation of the periodic endpoint expression, even though the latter gives
identical start and end values. This is not a stale source or a post-stop
recalculation: at the later 280° Bound segment, the source is unchanged,
`GraphValue.evaluate` is `0x1.6dbbf4753694dp-4` at both ends, the target
increment is zero, and its actual Motion end and committed bank remain
`0x1.6dbbf47536950p-4` on all three propagation passes.

The last-branch arithmetic is reproducible without the machine: piece 17
leaves `current = 0x1.99999999999a0p-5`, or `0.050000000000000044`;
the new branch evaluates its `base` as `.05`,
`0x1.999999999999ap-5`, and its endpoint as
`0x1.6dbbf4753694dp-4`. The existing `law_motion` expression
`current + (evaluate(high) - base)` consequently returns
`0x1.6dbbf47536950p-4`, the committed bank. If `current` were exactly
`.05`, the same expression would give the direct endpoint instead. This
localizes the discrepancy to the residual arriving from the preceding cam
piece, carried by path accumulation.

For the preceding segment, the source Motion's chunk 17 spans global
fractions `0.80625` to `0.8307692307692307` with source start
`-0x1.4219a47df92a2p+7` and delta `-0x1.4666666666668p+4`.
Its modulo cut is at local `0x1.cdcdcdcdcdcddp-1`
(`0.9019607843137255`, global `0.8283653846153846`). Before that cut,
`base = from = 0x1.999e99999999ap-1`; direct `evaluate(high)` is
`0x1.999999999999ap-5` (exact float `.05`), but
`from + (evaluate(high) - base)` is `0x1.99999999999a0p-5`
(`.050000000000000044`). The subsequent branch therefore starts from that
residual. This is the exact operation sequence, not a claim that direct
periodic endpoint evaluation itself differs between runtimes.

The source Motion itself has 23 chunks. Its first 16 chunks retain the
starting turn value. At chunk 16 (`t=0x1.9333333333334p-1` through
`0x1.9cccccccccccdp-1`) its start is
`-0x1.22e6714ac5f72p+7`, three representable steps below the originally
banked `-0x1.22e6714ac5f6fp+7`, and it begins turning. Chunk 17 ends at
`-0x1.6ae6714ac5f6ep+7`, one step above the final bank source, while
chunk 18 begins at `-0x1.6ae6714ac5f6fp+7`. That boundary is where the
target path completes its periodic cam rise and reaches the three-ULP-high
value. The trace distinguishes the actual piecewise source values from the
identical displayed source endpoints; it is not evidence that the final
source was stale.

The same 260° trace on untouched `acebc48` yielded the identical source
values, graph endpoint values, `Motion.end`, increment and bank. The difference
therefore predates `demand-bound-read-paths`; changing the Python bank to the
direct endpoint would alter the existing integrated-path/retained-state
semantics solely to erase a three-ULP difference. Viewer ADR-047 compares
discrete state exactly and floats under the corpus's published `1e-9`
relative agreement window. This observed `4.16e-17` difference is far below
that contract; a strict full-bank bitwise project oracle is a stronger local
gate and should classify this one float explicitly, without weakening checks
for coordinate IDs, discrete status, stop attribution, replay, geometry or
other coordinates. The viewer's corresponding 260° path still needs its own
trace before assigning which numerical step it takes.

Inputs were read from project-owned reports
`_build_checks/counter-bank-sixth-python-2026-09-22.json` and
`_build_counter_bank_sixth_c895dba/counter-browser-acceptance.json`. The
instrumented reproduction used the workspace venv with
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 SOLID_BUILD_DIR=_build_checks`,
CPU14 affinity, and no source edits. Source SHA-256: trial
`e4927898c6e24049ef0ad7025795081292fb48ddb6028a45319b4731584369bf`,
mechanism `eaf5c3cc08043b8d22298df600abe08a20024ef1c5c371a90a56c0a3ad60b0b7`,
detent motion `15943b5d6bb1d7fa51bbf4e1872658d97cdec901cd9e59e9b83b6a26595e043a`,
cam `c1c2608cc410b43bd8493010ccffaf89ca386f48aa6e6f19011a4b780d6d38a7`.

