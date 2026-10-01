# Addition — film specification

Status: version 2, 1 October 2026. Version 1 was written for Videomaker's
curta-video campaign before the tool filmed clocked takes; its narration was
reviewed and bought unchanged (five takes). Version 2 is the film as
produced: checked, previewed, looked at and rendered. Where it departs from
version 1 the section says so under "Departures from version 1" at the end;
the times below are the spoken ones.

## The lesson

The Curta adds by turning a crank. This film enters 23 on the setting
slides, turns the crank once, enters 145, turns again, and reads 168 on the
result dials, explaining on the way the parts that do it: the slides, the
stepped drum and the gears the slides place beside it, the shafts and the
dials, and the carry levers that this sum happens not to need. Then it shows
how machinome says the same machine: the Curta's container narrows to the
right half with its camera held, the Python that declares it types in on
the left, and the words the narrator names light in the code while the
crank turns again. About two minutes, 1920×1080, 30 fps, for a listener who
has never seen a Curta. Honest about what it shows: a simulation of a
printable 3x reproduction, not a filmed machine; committed digits are the
model's clocked requests, mid-stroke dial motion its closed-form pose, no
forces.

## The pilot's requirements, mapped

| requirement | where |
|---|---|
| One full scenario, 23 + 145 | the take `Addition` (takes.py), chapters `first` and `second`; the problem posed in `question`, answered in `closing` |
| A detailed explanation of how it works, components highlighted on narration | `set-23`, `add-23`, `set-145`, `add-145`: each slide highlighted as it is named, the stepped drum, the gears, the shafts and dials, the carry levers |
| How machinome works: code shown, words lit in sync with the narration | chapter `machinome`: three excerpts of `simulation/event_driven.py` typed beside the model, eleven tokens lit as they are spoken |
| The transition: the Curta full screen, its container shrinking to the right half, the code fading into a second container, narration over code while the Curta animates | `whole` → `inputs` by `Reframe(0.8)`; `inputs`, `turn`, `commit` replay the second stroke beside the code |
| Camera continuity through that transition | one view element, `machinome.curta`, on camera `face` in both shots; its take time continues across the join (hold at `set_145`, then running from `set_145`); the set's stage box and the split's right box share top and height, so the Curta keeps its size while its box narrows |

## The take

`takes.py`, `class Addition(Take)` on `EventDrivenCurta`, export
`../../export/event_driven_curta`. `digit_1` is the units slide: the `advance`
law reads the eight settings units first, and `register_reading` reads
`result_0` as the units (`simulation/event_driven.py`, `clocked_laws.py`).

| step | request | take seconds | mark after it |
|---|---|---|---|
| — | — | 0 | `rest` (the initial bank) |
| 1 | `Move(digit_1, to=3, over=1.5)` | 0 – 1.5 | `units_3` |
| 2 | `Move(digit_2, to=2, over=1.5)` | 1.5 – 3 | `set_23` |
| 3 | `Trigger("Turn crank")` (by 360, 6 s) | 3 – 9 | `added_23` |
| 4 | `Move(digit_1, to=5, over=1.25)` | 9 – 10.25 | `units_5` |
| 5 | `Move(digit_2, to=4, over=1.25)` | 10.25 – 11.5 | `tens_4` |
| 6 | `Move(digit_3, to=1, over=1.25)` | 11.5 – 12.75 | `set_145` |
| 7 | `Trigger("Turn crank")` | 12.75 – 18.75 | `added_145` |

As evaluated: every request admitted in full, no stop. Each stroke makes one
commit, at fraction 1 of its path, writing all seventeen register digits:
the first `result_0.value 3`, `result_1.value 2`, `turns_0.value 1`; the
second `result_0.value 8`, `result_1.value 6`, `result_2.value 1`,
`turns_0.value 2`. The register reads 0 through `set_23`, 23 from `added_23`
through `set_145`, and 168 at `added_145`, with 1 and then 2 turns on the
counter. Mid-stroke the dials move by the model's closed-form pose, not by
commits: in the stroke's own fraction a dial set to `d` rolls between crank
angles 124.75° − 11.25°·d and 124.75°. So the first stroke's dials count
between take seconds 4.52 and 5.08, the second's between 13.89 and 14.83;
the shots that show the counting are keyed to put that span under the words
that explain it.

The move durations are binary-exact (1.5, 1.25) so that the marks are exact
take seconds.

## The cameras

Measured on the export: the eight setting slides stand around the body from
azimuth 0° (the units, toward +x) to −146° (the eighth), the result dials on
the carriage rim above them, the crank on top.

- `face` — `(607, −509, 300)` → `(0, 0, −30)`, fov 30: the whole Curta a
  little above, from azimuth −40°, the low-order slides toward the camera.
  Chosen for the split's right half: that box (43 % × 86 % of the frame) is
  as tall as the full frame's stage (92 % × 86 %), and the field of view is
  vertical, so the body and crank fill about nine tenths of the height in
  both and the full frame is generous at the sides. Used by `question`,
  `machinome` (held through the reframe) and `closing`.
- `slides` — `(323, −69, −20)` → `(0, 0, −75)`, fov 30: level with the
  slides, facing the units, tens and hundreds slides; their knobs and the
  number rolls above them (3, 2; then 5, 4, 1) read.
- `dials` — `(253, −118, 210)` → `(25, −12, 30)`, fov 26: above the
  carriage rim, facing the low result dials, the crank turning above them;
  "0 0 0 2 3" and then "0 1 6 8" read.
- `inside` — `(440, −369, 170)` → `(0, 0, −30)`, fov 31, with the layer
  `shell` hidden (the enclosure, the carriage covers, the upper frame): the
  stepped drum at the axis, the slides' shafts, the transmission shafts and
  the dial wheels, the crank on top. Its highlights ghost the rest, which
  shows the drum through the shafts around it.

## The parts highlighted, and why

| words | parts | why |
|---|---|---|
| "the setting slides" | `input_selectors.selectors`, others dimmed | where a number is entered |
| "The units slide", "and the tens slide" (23); "The units slide moves", "the tens slide to four", "and the hundreds slide" (145) | the knob of `digit_selector_axle_1`, `_2`, `_3` | the slide named is the one moving |
| "a stepped drum" | `main_drive.stepped_drum`, others ghosted | the drum the crank turns |
| "Its teeth" | the drum and the input pinions of the units and tens transmission shafts (`transmission.result.ones.p_10219_410002_1`, `.tens.p_10230_410008_1_419229`) | the small gears the slides place along the drum, which meet its teeth |
| "Shafts carry" | `transmission.result.ones`, `.tens`, the units and tens result dials | the path from the drum to the dials, while the dials count |
| "Each column adds" | the units, tens and hundreds transmission shafts and dials | the three columns of 145 |
| "a carry lever" | `results_tens_lever_assembly_1` and `_2` | the carry levers into the tens and hundreds; the narration says this sum needs none (3 + 5, 2 + 4 and 0 + 1 stay below ten) |

## The code, and the words lit

All from `simulation/event_driven.py`, typed in as the shot opens:

- `drivers`, lines 52–60 (the eight `digit_N` slides and `crank_rotation`):
  at "Each slide is a Driver, an input you can move: digit one is the units,
  from zero to nine", line 52 lights `Driver`, `digit_1`, `range`; at "The
  crank is a Driver too, crank rotation, in degrees", line 60 lights
  `crank_rotation`, `unit`.
- `instruction`, line 94 (`instructions = {'Turn crank': Instruction(by=…,
  duration=6)}`): at "One full turn is an instruction, named Turn crank",
  `Instruction` and `Turn`.
- `relation`, lines 107–109 (`sources(…).commits(_results + _turns,
  at=stroke, law=advance)`): at "at every stroke, the inputs commit new
  result digits by the law named advance", `stroke`, `sources`, `commits`,
  `advance`.

## The template

`stage.tsx` and `stage.css`, black and brass on warm paper (the movie's
style: background `#f4efe4`, foreground `#161513`, accent `#a87b2c`):

- **`Curta`**, the root set: a masthead of the series "CURTA · HOW IT ADDS"
  at the top left in brass and the brand at the top right, muted, in
  `Chrome`; no rule, no bar, no progress. Slots: `stage` (the machine, 92 %
  × 86 % below the masthead), `headline` (a column at the left for a title),
  `aside` (a plate at the lower right for the sum). The headline column is
  33 % wide and its title 3.2 vw, so "23 + 145 = 168" stands on one line
  clear of the machine.
- **`CurtaSplit`**, derived: the same masthead; `left` (the source, 47 % ×
  60 % from 28 % down, its type 0.9 vw, so the longest excerpt line, the
  instruction's line 94, fits and the code sits level with the machine) and
  `right` (the machine, 43 % × 86 %, the stage's top and height).
- **`Sum`**, the project element: the rows "23", "+ 145", "= 168" of its
  `rows` prop; its action `light(row)` shows the rows through the one named
  and lights it in brass, so the sum forms as the digits land.

## Shot list

Chapter narrations are quoted whole; a cut is on a spoken phrase.

### 1 — `question`

*"This is the Curta, a mechanical calculator worked by hand, here as a
printable model at three times its size. What is twenty-three plus one
hundred forty-five?"*

1. `hook` — `Curta`, `stage` the Curta from `face` at rest (`rest`); fades
   in over 1 s. Until "What is".
2. `question` — the same view; `headline` the title "23 + 145", subtitle
   "Two numbers, two turns of the crank", fading in and out. Until the
   narration's end plus 1.2 s.

### 2 — `first`

*"To enter a number, pull down the setting slides on its side. The units
slide goes to three, and the tens slide to two. Now one full turn of the
crank. Inside, a stepped drum turns with it. Its teeth have different
lengths, so the small gear each slide sets beside it meets exactly as many
teeth as the slide's number. Shafts carry those steps up to the result
dials, which now read twenty-three."*

3. `set-23` — dissolve; `slides`. Model keyed: at rest until "The units
   slide", the units slide moving to 3 until "and the tens slide", the tens
   to 2 until "Now one full turn" (`set_23`). Highlights as named.
4. `add-23` — dissolve; `inside`, case hidden. Model keyed: `set_23` to
   4.4 s by "Shafts carry", then 4.4 to 5.2 s by "which now read", so the
   dials count under "those steps up to the result dials". Highlights: the
   drum, the drum and gears, the shafts and dials.
5. `read-23` — dissolve; `dials`, keyed 5.2 s to `added_23` by the end plus
   0.6 s (the crank finishing its turn, the dials reading 23), then held at
   `added_23`; the sum's first row "23" lights at "twenty-three". Until the
   end plus 1.2 s.

### 3 — `second`

*"Now the second number. The units slide moves to five, the tens slide to
four, and the hundreds slide to one. One more turn. Each column adds on its
own dial: three and five make eight, two and four make six, and the hundreds
dial takes the one. When a column passes nine, a carry lever moves the next
dial one extra step; here no column passes nine, so no carry is needed. The
dials read one hundred sixty-eight."*

6. `set-145` — dissolve; `slides`, the sum showing "23". Model keyed through
   `units_5`, `tens_4`, `set_145`, each slide moving as it is named and
   highlighted; "+ 145" lights at "and the hundreds slide". Until "One more
   turn".
7. `add-145` — dissolve; `inside`. Model keyed: `set_145` to 13.75 s by
   "three and five", 15.0 s by "When a column", 16.25 s by "The dials read":
   the three dials count under "three and five make eight, two and four make
   six, and the hundreds dial takes the one". The columns highlighted, then
   the two carry levers.
8. `read-168` — dissolve; `dials`, keyed 16.25 s to `added_145` by the
   narration's end, then held at `added_145`; "= 168" lights at "one hundred
   sixty-eight". Until the end plus 1.5 s.

### 4 — `machinome`

*"Let's watch that second turn again, beside the Python that describes this
machine in machinome. Each slide is a Driver, an input you can move: digit
one is the units, from zero to nine. The crank is a Driver too, crank
rotation, in degrees. One full turn is an instruction, named Turn crank. And
one relation says what the machine remembers: at every stroke, the inputs
commit new result digits by the law named advance."*

The chapter replays the second stroke, and says so: the dissolve into it
goes back from 168 to the bank of `set_145`.

9. `whole` — dissolve 0.8 s; `Curta`, `stage` the Curta from `face`, held
   at `set_145`. Until "beside the Python".
10. `inputs` — **`Reframe(0.8)`** into `CurtaSplit`: the same view element
    moves from the stage's box to the right box, camera held, take time
    running on from `set_145`; the `drivers` panel fades in on the left and
    types through line 60 in 1.5 s; tokens lit as above. Model `set_145` to
    15.75 s (the dials count during the drivers). Until "One full turn".
11. `turn` — the `instruction` panel, typed in 0.5 s; model 15.75 to 16.5 s.
    Until "And one relation".
12. `commit` — the `relation` panel, typed in 1 s; model keyed from 16.5 s to
    `added_145` at "commit" (the crank finishing the stroke as the word is
    spoken), held to the end plus 1.2 s.

### 5 — `closing`

*"Twenty-three plus one hundred forty-five makes one hundred sixty-eight, in
two turns of the crank. The interactive model is linked in the
description."*

13. `result` — dissolve 0.8 s; `Curta`, the Curta from `face` at
    `added_145`; `headline` the title "23 + 145 = 168"; fades out over 1.2 s.
    Until the end plus 1.6 s.

## Departures from version 1

Made in production; the narration is version 1's, unchanged.

- `read-168` and `read-23` end on a hold: their model keys reach the mark
  (`added_145` by the narration's end; `added_23` by the end plus 0.6 s) and
  hold it to the shot's end. A shot keeps moving through the dissolve after
  it at the rate its model ends with; `read-168` ran past the take's end
  (refused), and `read-23` ran into the next setting.
- "Its teeth" highlights the input pinions, the gears a slide places beside
  the drum, instead of version 1's transmission gear tips, which are the
  bevel tips at the top of the shafts, by the dials: the preview showed the
  light on the wrong end of the shaft.
- The template's code panel is larger and lower and the headline wider with
  a smaller title (see "The template"): the preview showed the code small
  and high beside the machine, and the closing title broken over two lines.

## Out of scope, on purpose

Subtraction, shifting the carriage and clearing: one scenario is the
pilot's. A carry that happens: 23 + 145 makes none, and the take is what
the machine did, so the narration names the carry levers and says this sum
needs none. A still or a clip: `CREDITS` clears no picture for the film. No
credit in the frames or the audio; `description.md` carries the record.
