# Remaining carry/frame contacts

Project `d6f298f` still uses the verified first-two-result-station frame fit.
A new read-only probe measures each of the fifteen installed carry sliders
against the complete production frame at initial position and 2.1/4.2 mm
downward stroke witnesses. No root state changes or new fit are applied.

| Stations | Native raised common (mm³) | Native lowered common (mm³) | Sampled midpoint |
|---|---:|---:|---|
| Result 1–2, previously fitted | 0 | 0 | Clear |
| Result 3–10 | approximately 4.626578 | approximately .099225 | Clear |
| Counter 1–5 | approximately 3.370756 | approximately 3.741717 | Clear |

All 45 native commons are valid; world64 checks independently reproduce the
same obstructed/clear classification. Every station's exact values, frame
displacements, initial travel and native common bounds are retained. The
213-coordinate bank is unchanged. This 9.763-second diagnostic is not an
admitted motion replay, a spring survey or a full-path clearance certificate.

The first diagnostic incorrectly transported the site-declared axis through
the imported leaf's frame. It completed, but its nonzero-stroke values are
invalid as carry-stroke evidence. The corrected version uses the station's
parent frame, as required by the existing public site-joint contract. The
`world_frames` helper now optionally exposes assembly frames; its default
leaf inventory is unchanged. A dedicated rotated-leaf test fails against the
old helper's missing option and passes with the extension. Neither this
harness error nor its correction is a framework limitation.

The existing frame fitter explicitly lists only stations `(0, -20)`. Thus
these remaining contacts are unfinished work, not a missing prior merge.
Counter endpoint volumes differ materially from result endpoint volumes;
the [new project plan](../../openspec/changes/extend-carry-frame-passages/proposal.md)
requires independently measured supports and local removal bounds before any
cut. No symmetry-based bank-wide cutter or source-overlap waiver is adopted.

Artifacts under `_build_checks/`:

- Corrected `carry-bank-parent-frame-witnesses-d6f298f.jsonl`, SHA-256
  `97b68752d24a8f7d55c7a052b8a7d66d41fda7466e4d8afe1ce12f6d60d8c678`.
- Invalid stroke-frame attempt `carry-bank-frame-witnesses-d6f298f.jsonl`,
  SHA-256 `466eb1bcd9e9c1d3adfe22c36dcd31e278d3565a9b0b97f39f3d6f9020560e13`.

Reproduce the corrected inventory with
`python -m simulation.tools.carry_bank_frame_contact`, explicitly pinning the
verified framework worktree used here (`cache-standing-bound-bind`, `a500a99`).
