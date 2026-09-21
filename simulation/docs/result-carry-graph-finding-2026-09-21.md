# Result-bank carry discrepancy under the same physical request

Status: reproduced project failure, not a framework diagnosis or approved fix.
Tasks 6.2/6.3 remain open. Production mechanics and contact profiles are unchanged.

## Actual operating failure

The counter-tens withdrawal diagnostic cannot reach its intended preparation.
Crank lift 9 mm, reverser −4.9425 mm and crank 90° complete, but the unchanged
90°→180° request stops at **163.42595046793576°**. The counter-tens shaft has
not left 114°. Result tens stands at **699.2537571367207°**, with its upper
stack carried to raw travel 0 mm. The history-enabled rerun records a lower
bound on `main_drive.crank.turn`; all 213 stopped values equal the previous
run exactly. See the [recorded-stop evidence](evidence/higher-counter-preparation-recorded-stop-2026-09-21.json)
and [bound/contact attribution](evidence/higher-counter-preparation-attribution-2026-09-21.json).

Numeric evaluation places the tens lower bound at the retained crank, while
the ones and pawl bounds leave room. The complete-print T07 bench clears the
stopped pose in both kernels but contacts after another .1° with the shaft
held. This supports the local restraint; it does not explain the shaft's
incomplete carry. Dropping that restraint is not an acceptable correction.

## Reduction which reproduces the complete result bank

`result_carry_graph_repro.py` extends the existing CAD-free carry reduction
with the other nine result-shaft laws and carry-lever laws. It retains all
eleven result shafts, eleven dials and ten carry levers, using the production
`shaft_motion`, `dial_motion` and `lever_motion` functions verbatim and the
source dial datums and lever rests. There are no register setters or custom
carry laws. Counter, pawl and CAD are omitted, and the bound reads the carry
lever directly rather than the operating upper-travel adapter.

The smaller reduction, with only ones/tens driven and only the first lever
active, completes this sequence both without restraint and with ones/tens
restraints. The expanded reduction behaves differently on framework
`e6a42c80e6dcc686c180b8a6d94037301c4213a5`:

| Result dependency graph | Contact restraints | 90°→180° outcome | Tens shaft |
| --- | --- | --- | --- |
| Smaller reduction | none or ones/tens | completes at 180° | 704° |
| Complete result bank | none | completes at 180° | **632°**, one carry short |
| Complete result bank | ones/tens | blocks at **163.42595046793576°** | **699.2537571367207°** |

All **41 mapped controls and result-bank coordinates** in the constrained
reduction equal the recorded operating machine exactly, including all eleven
shafts, eleven dials and ten levers. The [reproduction evidence](evidence/result-carry-graph-reproduction-2026-09-21.json)
retains that comparison, the reduced bank, source hashes and failure-log hash.
This is stronger than matching one stop angle, but does not identify a
particular framework algorithm as the cause.

The expected tens angle is not a guessed register outcome. At input zero
and 9 mm crank lift, ones receives ten source teeth and crosses its carry
pin. Tens receives nine input teeth, ending at −16 + 9×72 = 632°, and the
engaged carry contributes one further 72° to reach 704°. The measured tens
input and carry windows end at 144.75° and 157.625° respectively, before the
requested 180°. The smaller reduction reaches that same expected value.

## Reproduce and preserve the red tests

From this project, with the workspace Python environment and framework on
`PYTHONPATH`, run:

```sh
python -m unittest simulation.test_result_carry_graph_repro -v
```

The initial test invocation fails on the absent module. The first candidate
declaration then fails at construction because a class-body `_shaft` alias
became an undeclared relation path; no motion result came from it. Reading
the inherited shaft directly in the relation fixes the probe declaration.
The resulting two tests both fail their intended assertions in **281.535 s**:
blocked instead of completed with restraints, and 632 instead of 704 without.
Logs: `result-carry-graph-repro-red.log`, `result-carry-graph-repro-result.log`
and `result-carry-graph-repro-declared-paths.log` under `_build_checks/`.
These remain honest failing regressions, not expected failures or passes.

The unconstrained case was rerun with the assertion reporting its complete
bank; it again fails in **13.522 s**. Its first lever is fully carried at
0 mm, while tens remains at 632° and the ones shaft reaches 724°. The
[complete unconstrained bank](evidence/result-carry-graph-unconstrained-2026-09-21.json)
and separate log are retained. Only the failure diagnostic message changed;
the expected 704° and physical request sequence did not.

## Next decision

Investigate why extending the live result dependency graph changes the retained
carry under the same request, and why contact observation changes its partial
path. This needs a separately governed framework correctness investigation if
it enters framework implementation; the authorized read-only Python performance
investigation and pending viewer cache-lifetime proposal do not authorize a
correctness patch. No framework file has been changed by this reproduction.

Do not hide the discrepancy by splitting the operating request, reducing the
bank, fixing the carriage permanently, changing an arithmetic oracle, removing
the restraint or relaxing its geometry. A future correction must pass both
reduced cases, the actual 213-coordinate machine, ordinary arithmetic, retained
replay and measured contact gates before counter-tens operating work resumes.
