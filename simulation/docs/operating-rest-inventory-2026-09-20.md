# Operating rest inventory after enclosure seating

This is a measured list of remaining contacts, not an acceptance certificate.
The implemented model is project commit `0586179`, at its initial retained
state with no user commands. `tools/interference.py --operating --progress`
now selects that state explicitly instead of the older pose-model Rest
instruction. Adding `--exact` chooses native shapes where available; source
STL contacts still use the faceted path.

| Inventory | Rigid occurrences | Positive pairs | Refused commons |
|---|---:|---:|---:|
| Faceted | 390 | 268 | 0 |
| Native with STL fallback | 390 | 166 | 0 |

Every positive volume is retained, including nearly coincident face sums.
There is no epsilon or exception list. These totals are not 268 or 166
independent design defects: repeated fasteners, repeated spring/ball seats,
tessellation and genuine unfinished fits all contribute. The diagnostic's
faceted path uses float32 world vertices; exact tiny values need to be checked
against the contract runner and geometry before choosing a correction.

The largest three contacts are the spider mount/crank collar (504.871504 mm³),
clearing cover/counter body (468.259260 mm³ native), and thrust ring/crank
collar (225.523065 mm³). The next root-contract failure is bottom housing/main
body (2.977763 mm³ native versus 75.264083 mm³ faceted). Repeated threaded
fastener fits and marker/selector ball-and-spring seats also remain. Passing
the marker-body track tests does not certify those internal ball/spring seats.

The two complete numeric inventories are committed alongside this record:

- [Faceted pair inventory](evidence/operating-rest-inventory-2026-09-20-faceted.json)
- [Native pair inventory](evidence/operating-rest-inventory-2026-09-20-exact.json)

This traversal inventories rigid occurrences, not the source's ingredient
count, all flexible-wire contacts, or any moving trajectory. It does not
complete task 1.3, whose rest/frame contracts remain red, or the final
demonstration interference matrix. The source STEP and printable STL files
are unchanged.

At completion, the shared workspace dependency heads were framework
`44edea849ec9aa15c30bfbd1d4298805f5f78636` and viewer
`8efe10feb5699b00089c95ca6d09b57a4969197c`, advanced by separate release work.
Their version labels are not substituted for the earlier explicitly tested
browser pair. This inventory uses no browser. No framework or viewer changes
were made for this inventory.
