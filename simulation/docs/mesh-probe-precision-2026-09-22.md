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
