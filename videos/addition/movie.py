"""Addition: the Curta adds 23 and 145, and machinome says how.

The whole screenplay. The take, its cameras, the open-case layer and the
source excerpts are declared beside it in takes.py; the look is stage.tsx
and stage.css; spec.md says what each shot is written to prove.
"""

from machinome_movie import (Movie, Chapter, Shot, Narration, Cue, View, Source, Title,
    Set, Slot, Element, Action, Dissolve, Reframe, FadeIn, FadeOut, Format, Narrator, Style,
    Credits, Release, Evidence)

from simulation.event_driven import EventDrivenCurta
from videos.addition import takes

Take = takes.Addition

# The parts the narration names, by the model's own declarations.
SLIDES = EventDrivenCurta.input_selectors.selectors
UNITS_KNOB = SLIDES.digit_selector_axle_1.selector_knob_1_419057
TENS_KNOB = SLIDES.digit_selector_axle_2.selector_knob_1_419152
HUNDREDS_KNOB = SLIDES.digit_selector_axle_3.selector_knob_1_419225
DRUM = EventDrivenCurta.main_drive.stepped_drum
# The input pinions: each slides along its transmission shaft beside the drum,
# placed by its setting slide (simulation/channel_slider_frames.py).
UNITS_GEAR = EventDrivenCurta.transmission.result.ones.p_10219_410002_1
TENS_GEAR = EventDrivenCurta.transmission.result.tens.p_10230_410008_1_419229
UNITS_SHAFT = EventDrivenCurta.transmission.result.ones
TENS_SHAFT = EventDrivenCurta.transmission.result.tens
HUNDREDS_SHAFT = EventDrivenCurta.transmission.result.hundreds
UNITS_DIAL = EventDrivenCurta.carriage.registers.result_register.p_10203_1
TENS_DIAL = EventDrivenCurta.carriage.registers.result_register.p_10203_2
HUNDREDS_DIAL = EventDrivenCurta.carriage.registers.result_register.p_10205_1
TENS_CARRY = EventDrivenCurta.carry_mechanism.result_carries.results_tens_lever_assembly_1
HUNDREDS_CARRY = EventDrivenCurta.carry_mechanism.result_carries.results_tens_lever_assembly_2


# The film's template, drawn by stage.tsx beside this file.
class Curta(Set):
    module = "stage.tsx"
    series = "CURTA · HOW IT ADDS"          # props the template's masthead reads
    brand = "MACHINOME"
    stage = Slot()
    headline = Slot()
    aside = Slot()


class CurtaSplit(Curta):
    left = Slot()
    right = Slot()


# The sum as it forms: each row appears when its digits land on the
# machine, the newest lit.
class Sum(Element):
    module = "stage.tsx"
    light = Action(row=str)


SUM_ROWS = [{"key": "first", "text": "23"}, {"key": "second", "text": "+ 145"},
            {"key": "result", "text": "= 168"}]

jessica = Narrator(provider="elevenlabs", model="eleven_v3", voice="cgSgspJ2msm6clMCkdW9",
                   label="Jessica", output="pcm_24000",
                   settings={"stability": 0.5, "similarity_boost": 0.75},
                   direction="Curious, clear, unhurried. Leave room to watch the mechanism.")


class Question(Chapter):
    lines = Narration("This is the Curta, a mechanical calculator worked by hand, here as a printable "
                      "model at three times its size. What is twenty-three plus one hundred forty-five?")
    curta = View(Take, camera=Take.face)
    problem = Title("23 + 145", subtitle="Two numbers, two turns of the crank")
    hook = Shot(Curta, {Curta.stage: curta}, until=lines.spoken("What is"),
                fade_in=FadeIn(1.0), model=Take.run("rest", "rest"))
    question = Shot(Curta, {Curta.stage: curta, Curta.headline: problem},
                    until=lines.end(plus=1.2), model=Take.run("rest", "rest"),
                    cues=[Cue(0, problem.show(enter=0.6, leave=0.6), until=lines.end(plus=0.6))])


class First(Chapter):
    lines = Narration("To enter a number, pull down the setting slides on its side. The units slide goes "
                      "to three, and the tens slide to two. Now one full turn of the crank. Inside, a "
                      "stepped drum turns with it. Its teeth have different lengths, so the small gear each "
                      "slide sets beside it meets exactly as many teeth as the slide's number. Shafts "
                      "carry those steps up to the result dials, which now read twenty-three.")
    slides = View(Take, camera=Take.slides)
    inside = View(Take, camera=Take.inside, hide=[Take.shell])
    dials = View(Take, camera=Take.dials)
    total = Sum(rows=SUM_ROWS)
    set_23 = Shot(Curta, {Curta.stage: slides}, until=lines.spoken("Now one full turn"),
                   transition=Dissolve(0.6),
                   model=Take.keys({0: "rest", lines.spoken("The units slide"): "rest",
                                    lines.spoken("and the tens slide"): "units_3",
                                    lines.spoken("Now one full turn"): "set_23"}),
                   cues=[Cue(lines.spoken("the setting slides"), slides.highlight(SLIDES, others="dim"),
                             until=lines.spoken("The units slide")),
                         Cue(lines.spoken("The units slide"), slides.highlight(UNITS_KNOB, others="keep"),
                             until=lines.spoken("and the tens slide")),
                         Cue(lines.spoken("and the tens slide"), slides.highlight(TENS_KNOB, others="keep"),
                             until=lines.spoken("Now one full turn"))])
    add_23 = Shot(Curta, {Curta.stage: inside}, until=lines.spoken("which now read"),
                  transition=Dissolve(0.5),
                  model=Take.keys({0: "set_23", lines.spoken("Shafts carry"): 4.4,
                                   lines.spoken("which now read"): 5.2}),
                  cues=[Cue(lines.spoken("a stepped drum"), inside.highlight(DRUM, others="ghost"),
                            until=lines.spoken("Its teeth")),
                        Cue(lines.spoken("Its teeth"),
                            inside.highlight(DRUM, UNITS_GEAR, TENS_GEAR, others="ghost"),
                            until=lines.spoken("Shafts carry")),
                        Cue(lines.spoken("Shafts carry"),
                            inside.highlight(UNITS_SHAFT, TENS_SHAFT, UNITS_DIAL, TENS_DIAL, others="ghost"),
                            until=lines.spoken("which now read"))])
    read_23 = Shot(Curta, {Curta.stage: dials, Curta.aside: total}, until=lines.end(plus=1.2),
                   transition=Dissolve(0.5),
                   model=Take.keys({0: 5.2, lines.end(plus=0.6): "added_23",
                                    lines.end(plus=1.2): "added_23"}),
                   cues=[Cue(lines.spoken("twenty-three"), total.light(row="first"),
                             until=lines.end(plus=1.2))])


class Second(Chapter):
    lines = Narration("Now the second number. The units slide moves to five, the tens slide to four, and "
                      "the hundreds slide to one. One more turn. Each column adds on its own dial: three "
                      "and five make eight, two and four make six, and the hundreds dial takes the one. "
                      "When a column passes nine, a carry lever moves the next dial one extra step; here "
                      "no column passes nine, so no carry is needed. The dials read one hundred "
                      "sixty-eight.")
    slides = View(Take, camera=Take.slides)
    inside = View(Take, camera=Take.inside, hide=[Take.shell])
    dials = View(Take, camera=Take.dials)
    total = Sum(rows=SUM_ROWS)
    set_145 = Shot(Curta, {Curta.stage: slides, Curta.aside: total}, until=lines.spoken("One more turn"),
                   transition=Dissolve(0.6),
                   model=Take.keys({0: "added_23", lines.spoken("The units slide moves"): "added_23",
                                    lines.spoken("the tens slide to four"): "units_5",
                                    lines.spoken("and the hundreds slide"): "tens_4",
                                    lines.spoken("One more turn"): "set_145"}),
                   cues=[Cue(0, total.light(row="first"), until=lines.spoken("and the hundreds slide")),
                         Cue(lines.spoken("The units slide moves"), slides.highlight(UNITS_KNOB, others="keep"),
                             until=lines.spoken("the tens slide to four")),
                         Cue(lines.spoken("the tens slide to four"), slides.highlight(TENS_KNOB, others="keep"),
                             until=lines.spoken("and the hundreds slide")),
                         Cue(lines.spoken("and the hundreds slide"),
                             slides.highlight(HUNDREDS_KNOB, others="keep"), total.light(row="second"),
                             until=lines.spoken("One more turn"))])
    add_145 = Shot(Curta, {Curta.stage: inside}, until=lines.spoken("The dials read"),
                  transition=Dissolve(0.5),
                  model=Take.keys({0: "set_145", lines.spoken("three and five"): 13.75,
                                   lines.spoken("When a column"): 15.0,
                                   lines.spoken("The dials read"): 16.25}),
                  cues=[Cue(lines.spoken("Each column adds"),
                            inside.highlight(UNITS_SHAFT, TENS_SHAFT, HUNDREDS_SHAFT, UNITS_DIAL, TENS_DIAL,
                                             HUNDREDS_DIAL, others="ghost"),
                            until=lines.spoken("When a column")),
                        Cue(lines.spoken("a carry lever"),
                            inside.highlight(TENS_CARRY, HUNDREDS_CARRY, others="ghost"),
                            until=lines.spoken("The dials read"))])
    read_168 = Shot(Curta, {Curta.stage: dials, Curta.aside: total}, until=lines.end(plus=1.5),
                   transition=Dissolve(0.5),
                   model=Take.keys({0: 16.25, lines.end(): "added_145", lines.end(plus=1.5): "added_145"}),
                   cues=[Cue(0, total.light(row="second"), until=lines.spoken("one hundred sixty-eight")),
                         Cue(lines.spoken("one hundred sixty-eight"), total.light(row="result"),
                             until=lines.end(plus=1.5))])


class Machinome(Chapter):
    lines = Narration("Let's watch that second turn again, beside the Python that describes this machine "
                      "in machinome. Each slide is a Driver, an input you can move: digit one is the "
                      "units, from zero to nine. The crank is a Driver too, crank rotation, in degrees. "
                      "One full turn is an instruction, named Turn crank. And one relation says what the "
                      "machine remembers: at every stroke, the inputs commit new result digits by the "
                      "law named advance.")
    curta = View(Take, camera=Take.face)
    drivers = Source.panel(Take.drivers)
    instruction = Source.panel(Take.instruction)
    relation = Source.panel(Take.relation)
    whole = Shot(Curta, {Curta.stage: curta}, until=lines.spoken("beside the Python"),
                 transition=Dissolve(0.8), model=Take.run("set_145", "set_145"))
    inputs = Shot(CurtaSplit, {CurtaSplit.left: drivers, CurtaSplit.right: curta},
                  until=lines.spoken("One full turn"), transition=Reframe(0.8),
                  model=Take.run("set_145", 15.75),
                  cues=[Cue(0, drivers.type(through_line=60, over=1.5)),
                        Cue(lines.spoken("Each slide is a Driver, an input you can move: digit one is the "
                                         "units, from zero to nine"),
                            drivers.emphasize("Driver", ("digit one", "digit_1"),
                                              ("from zero to nine", "range"), line=52, hold=0.6)),
                        Cue(lines.spoken("The crank is a Driver too, crank rotation, in degrees"),
                            drivers.emphasize(("crank rotation", "crank_rotation"), ("in degrees", "unit"),
                                              line=60, hold=0.6))])
    turn = Shot(CurtaSplit, {CurtaSplit.left: instruction, CurtaSplit.right: curta},
                until=lines.spoken("And one relation"), model=Take.run(15.75, 16.5),
                cues=[Cue(0, instruction.type(through_line=94, over=0.5)),
                      Cue(lines.spoken("One full turn is an instruction, named Turn crank"),
                          instruction.emphasize(("an instruction", "Instruction"), ("Turn crank", "Turn"),
                                                hold=0.4))])
    commit = Shot(CurtaSplit, {CurtaSplit.left: relation, CurtaSplit.right: curta},
                  until=lines.end(plus=1.2),
                  model=Take.keys({0: 16.5, lines.spoken("commit"): "added_145",
                                   lines.end(plus=1.2): "added_145"}),
                  cues=[Cue(0, relation.type(through_line=109, over=1.0)),
                        Cue(lines.spoken("at every stroke, the inputs commit new result digits by the law "
                                         "named advance"),
                            relation.emphasize("stroke", ("the inputs", "sources"), ("commit", "commits"),
                                               "advance", hold=0.8))])


class Closing(Chapter):
    lines = Narration("Twenty-three plus one hundred forty-five makes one hundred sixty-eight, in two "
                      "turns of the crank. The interactive model is linked in the description.")
    curta = View(Take, camera=Take.face)
    answer = Title("23 + 145 = 168")
    result = Shot(Curta, {Curta.stage: curta, Curta.headline: answer}, until=lines.end(plus=1.6),
                  transition=Dissolve(0.8), fade_out=FadeOut(1.2),
                  model=Take.run("added_145", "added_145"),
                  cues=[Cue(0, answer.show(enter=0.6, leave=0.6), until=lines.end())])


class Addition(Movie):
    title = "Addition"
    series = "CURTA · HOW IT ADDS"
    status = "rehearsal"
    learning_goal = ("Show how the Curta adds 23 and 145 with its setting slides, stepped drum and "
                     "result dials, and how machinome declares that machine in Python.")
    format = Format(1920, 1080, fps=30)
    narrator = jessica
    style = Style(background="#f4efe4", foreground="#161513", accent="#a87b2c",
                  font="DejaVu Sans, sans-serif", safe_inset=0.08)
    evidence = Evidence(model="../../simulation/event_driven.py", laws="../../simulation/clocked_laws.py",
                        record="../../simulation/docs/clocked-curta-2026-09-17.md")
    credits = Credits(project="Curta Type I 3x",
                      creator="Marcus Wu, after Curt Herzstark's Curta; simulation by Luis Fagundes",
                      copyright="Copyright (C) 2026 Luis Henrique Cassis Fagundes (simulation)",
                      license="CC BY-NC-SA 4.0", license_file="../../LICENSE")
    release = Release(simulation_url=None, source_url=None, description="description.md")
    question = Question()
    first = First()
    second = Second()
    machinome = Machinome()
    closing = Closing()
