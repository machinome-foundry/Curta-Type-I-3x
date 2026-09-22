# Contact sampling of retained demonstrations

The arithmetic/replay suite passes all six demonstrations on the adopted
default model, but it does not establish moving clearance. The diagnostic
`tools/operating_demonstration_contacts.py` now attaches ordinary `Sim.every`
sampling to the same physical-action replays and inventories all rigid pairs.
It uses world64 faceted geometry by default, or native shapes with the existing
STL fallback when explicitly requested. Flexible leaves are not covered.

Every positive spatial common and every refused intersection is retained.
Comparison with rest reports added, removed and exactly changed volumes,
without a volume epsilon or an exception list. Unchanged positive pairs are
still positive, not relabelled as clearance. The two report tests first fail
for the absent module, then pass; they retain a new 1e-30 mm³ positive contact,
a one-ULP volume change and a refused common. Logs are
`_build_checks/demonstration-contact-report-{red,green}-3fefd59.log`.

The first addition run is in progress at 0.1-second samples with project
runtime `3fefd59` and this diagnostic, explicitly pinned via `PYTHONPATH` to
framework worktree `demand-bound-read-paths` at `4bff28e`. Its rest and sample
records stream to `_build_checks/operating-addition-contacts-first-3fefd59.jsonl`;
errors use the matching `.log`. No partial run or successful diagnostic exit
is a passing geometry gate. The finite cadence is 18 degrees during each
two-second crank turn; it cannot replace the independent dense tooth/contact
profile tests or establish continuous clearance between samples.

New contacts will be investigated as measured findings, not automatically
cut away. All demonstrations, both geometry paths and flexible-interface
coverage remain required before the demonstration geometry task closes.
