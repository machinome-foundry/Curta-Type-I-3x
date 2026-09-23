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

The first addition diagnostic subsequently completes all 44 samples in
263.098 seconds and exits zero. Its two turns retain the expected result and
counter outcomes (3, 1), then (5, 2). The JSON-lines file has SHA-256
`e7aa38533735a886081bed370dab62fd5e7ff5bd0b95f66f2cb0f07bed9cb4f8`.
Rest still has 249 positive pairs. Motion adds contacts between the rotating
bell and the static positioning ball #419094, and between the reverse-nose
plate and the lower drum. The former reaches tens of cubic millimetres;
the latter is small but remains positive and is not exempted. Neither is a
passing contact. The ball is the source's 7.5 mm-diameter occurrence, despite
its `6mm ball` name, not one of the seventeen 6 mm register balls.

The [ball-motion investigation](positioning-ball-following-2026-09-22.md)
rejects an orbiting-ball candidate after a second full-rigid replay finds a
larger ball/frame collision. Its isolated bell-clearance checks were not enough.
Production remains unchanged while radial following is measured. The small
reverse-nose/drum common is independently native-clear at eight phases but
positive in world64 STL geometry, with a 0.000001525879 mm face crossing at
world Z -119.85; that representation finding is not waived.

The later [reverse-nose seat fit](reverse-nose-seat-2026-09-23.md) resolves
that pair with a bounded .05 mm lower-face gap. Paired 44-sample additions
on the same framework remove only its 38 moving contacts; no other spatial
pair or volume changes. Both runs also reproduce a separate tiny crank/handle
contact at two poses, so it is not caused by the fit. That contact and the
missing ball-following motion remain open; this is not a passed demonstration
clearance gate.
