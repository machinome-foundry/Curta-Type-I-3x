# Actual standalone-page interaction evidence

`tools/operating_standalone_probe.py` serves the unmodified exported index,
manifest, bundle and contained model assets. It never remounts the viewer,
obtains a hidden run handle, modifies the page implementation, or submits
host movement requests. A hover-only search requires the actual nearest-hit
canvas title to name the intended part control. For overlapping freedoms,
the gesture uses the viewer's real labelled handle. Pointer release is
observed, then the visible outcome is awaited and readouts are recorded.

The ordinary timestep is unchanged. The page exposes 24 root input readouts
and one instruction row, but its auto-mount does not expose the full run bank.
Readouts have four decimal places: this gate does not prove sub-readout
independence, empty hidden command state or 213-coordinate parity. The
[hosted terminal tests](pointer-terminal-acceptance-2026-09-22.md) are separate
evidence for those stronger state checks. Neither declaration count nor a
hover hit alone is accepted as successful movement.

The report helper first fails red for the missing module, then its three tests
pass. They reject missing hover/release/outcome, no movement, missing inputs,
changed other readouts and page errors. The logs are
`_build_checks/standalone-report-{red,green}-e5636f8.log`.

## First production case

The actual default export `_build_counter_bank_production_bound_7107b1c`
passes the crank-lift drag with observed process exit zero. The canvas title
names `lift crank`, `one revolution` and `turn crank`; the distinct lift
handle is dragged upward. Crank elevation reaches 3.0000 mm, the UI outcome
is completed, and all other visible input values are unchanged. No page
error occurs. The final screenshot is inspected. This is one physical control,
not completion of the full standalone matrix.

Report `_build_checks/standalone-crank-lift-e5636f8.json` SHA-256:
`7e9f04a4aab11186f725c4db8031ddb0a0ae0078e802ca1bd6f4ed0f9fa509a5`.
The report pins the original index, manifest, bundle, hover attempts and exact
screen coordinates. Its bundle is `8a03c3a3...`, manifest `03099125...`, and
program `3e1d5051...`; these are the existing production export, not a newly
built viewer candidate. Other controls remain to be tested.
