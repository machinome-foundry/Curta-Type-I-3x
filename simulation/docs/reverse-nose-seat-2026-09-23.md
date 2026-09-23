# Reverse-nose plate: bounded drum-seat fit

The first complete addition contact survey found positive world64 contact
between the fixed reverse-nose plate and the rotating lower drum. Native
solids are clear at the eight measured phases, but the imported STL drum's
face extends to Z-119.8499984741211 while the plate reaches Z-119.85.
This 0.000001525879 mm positive thickness is not planar contact and is not
waived by a volume tolerance. The measured common reaches
0.00007211567673815568 mm³ at 180 degrees.

Native face inspection identifies the drum's swept upper land as R9 mm at
Z-119.85. The plate's opposite face, Z-116.85, is flush with the other
side of the same 3 mm slot. Its mount, outer outline and that upper face
need not move to address the lower-face crossing.

The initial `ReverseNoseSeatTrial` relieves only the plate's lower-face
sector inside R9.05 about the main shaft, by .05 mm. In source-part
coordinates the cutter is centred (-14.4, 0), Z2.95..3.10. This is a
bounded simulation fit, not a source-file edit, recommended manufacturing
tolerance or clearance exemption. No drum surface, mount or motion changes.

The four-test suite fails first on the unmodified plate: six moving world64
commons are positive, no relief exists and the lower face has no free gap.
With the fit, all four tests pass in 9.803 s, covering eight phases in both
crank modes, native/world64 clearance, one connected solid, no added material,
all removal inside the declared sector, unchanged bounding extents and the
unchanged 213-coordinate initial-bank witness. Downward .02 mm is free and
.1 mm is blocked by the relieved lower face. Upward .02 mm is blocked by
the protected upper slot face.

The first fitted run still failed a test's assumed bidirectional free play.
Read-only directional measurements locate its .953749307 mm³ common at
Z-116.85..-116.83, against the unmodified upper slot face. The test was
corrected to prove this existing capture rather than enlarge the fit. The
failed run remains recorded, not relabelled green.

An actual admitted 180-degree crank request clears this pair in both kernels.
The inspected world Y=0 section shows the retained slot and an enlarged
.05 mm lower-face gap. The trial's full rest inventory has the same 249
positive spatial pairs and exact volumes as the preceding addition baseline,
with no refused common; only diagnostic nonspatial signed sums differ.
Those remaining positive pairs are not accepted contacts.

Evidence under `_build_checks/`:

| Artifact | SHA-256 |
|---|---|
| `reverse-nose-seat-red-a2d0783.log` | `05be83c0ed1896ac22114f95af490b06ca1cc96a2e96a5a208ea20a1d2881d4d` |
| `reverse-nose-seat-green-a2d0783.log` — failed bidirectional assumption | `e7f0b687df2e4e1bb84b268ef6f535c75ea7153759fef95a1e8a20e8d237258f` |
| `reverse-nose-seat-directional-green-a2d0783.log` | `3496a6055cbb8c56925fb598402845f25ee6a94c52d8f980272ce472a918b162` |
| `reverse-nose-seat-section-a2d0783.json` | `20d5648f5c709d1c21010ad019c81d0f042fa08692cfcfc663e071f4c7238880` |
| `reverse-nose-seat-section-a2d0783.png` — inspected | `03b89f541ac589495757d53df9ba3bf09d1de102a8c75ad7c59af5f9e194e478` |

## Paired replay and adoption

The trial and unchanged production root were each replayed through the same
44 addition samples on pinned framework `a500a99`. The trial takes 158.471 s;
the paired baseline takes 158.368 s. Both produce (3, 1), then (5, 2), with
no refused commons. Comparing every spatial pair at every sample removes
only the reverse-nose/lower-drum contact, at 38 samples. No pair is added and
no other spatial common changes even by one bit.

Both runs also detect the same tiny crank/handle contact at times 1.6 and
3.7 seconds. It is retained as a separate unresolved finding, not attributed
to this fit or waived because of its magnitude. The bell/static-ball contact
also remains in both runs.

The five-test expanded trial passes in 40.180 s, additionally comparing every
other rigid leaf's vertices and triangle indices exactly against the unchanged
root at rest and after an actual 180-degree turn. Both complete state banks
are identical. The fit is now adopted through `PawlBearingPlate` using
`reverse_nose_parts.py`; upstream files, motion laws and inputs are unchanged.
All five checks rerun against the actual production root and pass in 56.368 s.
The old source plate remains available as `UnseatedReverseNoseReference`.

| Additional artifact | SHA-256 |
|---|---|
| `reverse-nose-seat-addition-a2d0783.jsonl` | `cbf72050fa362968a08da3f7131cea76840c59acd18aea729df5ce10567fbbf0` |
| `operating-addition-paired-reverse-nose-a2d0783.jsonl` | `2f9fc5ffb64987ff20553a632afd578160c5bfe18a3d3842aa36dd908a2bede9` |
| `reverse-nose-seat-paired-meshes-a2d0783.log` | `f96ad34c9ac4b58a568d6a11b3cb12b9bc51532f785292e071df0a65d7ffc293` |
| `reverse-nose-seat-production-a2d0783.log` | `63d7b8a7be4de2c1b48d4a09cec910d640b2032ca07c7d18a90bfd3fb13295e4` |

No whole-machine clearance or OpenSpec task is completed by this scoped fit.
