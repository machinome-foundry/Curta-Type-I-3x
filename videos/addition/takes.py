"""The clocked Curta before the camera: the take of 23 + 145, the cameras that
film it, the layer that opens the case, and the source excerpts the film
types beside the machine. Declared once, beside the model; any movie of this
project can film it.

The take is what the framework's simulation of `ClockedCurta` returns for
these steps: evaluation runs them once through `Sim` and records each
request, the bank at every mark and the export's identity. Nothing here
poses the machine; the steps only ask it.
"""

from machinome_movie import Camera, Layer, Mark, Move, Source, Take, Trigger

from simulation.clocked import ClockedCurta


class Addition(Take):
    model = ClockedCurta
    export = "../../export/clocked_curta"
    readiness = ("The clocked Curta exported by machinome export: settings, crank strokes, "
                 "committed register digits and carries are the framework's clocked requests; "
                 "mid-stroke dial motion is the model's closed-form pose; forces, friction and "
                 "spring dynamics are not simulated.")

    # digit_1 is the units slide: the advance law reads the eight settings
    # units first (simulation/clocked_laws.py), and register_reading reads
    # result_0 as the units.
    steps = [Mark("rest"),
             Move(ClockedCurta.digit_1, to=3, over=1.5), Mark("units_3"),
             Move(ClockedCurta.digit_2, to=2, over=1.5), Mark("set_23"),
             Trigger("Turn crank"), Mark("added_23"),
             Move(ClockedCurta.digit_1, to=5, over=1.25), Mark("units_5"),
             Move(ClockedCurta.digit_2, to=4, over=1.25), Mark("tens_4"),
             Move(ClockedCurta.digit_3, to=1, over=1.25), Mark("set_145"),
             Trigger("Turn crank"), Mark("added_145")]

    # The whole Curta a little above, from the side of the low-order slides
    # (azimuth -40 degrees; the eight slides stand from 0 to -146): framed
    # for the split's right half, whose box is as tall as the full frame's
    # stage, so the vertical field holds body and crank with a margin in
    # both and the full frame is generous at the sides. The reframe keeps it.
    face = Camera(position=(607, -509, 300), target=(0, 0, -30), fov=30)
    # Level with the setting slides, facing the units, tens and hundreds
    # slides (azimuth -12 degrees; the units slide stands at 0, the hundreds
    # at -45): the knobs and the number rolls above them read.
    slides = Camera(position=(323, -69, -20), target=(0, 0, -75), fov=30)
    # Above the carriage rim, facing the low result dials: the units, tens
    # and hundreds dials read, the crank turning above them.
    dials = Camera(position=(253, -118, 210), target=(25, -12, 30), fov=26)
    # The mechanism with the case open (the layer `shell` hidden), from the
    # face camera's side and a little closer: the stepped drum at the axis,
    # the slides' shafts around it, the transmission shafts and the dials
    # above, the crank on top. Its highlights ghost the rest.
    inside = Camera(position=(440, -369, 170), target=(0, 0, -30), fov=31)

    # What hides the mechanism: the outer housing, the carriage covers and
    # the upper frame.
    shell = Layer(ClockedCurta.enclosure, ClockedCurta.carriage.registers.covers,
                  ClockedCurta.frame.upper_frame)

    # The machine in machinome: the eight slides and the crank as drivers,
    # the crank's instruction, and the one relation that commits the
    # register digits at each stroke.
    drivers = Source("../../simulation/clocked.py", lines=(52, 60))
    instruction = Source("../../simulation/clocked.py", lines=(94, 94))
    relation = Source("../../simulation/clocked.py", lines=(107, 109))
