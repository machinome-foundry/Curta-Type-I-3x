# World-mesh diagnostic precision

The lower-frame investigation exposed a limitation in the project's standalone
faceted probes, not a framework error. The CLI preserves each supplied local
STL vertex and applies the full-precision placement. The bearing's STL face is
local Z20.100000381469727; rotating it 180° and translating by -118.35 puts
it at world Z-138.45000038146972. The housing's local Z12 shoulder becomes
world Z-138.45. Thus the faceted artifacts really overlap by a positive
3.8146972e-7 mm thickness even though the native source faces are flush.

The old standalone probe casts already-placed world vertices to float32.
Both faces then become Z-138.4499969482422. Its planar-common helper correctly
recognizes that rounded result as zero-dimensional in Z, but the input cast
has already hidden the positive thickness. The raw tetrahedron sums differ
between the representations too; none is an allowable volume tolerance.
An independent Sol review verified the CLI's faithful local-STL path and made
no framework change. The project fit must provide a real positive seat gap.

`simulation.tools.interference` now accepts `--world-precision 64`, preserving
the world coordinates through `Manifold.Mesh64`, and reports the selected
precision. The historical default 32 remains available to reproduce old
inventories, not as a sufficient acceptance gate. A one-test red/green
regression reproduces the rounded shoulder and proves that the 64-bit path
detects its positive volume while the 32-bit path loses it. The retained logs
are `_build_checks/interference-world-precision-{red,green}.log`.

The current production baseline at this finding has 262 positive rest pairs
under the 64-bit world probe, with no refused intersection. This is not directly
comparable to the earlier 252 count: both the result-bank parts and measurement
precision have changed. Paired before/after reports must use identical precision.

Historical standalone faceted admission matrices used the world-float32 probe;
they remain evidence at that recorded precision, not certification of every
placed STL contact. Their independent native measurements and framework CLI
contracts retain their own meaning. Final geometric acceptance must include
the strict CLI and full-precision placed meshes. No task or positive common
is waived by this finding, and no historical run is relabelled as a rerun.

## Precision-preserving contact rechecks

The shared contact reader and both station readers now expose an explicit
`world_precision=64` path. Their default 32 remains for historical scripts;
the result-bank and higher-counter profile CLIs default to 64, report that
choice, and hash the conversion/reader code as well as the profiles. A
two-test red/green fixture demonstrates that both the conversion and reader
retain the positive shoulder thickness. The combined precision/sampling
regressions pass 12/12 in 0.064 s. Logs are
`contact-world-precision-{red,green,regression}.log` under `_build_checks/`.

New full-precision faceted rechecks completed with observed exit zero:
counter tens (trial) passed 15,714 sampled admissions and result station three
(production) passed 23,556, each with zero positive commons. Their logs are
`counter-2-profile-world64-faceted-2026-09-22.log` (SHA256
`8354355dd1ec5eb800f11b5d6f3f4d74c389cfad7266ab5224dd9dec392887f7`)
and `result-3-profile-world64-faceted-2026-09-22.log` (SHA256
`55edccf56fba1d296886a92d0ed14e136de0d63fcaec99b667c7cda390ac9eaa`)
under `_build_checks/`. Both headers pin the probe and profile source hashes.
These are finite profile samples, not every possible pose or full operating
acceptance. The remaining station matrices have not been rerun at world64.

The actual counter-tens pair reader now also exposes explicit precision, and
the operating withdrawal test requests world64 for its admitted and forced
contact measurements. A shoulder regression failed first on the missing
argument, then the seven precision/probe tests passed in 0.015 s. Logs are
`counter-operating-precision-{red,green}.log`. The combined-root counter-tens
trial is being rerun; changing the probe alone does not establish acceptance.

The
running higher-counter station-three native job and station-six world32 job
began before this reader update; their pinned headers and original precision
remain unchanged. The latter finished 17,030 sampled admissions without a
positive common, with observed exit zero, but is explicitly world32 evidence.
