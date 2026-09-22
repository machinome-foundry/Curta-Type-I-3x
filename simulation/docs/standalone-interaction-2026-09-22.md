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

## Selector and next controls

The first coarse hover search misses selector 1 and exits one. Its untouched
pending report/image remain `standalone-selector-one-e5636f8` under
`_build_checks/`. A denser search over the visible selector band finds the
actual `set digit 1` hit at (842.025, 620). A 60-pixel downward drag passes:
digit 1 reads 4.0000, its outcome is completed, other visible inputs remain
unchanged and no page error occurs. The screenshot is inspected and the
process exits zero. Report `standalone-selector-one-dense-7a620d9.json` has
SHA-256 `76b66ec38efbc8442d4c85f6cc56efa6ac0de1abddb3dac39f92685c716d525a`.
No control proxy or hidden-part shortcut was added to find it.

The diagnostic now also supports an ordinary empty-canvas orbit gesture
(asserting no input changed), and physical button presses. A full-revolution
report may require an exact 360.0000-degree visible delta; a new red-first
test rejects 359.9999, then all four report tests pass. The button case is
running with an explicit 600-second observation deadline because normal
default-timestep execution is still slow. That deadline does not change
the simulated timestep or instruction duration. It is not yet a passing case.

The physical one-revolution click subsequently passes with observed exit zero.
The actual crank-bearing part at (842.025, 200) receives a press/release,
without a drag or an instruction-panel click. The instruction outcome is
completed, crank rotation reads exactly 360.0000 degrees, other visible input
readouts remain unchanged, and no page error occurs. The screenshot is
inspected. Report `standalone-crank-revolution-7a620d9.json` has SHA-256
`60ade952592bdd867e5f0fc6a4596d0fe43353cc45a665987138d0eed35d87a8`.
This proves the click reaches its specified visible endpoint at the default
timestep, not that the two simulated seconds execute in two wall-clock seconds.

The distinct partial-turn handle also passes on the same unchanged production
export. The actual labelled handle at (805.875, 254.25) receives a 60-pixel
rightward drag; crank rotation reads 1.0000 degree with a completed outcome.
All other visible input readouts are unchanged, no page error occurs, the
process exits zero and its screenshot is inspected. This is a partial turn,
not another full-turn button action. Report
`_build_checks/standalone-partial-crank-3fefd59.json` has SHA-256
`22816a000fb8f0ea0adfd929484d5c16181025540800979437787faf51b4fa02`.
Resume/wrong-order cases and the remaining standalone controls are still open.

## Fresh paired standing-cache export

Export `_build_operating_standing_cache_884b01e` uses framework `a500a99` and
viewer runtime `5149fe1` (later evidence-only `c5541f1` changes no bundle).
Its program is exactly equal to the prior production export, identity
`3e1d505123b75832f6e1b4353d7e9d7f5c5856375bcb67454ca15b602f140c20`,
with 213 coordinates. Manifest SHA-256 is
`001469d01ad5113b5620db782be3ca26b8f3280bb8751d168ef9888639811495`;
bundle SHA-256 is
`0d16382708d1672904572bf8f20277c5af60ed0ba8befc1c6cd53723423fdf84`.
The rejected ball-orbit candidate is not included.

A fresh physical partial-crank drag passes: 2.0000 degrees, completed,
unchanged other visible inputs, no page error and observed process exit zero.
The actual screenshot is inspected. Report
`_build_checks/standing-cache-standalone-partial-range-884b01e.json` SHA-256:
`261dec8087ea40542c38def6a7c08a1480ba0df9d479b44cba8ecbffead5be89`.

Two preceding failed harness attempts remain intact: one confused the later
labelled-handle location with the part's initial hover point; the next reached
2 degrees but incorrectly demanded the previous run's timing-specific 1-degree
quantum. A physical partial drag does not promise a fixed delta for identical
screen displacement at different runtime speeds. The diagnostic now explicitly
requires a finite positive partial turn below 360 degrees, preserving the
separate full-revolution button's exact 360-degree requirement. The added test
fails red before implementation, then all five report tests pass; negative,
zero, full-turn, beyond-full-turn and nonfinite values are rejected. Logs are
`_build_checks/standalone-partial-range-{red,green}-884b01e.log`.
