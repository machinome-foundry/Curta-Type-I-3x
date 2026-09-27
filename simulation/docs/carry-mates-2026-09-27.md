# Carry-station frame adoption

This increment follows sliding-group commit `4e56737` in the isolated project
worktree. All fifteen carry stations get three explicit mates: the slider
references its original parent-space `travel` joint, while the fixed bearing
and spring assembly use rigid mates. The spring keeps its intrinsic `spread`
coordinate and all six wire-shape laws; it is not a new mounting freedom.

`carry_frames.py` states each station's original rotation and translation as
a full frame. Its small project-local `source_frame` helper rotates the X and
Z basis directions using the recorded axis and angle, then supplies both
directions to `Frame` at full precision. Source constants were extracted
mechanically from the fifteen original scaffold render methods and are
explicit in the resulting module; no runtime source parsing or framework
internals are used. All three direct children are mated, so these subclasses
do not call the source placement render. Fits and generated source remain
unchanged. The retained production wrappers select these subclasses; the
original source carry banks remain available to historical probes.

## Evidence

Before implementation the adoption check fails fifteen station subcases
(zero mates instead of three), while the independent legacy pose/state/spring
shape/replay witness passes: 2 tests in 5.380 seconds. The witness uses source
carry stations with the original retained wrapper, checks seven stroke
settings, explicitly visits all fifteen sliders, bearings and spring wires,
compares every basis point at eight decimal places and all six shape values
of every wire, and replays snapshots exactly.

The initial six carry/crank tests pass in 11.299 seconds. The complete focused
adoption and running-marker batch passes all 27 tests in 24.673 seconds,
including the unchanged historical 216-coordinate hash.

After proving the unmodified witness green, independent in-memory +.2 mm
perturbations of result-station-two's slider seat, counter-station-four's
bearing seat and result-station-eight's spring seat each fail it. Their
selected physical slider, bearing and wire origins move respectively
.20000000000000284, .1999999999999993 and .20000000000000284 mm. Automatic
restoration returns each complete basis exactly to its previous value.

`CarryMateCaptureBench` uses the actual retained production station classes
and the original individual rest offsets. Its companion inherits the three
existing fifteen-station capture assertions unchanged: fixed closed spring
folds, .01 mm free/.2 mm blocked hook play, and spring-to-bearing clearance.
The faceted runner passes all three in 20.81 seconds with volume epsilon zero.
The exact-kernel runner also passes all three in 163.29 seconds.

Fresh `machinome build operating_curta` succeeds. The complete motion program
and all control definitions remain equal to frozen checkpoint `7ee005f`;
all 417 mesh/marking occurrences resolve and their STL bytes are identical.
The export retains version 13, 216 coordinates, 26 controls and 301 program
sources. Unlike the preceding identity-placement increment, these mates
express nontrivial source rotations, so literal operation spelling is not
claimed identical; the independent basis comparison checks their placement.

The candidate production blobs are
`2de4e391e3b53d20cf1fb65fb4161699a79bcd9c` (`carry_frames.py`) and
`02bc699fed63354febfffa05fa58e59830dba77a` (`running_parts.py`).
Capture fixtures are `cf1aa740e909e8ffb6006cfc47cd8765ec16a398` and
`1d413b161a31af3f4c9e56736820661efdf9fa40`.

The driven native view `_build/carry-mates-set.png` was inspected at
`stroke=2.562` with complete automatic framing. All fifteen sliders remain
in their bearing seats with their spring wires attached. The matching legacy
view `_build/carry-legacy-set.png` has identical decoded RGB pixels. Exact
capture is complete; the frozen outer-channel checkpoint subsequently passed
its eight-test contact suite, releasing that integration gate.
No whole-machine geometry acceptance is claimed.
